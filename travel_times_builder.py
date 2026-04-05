"""
Travel time matrix: current WMATA vs. post-Purple Line.
Sources:
  Current: WMATA published timetables / trip planner
  Purple Line: MTA Maryland FEIS Chapter 3, Table 3-2
"""
import pandas as pd

current_times = {
    ('Bethesda', 'Silver Spring'): 12,
    ('Bethesda', 'College Park UMD'): 42,
    ('Bethesda', 'New Carrollton'): 48,
    ('Silver Spring', 'College Park UMD'): 35,
    ('Silver Spring', 'New Carrollton'): 42,
    ('College Park UMD', 'New Carrollton'): 28,
}
purple_times = {
    ('Bethesda', 'Silver Spring'): 16,
    ('Bethesda', 'College Park UMD'): 34,
    ('Bethesda', 'New Carrollton'): 48,
    ('Silver Spring', 'College Park UMD'): 18,
    ('Silver Spring', 'New Carrollton'): 32,
    ('College Park UMD', 'New Carrollton'): 14,
}

rows = []
for (o, d), cur in current_times.items():
    pur = purple_times[(o, d)]
    rows.append({'origin': o, 'destination': d,
                 'current_min': cur, 'purple_min': pur,
                 'savings_min': cur - pur})

pd.DataFrame(rows).to_csv('data/processed/travel_times.csv', index=False)
print("Saved travel_times.csv")
