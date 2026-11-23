/*
  SawitSense soil node — NodeMCU ESP32 (ESP32-WROOM-32)
  Firmware 0.2.0 — conforms to 00_lead/INTERFACES.md v0.2.3

  Sensors: capacitive moisture (GPIO34), pH PO via 10k/20k divider (GPIO35), TDS (GPIO32, powered from GPIO25),
           DS18B20 (GPIO4), DHT22 (GPIO16). OLED SSD1306 I2C (21/22). LEDs G/A/R (18/19/23), status LED (2).
           Button GPIO27 to GND: short = send now, long (>=1.5 s) = next page,
           very long (>=5 s) on CALIB page = capture moisture dry / wet point.
  Serial commands (115200): help | cal show | cal dry | cal wet | cal ph686 | cal ph401 | cal id YYYY-MM-DD
                            | cal tdsk <k> | cal reset | send | raw
  Pin rationale: 02_hardware/02_system_design.md. Calibration: 02_hardware/04_calibration.md.

  Libraries: ArduinoJson (7.x), Adafruit SSD1306, Adafruit GFX, OneWire, DallasTemperature,
             DHT sensor library (Adafruit) + Adafruit Unified Sensor. Board: "ESP32 Dev Module".
*/
#include <WiFi.h>
#include <WiFiMulti.h>
#include <WiFiClientSecure.h>
#include <HTTPClient.h>
#include <Preferences.h>
#include <ArduinoJson.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include <OneWire.h>
#include <DallasTemperature.h>
#include <DHT.h>
#include <time.h>
#include <math.h>
#include "secrets.h"   // copy secrets.h.example -> secrets.h

#define FW_VERSION "0.2.3"

// ---------------- Pins ----------------
const int PIN_MOIST   = 34;  // ADC1_CH6
const int PIN_PH      = 35;  // ADC1_CH7 (through divider)
const int PIN_TDS     = 32;  // ADC1_CH4
const int PIN_TDS_PWR = 25;  // TDS module VCC (switched)
const int PIN_DS18    = 4;
const int PIN_DHT     = 16;
const int PIN_LED_G   = 18;
const int PIN_LED_A   = 19;
const int PIN_LED_R   = 23;
const int PIN_LED_NET = 2;   // on-board LED
const int PIN_BTN     = 27;

// ---------------- Timing ----------------
const uint32_t SEND_INTERVAL_MS   = 10000;   // INTERFACES §2: 10 s demo mode
const uint32_t CAL_FETCH_MS       = 300000;  // refresh TDS baseline every 5 min
const uint32_t HTTP_TIMEOUT_MS    = 4000;
const uint32_t LONG_PRESS_MS      = 1500;
const uint32_t VERY_LONG_PRESS_MS = 5000;
const uint32_t TDS_WARMUP_MS      = 800;
const uint8_t  MAX_REPLAY_PER_CYCLE = 5;
const uint32_t CLOUD_RETRY_MS     = 300000;  // v0.2.2: while on LAN, retry API_BASE every 5 min

// ---------------- Default calibration (overridden by NVS; see 04_calibration.md) ----------------
const float DEF_MOIST_DRY_MV = 2800.0;  // probe in air
const float DEF_MOIST_WET_MV = 1300.0;  // probe in water to the line
const float DEF_PH_V686      = 2.525;   // PO volts (after divider correction) in pH 6.86 buffer (2.50 V @ pH 7 offset)
const float DEF_PH_V401      = 3.035;   // PO volts in pH 4.01 buffer  (=> 0.179 V/pH) [RAW-PH]
const float DEF_PH_CAL_T     = 25.0;    // buffer temperature during pH calibration
const float DEF_TDS_K        = 1.0;     // TDS cell constant correction
const char* DEF_CAL_ID       = "uncalibrated";
const float PH_DIVIDER       = 20.0 / 30.0;  // 10k top / 20k bottom

// ---------------- Thresholds (INTERFACES v0.2 §4 — do not change without Lead) ----------------
const float MOIST_LOW = 30.0, MOIST_HIGH = 80.0;
const float PH_LIME = 4.0, PH_WATCH_HI = 4.2, PH_HIGH = 6.5;

