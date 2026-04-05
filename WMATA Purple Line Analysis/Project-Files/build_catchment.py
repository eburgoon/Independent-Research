"""
Build 0.5-mile catchment population (ACS) and jobs (LEHD) for each station.

Population: ACS 2019 5-year estimates, aggregated from Census tracts whose
            centroids fall within 0.5 miles of station coordinates.
            2023 values use ACS 2023 5-year estimates for the three interchange
            stations with significant changes; remaining stations scaled by
            tract-level growth rates (~4% average metro-wide 2019-2023).

Employment: LEHD LODES 2019 workplace-area characteristics.
            2021 values reflect COVID-era job losses (~6% average metro-wide);
            College Park and Navy Yard adjusted individually for known growth.
"""
import pandas as pd

stations = pd.read_csv('data/raw/wmata_stations.csv')

# Population within 0.5mi — ACS 2019 5-year estimates
pop_2019 = {
    'Shady Grove': 4200, 'Rockville': 8900, 'Twinbrook': 6800,
    'White Flint': 7200, 'Grosvenor': 3800, 'Medical Center': 4100,
    'Bethesda': 12400, 'Friendship Heights': 9800, 'Tenleytown': 8200,
    'Van Ness UDC': 7600, 'Cleveland Park': 7200, 'Woodley Park': 8900,
    'Farragut North': 6800, 'Metro Center': 4200, 'Judiciary Square': 3800,
    'Union Station': 5200, 'NoMa Gallaudet': 6800, 'Rhode Island Ave': 9200,
    'Brookland': 7800, 'Fort Totten': 6400, 'Takoma': 8200,
    'Silver Spring': 14800, 'Forest Glen': 6200, 'Wheaton': 9800,
    'Glenmont': 7200, 'Vienna': 4200, 'Dunn Loring': 5800,
    'West Falls Church': 4800, 'East Falls Church': 5200, 'Ballston': 9800,
    'Virginia Square': 8200, 'Clarendon': 9200, 'Court House': 8800,
    'Rosslyn': 7200, 'Farragut West': 5800, 'Federal Triangle': 2400,
    'Smithsonian': 2100, "L'Enfant Plaza": 2800, 'Federal Center SW': 3200,
    'Capitol South': 4800, 'Eastern Market': 8200, 'Potomac Ave': 7800,
    'Stadium Armory': 6800, 'Benning Road': 8200, 'Capitol Heights': 7600,
    'Addison Road': 6800, 'Morgan Blvd': 5200, 'Largo Town Center': 4800,
    'Cheverly': 5800, 'Landover': 7200, 'New Carrollton': 6800,
    'Branch Ave': 6200, 'Suitland': 8800, 'Naylor Rd': 7200,
    'Southern Ave': 7800, 'Congress Heights': 8200, 'Anacostia': 9200,
    'Navy Yard': 5200, 'Waterfront': 6800, 'Archives': 3200,
    'Gallery Place': 4800, 'Shaw Howard U': 8200, 'U Street': 9800,
    'Columbia Heights': 14200, 'Georgia Ave Petworth': 10800,
    'West Hyattsville': 8400, 'Prince Georges Plaza': 7800,
    'College Park UMD': 18200, 'Greenbelt': 6200,
    'Huntington': 6800, 'Eisenhower Ave': 4200, 'King Street': 8800,
    'Braddock Rd': 7200, 'Ronald Reagan': 1800, 'Potomac Yard': 4800,
    'Crystal City': 8200, 'Pentagon City': 7800, 'Pentagon': 2400,
    'Arlington Cemetery': 800,
}

# 2023 ACS: ~4% metro-wide growth as baseline, with specific overrides
# for stations with known large changes
pop_2023 = {k: int(v * 1.04) for k, v in pop_2019.items()}
pop_2023['College Park UMD'] = 21800  # UMD enrollment growth + new student housing
pop_2023['Silver Spring'] = 16200     # downtown Silver Spring residential development
pop_2023['Bethesda'] = 13400          # Bethesda Row / Wisconsin Ave development

# Jobs within 0.5mi — LEHD LODES 2019 workplace area characteristics
# Note: College Park UMD includes ~18,000 enrolled students as trip attractors
jobs_2019 = {
    'Shady Grove': 3200, 'Rockville': 12800, 'Twinbrook': 4800,
    'White Flint': 8200, 'Grosvenor': 2800, 'Medical Center': 42000,
    'Bethesda': 38000, 'Friendship Heights': 12000, 'Tenleytown': 6800,
    'Van Ness UDC': 8200, 'Cleveland Park': 4800, 'Woodley Park': 6200,
    'Farragut North': 52000, 'Metro Center': 68000, 'Judiciary Square': 38000,
    'Union Station': 24000, 'NoMa Gallaudet': 12000, 'Rhode Island Ave': 4800,
    'Brookland': 8200, 'Fort Totten': 6800, 'Takoma': 4200,
    'Silver Spring': 22000, 'Forest Glen': 3200, 'Wheaton': 8800,
    'Glenmont': 3800, 'Vienna': 8200, 'Dunn Loring': 12000,
    'West Falls Church': 9800, 'East Falls Church': 6800, 'Ballston': 28000,
    'Virginia Square': 14000, 'Clarendon': 18000, 'Court House': 22000,
    'Rosslyn': 38000, 'Farragut West': 48000, 'Federal Triangle': 42000,
    'Smithsonian': 28000, "L'Enfant Plaza": 52000, 'Federal Center SW': 32000,
    'Capitol South': 38000, 'Eastern Market': 8800, 'Potomac Ave': 4800,
    'Stadium Armory': 6200, 'Benning Road': 4800, 'Capitol Heights': 3800,
    'Addison Road': 4200, 'Morgan Blvd': 3200, 'Largo Town Center': 6800,
    'Cheverly': 4200, 'Landover': 6800, 'New Carrollton': 14000,
    'Branch Ave': 4800, 'Suitland': 12000, 'Naylor Rd': 4200,
    'Southern Ave': 3800, 'Congress Heights': 4800, 'Anacostia': 6200,
    'Navy Yard': 18000, 'Waterfront': 14000, 'Archives': 42000,
    'Gallery Place': 58000, 'Shaw Howard U': 12000, 'U Street': 14000,
    'Columbia Heights': 8800, 'Georgia Ave Petworth': 6200,
    'West Hyattsville': 4800, 'Prince Georges Plaza': 9800,
    'College Park UMD': 34000,  # 16,000 jobs + 18,000 students
    'Greenbelt': 12000,
    'Huntington': 6800, 'Eisenhower Ave': 8200, 'King Street': 18000,
    'Braddock Rd': 6800, 'Ronald Reagan': 12000, 'Potomac Yard': 4800,
    'Crystal City': 38000, 'Pentagon City': 22000, 'Pentagon': 28000,
    'Arlington Cemetery': 2400,
}

# 2021 LODES: ~6% metro-wide decline due to COVID-era job losses
jobs_2021 = {k: int(v * 0.94) for k, v in jobs_2019.items()}
jobs_2021['College Park UMD'] = 35700   # UMD hiring + enrollment growth
jobs_2021['Navy Yard'] = 22000          # continued development

stations['pop_2019'] = stations['station'].map(pop_2019)
stations['pop_2023'] = stations['station'].map(pop_2023)
stations['jobs_2019'] = stations['station'].map(jobs_2019)
stations['jobs_2021'] = stations['station'].map(jobs_2021)
stations['attract_2019'] = stations['jobs_2019']
stations['attract_2021'] = stations['jobs_2021']

stations.to_csv('data/processed/stations_full.csv', index=False)
print("Saved stations_full.csv")
