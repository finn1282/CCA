"""M5 — Sentinel-2 NDVI anomaly per estate block, pre-computed in Google Earth Engine (stakeholder step, D31).

What it does
  1. AOI: a 4 km x 4 km oil-palm area in Johor (default, editable with --lon/--lat/--size-km).
  2. Masks to industrial/smallholder oil palm (Descals et al. 2021, BIOPAMA/GlobalOilPalm/v1, CC BY 4.0).
  3. Sentinel-2 L2A (COPERNICUS/S2_SR_HARMONIZED) cloud-masked with Cloud Score+ → monthly median NDVI.
  4. Splits the AOI into a grid of "blocks" (default 4x4 = 16 blocks of 1 km²), named B01..B16.
  5. Per block: monthly mean NDVI series; z-score of the latest month vs the block's own history.
  6. Writes for the dashboard (03_software/src/static/precomputed/):
       satellite.json        — blocks, months, estate series, z-scores (read by /api/v1/satellite and the cascade)
       satellite_ndvi.png    — latest-month NDVI anomaly (z) map with block grid
     and optionally starts a GeoTIFF export to Google Drive (--drive).

Credentials: never hard-coded. Set EE_PROJECT (your Earth Engine Cloud project ID) and authenticate once with
`earthengine authenticate` (stores a token in your home folder, outside the repo).
Run:  EE_PROJECT=my-project python gee/ndvi_estate.py
Attribution required on any output: "Contains modified Copernicus Sentinel data [year]" (COPERNICUS-LEGAL).
"""
from __future__ import annotations

import argparse
import json
import os
import statistics
import urllib.request
from datetime import date
from pathlib import Path

import ee

OUT = Path(__file__).resolve().parents[1] / "src" / "static" / "precomputed"


