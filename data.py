import pandas as pd 
import numpy as np

from utils import load_state_abbrevs

import warnings
warnings.filterwarnings("ignore")

def __preprocess_counties_data(counties_df):
    """Preprocess the NY Times Counties Data
    
    Essentially: replace missing values with 0's, remove rows with no relevant information, convert some columns
                 to appropriate data types
                 
    Args:
    =====
        counties_df (pd.DataFrame): A pandas DataFrame of the NY Times Counties Data
        
    Returns:
    ========
        counties_df (pd.DataFrame): A pandas DataFrame of the cleaned NY Times Counties Data
    """
    # Convert the date column to datetime format
    counties_df.loc[:, "date"] = pd.to_datetime(counties_df.loc[:, 'date'], format = '%Y-%m-%d')
    
    # Replace all missing values in the dataframe with 0's
    counties_df.fillna(0, inplace = True)
    
    # Columns to be converted from type float to type int
    # Converting because Plotly only takes fips as int, and there cannot be 0.5 of a case, death, etc..
    numeric_cols = ['fips', 'cases', 'deaths', 'confirmed_cases', 
                    'confirmed_deaths', 'probable_cases', 'probable_deaths']
    counties_df.loc[:, numeric_cols] = counties_df.loc[:, numeric_cols].applymap(np.int64)
    
    # Columns to be converted to type string
    string_cols = ['county', 'state']
    counties_df.loc[:, string_cols] = counties_df.loc[:, string_cols].applymap(str)
    
    return counties_df

def __preprocess_geocodes_data(geocode_df):
    """Preprocess the Geocodes USA Counties Data
    
    Same purpose as the __preprocess_counties_data() function
    
    Args:
    =====
        geocode_df (pd.DataFrame): A pandas DataFrame of the Geocodes USA Counties data
        
    Returns:
    ========
        small_geocode (pd.DataFrame): A pandas DataFrame of the cleaned Geocodes USA Counties data
    """
    # Remove all rows that are related to military bases
    geocode_df = geocode_df[geocode_df.loc[:, "state"] != "AE"]
    
    # Replace all missing values in the dataframe with 0's
    geocode_df.fillna(0, inplace = True)
    
    # Load the state abbreviations dictionary
    state_abbrevs = load_state_abbrevs()
    
    # Convert each of the state abbreviations in the "state" column
    # to their full state name to maintain consistency with counties_df
    geocode_df.loc[:, "state"] = geocode_df.loc[:, "state"].map(state_abbrevs)
    
    # After converting the state abbreviations, there are some additional missing values,
    # drop these missing values as they are not relevant
    geocode_df.loc[:, "state"].dropna(inplace = True)
    
    # Remove rows that have no county value
    geocode_df = geocode_df[geocode_df.loc[:, "county"] != 0]
    
    # Since the dataframe has multiple listings of the same county and state but with very
    # similar latitude and longitude values, I decided to group these same counties and states into one by
    # taking the average of their latitude, longitude, and estimated population values
    # From geocode_df, I keep columns that I deem relevant and consistent with counties_df
    small_geocode = geocode_df.groupby(["county", "state"], as_index = False)["latitude", "longitude", "estimated_population"].mean()
    
    # Additional cleaning
    # Some Puerto Rico counties have accents, need to remove them to be consistent with
    # counties_df
    small_geocode.loc[:, "county"] = small_geocode.loc[:, "county"].replace({"BayamÃƒÂ³n": "Bayamon"})
    small_geocode.loc[:, "county"] = small_geocode.loc[:, "county"].replace({"CataÃƒÂ±o": "Catano"})
    small_geocode.loc[:, "county"] = small_geocode.loc[:, "county"].replace({"CanÃƒÂ³vanas": "Canovanas"})
    
    # Round the values in estimated_population to the nearest integer
    # since you cannot have half of a person
    small_geocode.loc[:, "estimated_population"] = small_geocode.loc[:, "estimated_population"].round(0).astype(int)
    
    return small_geocode

def load_data(nytimes_url  = "https://raw.githubusercontent.com/nytimes/covid-19-data/master/live/us-counties.csv",
              data_gov_url = "https://data.healthcare.gov/resource/geocodes-usa-with-counties.json"):

    """Load in the data from the URL links into pandas DataFrames

    Args:
    =====
        nytimes_url  (str): The URL link from the NY Times GitHub of the COVID-19 US County cases data
        data_gov_url (str): The URL link from data.gov of the US counties geocodes

    Returns:
    ========
        merged_df (pd.DataFrame): The merged and cleaned pandas DataFrame of the
                                  NY Times Counties and Geocodes USA Counties data
    """
    counties_df = pd.read_csv(nytimes_url)

    geocode_df = pd.read_json(data_gov_url)
    
    # Preprocess the two dataframes
    counties_df_preprocessed = __preprocess_counties_data(counties_df)
    geocode_df_preprocessed = __preprocess_geocodes_data(geocode_df)
    
    # Finally, merge the two dataframes on the same two columns "county"
    # and "state"
    merged_df = pd.merge(counties_df_preprocessed, 
                         geocode_df_preprocessed, 
                         on = ["county", "state"])

    return merged_df