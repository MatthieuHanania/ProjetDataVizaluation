# The Deck has been inspired from https://github.com/streamlit/demo-uber-nyc-pickups/blob/master/streamlit_app.py
# by carolinedlu From Streamlit


import streamlit as st
import pydeck as pdk
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from PIL import Image


st.set_page_config(layout="wide")


# We start this function only one time
@st.cache
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    return data


# Line spacing in the sidebar and the page
def blankSidebar(quantity):
    for i in range(quantity):
        st.sidebar.write("")


def blank(quantity):
    for i in range(quantity):
        st.write("")

def count_rows(rows):
    return len(rows)


# ------ CREATING FUNCTION FOR MAPS

def map(data, latitude, longitude, zoom):
    st.write(pdk.Deck(
        map_style="mapbox://styles/mapbox/light-v9",
        initial_view_state={
            "latitude": latitude,
            "longitude": longitude,
            "zoom": zoom,
            "pitch": 50,
        },
        layers=[
            pdk.Layer(
                "HexagonLayer",
                data=data,
                get_position=["longitude", "latitude"],
                radius=100,
                elevation_scale=4,
                elevation_range=[0, 1000],
                pickable=True,  # display a tooltip
                extruded=True,  # 3D representation
            ),
        ]
    ))


# Parameters
DATE_TIME = "ts"
WEEKDAY = "weekday"
MONTH = "month"
YEAR = "year"
HOUR = "heure"
DATA_URL = (
    "all_clean_data.csv"
)

# Loading data
data = load_data(345000)

st.balloons()

st.title("My Google Map Analyze")
st.subheader("by Matthieu Hanania 4/10/2021")
st.write("**GitHub** : https://github."
         "m/MatthieuHanania")
st.write("**Linkedin** : https://www.linkedin.com/in/matthieu-hanania-6835ba177/")

st.write("In this website, I visualize my google map data.")
blank(4)



# -------------THE SIDEBAR
days = ['Monday', 'Tuesay', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November',
          'December']
years = [2016, 2018, 2019, 2020, 2021]

st.sidebar.header("Options")
blankSidebar(2)


day_ = st.sidebar.selectbox('select a day of the week', days)
day_index = days.index(day_)

month_ = st.sidebar.selectbox('select a month', months)
month_index = months.index(month_)

year_ = st.sidebar.selectbox("select a year", years, index=4)
year_index = years.index(year_)



# --------------THE PAGE


st.header("**Firsly, let's see a global map of my data...**")
st.write("We see 4 zones : Paris, Lebanon, Brittany and Italy")
st.write('This kind of map is not very precise')

map_data = pd.DataFrame(data[['latitude', 'longitude']])
map_data.columns = ['latitude', 'longitude']
st.map(map_data)

blank(2)

# ----- MAP

# CENTER OF MAPS
midpoint = (48.7911052, 2.2870373)
Libanon = (33.87781991113338, 35.59921650712615)
bretagne = (48.11315033595835, -1.6382935089393325)
Borgomanero = (45.6989107, 8.4623673)

st.header("**...Then, we focus on theses points:**")

st.subheader("** First : Ile de France**")


# FILTERING DATA BY DAY SELECTED
dataFrance = data[(data['longitude'] >= 1) & (data['longitude'] <= 4)]
dataFilter = dataFrance[dataFrance[WEEKDAY] == day_index]

# France
st.write("**All", day_, " Ile de France**")
st.write(
    "We can see where I go at EFREI during the week and saturday because of DE, and even the day I go in vacation (airport)")
st.write(
    "We can see different ways to go at scool, **metro** (inside paris), **car** (direct path) and **bus**( l'hay les roses)")
map(dataFilter, midpoint[0], midpoint[1], 11)



#-----VACATION
blank(2)
st.subheader("**Vacation times !**")
colLiban, colBrit = st.columns((1, 1))

#nothing is use to make the map size equals to the half of the total size
colIta, noting = st.columns((1, 1))

with colLiban:
    # Focus data on libannon
    dataLiban = data[data['longitude'] >= 30]
    st.write("**Where did I go in Libannon**")
    st.write("Vacation Times ! (but without 4g or data)")
    map(dataLiban, Libanon[0], Libanon[1], 11)

with colBrit:
    # Focus data on brittany
    dataBrit = data[data['longitude'] <= 0]
    st.write("**Where did I go in Brittany**")
    st.write("It has been a long time since I went there")
    map(dataBrit, bretagne[0], bretagne[1], 11)


with colIta:
    # Focus data on Italia
    dataIta = data[(data['longitude'] >= 6) & (data['longitude'] <= 9)]
    st.write("**Where did I go in Italie**")
    st.write("Google map is useless when points are not collected...")
    map(dataIta, Borgomanero[0], Borgomanero[1], 12)



# PLOT OF MONTH


