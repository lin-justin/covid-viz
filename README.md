# COVID-19 Visualization

This is my approach and solution to the Singular Genomics Software Project (part of interview process).

## Description

The intention is to build a visualization tool for COVID-19 data across different counties in the United States. The program should be capable of answering the questions like: "How many confirmed cases of COVID-19 have occurred within 100 miles of Holtsville County, NY?"

The two datasets used are:

- [live COVID-19 cases by US County](https://github.com/nytimes/covid-19-data/blob/master/live/us-counties.csv)
- [US Counties with geo coordinates](https://data.healthcare.gov/dataset/Geocodes-USA-with-Counties/52wv-g36k)

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
