# Estimating Post-Opening Ridership at WMATA–Purple Line Interchange Stations

Independent research project — Ethan Burgoon, April 2026

## Overview

This project uses a gravity model calibrated on WMATA station-level ridership data to predict how daily entries will change at the four Purple Line–Metro interchange stations (Bethesda, Silver Spring, College Park–UMD, New Carrollton) when the Maryland Purple Line opens in late 2027.

## Structure

```
purple-line-project/
├── paper.tex                          # LaTeX source (compile on Overleaf)
├── README.md
├── scripts/
│   ├── wmata_stations.py              # Station dataset (coords, ridership, lines)
│   ├── build_catchment.py             # Catchment pop (ACS) and jobs (LEHD)
│   ├── travel_times_builder.py        # Current vs Purple Line travel times
│   └── gravity_model.py              # OLS calibration + predictions
├── data/
│   ├── raw/                           # wmata_stations.csv (generated)
│   └── processed/                     # stations_full.csv, travel_times.csv, predictions.csv
└── figures/                           # PNG figures (referenced by paper.tex)
```

## Running

Scripts should be run in order from the project root:

```bash
python scripts/wmata_stations.py
python scripts/build_catchment.py
python scripts/travel_times_builder.py
python scripts/gravity_model.py
```

Requires: `pandas`, `numpy`, `statsmodels`, `matplotlib`

## Data Sources

- **Ridership**: WMATA Ridership Data Portal (2019 pre-pandemic, 2023–24 recovery)
- **Population**: ACS 5-year estimates (2019, 2023)
- **Employment**: LEHD LODES (2019, 2021)
- **Travel times**: WMATA timetables + FEIS Chapter 3

## Key Results (30% detour-rider shift, 2024 base)

| Station | Current | Predicted | Change |
|---------|---------|-----------|--------|
| Bethesda | 9,200 | 9,200 | +0% |
| Silver Spring | 7,400 | 8,771 | +19% |
| College Park–UMD | 2,800 | 3,905 | +39% |
| New Carrollton | 4,200 | 5,340 | +27% |

Note: Bethesda's average savings (8 min) falls below the 10-minute detour threshold, so the model predicts zero detour-rider gain there. Bethesda's actual post-opening growth will likely come from induced demand along the Montgomery County corridor, which this model does not capture.