blank(2)
st.header('**How many points for each month ? (two ways):**')

heatMonth, MonthPlot = st.columns((1, 1))

# HeatMap of data by mounth and year
with heatMonth:
    dfH = data.groupby(['month', 'year']).apply(count_rows).unstack()

    st.subheader("**HeatMap :**")
    st.write("This represent the number of point counted by year and month")
    st.write("Points are created when I turn on my localisation, so .... We can see correlation with pokemon Go")
    fig, ax = plt.subplots()
    sns.heatmap(dfH, annot=True, linewidths=.5)
    st.write(fig)

# Histogram of how many points are counted by month of a given year
with MonthPlot:
    st.subheader("**Histogram :**")

    dataFilter_onlyMonth = data[(data[YEAR] == year_)]

    hist_values_month = np.histogram(
        dataFilter_onlyMonth[MONTH], bins=12, range=(1, 12))[0]

    st.bar_chart(hist_values_month)
    st.write("**This represent the number of points grouped by mouth on", year_, "**")

# Picture of pokemon GO
pogo1, pogo2, pogo3, nothing = st.columns((1, 1, 1, 1))
with pogo1:
    image = Image.open('POGO9-16.png')
    st.image(image, caption='A pokemon captured on 09/2016')

with pogo2:
    image = Image.open('POGO10-16.png')
    st.image(image, caption='My last pokemon on 2016')

with pogo3:
    image = Image.open('POGO9-19.png')
    st.image(image, caption='Since this time, my localisation is almost always on. #LeMeilleurDresseur ;)')

# CORRELATION ?
blank(2)
st.header('**Can we see a correlation between variables ? :**')
st.write("We see correlation between variables, we can see that variables are absolutely not correlated")

heatTotal, rien = st.columns((1, 1))

with heatTotal:
    fig, ax = plt.subplots()
    sns.heatmap(data.corr(), ax=ax)
    st.write(fig)

# POINTS GROUPED BY HOUR
blank(2)
st.header('**How many points by hour and day? :**')

# group by hour
st.write("Quantity of point by **hour **on** ", months[month_index], "/", year_index, "**")
st.subheader("**Week VS Weekend**")

week, weekend = st.columns((1, 1))

with week:

    dataFilter_hour_week = data[
        (data[MONTH] == month_index + 1) & (data[YEAR] == year_) & (data[WEEKDAY] < 5)]

    hist_values_hour_week = np.histogram(
        dataFilter_hour_week[HOUR], bins=24, range=(0, 23))[0]

    st.write("WEEK")
    st.area_chart(hist_values_hour_week)


with weekend:
    dataFilter_hour_WE = data[(data[MONTH] == month_index + 1) & (data[YEAR] == year_) & (data[WEEKDAY] >= 5)]

    hist_values_hour_WE = np.histogram(
        dataFilter_hour_WE[HOUR], bins=24, range=(0, 23))[0]

    st.write("WEEKEND")
    st.area_chart(hist_values_hour_WE)

st.write("We can see that there are more point on week (because there are more days during a week). And during the week, points are counted earlier.")


st.subheader("**This represent how many points a counted by hour on a given mouth and year**")
day, picture = st.columns((2, 1))

with day:
    # group by day
    dataFilter_hour = data[(data[MONTH] == month_index + 1) & (data[YEAR] == year_)]
    st.write("Quantity of point by **day **on**", months[month_index], "/", year_, "**")

    hist_values_hour = np.histogram(
        dataFilter_hour[WEEKDAY], bins=7, range=(0, 6))[0]

    st.bar_chart(hist_values_hour)
    st.write("**This represent how many points a counted by weekday on a given mouth and year**")

with picture:
    # picture
    if month_index + 1 == 1 and year_ == 2021:
        image = Image.open('DE janvier 2021.png')
        st.image(image, caption='With saturday comes DE and check every miutes if I am not late')

    elif month_index + 1 == 1 and year_ == 2020:
        image = Image.open('stage.jpg')
        st.image(image, caption='Internship time !')
    else:
        image = Image.open('no-image.png')
        st.image(image, caption='Sorry, no picture for this time :)')


# --- The day with the most of point
blank(2)
st.header('**What is the day I turn on the most my localisation ? :**')

#nothing is use to make the heatmap size equals to the half of the total size
HeatYear, nothing = st.columns((1, 1))

with HeatYear:
    # Correlation of points by weekday and month
    dataFilter_year = data[(data[YEAR] == year_)]

    st.write("This represent how many points are counted every day on every month of", year_)
    st.write("More points during weekend")
    dfH = dataFilter_year.groupby([WEEKDAY, MONTH]).apply(count_rows).unstack()
    fig, ax = plt.subplots()
    sns.heatmap(dfH, linewidths=.5, yticklabels=days)
    st.write(fig)
