import argparse

from geopy.point import Point
from geopy.units import kilometers
import geopy.distance

def load_state_abbrevs():
    """Utility function of each state's abbreviations
    
    Returns:
    ========
        state_abbrevs (dict): A dictionary containing each state's abbreviations
    """
    state_abbrevs = {"AL": "Alabama",
                     "AK": "Alaska",
                     "AZ": "Arizona",
                     "AR": "Arkansas",
                     "CA": "Calfornia",
                     "CO": "Colorado",
                     "CT": "Connecticut",
                     "DE": "Delaware",
                     "FL": "Florida",
                     "GA": "Georgia",
                     "HI": "Hawaii",
                     "ID": "Idaho",
                     "IL": "Illinois",
                     "IN": "Indiana",
                     "IA": "Iowa",
                     "KS": "Kansas",
                     "KY": "Kentucky",
                     "LA": "Louisiana",
                     "ME": "Maine",
                     "MD": "Maryland",
                     "MA": "Massachusetts",
                     "MI": "Michigan",
                     "MN": "Minnesota",
                     "MS": "Mississippi",
                     "MO": "Missouri",
                     "MT": "Montana",
                     "NE": "Nebraska",
                     "NV": "Nevada",
                     "NH": "New Hampshire",
                     "NJ": "New Jersey",
                     "NM": "New Mexico",
                     "NY": "New York",
                     "NC": "North Carolina",
                     "ND": "North Dakota",
                     "OH": "Ohio",
                     "OK": "Oklahoma",
                     "OR": "Oregon",
                     "PA": "Pennsylvania",
                     "PR": "Puerto Rico",
                     "RI": "Rhode Island",
                     "SC": "South Carolina",
                     "SD": "South Dakota",
                     "TN": "Tennessee",
                     "TX": "Texas",
                     "UT": "Utah",
                     "VT": "Vermont",
                     "VA": "Virginia",
                     "WA": "Washington",
                     "WV": "West Virginia",
                     "WI": "Wisconsin",
                     "WY": "Wyoming"}
    
    return state_abbrevs

def calculate_surrounding_coords(sample, num_miles):
    """The project asks to address the question "How many [statistic] COVID-19 occurred
    within [num_miles] from [US County]?"

    My approach was to calculate the surrounding coordinates from the base coordinate within
    the user specified num_miles radius and zoom in on that area in Plotly.

    Args:
    =====
        sample (pd.DataFrame): The pandas DataFrame filtered by user-specified county
        num_miles (int)  : The number of miles between 0 and 1000

    Returns:
    =======
        lat (list): A list that contains the latitude values from NSEW
        lon (list): A list that contains the longitude values from NSEW
    """
    miles_to_km = kilometers(miles = num_miles)

    start = Point(sample["latitude"].values[0], sample["longitude"].values[0])

    d = geopy.distance.geodesic()

    dest_north = d.destination(start, distance = miles_to_km, bearing = 0)
    dest_east = d.destination(start, distance = miles_to_km, bearing = 90)
    dest_south = d.destination(start, distance = miles_to_km, bearing = 180)
    dest_west = d.destination(start, distance = miles_to_km, bearing = 270)
    
    lat = [dest_north.latitude, dest_east.latitude, sample["latitude"].values[0], 
           dest_south.latitude, dest_west.latitude]
    
    lon = [dest_north.longitude, dest_east.longitude, sample["longitude"].values[0],
           dest_south.longitude, dest_west.longitude]
    
    return lat, lon

def load_args():
    """Utility function to load the command line arguments
    """
    parser = argparse.ArgumentParser()

    parser.add_argument("--county",
                        type = str,
                        default = "Barnstable County, MA",
                        required = True,
                        help = """
                        The county and the state it's in.
                        Please specify as so: 'Barnstable County, MA'
                        """)

    parser.add_argument("--statistic", 
                        type = str, 
                        default = "cases",
                        required = True, 
                        help = """
                        The COVID-19 statistic of interest.
                        Options are: 'cases', 'deaths', 'confirmed cases',
                                     'confirmed_cases', 'confirmed_deaths', 
                                     'probable_cases','probable_deaths'
                        """)

    parser.add_argument("--num_miles",
                        type = int,
                        default = 0,
                        required = True,
                        help = "A number between 0 and 1000")

    args = parser.parse_args()

    return args