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

    state_abbrevs = load_state_abbrevs()

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

            colorscale = ["#8dd3c7", "#ffffb3", "#bebada", "#fb8072",
                         "#80b1d3", "#fdb462", "#b3de69", "#fccde5",
                         "#d9d9d9", "#bc80bd", "#ccebc5", "#ffed6f",
                         "#8dd3c7", "#ffffb3", "#bebada", "#fb8072",
                         "#80b1d3", "#fdb462", "#b3de69", "#fccde5",
                         "#d9d9d9", "#bc80bd", "#ccebc5", "#ffed6f",
                         "#8dd3c7", "#ffffb3", "#bebada", "#fb8072",
                         "#80b1d3", "#fdb462", "#b3de69", "#fccde5",
                         "#d9d9d9", "#bc80bd", "#ccebc5", "#ffed6f"]

            fig = ff.create_choropleth(
                fips = fips, 
                values = values, 
                scope = scope,
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

            colorscale = ["#8dd3c7", "#ffffb3", "#bebada", "#fb8072",
                         "#80b1d3", "#fdb462", "#b3de69", "#fccde5",
                         "#d9d9d9", "#bc80bd", "#ccebc5", "#ffed6f",
                         "#8dd3c7", "#ffffb3", "#bebada", "#fb8072",
                         "#80b1d3", "#fdb462", "#b3de69", "#fccde5",
                         "#d9d9d9", "#bc80bd", "#ccebc5", "#ffed6f",
                         "#8dd3c7", "#ffffb3", "#bebada", "#fb8072",
                         "#80b1d3", "#fdb462", "#b3de69", "#fccde5",
                         "#d9d9d9", "#bc80bd", "#ccebc5", "#ffed6f"]

            fig = ff.create_choropleth(
                fips = fips, 
                values = values, 
                scope = scope,
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

            sample = df[(df["county"].isin([county])) & (df["state"].isin([state]))]
            lat, lon = calculate_surrounding_coords(sample, num_miles)

            # Here, I filtered out the counties and states that do not meet the specified radius
            # Remember:
            # lat = [north, east, south, west]
            # long = [north, east, south, west]
            new_df = df[(df.latitude < lat[0]) & (df.latitude > lat[2]) & (df.longitude > lon[3]) & (df.longitude < lon[1])]

            values = new_df[statistic].tolist()
            fips = new_df["fips"].tolist()

            colorscale = ["#8dd3c7", "#ffffb3", "#bebada", "#fb8072",
                         "#80b1d3", "#fdb462", "#b3de69", "#fccde5",
                         "#d9d9d9", "#bc80bd", "#ccebc5", "#ffed6f",
                         "#8dd3c7", "#ffffb3", "#bebada", "#fb8072",
                         "#80b1d3", "#fdb462", "#b3de69", "#fccde5",
                         "#d9d9d9", "#bc80bd", "#ccebc5", "#ffed6f",
                         "#8dd3c7", "#ffffb3", "#bebada", "#fb8072",
                         "#80b1d3", "#fdb462", "#b3de69", "#fccde5",
                         "#d9d9d9", "#bc80bd", "#ccebc5", "#ffed6f"]

            fig = ff.create_choropleth(
                fips = fips, 
                values = values, 
                scope = list(set(new_df["state"].tolist())),
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

            fig.layout.template = None
            fig.update_geos(fitbounds = "locations")
            fig.show()
            
        else:
            sample = df[df["county"].isin([county])]
            lat, lon = calculate_surrounding_coords(sample, num_miles)
            new_df = df[(df.latitude < lat[0]) & (df.latitude > lat[2]) & (df.longitude > lon[3]) & (df.longitude < lon[1])]

            values = new_df[statistic].tolist()
            fips = new_df["fips"].tolist()

            colorscale = ["#8dd3c7", "#ffffb3", "#bebada", "#fb8072",
                         "#80b1d3", "#fdb462", "#b3de69", "#fccde5",
                         "#d9d9d9", "#bc80bd", "#ccebc5", "#ffed6f",
                         "#8dd3c7", "#ffffb3", "#bebada", "#fb8072",
                         "#80b1d3", "#fdb462", "#b3de69", "#fccde5",
                         "#d9d9d9", "#bc80bd", "#ccebc5", "#ffed6f",
                         "#8dd3c7", "#ffffb3", "#bebada", "#fb8072",
                         "#80b1d3", "#fdb462", "#b3de69", "#fccde5",
                         "#d9d9d9", "#bc80bd", "#ccebc5", "#ffed6f"]

            fig = ff.create_choropleth(
                fips = fips, 
                values = values, 
                scope = list(set(new_df["state"].tolist())),
                colorscale = colorscale, 
                show_state_data = True,
                show_hover = True,
                centroid_marker = {"opacity": 0},
                asp = 2.9,
                state_outline = {'width': 1},
                legend_title = '# of {}'.format(statistic),
                title = '{} County, {} (within {} miles) COVID-19 {}'.format(county, state, num_miles, statistic)
            )

            fig.layout.template = None
            fig.update_geos(fitbounds = "locations")
            fig.show()

def main():
    merged_df = load_data()
    args = load_args()

    plot(merged_df, args.county, args.statistic, args.num_miles)

if __name__ == "__main__":
    main()
