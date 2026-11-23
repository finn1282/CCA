# Deploy SawitSense to Azure App Service + Blob Storage (stakeholder step, D31)

> Internal build doc (D20). This is the **demonstration** deployment on Azure for Students.
> - The report describes the full production design (`04_cloud_design.md`); `07_actual_build_vs_target.md` maps one to the other.
> - Takes about 30 minutes. Uses only the free student credit; the B1 plan is the only resource that bills.
> - **If Azure sign-up fails, use `ALTERNATIVES.md`.** The laptop-local run is first-class and already works.

**Result:**
- A public HTTPS URL, `https://<app-name>.azurewebsites.net`, for the dashboard and API.
- The ripeness model is stored in Blob Storage.
- Device keys and the admin token are set as App Service settings, never in the repo.

## 0. Before you start
1. You need an Azure for Students subscription (portal.azure.com shows "Azure for Students").
2. Install the **Azure CLI**: https://learn.microsoft.com/cli/azure/install-azure-cli. Then log in:
   ```bash
   az login
   az account show --query name
   ```
   The second command should print "Azure for Students".
3. The trained model files must be in `03_software/models/`: `m1_ripeness.onnx` and `m1_ripeness.json` (see `training/RUN_ON_KAGGLE.md`).
4. **Choose secrets now** and keep them in a password manager, not in the repo:
   - one key per device, for example generated with `python -c "import secrets;print(secrets.token_urlsafe(24))"`;
   - one admin token for the dashboard.

## 1. Set variables (one terminal session)
```bash
cd CCA/03_software
export RG=sawitsense-rg
export LOC=malaysiawest          # if step 2 says "not allowed / not available", use: southeastasia
export APP=sawitsense-$RANDOM    # must be globally unique; note the final name
export PLAN=sawitsense-plan
export ST=sawitsense$RANDOM      # storage account: lowercase letters/digits only
export SOIL_KEY='paste-soil-node-key'
export CAM_KEY='paste-camera-key'
export ADMIN_TOKEN='paste-admin-token'
```
On Windows, use PowerShell `$env:NAME="value"` for each line, or run these steps in Azure Cloud Shell (bash) from the portal.

## 2. Resource group, plan and web app
```bash
az group create -n $RG -l $LOC
az appservice plan create -g $RG -n $PLAN --is-linux --sku B1 -l $LOC
az webapp create -g $RG -p $PLAN -n $APP --runtime "PYTHON:3.12"
```
If `malaysiawest` is refused (student subscriptions restrict regions), delete the group with `az group delete -n $RG -y`, set `LOC=southeastasia` and repeat step 2. This affects the demo only; the report keeps Malaysia West.

## 3. Blob Storage for the model
```bash
az storage account create -g $RG -n $ST -l $LOC --sku Standard_LRS --allow-blob-public-access false
az storage container create --account-name $ST -n models --auth-mode login
az storage blob upload --account-name $ST -c models -f models/m1_ripeness.onnx -n m1_ripeness.onnx --auth-mode login
az storage blob upload --account-name $ST -c models -f models/m1_ripeness.json -n m1_ripeness.json --auth-mode login
```
If `--auth-mode login` gives a permission error, give yourself the "Storage Blob Data Contributor" role:
```bash
az role assignment create --role "Storage Blob Data Contributor" \
  --assignee $(az ad signed-in-user show --query id -o tsv) \
  --scope $(az storage account show -n $ST --query id -o tsv)
```
Wait one minute after assigning the role, then retry.

Next, create **read-only SAS links valid for 60 days**. The app downloads the model with them once.
```bash
EXP=$(date -u -d "+60 days" +%Y-%m-%dT%H:%MZ 2>/dev/null || date -u -v+60d +%Y-%m-%dT%H:%MZ)
MODEL_URL=$(az storage blob generate-sas --account-name $ST -c models -n m1_ripeness.onnx --permissions r --expiry $EXP --auth-mode login --as-user --full-uri -o tsv)
META_URL=$(az storage blob generate-sas --account-name $ST -c models -n m1_ripeness.json --permissions r --expiry $EXP --auth-mode login --as-user --full-uri -o tsv)
```

