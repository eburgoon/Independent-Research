"""
Gravity Model Calibration and Prediction
=========================================
Model: T_j = k * P_i^alpha * A_j^beta / d_ij^gamma
Linearized: ln(T_j) = ln(k) + alpha*ln(P_i) + beta*ln(A_j) - gamma*ln(d_ij)
Calibration: OLS on 79 WMATA stations (2019 and 2023-24)
Prediction: 4 interchange stations, single 30% detour-rider shift
"""
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import statsmodels.api as sm
from statsmodels.stats.outliers_influence import variance_inflation_factor
import warnings
warnings.filterwarnings('ignore')

FIGURES  = 'figures'
PROCESSED = 'data/processed'

stations = pd.read_csv(f'{PROCESSED}/stations_full.csv')
stations = stations.dropna(subset=['pop_2019','jobs_2019','entries_2019'])

# ── Impedance proxy ───────────────────────────────────────────────────────────
# Activity density → scaled to access time range [5, 25] minutes
# NOTE: This proxy is derived from activity density and therefore shares
# variance with the attractiveness term (ln_A). VIF analysis below quantifies
# this collinearity. A more robust specification would use an independent
# impedance measure (e.g., average commute time from ACS).
d_min, d_max = 5, 25
stations['d_proxy'] = d_max - (
    (stations['activity_density'] / stations['activity_density'].max())
    * (d_max - d_min)
) if 'activity_density' in stations.columns else d_max - (
    ((stations['jobs_2019'] + stations['pop_2019']) /
     (stations['jobs_2019'] + stations['pop_2019']).max())
    * (d_max - d_min)
)
stations['d_proxy'] = stations['d_proxy'].clip(d_min, d_max)

# ── OLS Calibration — 2019 ────────────────────────────────────────────────────
df19 = stations[(stations['entries_2019'] > 0) &
                (stations['pop_2019'] > 0) &
                (stations['jobs_2019'] > 0)].copy()
df19['ln_T'] = np.log(df19['entries_2019'])
df19['ln_P'] = np.log(df19['pop_2019'])
df19['ln_A'] = np.log(df19['jobs_2019'])
df19['ln_d'] = np.log(df19['d_proxy'])

X19 = sm.add_constant(df19[['ln_P', 'ln_A', 'ln_d']])
model_2019 = sm.OLS(df19['ln_T'], X19).fit()

# ── OLS Calibration — 2024 ────────────────────────────────────────────────────
df24 = stations[(stations['entries_2024'] > 0) &
                (stations['pop_2023'] > 0) &
                (stations['jobs_2021'] > 0)].copy()
df24['ln_T'] = np.log(df24['entries_2024'])
df24['ln_P'] = np.log(df24['pop_2023'])
df24['ln_A'] = np.log(df24['jobs_2021'])
df24['ln_d'] = np.log(df24['d_proxy'])

X24 = sm.add_constant(df24[['ln_P', 'ln_A', 'ln_d']])
model_2024 = sm.OLS(df24['ln_T'], X24).fit()

# ── Print Results ─────────────────────────────────────────────────────────────
print("=" * 60)
print("2019 MODEL")
print("=" * 60)
print(model_2019.summary())

print("\n" + "=" * 60)
print("2024 MODEL")
print("=" * 60)
print(model_2024.summary())

# ── VIF Analysis ──────────────────────────────────────────────────────────────
print("\n" + "=" * 60)
print("VARIANCE INFLATION FACTORS (2019)")
print("=" * 60)
for i, col in enumerate(['const', 'ln_P', 'ln_A', 'ln_d']):
    vif = variance_inflation_factor(X19.values, i)
    print(f"  {col:>8}: VIF = {vif:.2f}")

# ── Prediction — Single 30% Scenario ─────────────────────────────────────────
# Detour riders: corridor population who gain >=10 min travel time savings
# DC metro transit mode share: 38% (ACS), avg household size: 2.4

transit_mode_share = 0.38
household_size     = 2.4
SHIFT_RATE         = 0.30   # 30% detour-rider shift (steady-state, 2-3 yr)
MIN_SAVINGS        = 10     # minutes — threshold for defining detour riders

# Purple Line corridor catchment populations newly accessible to each station.
# Each station's catchment includes only the corridor segments whose riders
# would plausibly transfer at THAT station specifically.
#
# Bethesda:         Western MoCo corridor (Chevy Chase Lake → Bethesda)
# Silver Spring:    Western MoCo corridor + Langley Park/Long Branch
# College Park UMD: College Park corridor + Langley Park/Long Branch
# New Carrollton:   College Park corridor + Riverdale/Hyattsville
#                   (NOT the full SS+CP corridor — those riders transfer earlier)
corridor_pop = {
    'Bethesda':         21800,
    'Silver Spring':    21800 + 7072,
    'College Park UMD': 16200 + 7072,
    'New Carrollton':   16200 + 7800,    # Fixed: CP corridor + eastern PG corridor only
}

# Average travel time savings (minutes) for each station's catchment
avg_time_savings = {
    'Bethesda':         8.0,
    'Silver Spring':    13.5,
    'College Park UMD': 15.5,
    'New Carrollton':   12.0,
}

rows = []
for station in ['Bethesda', 'Silver Spring', 'College Park UMD', 'New Carrollton']:
    savings = avg_time_savings[station]

    # Only count detour riders if average savings >= threshold
    if savings >= MIN_SAVINGS:
        detour_pool = (corridor_pop[station] / household_size) * transit_mode_share
    else:
        detour_pool = 0

    delta = SHIFT_RATE * detour_pool

    for period, base_col in [('2019', 'entries_2019'), ('2024', 'entries_2024')]:
        base = int(stations.loc[stations.station == station, base_col].values[0])
        rows.append({
            'station': station,
            'period': period,
            'base_entries': base,
            'detour_pool': round(detour_pool),
            'delta_detour': round(delta),
            'predicted_entries': round(base + delta),
            'pct_change': round((delta / base) * 100, 1),
            'time_savings_min': savings,
            'meets_threshold': savings >= MIN_SAVINGS,
        })

df_pred = pd.DataFrame(rows)
df_pred.to_csv(f'{PROCESSED}/predictions.csv', index=False)

# Print summary
print("\n" + "=" * 60)
print(f"PREDICTIONS (30% shift, >={MIN_SAVINGS} min savings threshold)")
print("=" * 60)

for period in ['2019', '2024']:
    print(f"\n  {period} BASE:")
    sub = df_pred[df_pred.period == period]
    for _, r in sub.iterrows():
        flag = "" if r.meets_threshold else " [below threshold]"
        print(f"    {r.station:<22} {r.base_entries:>6,} → {r.predicted_entries:>6,}"
              f"  (+{r.pct_change:.1f}%){flag}")
