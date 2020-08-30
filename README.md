# COVID-19 Visualization

This is my approach and solution to the [Singular Genomics](https://singulargenomics.com/) Software Project for the Software Engineer position.

## Description

The intention is to build a visualization tool for COVID-19 data across different counties in the United States. The program should be capable of answering the questions like: "How many confirmed cases of COVID-19 have occurred within 100 miles of Holtsville County, NY?"

The two datasets used are:

- [live COVID-19 cases by US County](https://github.com/nytimes/covid-19-data/blob/master/live/us-counties.csv)
- [US Counties with geo coordinates](https://data.healthcare.gov/dataset/Geocodes-USA-with-Counties/52wv-g36k)

## Approach

Given the two datasets, the main data of interest was the NY Times live COVID-19 cases by US County dataset, however, because the project requires the program to deal with a specified radius of a county, the geo coordinates of such counties are required which the Geocodes dataset provides. 

Through some data exploration:

1. There are counties in the NY Times dataset that exist in the Geocodes dataset but in the Geocodes dataset, the same counties are repeated multiple times with slightly different latitude and longitude coordinates. 

2. Both datasets contained `county` and `state` columns so using `merge` is possible. 

To fix the duplicate counties and states in the Geocodes dataset, I combined the rows of the `county` and `state` columns using a `groupby` [function](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.groupby.html) and took the average of their respective latitude and longitude values to create a unique row containing one county and its respective state.

From there, I used a `merge` [function](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.merge.html) to join the two datasets on the `county` and `state` columns. In other words, I created a dataset that contains the counties and states from the NY Times dataset with their respective latitude and longitude values from the Geocodes dataset.

Finally, with a dataset with all the relevant information, I used [Plotly](https://plotly.com/python/county-choropleth/) to visualize COVID-19 data across different counties.

In addition, there are counties with the same name but in different states, for example: 

- Suffolk County, MA
- Suffolk County, NY
- Bristol County, MA
- Bristol County, RI

To deal with this, I implemented a `if-else` conditional to specially plot these counties since there are only 4 of these special cases.

## Installation

Clone the repository

```
git clone https://github.com/lin-justin/covid-viz.git
cd covid-viz
```

Create Conda environment

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
                        'cases', 'deaths', 'confirmed cases',
                        'confirmed_cases', 'confirmed_deaths',
                        'probable_cases','probable_deaths'
  --num_miles NUM_MILES
                        A number between 0 and 1000
```

Run `plot.py`

```
python plot.py --county="Barnstable County, MA" --statistic="confirmed_cases" --num_miles=0
```

After the script has ran, a new window will open in your web browser showing the resulting visualization.