// ---------------- Objects ----------------
Adafruit_SSD1306 oled(128, 64, &Wire, -1);
OneWire oneWire(PIN_DS18);
DallasTemperature ds18(&oneWire);
DHT dht(PIN_DHT, DHT22);
WiFiMulti wifiMulti;
Preferences prefs;
bool oledOk = false;

// Calibration state
float moistDryMv, moistWetMv, phV686, phV401, phCalT, tdsK;
String calId;
float tdsBaseline = NAN, tdsMargin = 0.30;   // from backend (last received), cached in NVS

// Reading (NAN = null)
struct Reading {
  uint32_t seq;
  time_t ts;          // 0 = unknown
  float moist, ph, tds, soilT, airT, airRh;
  int8_t rssi;
  uint32_t capMs;     // millis() at capture -> age_s
};
const int BUF_N = 30;   // offline ring buffer
Reading ring[BUF_N];
int ringHead = 0, ringCount = 0;

uint32_t seqNo = 0;
Reading last;
float lastMoistMv = NAN, lastPhV = NAN, lastTdsV = NAN;

// Display state
enum Page { PAGE_DECISION = 0, PAGE_READINGS, PAGE_NETWORK, PAGE_CALIB, PAGE_COUNT };
int page = PAGE_DECISION;
String decSource = "BOOT", decLine1 = "SawitSense", decLine2 = "starting...", decLed = "", decEvidence = "";
String lastBaseUsed = "-";
int lastHttpCode = 0;
int calibStep = 0;  // 0 = next capture is DRY, 1 = next is WET
String calibMsg = "";
bool onLan = false;             // true while the laptop (API_BASE_LOCAL) is the answering base
uint32_t tLastCloudTry = 0;

uint32_t tLastSend = 0, tLastCal = 0, tBtnDown = 0;
bool btnWasDown = false, forceSend = false;

// ============================================================ helpers
float readMv(int pin, int n = 32) {
  // average of n samples using eFuse-calibrated millivolts (ESP-FAQ ADC recommendation)
  uint32_t sum = 0;
  for (int i = 0; i < n; i++) { sum += analogReadMilliVolts(pin); delay(2); }
  return (float)sum / n;
}
void jsonNum(JsonDocument& d, const char* k, float v, int dp) {
  if (isnan(v)) d[k] = nullptr; else d[k] = roundf(v * powf(10, dp)) / powf(10, dp);
}
void setLed(const String& c) {
  digitalWrite(PIN_LED_G, c == "green");
  digitalWrite(PIN_LED_A, c == "amber");
  digitalWrite(PIN_LED_R, c == "red");
}
String isoTime(time_t t) {
  if (t == 0) return "";
  struct tm tmv; gmtime_r(&t, &tmv);
  char b[25]; strftime(b, sizeof b, "%Y-%m-%dT%H:%M:%SZ", &tmv);
  return String(b);
}
// v0.2.3: values are rounded once at capture to what the payload sends (1 decimal), so LOCAL == CLOUD at thresholds
float r1(float v) { return isnan(v) ? NAN : roundf(v * 10.0f) / 10.0f; }
bool allSoilNull(const Reading& r) { return isnan(r.moist) && isnan(r.ph) && isnan(r.tds); }
time_t nowOrZero() { time_t t = time(nullptr); return (t > 1700000000) ? t : 0; }

// ============================================================ NVS
void loadPrefs() {
  prefs.begin("sawit", false);
  moistDryMv = prefs.getFloat("mdry", DEF_MOIST_DRY_MV);
  moistWetMv = prefs.getFloat("mwet", DEF_MOIST_WET_MV);
  phV686     = prefs.getFloat("v686", DEF_PH_V686);
  phV401     = prefs.getFloat("v401", DEF_PH_V401);
  phCalT     = prefs.getFloat("phT",  DEF_PH_CAL_T);
  tdsK       = prefs.getFloat("tdsk", DEF_TDS_K);
  calId      = prefs.getString("calid", DEF_CAL_ID);
  tdsBaseline= prefs.getFloat("tdsb", NAN);
  tdsMargin  = prefs.getFloat("tdsm", 0.30);
  // seq is stored in blocks of 10 so a reboot never repeats a number (monotonic, INTERFACES §2)
  seqNo = prefs.getUInt("seq", 0) + 10;
  prefs.putUInt("seq", seqNo);
}
void saveSeqIfNeeded() { if (seqNo % 10 == 0) prefs.putUInt("seq", seqNo); }

