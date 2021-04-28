"""
Christian Fabbri
CS 230 SN5
Final Project based on NYC Crash data set
"""

import pandas as pd
import matplotlib.pyplot as plt

plt.rc('xtick', labelsize=7)
import streamlit as st
import pydeck as pdk

boroughs = ['BROOKLYN', 'QUEENS', 'MANHATTAN', 'BRONX', 'STATEN ISLAND']


def read_data(file):
    df = pd.read_csv(file)
    lst = []

    columns = ['BOROUGH', 'DATE', 'ON STREET NAME', 'LATITUDE', 'LONGITUDE', 'VEHICLE 1 FACTOR', 'VEHICLE 2 FACTOR',
               'PERSONS INJURED']
    for index, row in df.iterrows():
        sub = []
        for col in columns:
            index_num = df.columns.get_loc(col)
            sub.append(row[index_num])
        lst.append(sub)
    return lst


def street_list(data):
    streets = []

    for i in range(len(data)):
        if data[i][2] not in streets:
            streets.append(data[i][2])

    return streets


def freq_data(data, streets):
    freq_dict = {}

    for street in streets:
        freq = 0
        for i in range(len(data)):
            if data[i][2] == street:
                freq += 1
        freq_dict[street] = freq
    return freq_dict


# print(freq_data(read_data('nyc_veh_crash_sample.csv'), street_list(read_data('nyc_veh_crash_sample.csv'))))

def freq_borough(data, boroughs):
    freq_bdict = {}

    for borough in boroughs:
        freq = 0
        for i in range(len(data)):
            if data[i][0] == borough:
                freq += 1
        freq_bdict[borough] = freq
    return freq_bdict


def bar_chart(freq_dict):
    plt.figure()
    # create a dictionary that has only the top 10 streets for most accidents and the number of accidents as values
    sorted_dict = {}
    sorted_keys = sorted(freq_dict, key=freq_dict.get, reverse=True)[:10]

    for i in sorted_keys:
        sorted_dict[i] = freq_dict[i]

    color = st.sidebar.color_picker('Choose a color for the bars', '#B72A2D')
    x = sorted_dict.keys()
    y = sorted_dict.values()
    plt.bar(x, y, color=color)
    plt.xlabel('Street')
    plt.ylabel('Number of Accidents')
    plt.xticks(rotation=90)
    plt.title("Top 10 Streets with the Most Accidents")

    return plt


# print(bar_chart(freq_data(read_data('nyc_veh_crash_sample.csv'), street_list(read_data('nyc_veh_crash_sample.csv')))))
def map(data, borough):
    loc = []
    for i in range(len(data)):
        if data[i][0] in borough:
            loc.append([data[i][0], data[i][3], data[i][4]])

    print(loc)
    map_df = pd.DataFrame(loc, columns=['BOROUGH', 'lat', 'lon'])
    map_df = map_df.dropna()

    view_state = pdk.ViewState(latitude=map_df['lat'].mean(), longitude=map_df['lon'].mean(), zoom=10,
                               pitch=0)
    layer = pdk.Layer('ScatterplotLayer', data=map_df, get_position='[lon, lat]', get_radius=100,
                      get_color=[0, 255, 255], pickable=True)
    tool_tip = {'html': 'Borough: <br/>{BOROUGH}', 'style': {'backgroundColor': 'steelblue', 'color': 'white'}}

    map = pdk.Deck(map_style='mapbox://styles/mapbox/light-v9', initial_view_state=view_state, layers=[layer],
                   tooltip=tool_tip)

    st.pydeck_chart(map)


def pie_chart(freq_bdict):
    plt.figure()
    sorted_dict = {}
    sorted_keys = sorted(freq_bdict, key=freq_bdict.get)
    for i in sorted_keys:
        sorted_dict[i] = freq_bdict[i]

    freq = sorted_dict.values()
    label = sorted_dict.keys()
    plt.pie(freq, labels=label, autopct="%1.2f%%")
    return plt


def main():
    data = read_data('nyc_veh_crash_sample.csv')

    st.title("NYC Crash Data Application")
    st.write("Welcome! This site will provide you with stats and charts about car accidents in NYC!")
    streets = street_list(data)
    st.pyplot(bar_chart(freq_data(data, streets)))

    st.write("Map of Accidents by Borough")
    select_boroughs = st.sidebar.multiselect('Select borough(s) to view an accident map for', boroughs)
    if len(select_boroughs) > 0:
        map(data, select_boroughs)

    st.write("Percentage of Accidents by Borough")
    st.pyplot(pie_chart(freq_borough(data, boroughs)))

    st.write("Relevant stats on Each Accident in Selected Borough")

    # My read data function reads everything into a list so I created a new dataframe to show stats
    # on the columns I wanted to include in my table as they are different than the ones in my read data function.
    df = pd.read_csv('nyc_veh_crash_sample.csv')
    df.drop(['UNIQUE KEY', 'LATITUDE', 'LONGITUDE', 'CROSS STREET NAME', 'OFF STREET NAME'],inplace=True, axis=1)
    df.drop(['PEDESTRIANS INJURED', 'PEDESTRIANS KILLED', 'CYCLISTS INJURED', 'CYCLISTS KILLED'],inplace=True, axis=1)
    df.drop(['MOTORISTS INJURED', 'MOTORISTS KILLED', 'VEHICLE 1 TYPE', 'VEHICLE 2 TYPE', 'VEHICLE 3 TYPE'],inplace=True, axis=1)
    df.drop(['VEHICLE 4 TYPE', 'VEHICLE 5 TYPE', 'VEHICLE 3 FACTOR', 'VEHICLE 4 FACTOR', 'VEHICLE 5 FACTOR'],inplace=True, axis=1)
    boroughchoice = st.sidebar.radio('Select borough to view statistics for: ', boroughs)
    borough_choice = df[df['BOROUGH'] == boroughchoice]
    st.write(borough_choice)


main()
