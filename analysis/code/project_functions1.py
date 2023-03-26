import numpy as np
from math import pi
import pandas as pd

def load_and_process():
    
    # cords - mapping zip codes to long/lat coordinates
    cords = pd.read_csv("../data/raw/zip_lat_long.csv")
    
    ## counties - Relating US counties to their long/lat position on the Earth
    # Combine the county name with the state code
    def combine_name_state(row):
        row["name"] = f"{row['name']} {row['STUSAB']}"
        return row

    counties = (
        pd.read_csv("../data/raw/us-county-boundaries.csv", sep=";")
        .rename({
            "NAME": "name",
            "INTPTLAT": "lat",
            "INTPTLON": "long",
        }, axis="columns")
        .apply(combine_name_state, axis="columns")
        .drop(["STUSAB"], axis="columns")
    )
    

    ## pol - Election results from the 2012 American presidential election
    def combine_name_state(row):
        row["county"] = f"{row['county']} {row['state']}"
        return row

    pol = (
        pd.read_csv("../data/raw/countypres_2000-2020.csv")
        .query("`year` == 2012 & `party` == 'DEMOCRAT'")
        .reset_index()
        .drop([
            "year", "state", "county_fips", "office",
            "candidate", "version", "mode", "index",
            "party"
        ], axis="columns")
        .rename({
            "county_name": "county",
            "state_po": "state",
            "candidatevotes": "votes",
            "totalvotes": "total"
        }, axis="columns")
        .apply(lambda x: x.str.capitalize() if x.name == "county" else x)
        .apply(combine_name_state, axis="columns")
        .merge(counties, left_on="county", right_on="name")
        .drop(["state", "name"], axis="columns")
        .assign(percent=lambda x: x.votes/x.total)
        .drop(["votes", "total"], axis="columns")
    )

    ## gb - the gaybourhoods dataset
    gb = (
        pd.read_csv("../data/raw/gaybourhoods.csv")
        .merge(cords, left_on="GEOID10", right_on="ZIP")
        .drop([
            "Tax_Mjoint", "TaxRate_SS", "TaxRate_FF", "TaxRate_MM",
            "Cns_RateSS", "Cns_RateFF", "Cns_RateMM", "CountBars",
            "Mjoint_MF", "Mjoint_SS", "Mjoint_FF", "Mjoint_MM",
            "Cns_TotHH", "Cns_UPSS", "Cns_UPFF", "Cns_UPMM",
            "ParadeFlag", "FF_Tax", "FF_Cns", "MM_Tax", "MM_Cns",
            "SS_Index_Weight", "Parade_Weight", "Bars_Weight",
            "GEOID10", "ZIP", "FF_Index", "MM_Index",
        ], axis="columns")
        .rename({
            "LAT": "lat",
            "LNG": "long",
        }, axis="columns")
    )
    
    def kinsify(index, **kwargs):
        max_index = 25
        if index < max_index/7:
            return 0
        elif index < max_index*2/7:
            return 1
        elif index < max_index*3/7:
            return 2
        elif index < max_index*4/7:
            return 3
        elif index < max_index*5/7:
            return 4
        elif index < max_index*6/7:
            return 5
        else:
            return 6
    
    gb["kinsey"] = gb.SS_Index.apply(kinsify, axis="columns")
   
    percent_democrat = np.empty(len(gb.index))
    neighbourhood_kinsey = np.empty(len(gb.index))
    for i, row in gb.iterrows():
        percent_democrat[i] = nearest_neighbour(pol, (row.long, row.lat), interval=.1).percent
        neighbourhood_kinsey[i] = select_smallest_neighbourhood(gb, (row.long, row.lat), interval=.1).kinsey.mean()

    gb["percent_democrat"] = pd.Series(data=percent_democrat)
    gb["neighbourhood_kinsey"] = pd.Series(data=neighbourhood_kinsey)
    
    return (gb, pol, counties, cords)

def select_region(df, left, right, bottom, top):
    """
    Takes a dataframe with columns `long` and `lat` corresponding to
    coordinates and returns a subset of the dataframe containing only entries
    between the given boundaries
    """
    return df[(df["long"] > left) & (df["long"] < right) & (df["lat"] > bottom) & (df["lat"] < top)]

def select_smallest_neighbourhood(df, pos, interval=1, multiplier=1.5, expansion_limit=10):
    subset = select_region(df, pos[0]-interval, pos[0]+interval, pos[1]-interval, pos[1]+interval)
    cinterval = interval
    while subset.count().lat == 0:
        cinterval += interval
        #interval *= multiplier
        subset = select_region(df, pos[0]-cinterval, pos[0]+cinterval, pos[1]-cinterval, pos[1]+cinterval)
    
    return subset

def nearest_neighbour(df, pos, interval=1, multiplier=1.5, expansion_limit=10):
    """
    Given a dataframe with columns `long` and `lat` corresponding to
    coordinates and a `pos` pair of long/lat coordinates, determine the
    coordinates of the nearest observation in the dataset by running the
    following algorithm:
    1. Find all points within (long+-interval, lat+-interval)
    2. If there are no other points within the range, start from step 1 and
    set interval *= multiplier
    3. Calculate the distance between pos and each point in the interval
    3. Return the point with the lowest distance that isn't pos
    """
    
    subset = select_smallest_neighbourhood(df, pos, interval, multiplier, expansion_limit)
    
    subset = subset.assign(distance=distance(*pos, subset["lat"], subset["long"]))
    return subset.sort_values("distance").reset_index().iloc[0]

# Efficient implementation of the haversine formula
# Source: https://stackoverflow.com/a/21623206
def distance(lat1, lon1, lat2, lon2):
    p = pi/180
    a = 0.5 - np.cos((lat2-lat1)*p)/2 + np.cos(lat1*p) * np.cos(lat2*p) * (1-np.cos((lon2-lon1)*p))/2
    return 12742 * np.arcsin(np.sqrt(a))