// ============================================================ sensors
float readMoisturePct() {
  float mv = readMv(PIN_MOIST);
  lastMoistMv = mv;
  if (mv < 100 || mv > 3250) return NAN;          // disconnected / shorted
  float pct = (moistDryMv - mv) / (moistDryMv - moistWetMv) * 100.0;
  return constrain(pct, 0.0, 100.0);
}
float readSolutionTemp() {
  ds18.requestTemperatures();
  float t = ds18.getTempCByIndex(0);
  if (t == DEVICE_DISCONNECTED_C || t < -20 || t > 80 || t == 85.0) return NAN;
  return t;
}
float readPh(float tempC) {
  digitalWrite(PIN_TDS_PWR, LOW);   // TDS excitation off while pH is read (INTERFACES §4 note)
  delay(300);
  float vPin = readMv(PIN_PH, 64) / 1000.0;
  float vPo = vPin / PH_DIVIDER;
  lastPhV = vPo;
  if (vPo < 0.2 || vPo > 4.9) return NAN;          // board unpowered / probe missing
  float slope = (phV401 - phV686) / (6.86 - 4.01);  // V per pH unit at calibration temperature
  if (fabs(slope) < 0.05) return NAN;              // invalid calibration
  float t = isnan(tempC) ? phCalT : tempC;
  slope *= (t + 273.15) / (phCalT + 273.15);       // Nernst slope temperature correction
  float ph = 6.86 + (phV686 - vPo) / slope;
  if (ph < 0 || ph > 14) return NAN;
  return ph;
}
float readTds(float tempC) {
  digitalWrite(PIN_TDS_PWR, HIGH);
  delay(TDS_WARMUP_MS);
  float v = readMv(PIN_TDS, 64) / 1000.0;
  digitalWrite(PIN_TDS_PWR, LOW);
  lastTdsV = v;
  if (v > 2.6) return NAN;                          // outside module range
  float t = isnan(tempC) ? 25.0 : tempC;
  float vc = v / (1.0 + 0.02 * (t - 25.0));        // DFRobot SEN0244 temperature compensation
  float tds = (133.42 * vc * vc * vc - 255.86 * vc * vc + 857.39 * vc) * 0.5 * tdsK;
  return max(tds, 0.0f);
}
Reading takeReading() {
  Reading r;
  r.seq = ++seqNo; saveSeqIfNeeded();
  r.ts = nowOrZero();
  r.capMs = millis();
  r.moist = readMoisturePct();
  r.soilT = readSolutionTemp();
  r.ph = readPh(r.soilT);
  r.tds = readTds(r.soilT);
  float h = dht.readHumidity(), t = dht.readTemperature();
  r.airRh = isnan(h) ? NAN : h;
  r.airT = isnan(t) ? NAN : t;
  r.rssi = (WiFi.status() == WL_CONNECTED) ? WiFi.RSSI() : 0;
  r.moist = r1(r.moist); r.ph = r1(r.ph); r.tds = r1(r.tds);
  r.soilT = r1(r.soilT); r.airT = r1(r.airT); r.airRh = r1(r.airRh);
  Serial.printf("[read] seq=%u moist=%.1f%% (%.0fmV) pH=%.2f (PO %.3fV) tds=%.0fppm (%.3fV) T=%.1f air=%.1fC/%.0f%%\n",
                r.seq, r.moist, lastMoistMv, r.ph, lastPhV, r.tds, lastTdsV, r.soilT, r.airT, r.airRh);
  return r;
}

