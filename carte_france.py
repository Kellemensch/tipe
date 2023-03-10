import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from shapely.geometry import Point

france = gpd.read_file(r'C:/Users/Baptiste/Documents/Prepa/1.MPI/TIPE/regions_2015_metropole_region/regions_2015_metropole_region.shp')


data = pd.read_csv("C:/Users/Baptiste/Documents/Prepa/1.MPI/TIPE/Donnéees_synopopendata_2018-2020/donnees-synop-essentielles-omm.csv", sep=';',encoding='latin-1',on_bad_lines='skip')
colonnes = ['Date','Nom','Température','Precipitations_dans_les_24_dernieres_heures','Latitude','Longitude']
data = data[colonnes]
data = data.dropna(axis=1, how='all') #efface les colonnes dans lesquelles il n'y a aucune valeur
data = data.dropna(subset=colonnes) #efface les lignes pour lesquelles il manque une valeur
#on garde seulement la france metropolitaine
data = data[(data['Latitude'] > 30) & (data['Latitude'] < 60) & (data['Longitude'] > -15) & (data['Longitude'] < 15)]
coords = np.array(data[['Latitude', 'Longitude']].drop_duplicates())

# gpd.GeoDataFrame(data, geometry=gpd.points_from_xy(data.Longitude, data.Latitude))
# points = [Point(lon, lat) for [lat, lon] in coords]
# geo_df = gpd.GeoDataFrame(geometry=points)
# fig, ax = plt.subplots(figsize=(10, 10))

# # Plot la carte géopandas de la France
# france.plot(ax=ax, alpha=0.4, color='grey')

# # Plot les points de coordonnées sur la carte
# geo_df.plot(ax=ax, markersize=10, color='red', marker='o')

# plt.show()


#france = france.merge(coords)

#france.plot(column='Température', cmap='coolwarm', legend=True)
france.plot()
plt.show()
