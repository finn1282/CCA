// SawitSense presentation: demo configuration (edit at the rehearsal, D39).
// The admin token for a cloud dashboard goes ONLY in the git-ignored config.local.js:
//   window.SAWIT_LOCAL = { token: "..." };
window.SAWIT_CONFIG = {
  // Primary backend chosen at the rehearsal: cloud (https://<app>.azurewebsites.net) if stable, else the laptop.
  DASHBOARD_URL: "http://localhost:8000",
  // Laptop backend used when the primary fails (key F). Same SAWIT_DEVICE_KEYS as the cloud (S-02).
  FALLBACK_URL: "http://localhost:8000",
  // Shown by key S (simulator mode). {BASE} is replaced with the backend URL that is active at the time.
  // In cloud mode, add: --device <id> --key <key> using a key from SAWIT_DEVICE_KEYS.
  SIMULATOR_CMD: "cd 03_software/src && ../.venv/bin/python simulator.py --scenario cycle --interval 2 --base {BASE}",
  // How often the demo scene checks GET /api/v1/health (ms).
  HEALTH_INTERVAL_MS: 5000
};