// ============================================================ local rules (INTERFACES v0.2 §4)
// priority: irrigate/drain (4) > lime (3) > fertilise/skip_fertiliser (2) > watch (1) > ok (0)
void showNoData(const String& tag) {
  // v0.2.3: all rule sensors null -> amber NO DATA in every mode (never green OK)
  decSource = tag; decLine1 = "NO DATA"; decLine2 = "check sensors"; decLed = "amber"; decEvidence = "";
  setLed(decLed);
}
void localDecision(const Reading& r) {
  if (allSoilNull(r)) { showNoData("LOCAL"); return; }
  int best = 0; String act = "ok", led = "green", l2 = "all in range";
  auto consider = [&](int prio, const char* a, const char* c, String why) {
    if (prio > best) { best = prio; act = a; led = c; l2 = why; }
  };
  if (!isnan(r.moist)) {
    if (r.moist < MOIST_LOW)  consider(4, "irrigate", "red",   "moist " + String(r.moist, 0) + "%<30%");
    if (r.moist > MOIST_HIGH) consider(4, "drain",    "amber", "moist " + String(r.moist, 0) + "%>80%");
  }
  if (!isnan(r.ph)) {
    if (r.ph < PH_LIME)                        consider(3, "lime",  "red",   "pH " + String(r.ph, 1) + "<4.0");
    else if (r.ph < PH_WATCH_HI)               consider(1, "watch", "amber", "pH " + String(r.ph, 1) + " 4.0-4.2");
    else if (r.ph > PH_HIGH)                   consider(1, "watch", "amber", "pH " + String(r.ph, 1) + ">6.5");
  }
  if (!isnan(r.tds) && !isnan(tdsBaseline) && tdsBaseline > 0) {   // else TDS rules skipped
    if (r.tds < tdsBaseline * (1 - tdsMargin)) consider(2, "fertilise",       "amber", "TDS low (sim)");
    if (r.tds > tdsBaseline * (1 + tdsMargin)) consider(2, "skip_fertiliser", "amber", "TDS high (sim)");
  }
  String l1 = act; l1.toUpperCase();
  if (l1 == "SKIP_FERTILISER") l1 = "SKIP FERTILISER";
  decSource = "LOCAL"; decLine1 = l1.substring(0, 16); decLine2 = l2.substring(0, 16);
  decLed = led; decEvidence = "";
  setLed(led);
}

