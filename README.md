# Weather Data Analysis

The goal of this project is to build a tool for spotting and examining weather patterns that trigger events such as basement flooding, sump pump activity, roof leaks, etc..

How to obtain past daily weather logs from the NOAA and format similar to their CDO (climate data online) service:

[NOAA Data Retrieval.ipynb](https://github.com/undineleopold/DataAnalysis/blob/main/NOAA%20Data%20Retrieval.ipynb)

Example: Analyzing combinations of Rain and Wind in Watertown, MA, thresholding with sliders:

![example image with sliders](/MarkdownFiles/output_38_0.png "example image with sliders")

A detailed breakdown of this example can be found in:

[Rain and Wind analysis.ipynb](https://github.com/undineleopold/DataAnalysis/blob/main/Rain%20and%20Wind%20analysis.ipynb)

Markdown versions of the notebooks:

[NOAA Data Retrieval.md](https://github.com/undineleopold/DataAnalysis/blob/main/MarkdownFiles/NOAA%20Data%20Retrieval.md)

[Rain and Wind analysis.md](https://github.com/undineleopold/DataAnalysis/blob/main/MarkdownFiles/Rain%20and%20Wind%20analysis.md)

Some helpful functions are corralled in [weatherdata.py](https://github.com/undineleopold/DataAnalysis/blob/main/weatherdata.py). The code in [demo.py](https://github.com/undineleopold/DataAnalysis/blob/main/demo.py) makes use of these functions for selection and quick retrieval of data for a city (US/Canada only), generating the interactive plot of rain and wind data from the 2020s. 

Demo:

https://github.com/undineleopold/DataAnalysis/assets/79616083/ba19d501-a0b1-4b19-b491-c809cf979c06

