/*
  SawitSense camera node — AI-Thinker ESP32-CAM (OV2640) on ESP32-CAM-MB USB base
  Firmware 0.2.0 — conforms to 00_lead/INTERFACES.md v0.2 §3

  Capture & upload only (no on-device inference). Triggers:
    (a) primary: polls GET {base}/api/v1/devices/{DEVICE_ID}/commands every 2.5 s, captures on {"cmd":"capture"}
    (b) fallback: local web page http://<cam-ip>/  (buttons: Capture & upload, Preview)
    (c) fallback: one capture + upload on boot (press RST on the board)
  Upload: POST {base}/api/v1/infer/ripeness, body raw image/jpeg, headers X-Device-Id / X-Device-Key.
  Board: "AI Thinker ESP32-CAM" (esp32:esp32:esp32cam). Power from laptop USB, short data cable (D26).
*/
#include <WiFi.h>
#include <WiFiMulti.h>
#include <WiFiClientSecure.h>
#include <HTTPClient.h>
#include <WebServer.h>
#include <ArduinoJson.h>
#include "esp_camera.h"
#include "secrets.h"   // copy secrets.h.example -> secrets.h

#define FW_VERSION "0.2.0"

// ---- AI-Thinker pin map (fixed by the board) ----
#define PWDN_GPIO_NUM 32
#define RESET_GPIO_NUM -1
#define XCLK_GPIO_NUM 0
#define SIOD_GPIO_NUM 26
#define SIOC_GPIO_NUM 27
#define Y9_GPIO_NUM 35
#define Y8_GPIO_NUM 34
#define Y7_GPIO_NUM 39
#define Y6_GPIO_NUM 36
#define Y5_GPIO_NUM 21
#define Y4_GPIO_NUM 19
#define Y3_GPIO_NUM 18
#define Y2_GPIO_NUM 5
#define VSYNC_GPIO_NUM 25
#define HREF_GPIO_NUM 23
#define PCLK_GPIO_NUM 22
const int PIN_FLASH = 4;      // white flash LED (active high)
const int PIN_STATUS = 33;    // small red LED (active low)

// ---- Options ----
const bool USE_FLASH = false;          // glare on glossy prints; enable if the room is dark
const bool CAPTURE_ON_BOOT = true;
const uint32_t POLL_MS = 2500;         // INTERFACES §3: every 2–3 s
const uint32_t HTTP_TIMEOUT_MS = 8000; // inference may take a few seconds

WiFiMulti wifiMulti;
WebServer server(80);
bool preferLocal = false;
String lastResult = "no capture yet";
uint32_t tLastPoll = 0, captures = 0;

// ------------------------------------------------------------ camera
bool initCamera() {
  camera_config_t c = {};
  c.ledc_channel = LEDC_CHANNEL_0; c.ledc_timer = LEDC_TIMER_0;
  c.pin_d0 = Y2_GPIO_NUM; c.pin_d1 = Y3_GPIO_NUM; c.pin_d2 = Y4_GPIO_NUM; c.pin_d3 = Y5_GPIO_NUM;
  c.pin_d4 = Y6_GPIO_NUM; c.pin_d5 = Y7_GPIO_NUM; c.pin_d6 = Y8_GPIO_NUM; c.pin_d7 = Y9_GPIO_NUM;
  c.pin_xclk = XCLK_GPIO_NUM; c.pin_pclk = PCLK_GPIO_NUM; c.pin_vsync = VSYNC_GPIO_NUM; c.pin_href = HREF_GPIO_NUM;
  c.pin_sccb_sda = SIOD_GPIO_NUM; c.pin_sccb_scl = SIOC_GPIO_NUM;
  c.pin_pwdn = PWDN_GPIO_NUM; c.pin_reset = RESET_GPIO_NUM;
  c.xclk_freq_hz = 20000000;
  c.pixel_format = PIXFORMAT_JPEG;
  c.grab_mode = CAMERA_GRAB_LATEST;
  if (psramFound()) { c.frame_size = FRAMESIZE_SVGA; c.jpeg_quality = 12; c.fb_count = 2; c.fb_location = CAMERA_FB_IN_PSRAM; }
  else              { c.frame_size = FRAMESIZE_VGA;  c.jpeg_quality = 14; c.fb_count = 1; c.fb_location = CAMERA_FB_IN_DRAM; }
  esp_err_t err = esp_camera_init(&c);
  if (err != ESP_OK) { Serial.printf("[cam] init failed 0x%x\n", err); return false; }
  Serial.printf("[cam] ok, PSRAM=%d, %s\n", psramFound(), psramFound() ? "SVGA" : "VGA");
  return true;
}
camera_fb_t* grab() {
  if (USE_FLASH) { digitalWrite(PIN_FLASH, HIGH); delay(120); }
  camera_fb_t* fb = esp_camera_fb_get();   // first frame after idle can be stale/dark: take two
  if (fb) { esp_camera_fb_return(fb); fb = esp_camera_fb_get(); }
  if (USE_FLASH) digitalWrite(PIN_FLASH, LOW);
  return fb;
}