// ============================================================ network
void wifiEnsure() {
  if (WiFi.status() == WL_CONNECTED) return;
  wifiMulti.run(3000);
  if (WiFi.status() == WL_CONNECTED) {
    Serial.printf("[wifi] connected %s ip=%s rssi=%d\n", WiFi.SSID().c_str(),
                  WiFi.localIP().toString().c_str(), WiFi.RSSI());
    configTime(0, 0, "pool.ntp.org", "time.google.com");
  }
}
// Performs one request against base; returns HTTP code (<0 = transport error).
int httpRequest(const String& base, const String& path, const char* method, const String& body, String& resp) {
  HTTPClient http;
  WiFiClientSecure tls;
  WiFiClient plain;
  String url = base + path;
  bool ok;
  if (base.startsWith("https://")) {
#if ALLOW_INSECURE_TLS
    tls.setInsecure();
#else
    tls.setCACert(ROOT_CA);
#endif
    ok = http.begin(tls, url);
  } else {
    ok = http.begin(plain, url);   // plain HTTP: only for API_BASE_LOCAL (INTERFACES §1)
  }
  if (!ok) return -100;
  http.setTimeout(HTTP_TIMEOUT_MS);
  http.setConnectTimeout(HTTP_TIMEOUT_MS);
  http.addHeader("X-Device-Id", DEVICE_ID);
  http.addHeader("X-Device-Key", DEVICE_KEY);
  int code;
  if (strcmp(method, "POST") == 0) { http.addHeader("Content-Type", "application/json"); code = http.POST(body); }
  else code = http.GET();
  if (code > 0) resp = http.getString();
  http.end();
  return code;
}
// Base selection (INTERFACES v0.2.2 §2): cloud first; once the laptop (LAN) answered, stay on LAN and
// retry API_BASE every CLOUD_RETRY_MS, switching back on success.
// Returns the best HTTP code (2xx wins, else 4xx, else last error); sets usedBase to "CLOUD" or "LAN".
int requestAny(const String& path, const char* method, const String& body, String& resp, String& usedBase) {
  bool cloudFirst = !onLan || (millis() - tLastCloudTry >= CLOUD_RETRY_MS);
  const char* bases[2] = { cloudFirst ? API_BASE : API_BASE_LOCAL, cloudFirst ? API_BASE_LOCAL : API_BASE };
  int best = -1;
  for (int i = 0; i < 2; i++) {
    if (strlen(bases[i]) == 0) continue;
    bool isCloud = (strcmp(bases[i], API_BASE) == 0);
    if (isCloud) tLastCloudTry = millis();
    digitalWrite(PIN_LED_NET, LOW);
    int code = httpRequest(String(bases[i]), path, method, body, resp);
    digitalWrite(PIN_LED_NET, WiFi.status() == WL_CONNECTED);
    if (code >= 200 && code < 300) {
      usedBase = isCloud ? "CLOUD" : "LAN";
      if (onLan == isCloud) Serial.printf("[net] now using %s\n", usedBase.c_str());
      onLan = !isCloud;
      return code;
    }
    Serial.printf("[http] %s %s%s -> %d\n", method, bases[i], path.c_str(), code);
    if (code >= 400 && code < 500) best = code; else if (best < 400) best = code;
  }
  usedBase = "LOCAL";
  return best;
}
bool isRejected(int code) { return code >= 400 && code < 500; }   // permanent: do not buffer / drop from queue
String toJson(const Reading& r, bool buffered) {
  JsonDocument d;
  d["device_id"] = DEVICE_ID;
  d["seq"] = r.seq;
  if (r.ts) d["ts"] = isoTime(r.ts); else d["ts"] = nullptr;
  d["buffered"] = buffered;
  d["age_s"] = (uint32_t)((millis() - r.capMs) / 1000);   // v0.2.2: 0 for fresh readings
  d["block_id"] = BLOCK_ID;
  jsonNum(d, "soil_moisture_pct", r.moist, 1);
  jsonNum(d, "soil_ph", r.ph, 1);
  jsonNum(d, "tds_ppm", r.tds, 1);
  d["ec_us_cm"] = nullptr;                         // backend derives EC ≈ TDS/0.5 (INTERFACES §2)
  jsonNum(d, "soil_temp_c", r.soilT, 1);
  jsonNum(d, "air_temp_c", r.airT, 1);
  jsonNum(d, "air_rh_pct", r.airRh, 1);
  if (r.rssi != 0) d["rssi_dbm"] = r.rssi; else d["rssi_dbm"] = nullptr;
  d["cal_id"] = calId;
  d["fw_version"] = FW_VERSION;
  String s; serializeJson(d, s);
  return s;
}
void bufferPush(const Reading& r) {
  ring[(ringHead + ringCount) % BUF_N] = r;
  if (ringCount < BUF_N) ringCount++; else ringHead = (ringHead + 1) % BUF_N;  // drop oldest
}
void bufferPop() { ringHead = (ringHead + 1) % BUF_N; ringCount--; }
bool applyCloudResponse(const String& resp, const String& tag) {
  JsonDocument d;
  if (deserializeJson(d, resp)) return false;
  String a = d["action"] | "";
  if (a.length() == 0) return false;
  String l1 = d["oled"][0] | "", l2 = d["oled"][1] | "";
  if (l1.length() == 0) { l1 = a; l1.toUpperCase(); }
  if (l2.length() == 0) l2 = String((const char*)(d["reason"] | ""));
  decSource = tag; decLine1 = l1.substring(0, 16); decLine2 = l2.substring(0, 16);
  decLed = d["led"] | "amber"; decEvidence = d["evidence_id"] | "";
  if (allSoilNull(last) && decLine1 != "NO DATA") showNoData(tag);
  else setLed(decLed);
  Serial.printf("[%s] action=%s led=%s ev=%s reason=%s\n", tag.c_str(), a.c_str(), decLed.c_str(),
                decEvidence.c_str(), (const char*)(d["reason"] | ""));
  return true;
}
void fetchCalibration() {
  // Per-device TDS calibration read-back (INTERFACES v0.2.1, D30): {tds_baseline_ppm, tds_margin, updated_at}
  if (WiFi.status() != WL_CONNECTED) return;
  String resp, used;
  int code = requestAny(String("/api/v1/devices/") + DEVICE_ID + "/calibration", "GET", "", resp, used);
  if (code < 200 || code >= 300) return;
  JsonDocument d;
  if (deserializeJson(d, resp)) return;
  float b = d["tds_baseline_ppm"] | NAN;            // null or missing => baseline cleared on the server
  float m = d["tds_margin"] | NAN;
  if (!isnan(b) && b > 0) { tdsBaseline = b; prefs.putFloat("tdsb", b); }
  else { tdsBaseline = NAN; prefs.remove("tdsb"); }  // LOCAL mode then skips TDS rules
  if (!isnan(m) && m > 0 && m < 1) { tdsMargin = m; prefs.putFloat("tdsm", m); }
  Serial.printf("[cal] backend TDS baseline=%.0f margin=%.2f (via %s)\n", tdsBaseline, tdsMargin, used.c_str());
}
void cycle() {
  wifiEnsure();
  last = takeReading();
  bool linkOk = WiFi.status() == WL_CONNECTED;
  // 1) replay oldest buffered readings FIRST (INTERFACES v0.2.2), so the fresh reading is the newest row
  for (uint8_t i = 0; linkOk && i < MAX_REPLAY_PER_CYCLE && ringCount > 0; i++) {
    String r2, u2;
    int c = requestAny("/api/v1/readings", "POST", toJson(ring[ringHead], true), r2, u2);
    if (c >= 200 && c < 300) { Serial.printf("[buf] replayed seq=%u via %s\n", ring[ringHead].seq, u2.c_str()); bufferPop(); }
    else if (isRejected(c))  { Serial.printf("[buf] DROPPED seq=%u (HTTP %d rejected)\n", ring[ringHead].seq, c); bufferPop(); }
    else { linkOk = false; break; }                  // transport error / 5xx: try again next cycle
  }
  // 2) fresh reading
  String resp, used = "LOCAL";
  lastHttpCode = linkOk ? requestAny("/api/v1/readings", "POST", toJson(last, false), resp, used) : -1;
  if (lastHttpCode >= 200 && lastHttpCode < 300) {
    lastBaseUsed = used;
    if (!applyCloudResponse(resp, used)) localDecision(last);
    return;
  }
  localDecision(last);
  lastBaseUsed = "offline";
  if (isRejected(lastHttpCode)) {
    Serial.printf("[http] seq=%u rejected (HTTP %d) - not buffered\n", last.seq, lastHttpCode);
  } else {
    bufferPush(last);
    Serial.printf("[buf] stored seq=%u (%d buffered)\n", last.seq, ringCount);
  }
}

