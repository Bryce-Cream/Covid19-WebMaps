import folium
import pandas
import requests
#Creating the base map to start at the University Windsor
map = folium.Map(location=[42.30, -83.06], zoom_start=6, tiles="Stamen Terrain")

#I am using API from thevirustracker.com
res = requests.get('https://api.thevirustracker.com/free-api?countryTotals=ALL')
#Convert to a json file
covid_current=res.json()

#I am planning on doing 3 separate map layers
#We are changing our data to total_new_cases_today, total_new_deaths_today, total_active_cases
#Creating the C19 DataFrame with pandas
df=[]
for x in range(1, len(covid_current['countryitems'][0])):
    df.append([covid_current['countryitems'][0]['{}'.format(x)]['title'],
    covid_current['countryitems'][0]['{}'.format(x)]['total_new_cases_today'],
    covid_current['countryitems'][0]['{}'.format(x)]['total_new_deaths_today'],
    covid_current['countryitems'][0]['{}'.format(x)]['total_active_cases']])

df_covid = pandas.DataFrame(df, columns = ['Country', 'New Cases Today','New Deaths Today', 'Total Active Cases'])

#Replacing the country names to from the dataset to match Foliums provided
df_covid.replace('USA', "United States of America", inplace = True)
df_covid.replace('Tanzania', "United Republic of Tanzania", inplace = True)
df_covid.replace('Democratic Republic of Congo', "Democratic Republic of the Congo", inplace = True)
df_covid.replace('Congo', "Republic of the Congo", inplace = True)
df_covid.replace('Lao', "Laos", inplace = True)
df_covid.replace('Syrian Arab Republic', "Syria", inplace = True)
df_covid.replace('Serbia', "Republic of Serbia", inplace = True)
df_covid.replace('Czechia', "Czech Republic", inplace = True)
df_covid.replace('UAE', "United Arab Emirates", inplace = True)










"""
#Adding the Choropleth layer onto our base map
folium.Choropleth(
    #The GeoJSON data to represent the world country
    geo_data=country_shapes,
    name='choropleth COVID-19',
    data=df_covid,
    #The column aceppting list with 2 value; The country name and  the numerical value
    columns=['Country', 'Total Case'],
    key_on='feature.properties.name',
    fill_color='PuRd',
    nan_fill_color='white'
).add_to(m)




for lat, lon, name in   zip(country['latitude'],country['longitude'],country['name']):
    #Creating the marker
    folium.Marker(
    #Coordinate of the country
    location=[lat, lon],
    #The popup that show up if click the marker
    popup=name
    ).add_to(m)
m
"""

data = pandas.read_csv("volcanoes.txt")
lat = list(data["LAT"])
lon = list(data["LON"])
elev = list(data["ELEV"])

def color_producer(elevation):
    if elevation < 1000:
        return 'green'
    elif 1000<= elevation < 3000:
        return 'orange'
    else:
        return 'red'


fgv = folium.FeatureGroup(name="Volcanoes")

#Used for iterating through two list simultaneously
for lt, ln, el in zip(lat, lon, elev):
    fgv.add_child(folium.CircleMarker(location=[lt, ln], radius= 6, popup=str(el)+" m",
    fill_color=color_producer(el), color='grey', fill_opacity=0.7))#May need to put fill = True if error

fgp = folium.FeatureGroup(name="Population")

fgp.add_child(folium.GeoJson(data=open('world.json', 'r', encoding='utf-8-sig').read(),
style_function=lambda x: {'fillColor': 'green' if x['properties']['POP2005'] < 10000000
else 'orange' if 10000000 <= x['properties']['POP2005'] < 20000000 else 'red'}))

map.add_child(fgv)
map.add_child(fgp)
map.add_child(folium.LayerControl())

map.save("Map1.html")
