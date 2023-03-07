import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math


###################################### Ouverture du fichier et paramètres du problème
data = pd.read_csv("C:/Users/Baptiste/Documents/Prepa/1.MPI/TIPE/Donnéees_synopopendata_2018-2020/donnees-synop-essentielles-omm.csv", sep=';',encoding='latin-1',on_bad_lines='skip')

#choix des colonnes à garder et suppression des colonnes vides
colonnes = ['Date','Nom','Température','Precipitations_dans_les_24_dernieres_heures','Latitude','Longitude']
data = data[colonnes]
data = data.dropna(axis=1, how='all') #efface les colonnes dans lesquelles il n'y a aucune valeur
data = data.dropna(subset=colonnes) #efface les lignes pour lesquelles il manque une valeur
#on garde seulement la france metropolitaine
data = data[(data['Latitude'] > 30) & (data['Latitude'] < 60) & (data['Longitude'] > -15) & (data['Longitude'] < 15)]

#reformatage date
data['Date'] = data['Date'].str[:10]
data['Date'] = pd.to_datetime(data['Date'])

#limites geographiques pour exclure les iles qui faussent les résultats
latitude_min = 30
longitude_min = -15

coords = np.array(data[['Latitude', 'Longitude']].drop_duplicates()) #prend les coordonnées de manière unique


def pluie_annuelle(dataset):
	#stats de pluie annuelle
	grouped = dataset.groupby(['Latitude', 'Longitude'])['Precipitations_dans_les_24_dernieres_heures'].sum()
	pluie_annuelle = grouped.to_dict()
	min_pluie = sorted(pluie_annuelle.items(), key=lambda x: x[1])
	#print(min_pluie)
	return min_pluie

def main():
	##################################### Création des statistiques
	#stats de pluie annuelle
	min_pluie = pluie_annuelle(data)

	#stats de fréquence des pluies
	#initialisation de deux colonnes
	data['Jour_pluie'] = 0
	data['Jours_totaux'] = 0

	for index, row in data.iterrows():
	    if row['Precipitations_dans_les_24_dernieres_heures'] > 1:
	        data.at[index, 'Jour_pluie'] = 1
	    data.at[index, 'Jours_totaux'] = 1

	coord = data.groupby(['Latitude', 'Longitude'])

	#formule = nombre jours de pluie / nombre jours totaux
	frequence_pluie = coord.apply(lambda x: x['Jour_pluie'].sum()/(x['Jours_totaux'].sum()))
	frequence_pluie = frequence_pluie.to_dict() #dictionnaire des fréquences
	frequ_filtree = {k: v for k, v in frequence_pluie.items() if k[0] >= latitude_min and k[1] >= longitude_min}
	min_freq = sorted(frequ_filtree.items(), key=lambda x: x[1])


	#stat de température
	#coord = data.groupby(['Latitude', 'Longitude'])
	temp_moyenne = coord['Température'].mean()
	temp_dict = temp_moyenne.to_dict()
	temp_filtree = {k: v for k, v in temp_dict.items() if k[0] >= latitude_min and k[1] >= longitude_min}
	temp_trie = sorted(temp_filtree.items(), key=lambda x: x[1], reverse=True) #trie les valeurs en ordre decroissant
	#premiere place : Nice



	#################################Affichage des résultats
	def location(coord, dataframe):
		#transforme un couple de coordonnées en le nom de l'endroit
		lat = coord[0]
		lon = coord[1]
		location = dataframe.loc[(dataframe['Latitude'].eq(lat)) & (dataframe['Longitude'].eq(lon)), 'Nom'].values[0]
		return location

	print("Coordonnées pour lesquelles il pleut le moins en moyenne : ", location(min_pluie[0][0], data)," avec une fréquence de :",min_pluie[0][1])
	print("Coordonnées pour lesquelles il pleut le moins souvent : ", location(min_freq[0][0], data)," avec une fréquence de :",min_freq[0][1])
	print("Coordonnées pour lesquelles il fait le plus chaud : ", location(temp_trie[0][0], data)," avec une température moyenne de : ",temp_trie[0][1]-273.15)

#main()




###########################################################Résultats, courbes
# #basemap
# fig = plt.figure(figsize=(8, 8))
# m = Basemap(projection='lcc', resolution=None,
#             width=8E6, height=8E6, 
#             lat_0=45, lon_0=-100,)
# m.etopo(scale=0.5, alpha=0.5)

# # Map (long, lat) to (x, y) for plotting
# x, y = m(-122.3, 47.6)
# plt.plot(x, y, 'ok', markersize=5)
# plt.text(x, y, ' Seattle', fontsize=12)

#folium
# import folium
# from IPython.display import display
# #la carte du monde
# world_map=folium.Map()
# display(world_map)

#geopandas
#countries = gpd.read_file(gpd.datasets.get_path("naturalearth_lowres"))
#countries.head()