// ============================================================ display
void drawOled() {
  if (!oledOk) return;
  oled.clearDisplay();
  oled.setTextColor(SSD1306_WHITE);
  oled.setTextSize(1);
  oled.setCursor(0, 0);
  bool net = WiFi.status() == WL_CONNECTED;
  oled.printf("SawitSense  %s\n", decSource.c_str());
  oled.drawFastHLine(0, 9, 128, SSD1306_WHITE);
  oled.setCursor(0, 12);
  switch (page) {
    case PAGE_DECISION:
      oled.setTextSize(decLine1.length() <= 10 ? 2 : 1);
      oled.println(decLine1);
      oled.setTextSize(1);
      oled.println(decLine2);
      oled.setCursor(0, 46);
      oled.printf("led:%s %s\n", decLed.c_str(), decEvidence.c_str());
      oled.printf("#%u %s buf:%d", last.seq, net ? "net" : "NO NET", ringCount);
      break;
    case PAGE_READINGS:
      oled.printf("Moist %s %%\n", isnan(last.moist) ? "--" : String(last.moist, 1).c_str());
      oled.printf("pH    %s\n", isnan(last.ph) ? "--" : String(last.ph, 2).c_str());
      oled.printf("TDS   %s ppm\n", isnan(last.tds) ? "--" : String(last.tds, 0).c_str());
      oled.printf("Tsol  %s C\n", isnan(last.soilT) ? "--" : String(last.soilT, 1).c_str());
      oled.printf("Air   %s C %s%%\n", isnan(last.airT) ? "--" : String(last.airT, 1).c_str(),
                  isnan(last.airRh) ? "--" : String(last.airRh, 0).c_str());
      break;
    case PAGE_NETWORK:
      oled.printf("WiFi %s\n", net ? WiFi.SSID().c_str() : "disconnected");
      oled.printf("IP %s\n", net ? WiFi.localIP().toString().c_str() : "-");
      oled.printf("RSSI %d  via %s\n", net ? WiFi.RSSI() : 0, lastBaseUsed.c_str());
      oled.printf("HTTP %d  buf %d\n", lastHttpCode, ringCount);
      oled.printf("cal %s\n", calId.c_str());
      oled.printf("fw %s seq %u", FW_VERSION, last.seq);
      break;
    case PAGE_CALIB:
      oled.printf("moist %.0f mV\n", readMv(PIN_MOIST, 8));
      oled.printf("dry %.0f wet %.0f\n", moistDryMv, moistWetMv);
      oled.printf("pH PO %.3f V\n", lastPhV);
      oled.printf("Hold 5s: %s\n", calibStep == 0 ? "DRY (air)" : "WET (water)");
      oled.println(calibMsg);
      break;
  }
  oled.display();
}

