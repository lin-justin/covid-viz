# COVID-19 Visualization

This is my approach and solution to the [Singular Genomics](https://singulargenomics.com/) Software Project for the Software Engineer position.

## Description

The intention is to build a visualization tool for COVID-19 data across different counties in the United States. The program should be capable of answering the questions like: "How many confirmed cases of COVID-19 have occurred within 100 miles of Holtsville County, NY?"

The two datasets used are:

- [live COVID-19 cases by US County](https://github.com/nytimes/covid-19-data/blob/master/live/us-counties.csv)
- [US Counties with geo coordinates](https://data.healthcare.gov/dataset/Geocodes-USA-with-Counties/52wv-g36k)

## Approach

Given the two datasets, the main data of interest was the NY Times live COVID-19 cases by US County dataset, however, because the project requires the program to deal with a specified radius of a county, the geo coordinates of such counties are required which the Geocodes dataset provides. 

From my data exploration:

1. There are counties in the NY Times dataset that exist in the Geocodes dataset, but in the Geocodes dataset, the same counties are repeated multiple times with slightly different latitude and longitude coordinates. 

2. Both datasets contain `county` and `state` columns so using a `merge` function is possible. 

To fix the duplicate counties and states in the Geocodes dataset, I combined the rows of the `county` and `state` columns using a `groupby` [function](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.groupby.html) and took the average of their respective latitude and longitude values to create unique rows that contain only one county and its respective state to match with the NY Times dataset.

From there, I used a `merge` [function](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.merge.html) to join the two datasets on their `county` and `state` columns. In other words, I created a dataset that contains all the COVID-19 related data from the NY Times dataset with the addition of the counties latitude and longitude values from the Geocodes dataset.

Finally, with a dataset with all the relevant information, I used [Plotly](https://plotly.com/python/county-choropleth/) to visualize COVID-19 data across different counties.

There were special cases where counties have the same name but are located in different states, for example: 

- Suffolk County, MA
- Suffolk County, NY
- Bristol County, MA
- Bristol County, RI

In addition, if the user specifies a large number for the `num_miles` parameter, for example 500, the visualization will need to display COVID-19 data in other counties in other states, if the merged dataset contains the latitude and longitude values for them. To account for this, it is necessary to calculate the surrounding coordinates (North, South, East, West) from the origin coordinates (i.e. the coordinates of the county specified by the user) based on the number of miles specified by the user. Using the surrounding coordinates, filter the merged datasets to only get the counties with latitude and longitude values that satisfy the range of the surrounding coordinates. 

For example, if the origin coordinates are (42.5 lat, -71.3 long) and `num_miles` is 100, coordinates to the west are (42.5 lat, -73.3 long), east is (42.5 lat, -69.3 long), north is (43.9 lat, -71.3 long), and south is (40.9 lat, -71.3 long). We want to find coordinates of counties that are within these four surrounding coordinates and plot them.

## Installation

Most importantly, please have [Anaconda](https://docs.anaconda.com/anaconda/install/) (or [Miniconda](https://docs.conda.io/en/latest/miniconda.html)) and [Git](https://git-scm.com/downloads) installed.

Once they are installed, follow the steps below:

1. Clone the repository

```
git clone https://github.com/lin-justin/covid-viz.git
cd covid-viz
```

2. Create and activate the Conda environment

```
conda env create -f environment.yml
conda activate covid-viz
```

## Usage

Command line help

```
python plot.py -h

usage: plot.py [-h] --county COUNTY --statistic STATISTIC --num_miles
               NUM_MILES

optional arguments:
  -h, --help            show this help message and exit
  --county COUNTY       The county and the state it's in. Please specify as
                        so: 'Barnstable County, MA'
  --statistic STATISTIC
                        The COVID-19 statistic of interest. Options are:
                        'cases', 'deaths', 'confirmed_cases',
                        'confirmed_cases', 'confirmed_deaths',
                        'probable_cases', 'probable_deaths'
  --num_miles NUM_MILES
                        A number between 0 and 1000
```

Run `plot.py`

```
python plot.py --county="Barnstable County, MA" --statistic="confirmed_cases" --num_miles=0
```

After the script finishes, a new window or tab will open in your web browser showing the resulting visualization.

## Example Output

![picture alt](https://github.com/lin-justin/covid-viz/blob/master/results/bristol_county_ma_10_miles.png)

![picture alt](https://github.com/lin-justin/covid-viz/blob/master/results/middlesex_county_ma_9_miles.png)

![picture alt](https://github.com/lin-justin/covid-viz/blob/master/results/middlesex_county_ma_100_miles.png)