def month_starts(n_months: int) -> list[str]:
    today = date.today().replace(day=1)
    y, m = today.year, today.month
    out = []
    for _ in range(n_months):
        m -= 1
        if m == 0:
            y, m = y - 1, 12
        out.append(f"{y:04d}-{m:02d}-01")
    return sorted(out)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--lon", type=float, default=103.30, help="AOI centre longitude (default: Kluang district, Johor)")
    ap.add_argument("--lat", type=float, default=1.96, help="AOI centre latitude")
    ap.add_argument("--size-km", type=float, default=4.0)
    ap.add_argument("--grid", type=int, default=4, help="blocks per side")
    ap.add_argument("--months", type=int, default=24)
    ap.add_argument("--cs", type=float, default=0.60, help="Cloud Score+ clear threshold")
    ap.add_argument("--drive", action="store_true", help="also export latest NDVI GeoTIFF to Google Drive")
    a = ap.parse_args()

    project = os.environ.get("EE_PROJECT")
    if not project:
        raise SystemExit("Set EE_PROJECT to your Earth Engine Cloud project ID (see gee/RUN_EARTH_ENGINE.md)")
    ee.Initialize(project=project)

    half = a.size_km / 2 / 111.32
    aoi = ee.Geometry.Rectangle([a.lon - half, a.lat - half, a.lon + half, a.lat + half])

    palm = ee.ImageCollection("BIOPAMA/GlobalOilPalm/v1").select("classification").mosaic()
    palm_mask = palm.lte(2)  # 1 industrial, 2 smallholder, 3 other land cover

    s2 = ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED").filterBounds(aoi)
    csp = ee.ImageCollection("GOOGLE/CLOUD_SCORE_PLUS/V1/S2_HARMONIZED")

    def ndvi(img):
        clear = img.select("cs").gte(a.cs)
        return img.normalizedDifference(["B8", "B4"]).rename("ndvi").updateMask(clear).updateMask(palm_mask)

    s2 = s2.linkCollection(csp, ["cs"]).map(ndvi)

    # Grid of blocks
    step = a.size_km / a.grid / 111.32
    x0, y0 = a.lon - half, a.lat + half
    feats = []
    for r in range(a.grid):
        for c in range(a.grid):
            bid = f"B{r * a.grid + c + 1:02d}"
            g = ee.Geometry.Rectangle([x0 + c * step, y0 - (r + 1) * step, x0 + (c + 1) * step, y0 - r * step])
            feats.append(ee.Feature(g, {"block_id": bid}))
    blocks = ee.FeatureCollection(feats)

    months = month_starts(a.months)
    series: dict[str, list] = {f["properties"]["block_id"]: [] for f in blocks.getInfo()["features"]}
    estate, valid_months, latest_img, good = [], [], None, []
    for m in months:
        start = ee.Date(m)
        comp = s2.filterDate(start, start.advance(1, "month")).median().clip(aoi)
        stats = comp.reduceRegions(collection=blocks, reducer=ee.Reducer.mean(), scale=10).getInfo()
        est = comp.reduceRegion(ee.Reducer.median(), aoi, 10, maxPixels=1e9).get("ndvi").getInfo()
        for f in stats["features"]:
            v = f["properties"].get("mean")
            series[f["properties"]["block_id"]].append(round(v, 4) if v is not None else None)
        estate.append(round(est, 4) if est is not None else None)
        valid_months.append(m[:7])
        if est is not None:
            latest_img, latest_month = comp, m[:7]
            good.append(m)
        print(m[:7], "estate NDVI", estate[-1])

    out_blocks = []
    for bid, vals in series.items():
        hist = [v for v in vals[:-1] if v is not None]
        last = next((v for v in reversed(vals) if v is not None), None)
        if last is not None and len(hist) >= 6 and statistics.pstdev(hist) > 0:
            z = round((last - statistics.mean(hist)) / statistics.pstdev(hist), 2)
        else:
            z = None
        out_blocks.append({"block_id": bid, "ndvi_latest": last, "ndvi_z_latest": z, "series": vals})

    # Anomaly map: z of latest composite vs mean/std of the history composites
    if latest_img is None or len(good) < 4:
        raise SystemExit("Too few cloud-free months — enlarge --months or lower --cs")
    hist_col = ee.ImageCollection([s2.filterDate(ee.Date(m), ee.Date(m).advance(1, "month")).median() for m in good[:-1]])
    zimg = latest_img.subtract(hist_col.mean()).divide(hist_col.reduce(ee.Reducer.stdDev()))
    vis = zimg.visualize(min=-2.5, max=2.5, palette=["b2182b", "ef8a62", "fddbc7", "f7f7f7", "d1e5f0", "67a9cf", "2166ac"])
    grid = ee.Image().byte().paint(blocks, 0, 1).visualize(palette=["000000"])
    url = vis.blend(grid).getThumbURL({"region": aoi, "dimensions": 768, "format": "png"})
    OUT.mkdir(parents=True, exist_ok=True)
    urllib.request.urlretrieve(url, OUT / "satellite_ndvi.png")

    meta = {
        "available": True,
        "source": f"Sentinel-2 L2A (Copernicus), Cloud Score+ ≥ {a.cs}, oil-palm mask Descals et al. 2021 — Earth Engine",
        "attribution": f"Contains modified Copernicus Sentinel data {date.today().year}",
        "aoi": {"lon": a.lon, "lat": a.lat, "size_km": a.size_km, "grid": a.grid},
        "latest_month": latest_month, "months": valid_months, "estate_ndvi": estate,
        "method": "Monthly median NDVI per block; z = (latest − mean(history)) / sd(history); flag z ≤ −1.5",
        "image": "/static/precomputed/satellite_ndvi.png",
        "blocks": out_blocks,
    }
    (OUT / "satellite.json").write_text(json.dumps(meta, indent=1))
    print("wrote", OUT / "satellite.json", "and satellite_ndvi.png")
    flagged = [b["block_id"] for b in out_blocks if b["ndvi_z_latest"] is not None and b["ndvi_z_latest"] <= -1.5]
    print("blocks flagged for drone survey (z ≤ −1.5):", flagged or "none")

    if a.drive:
        task = ee.batch.Export.image.toDrive(image=latest_img.toFloat(), description="sawitsense_ndvi_latest",
                                             folder="sawitsense", region=aoi, scale=10, fileFormat="GeoTIFF")
        task.start()
        print("Drive export started (check https://code.earthengine.google.com/tasks)")


if __name__ == "__main__":
    main()