// ============================================================ calibration commands
void calCapture(const String& what) {
  if (what == "dry")   { moistDryMv = readMv(PIN_MOIST, 64); prefs.putFloat("mdry", moistDryMv); calibMsg = "dry=" + String(moistDryMv, 0); }
  else if (what == "wet") { moistWetMv = readMv(PIN_MOIST, 64); prefs.putFloat("mwet", moistWetMv); calibMsg = "wet=" + String(moistWetMv, 0); }
  else if (what == "ph686" || what == "ph401") {
    digitalWrite(PIN_TDS_PWR, LOW); delay(300);
    float v = readMv(PIN_PH, 128) / 1000.0 / PH_DIVIDER;
    float t = readSolutionTemp();
    if (what == "ph686") { phV686 = v; prefs.putFloat("v686", v); } else { phV401 = v; prefs.putFloat("v401", v); }
    if (!isnan(t)) { phCalT = t; prefs.putFloat("phT", t); }
    calibMsg = what + "=" + String(v, 3) + "V";
  }
  Serial.printf("[cal] %s\n", calibMsg.c_str());
}
void handleSerial() {
  if (!Serial.available()) return;
  String cmd = Serial.readStringUntil('\n'); cmd.trim();
  if (cmd == "help") Serial.println("cal show|dry|wet|ph686|ph401|id YYYY-MM-DD|tdsk <k>|reset ; send ; raw");
  else if (cmd == "send") forceSend = true;
  else if (cmd == "raw") Serial.printf("[raw] moist %.0f mV, pH pin %.0f mV, TDS %.0f mV\n",
                                       readMv(PIN_MOIST), readMv(PIN_PH), readMv(PIN_TDS));
  else if (cmd == "cal show") {
    float slope = (phV401 - phV686) / (6.86 - 4.01);
    Serial.printf("[cal] id=%s moist dry=%.0f wet=%.0f mV | pH V6.86=%.3f V4.01=%.3f slope=%.3f V/pH @%.1fC | tdsK=%.3f | tds baseline=%.0f margin=%.2f\n",
                  calId.c_str(), moistDryMv, moistWetMv, phV686, phV401, slope, phCalT, tdsK, tdsBaseline, tdsMargin);
  }
  else if (cmd == "cal dry" || cmd == "cal wet" || cmd == "cal ph686" || cmd == "cal ph401") calCapture(cmd.substring(4));
  else if (cmd.startsWith("cal id ")) { calId = cmd.substring(7); prefs.putString("calid", calId); Serial.printf("[cal] id=%s\n", calId.c_str()); }
  else if (cmd.startsWith("cal tdsk ")) { tdsK = cmd.substring(9).toFloat(); prefs.putFloat("tdsk", tdsK); Serial.printf("[cal] tdsK=%.3f\n", tdsK); }
  else if (cmd == "cal reset") {
    uint32_t s = prefs.getUInt("seq", 0); prefs.clear(); prefs.putUInt("seq", s);  // keep seq monotonic
    loadPrefs(); Serial.println("[cal] reset to defaults");
  }
  else if (cmd.length()) Serial.println("? type help");
}

