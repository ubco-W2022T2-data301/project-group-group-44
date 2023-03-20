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
        .query("`year` == 2012")
        .reset_index()
        .drop([
            "year", "state", "county_fips", "office",
            "candidate", "version", "mode", "index",
        ], axis="columns")
        .rename({
            "county_name": "county",
            "state_po": "state",
            "candidatevotes": "votes",
            "totalvotes": "total"
        }, axis="columns")
        .apply(lambda x: x.str.capitalize() if x.name == "county" or x.name == "party" else x)
        .apply(combine_name_state, axis="columns")
        .merge(counties, left_on="county", right_on="name")
        .drop(["state", "name"], axis="columns")
        .assign(percent=lambda x: x.votes/x.total)
    )

    ## gb - the gaybourhoods dataset
    gb = (
        pd.read_csv("../data/raw/gaybourhoods.csv")
        .merge(cords, left_on="GEOID10", right_on="ZIP") \
        .drop([
            "Mjoint_MF", "Mjoint_SS", "Mjoint_FF", "Mjoint_MM",
            "Cns_TotHH", "Cns_UPSS", "Cns_UPFF", "Cns_UPMM",
            "ParadeFlag", "FF_Tax", "FF_Cns", "MM_Tax", "MM_Cns",
            "SS_Index_Weight", "Parade_Weight", "Bars_Weight",
            "GEOID10", "ZIP",
        ], axis="columns") \
        .rename({
            "LAT": "lat",
            "LNG": "long",
        }, axis="columns")
    )
    
    return (gb, pol, counties, cords)