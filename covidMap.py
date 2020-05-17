import folium
import pandas
import requests
#Creating the base map to start at the University Windsor
new_cases_map = folium.Map(location=[42.30, -83.06], zoom_start=6, tiles="Stamen Terrain")
new_deaths_map = folium.Map(location=[42.30, -83.06], zoom_start=6, tiles="Stamen Terrain")
active_cases_map = folium.Map(location=[42.30, -83.06], zoom_start=6, tiles="Stamen Terrain")

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

#Getting the maxes for each of the categories
maxNCT = df_covid['New Cases Today'].max() + 1
maxNDT = df_covid['New Deaths Today'].max() + 1
maxTAC = df_covid['Total Active Cases'].max() + 1

#Data for the polygons of countries
url = 'https://raw.githubusercontent.com/python-visualization/folium/master/examples/data'
country_shapes = f'{url}/world-countries.json'

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

folium.Choropleth(
    geo_data=country_shapes,
    name='New Cases Today',
    data=df_covid,
    columns=['Country', 'New Cases Today'],
    key_on='feature.properties.name',
    bins=[0, maxNCT*.2, maxNCT*.4, maxNCT*.6, maxNCT*.8, maxNCT],
    nan_fill_color='white',
    fillColor='YlOrRd',
    highlight=True
).add_to(new_cases_map)

folium.Choropleth(
    geo_data=country_shapes,
    name='New Deaths Today',
    data=df_covid,
    columns=['Country', 'New Deaths Today'],
    key_on='feature.properties.name',
    fillColor='YlOrRd',
    bins=[0, maxNDT*.2, maxNDT*.4, maxNDT*.6, maxNDT*.8, maxNDT],
    nan_fill_color='white',
    highlight=True
).add_to(new_deaths_map)

folium.Choropleth(
    geo_data=country_shapes,
    name='Active Cases',
    data=df_covid,
    columns=['Country', 'Total Active Cases'],
    key_on='feature.properties.name',
    fillColor='YlOrRd',
    bins=[0, maxTAC*.2, maxTAC*0.4, maxTAC*.6, maxTAC*0.8, maxTAC],
    nan_fill_color='white',
    highlight=True
).add_to(active_cases_map)

folium.LayerControl().add_to(new_cases_map)
folium.LayerControl().add_to(new_deaths_map)
folium.LayerControl().add_to(active_cases_map)

new_cases_map.save("NewCasesMap.html")
new_deaths_map.save("NewDeathsMap.html")
active_cases_map.save("ActiveCasesMap.html")