// ============================================================ button
void handleButton() {
  bool down = digitalRead(PIN_BTN) == LOW;
  uint32_t now = millis();
  if (down && !btnWasDown) { tBtnDown = now; btnWasDown = true; }
  if (!down && btnWasDown) {
    btnWasDown = false;
    uint32_t held = now - tBtnDown;
    if (held < 40) return;                       // debounce
    if (held >= VERY_LONG_PRESS_MS && page == PAGE_CALIB) {
      calCapture(calibStep == 0 ? "dry" : "wet");
      calibStep = 1 - calibStep;
    } else if (held >= LONG_PRESS_MS) {
      page = (page + 1) % PAGE_COUNT;
    } else {
      forceSend = true;
    }
    drawOled();
  }
}

// ============================================================ setup / loop
void setup() {
  Serial.begin(115200);
  delay(200);
  Serial.printf("\nSawitSense soil node fw %s (%s)\n", FW_VERSION, DEVICE_ID);
  pinMode(PIN_LED_G, OUTPUT); pinMode(PIN_LED_A, OUTPUT); pinMode(PIN_LED_R, OUTPUT);
  pinMode(PIN_LED_NET, OUTPUT); pinMode(PIN_TDS_PWR, OUTPUT); digitalWrite(PIN_TDS_PWR, LOW);
  pinMode(PIN_BTN, INPUT_PULLUP);
  analogReadResolution(12);
  analogSetPinAttenuation(PIN_MOIST, ADC_11db);
  analogSetPinAttenuation(PIN_PH, ADC_11db);
  analogSetPinAttenuation(PIN_TDS, ADC_11db);
  // LED self-test
  setLed("green"); delay(250); setLed("amber"); delay(250); setLed("red"); delay(250); setLed("");

  loadPrefs();
  Wire.begin(21, 22);
  oledOk = oled.begin(SSD1306_SWITCHCAPVCC, 0x3C);
  if (!oledOk) Serial.println("[oled] not found at 0x3C");
  ds18.begin();
  dht.begin();
  drawOled();

  WiFi.mode(WIFI_STA);
  wifiMulti.addAP(WIFI_SSID, WIFI_PASS);
  if (strlen(WIFI_SSID_2) > 0) wifiMulti.addAP(WIFI_SSID_2, WIFI_PASS_2);
  wifiEnsure();
  digitalWrite(PIN_LED_NET, WiFi.status() == WL_CONNECTED);
  fetchCalibration();
  tLastCal = millis();
  forceSend = true;
}

void loop() {
  handleSerial();
  handleButton();
  uint32_t now = millis();
  if (forceSend || now - tLastSend >= SEND_INTERVAL_MS) {
    forceSend = false;
    tLastSend = now;
    cycle();
    drawOled();
  }
  if (now - tLastCal >= CAL_FETCH_MS) { tLastCal = now; fetchCalibration(); }
  static uint32_t tDraw = 0;
  if (page == PAGE_CALIB && now - tDraw > 500) { tDraw = now; drawOled(); }
  digitalWrite(PIN_LED_NET, WiFi.status() == WL_CONNECTED);
  delay(10);
}