// ------------------------------------------------------------ network
void wifiEnsure() {
  if (WiFi.status() == WL_CONNECTED) return;
  wifiMulti.run(5000);
  if (WiFi.status() == WL_CONNECTED)
    Serial.printf("[wifi] %s ip=%s rssi=%d  -> local page http://%s/\n", WiFi.SSID().c_str(),
                  WiFi.localIP().toString().c_str(), WiFi.RSSI(), WiFi.localIP().toString().c_str());
}
int httpRequest(const String& base, const String& path, const uint8_t* body, size_t len, String& resp) {
  HTTPClient http; WiFiClientSecure tls; WiFiClient plain;
  String url = base + path; bool ok;
  if (base.startsWith("https://")) {
#if ALLOW_INSECURE_TLS
    tls.setInsecure();
#else
    tls.setCACert(ROOT_CA);
#endif
    ok = http.begin(tls, url);
  } else ok = http.begin(plain, url);   // plain HTTP only for API_BASE_LOCAL
  if (!ok) return -100;
  http.setTimeout(HTTP_TIMEOUT_MS); http.setConnectTimeout(5000);
  http.addHeader("X-Device-Id", DEVICE_ID);
  http.addHeader("X-Device-Key", DEVICE_KEY);
  int code;
  if (body) { http.addHeader("Content-Type", "image/jpeg"); code = http.POST((uint8_t*)body, len); }
  else code = http.GET();
  if (code > 0) resp = http.getString();
  http.end();
  return code;
}
int requestAny(const String& path, const uint8_t* body, size_t len, String& resp) {
  String bases[2] = { preferLocal ? API_BASE_LOCAL : API_BASE, preferLocal ? API_BASE : API_BASE_LOCAL };
  int code = -1;
  for (int i = 0; i < 2; i++) {
    if (bases[i].length() == 0) continue;
    code = httpRequest(bases[i], path, body, len, resp);
    if (code >= 200 && code < 300) { preferLocal = (bases[i] == String(API_BASE_LOCAL)); return code; }
    if (body) Serial.printf("[http] %s%s -> %d\n", bases[i].c_str(), path.c_str(), code);
  }
  return code;
}

// ------------------------------------------------------------ capture + upload
String captureAndUpload(const char* trigger) {
  wifiEnsure();
  digitalWrite(PIN_STATUS, LOW);
  camera_fb_t* fb = grab();
  if (!fb) { digitalWrite(PIN_STATUS, HIGH); return lastResult = "capture failed"; }
  Serial.printf("[cap] trigger=%s %u bytes\n", trigger, fb->len);
  String resp;
  int code = (WiFi.status() == WL_CONNECTED) ? requestAny("/api/v1/infer/ripeness", fb->buf, fb->len, resp) : -1;
  esp_camera_fb_return(fb);
  digitalWrite(PIN_STATUS, HIGH);
  captures++;
  if (code < 200 || code >= 300) return lastResult = "upload failed (HTTP " + String(code) + ")";
  JsonDocument d;
  if (deserializeJson(d, resp)) return lastResult = "bad response";
  String label = d["label"] | "?";
  float conf = d["confidence"] | 0.0f;
  String advice = d["harvest_advice"] | "";
  String ev = d["evidence_id"] | "";
  lastResult = label + " (" + String(conf, 2) + ") " + advice + " " + ev;
  Serial.printf("[infer] %s\n", lastResult.c_str());
  return lastResult;
}
void pollCommands() {
  if (WiFi.status() != WL_CONNECTED) return;
  String resp;
  int code = requestAny(String("/api/v1/devices/") + DEVICE_ID + "/commands", nullptr, 0, resp);
  if (code != 200 || resp.length() == 0) return;      // 204 / empty = no command
  JsonDocument d;
  if (deserializeJson(d, resp)) return;
  String cmd = d["cmd"] | "";
  if (cmd == "capture") captureAndUpload("dashboard");
}

// ------------------------------------------------------------ local web page (fallback trigger)
void handleRoot() {
  String h = F("<!doctype html><meta name=viewport content='width=device-width'><title>SawitSense cam</title>"
               "<body style='font-family:sans-serif;max-width:640px;margin:16px'><h2>SawitSense camera</h2>"
               "<p><a href='/capture'><button style='font-size:20px'>Capture &amp; upload</button></a> "
               "<a href='/preview'><button style='font-size:20px'>Preview (no upload)</button></a></p><p>Last result: <b>");
  h += lastResult + "</b></p><p>Device " DEVICE_ID " fw " FW_VERSION ", captures " + String(captures) + "</p>";
  server.send(200, "text/html", h);
}
void handleCapture() {
  String r = captureAndUpload("local-page");
  server.sendHeader("Location", "/");
  server.send(303, "text/plain", r);
}
void handlePreview() {
  camera_fb_t* fb = grab();
  if (!fb) { server.send(500, "text/plain", "capture failed"); return; }
  server.send_P(200, "image/jpeg", (const char*)fb->buf, fb->len);
  esp_camera_fb_return(fb);
}

void setup() {
  Serial.begin(115200);
  Serial.printf("\nSawitSense cam node fw %s (%s)\n", FW_VERSION, DEVICE_ID);
  pinMode(PIN_FLASH, OUTPUT); digitalWrite(PIN_FLASH, LOW);
  pinMode(PIN_STATUS, OUTPUT); digitalWrite(PIN_STATUS, HIGH);
  if (!initCamera()) { delay(3000); ESP.restart(); }
  WiFi.mode(WIFI_STA);
  WiFi.setSleep(false);
  wifiMulti.addAP(WIFI_SSID, WIFI_PASS);
  if (strlen(WIFI_SSID_2) > 0) wifiMulti.addAP(WIFI_SSID_2, WIFI_PASS_2);
  wifiEnsure();
  server.on("/", handleRoot);
  server.on("/capture", handleCapture);
  server.on("/preview", handlePreview);
  server.begin();
  if (CAPTURE_ON_BOOT) captureAndUpload("boot");
}

void loop() {
  server.handleClient();
  uint32_t now = millis();
  if (now - tLastPoll >= POLL_MS) { tLastPoll = now; wifiEnsure(); pollCommands(); }
  delay(5);
}
