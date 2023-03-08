import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from shapely.geometry import Point	
from code3 import pluie_annuelle, frequence_pluie, temperature_moyenne
import mplcursors

#ouverture du fichier shapefile
france = gpd.read_file(r'C:/Users/Baptiste/Documents/Prepa/1.MPI/TIPE/regions_2016_osm_100m/regions_2016_osm_100m.shp')

#ouverture des données meteo
data = pd.read_csv("C:/Users/Baptiste/Documents/Prepa/1.MPI/TIPE/Donnéees_synopopendata_2018-2020/donnees-synop-essentielles-omm.csv", sep=';',encoding='latin-1',on_bad_lines='skip')
colonnes = ['Date','Nom','Température','Precipitations_dans_les_24_dernieres_heures','Latitude','Longitude']
data = data[colonnes]
data = data.dropna(axis=1, how='all') #efface les colonnes dans lesquelles il n'y a aucune valeur
data = data.dropna(subset=colonnes) #efface les lignes pour lesquelles il manque une valeur
#on garde seulement la france metropolitaine
data = data[(data['Latitude'] > 30) & (data['Latitude'] < 60) & (data['Longitude'] > -15) & (data['Longitude'] < 15)]
coords = np.array(data[['Latitude', 'Longitude']].drop_duplicates())




def affiche_pluie_an(dataset):
	#récupération des résultats
	pluie_an = pluie_annuelle(dataset)


	pluie_coords = [(Point(lon, lat), pluie) for (lat, lon), pluie in pluie_an]
	geo_df_pluie = gpd.GeoDataFrame(pluie_coords, columns=['geometry', 'pluie'])
	geo_df_pluie = geo_df_pluie.set_crs('EPSG:4326') #mise en forme correcte, la meme que le shapefile

	# Création d'un nouveau GeoDataFrame avec les données et la colonne 'pluie_an'
	# geo_df_pluie = geo_df.copy()
	# geo_df_pluie['pluie_an'] = [pluie for coord,pluie in pluie_an]

	

	# Créer un objet ScalarMappable pour la couleur de la carte
	cmap = 'OrRd' # gradient de couleurs
	vmax, vmin = max(pluie_an, key=lambda x: x[1])[1], min(pluie_an, key=lambda x: x[1])[1] # limites du gradient
	sm = plt.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(vmin=vmin, vmax=vmax))
	sm._A = [] # nécessité de redéfinir une propriété privée pour éviter un avertissement


	# Affichage des points avec un gradient de couleur en fonction de 'pluie_an'
	geo_df_pluie.plot(cmap=cmap, markersize=100, marker='o', ax=ax, column='pluie')

	# Ajouter la légende et les labels
	cbar = plt.colorbar(sm)
	cbar.ax.set_ylabel('Pluie par an (mm)')

	ax.set_title("Pluie annuelle")
	print(pluie_an)
	print(geo_df_pluie['pluie'])



def affiche_fréquences_pluie(dataset):
	min_freq = frequence_pluie(dataset)

	freq_coords = [(Point(lon, lat), freq) for (lat, lon), freq in min_freq]
	geo_df_freq = gpd.GeoDataFrame(freq_coords, columns=['geometry', 'frequence'])
	geo_df_freq = geo_df_freq.set_crs('EPSG:4326') #mise en forme correcte, la meme que le shapefile

	# Créer un objet ScalarMappable pour la couleur de la carte
	cmap = 'OrRd' # gradient de couleurs
	vmax, vmin = max(min_freq, key=lambda x: x[1])[1], min(min_freq, key=lambda x: x[1])[1] # limites du gradient
	sm = plt.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(vmin=vmin, vmax=vmax))
	sm._A = [] # nécessité de redéfinir une propriété privée pour éviter un avertissement


	# Affichage des points avec un gradient de couleur en fonction de 'pluie_an'
	geo_df_freq.plot(cmap=cmap, markersize=100, marker='o', ax=ax, column='frequence')

	# Ajouter la légende et les labels
	cbar = plt.colorbar(sm)
	cbar.ax.set_ylabel('Frequence des pluies')

	ax.set_title("Fréquences des pluies au cours de l'annnée")


def affiche_temperature_moyenne(dataset):
	temp_moy = temperature_moyenne(dataset)

	temp_coords = [(Point(lon, lat), temp) for (lat, lon), temp in temp_moy]
	geo_df_temp = gpd.GeoDataFrame(temp_coords, columns=['geometry', 'température'])
	geo_df_temp = geo_df_temp.set_crs('EPSG:4326') #mise en forme correcte, la meme que le shapefile

	# Créer un objet ScalarMappable pour la couleur de la carte
	cmap = 'OrRd' # gradient de couleurs
	vmax, vmin = max(temp_moy, key=lambda x: x[1])[1], min(temp_moy, key=lambda x: x[1])[1] # limites du gradient
	#vmax, vmin = 300,280
	sm = plt.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(vmin=vmin, vmax=vmax))
	sm._A = [] # nécessité de redéfinir une propriété privée pour éviter un avertissement


	# Affichage des points avec un gradient de couleur en fonction de 'pluie_an'
	geo_df_temp.plot(cmap=cmap, markersize=100, marker='o', ax=ax, column='température')

	# Ajouter la légende et les labels
	cbar = plt.colorbar(sm)
	cbar.ax.set_ylabel("Température moyenne")

	ax.set_title("Températures moyennes au cours des 4 ans")



#création de la carte avec les coordonnees
# points = [Point(lon, lat) for lat, lon in coords]
# geo_df = gpd.GeoDataFrame(geometry=points)
# geo_df = geo_df.set_crs('EPSG:4326') #mise en forme correcte, la meme que le shapefile



fig, ax = plt.subplots(figsize=(10, 10))

# # Plot la carte géopandas de la France
france.plot(ax=ax, alpha=0.4, color='gray')


#appels aux résultats
affiche_pluie_an(data)
# affiche_fréquences_pluie(data)
#affiche_temperature_moyenne(data)

#affiche tout
plt.show()
mplcursors.cursor(hover=True)