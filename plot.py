import warnings
warnings.filterwarnings("ignore")

import pandas as pd
import numpy as np

import plotly.figure_factory as ff
import plotly.graph_objects as go

from data import load_data
from utils import load_state_abbrevs, load_args, calculate_surrounding_coords, check_county, check_state

def plot(df, county = "Barnstable County, MA", statistic = "cases", num_miles = 0):
    """Plot the user-specified county visualizing the user-specified statistic

    If the number of miles specified is 0, plot the entire county of the user-specified
    statistic, else plot the area of the county based on the specified number of miles (> 0).

    There is a case where there are multiple counties with the same name but are in
    different states. In this case: 
        
        Suffolk, New York
        Suffolk Massachusetts
        Bristol, Rhode Island
        Bristol Massachusetts

    ```python
    # This is the code to find the counties that appear more than once
    v = merged_df.county.value_counts()

    merged_df[merged_df.county.isin(v.index[v.gt(1)])]
    ```

    To deal with this (since there weren't that many), my approach was if any of these 
    special case counties and states are specified, implement another if-else conditional
    under the specified number of miles. See below.

    Args:
    =====
        df (pd.DataFrame): A pandas DataFrame from load_data()
        county (str): A US county
                      Default is 'Barnstable County, MA'
        statistic (str): COVID-19 statistic of interest
                         Default is 'cases'
        num_miles (int): The number of miles between 0 and 1000
                         Default is 0
    """
    # Split the user-specified county string and extract only the county
    # For example, the user specified county is "Barnstable County, MA",
    # extract the county "Barnstable" and the state "MA"
    split_county = county.split(" County, ")
    county = split_county[0]
    state = split_county[1]
    
    # Check if user inputted county and state exists in the dataframe
    county = check_county(df, county)

    state = state_abbrevs[state]
    
    state = check_state(df, state)

    # Check to make sure num_miles is within the range of 0 and 1000
    if num_miles < 0 or num_miles > 1000:
        raise Exception("Please input a number between 0 and 1000")
    
    # If the user specifies no miles, then plot the entire county
    # with the specified statistic
    if num_miles == 0:
        if (county == "Suffolk" and state == "Massachusetts") \
            or (county == "Bristol" and state == "Massachusetts") \
            or (county == "Suffolk" and state == "New York") \
            or (county == "Bristol" and state == "Rhode Island"):

            scope = [county, state]

            sample = df[(df["county"].isin(scope)) & (df["state"].isin(scope))]

            values = sample[statistic].tolist()
            fips = sample["fips"].tolist()

            colorscale = ["#f7fbff","#ebf3fb","#deebf7","#d2e3f3","#c6dbef","#b3d2e9","#9ecae1",
                          "#85bcdb","#6baed6","#57a0ce","#4292c6","#3082be","#2171b5","#1361a9",
                          "#08519c","#0b4083","#08306b"]

            endpts = list(np.linspace(1, 12, len(colorscale) - 1))

            fig = ff.create_choropleth(
                fips = fips, 
                values = values, 
                scope = scope,
                binning_endpoints = endpts,
                colorscale = colorscale, 
                show_state_data = True,
                show_hover = True,
                asp = 2.9,
                county_outline={'color': 'rgb(15, 15, 55)', 'width': 0.5},
                simplify_county = 0,
                simplify_state = 0, 
                state_outline = {'width': 1},
                legend_title = '# of {}'.format(statistic),
                title = '{} County, {} COVID-19 {}'.format(county, state, statistic)
            )

            fig.layout.template = None
            fig.update_geos(fitbounds = "locations")
            fig.show()
        
        else:
            scope = [county]

            sample = df[df["county"].isin(scope)]

            values = sample[statistic].tolist()
            fips = sample["fips"].tolist()

            colorscale = ["#f7fbff","#ebf3fb","#deebf7","#d2e3f3","#c6dbef","#b3d2e9","#9ecae1",
                          "#85bcdb","#6baed6","#57a0ce","#4292c6","#3082be","#2171b5","#1361a9",
                          "#08519c","#0b4083","#08306b"]

            endpts = list(np.linspace(1, 12, len(colorscale) - 1))

            fig = ff.create_choropleth(
                fips = fips, 
                values = values, 
                scope = scope,
                binning_endpoints = endpts,
                colorscale = colorscale, 
                show_state_data = True,
                show_hover = True,
                asp = 2.9,
                county_outline={'color': 'rgb(15, 15, 55)', 'width': 0.5},
                simplify_county = 0,
                simplify_state = 0, 
                state_outline = {'width': 1},
                legend_title = '# of {}'.format(statistic),
                title = '{} County, {} COVID-19 {}'.format(county, state, statistic)
            )

            fig.layout.template = None
            fig.update_geos(fitbounds = "locations")
            fig.show()
    
    # Else plot the area based on the number of miles specified
    else:
        if (county == "Suffolk" and state == "Massachusetts") \
            or (county == "Bristol" and state == "Massachusetts") \
            or (county == "Suffolk" and state == "New York") \
            or (county == "Bristol" and state == "Rhode Island"):

            scope = [county, state]

            sample = df[(df["county"].isin(scope)) & (df["state"].isin(scope))]

            values = sample[statistic].tolist()
            fips = sample["fips"].tolist()

            colorscale = ["#f7fbff","#ebf3fb","#deebf7","#d2e3f3","#c6dbef","#b3d2e9","#9ecae1",
                          "#85bcdb","#6baed6","#57a0ce","#4292c6","#3082be","#2171b5","#1361a9",
                          "#08519c","#0b4083","#08306b"]

            endpts = list(np.linspace(1, 12, len(colorscale) - 1))

            fig = ff.create_choropleth(
                fips = fips, 
                values = values, 
                scope = scope,
                binning_endpoints = endpts,
                colorscale = colorscale, 
                show_state_data = True,
                show_hover = True,
                asp = 2.9,
                county_outline={'color': 'rgb(15, 15, 55)', 'width': 0.5},
                simplify_county = 0,
                simplify_state = 0, 
                state_outline = {'width': 1},
                legend_title = '# of {}'.format(statistic),
                title = '{} County, {}  <br> (within {} miles) COVID-19 {}'.format(county, state, num_miles, statistic)
            )

            lat, lon = calculate_surrounding_coords(sample, num_miles)

            fig.layout.template = None
            fig.update_geos(fitbounds = "locations")
            fig.add_trace(go.Scattergeo(lon = lon,
                                        lat = lat,
                                        mode = 'markers'))
            fig.show()
            
        else:
            scope = [county]

            sample = df[df["county"].isin(scope)]

            values = sample[statistic].tolist()
            fips = sample["fips"].tolist()

            colorscale = ["#f7fbff","#ebf3fb","#deebf7","#d2e3f3","#c6dbef","#b3d2e9","#9ecae1",
                          "#85bcdb","#6baed6","#57a0ce","#4292c6","#3082be","#2171b5","#1361a9",
                          "#08519c","#0b4083","#08306b"]

            endpts = list(np.linspace(1, 12, len(colorscale) - 1))

            fig = ff.create_choropleth(
                fips = fips, 
                values = values, 
                scope = scope,
                binning_endpoints = endpts,
                colorscale = colorscale, 
                show_state_data = True,
                show_hover = True,
                asp = 2.9,
                county_outline={'color': 'rgb(15, 15, 55)', 'width': 0.5},
                simplify_county = 0,
                simplify_state = 0, 
                state_outline = {'width': 1},
                legend_title = '# of {}'.format(statistic),
                title = '{} County, {} <br> (within {} miles) COVID-19 {}'.format(county, state, num_miles, statistic)
            )

            lat, lon = calculate_surrounding_coords(sample, num_miles)

            fig.layout.template = None
            fig.update_geos(fitbounds = "locations")
            fig.add_trace(go.Scattergeo(lon = lon,
                                        lat = lat,
                                        mode = 'markers'))
            fig.show()

def main():
    merged_df = load_data()
    args = load_args()

    plot(merged_df, args.county, args.statistic, args.num_miles)

if __name__ == "__main__":
    main()