## 4. App settings (secrets live only here)
```bash
az webapp config appsettings set -g $RG -n $APP --settings \
  SAWIT_MODE=cloud \
  SAWIT_DEVICE_KEYS="soilnode-01:$SOIL_KEY,cam-01:$CAM_KEY" \
  SAWIT_ADMIN_TOKEN="$ADMIN_TOKEN" \
  SAWIT_RUNTIME_DIR=/home/data \
  SAWIT_MODEL=/home/data/models/m1_ripeness.onnx \
  SAWIT_MODEL_URL="$MODEL_URL" \
  SAWIT_MODEL_META_URL="$META_URL" \
  SCM_DO_BUILD_DURING_DEPLOYMENT=true \
  WEBSITES_ENABLE_APP_SERVICE_STORAGE=true
az webapp config set -g $RG -n $APP --startup-file "startup.sh" --always-on true --http20-enabled true
az webapp update -g $RG -n $APP --https-only true
```
- `SAWIT_MODE=cloud` switches the server to **fail-closed**. The demo keys are disabled, and the admin token is required for dashboard reads and writes (D-12, S-08).
- `/home/data` is persistent App Service storage, so the evidence log survives restarts.

## 5. Build and deploy the code
```bash
bash deploy/make_package.sh
az webapp deploy -g $RG -n $APP --src-path deploy/sawitsense.zip --type zip
```
The first deploy installs the requirements on the server, which takes 3–6 minutes.

## 6. Smoke-check the URL
```bash
URL=https://$APP.azurewebsites.net
curl -s $URL/api/v1/health
```
Expect `{"status":"ok","version":"0.2.5","mode":"cloud","ripeness_model":"m1-effb0-0.1",...}`. The first call can take about 20 s while the model downloads from Blob.

Then send one simulated reading with the **real** key:
```bash
cd src
python simulator.py --base $URL --device soilnode-01 --key "$SOIL_KEY" --scenario acidic --count 3 --interval 1
```
Expect `-> lime red ...` on the last lines.

Finally, open the dashboard **with the token**: `https://<app-name>.azurewebsites.net/?token=<ADMIN_TOKEN>`. Without the token, the panels show "offline" (403), which is intended.

If something fails, read the live log:
```bash
az webapp log tail -g $RG -n $APP
```

## 7. Point the devices at the cloud
In each `secrets.h` (git-ignored; see `02_hardware/firmware/*/secrets.h.example`):
- `API_BASE` = `https://<app-name>.azurewebsites.net`
- `DEVICE_KEY` = the matching key from step 1

**Important (S-02): one key per device, used everywhere.** The same `DEVICE_KEY` is sent to the cloud *and* to the laptop fallback (`API_BASE_LOCAL`). The laptop must therefore accept the **same keys**. Before starting the laptop backend, export the same value:
```bash
export SAWIT_DEVICE_KEYS="soilnode-01:<soil key>,cam-01:<cam key>"
```
Otherwise the laptop answers 401 and the fallback silently fails. `06_implementation_guide_beginner.md` §4 repeats this.

**One backend at a time (D39).** The cloud and the laptop keep separate databases and command queues. On demo day, choose one, point the dashboard *and* both devices at it, and check that the dashboard's mode pill (CLOUD/LOCAL) matches what the OLED shows.

## 8. Security notes (demo scope)
- Reads and writes need the admin token in cloud mode. `/api/v1/health` stays public for monitoring.
- Heat-map and image URLs (`/static/heatmaps/…`, `/media/images/…`) are unguessable evidence-ID paths but are not token-protected. Acceptable for a demo; the production design uses Entra ID (`04_cloud_design.md`).
- Rotate keys after the presentation (`az webapp config appsettings set …`). Delete everything when done:
  ```bash
  az group delete -n $RG -y
  ```
  This stops all spending.

## 9. Credit hygiene
- The B1 plan is the only resource that bills continuously. Stop it when idle with `az webapp stop -g $RG -n $APP`, and start it again with `az webapp start …`.
- Check spending under portal → Subscriptions → Azure for Students → Cost analysis.
