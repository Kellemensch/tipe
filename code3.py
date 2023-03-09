import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math


###################################### Ouverture du fichier et paramètres du problème
data = pd.read_csv("C:/Users/Baptiste/Documents/Prepa/1.MPI/TIPE/Donnéees_synopopendata_2018-2020/donnees-synop-essentielles-omm.csv", sep=';',encoding='latin-1',on_bad_lines='skip')

# Choix des colonnes à garder et suppression des colonnes vides
colonnes = ['Date','Nom','Température','Precipitations_dans_les_24_dernieres_heures','Latitude','Longitude', 'Température (°C)']
data = data[colonnes]
data = data.dropna(axis=1, how='all') #efface les colonnes dans lesquelles il n'y a aucune valeur
data = data.dropna(subset=colonnes) #efface les lignes pour lesquelles il manque une valeur
# On garde seulement la france metropolitaine
data = data[(data['Latitude'] > 30) & (data['Latitude'] < 60) & (data['Longitude'] > -15) & (data['Longitude'] < 15)]

# Reformatage date
data['Date'] = data['Date'].str[:10]
data['Date'] = pd.to_datetime(data['Date'])

# Limites geographiques pour exclure les iles qui faussent les résultats
latitude_min = 30
longitude_min = -15

coords = np.array(data[['Latitude', 'Longitude']].drop_duplicates()) # Prend les coordonnées de manière unique


def pluie_annuelle(dataset):
	# Stats de pluie annuelle
	grouped = dataset.groupby(['Latitude', 'Longitude'])['Precipitations_dans_les_24_dernieres_heures'].sum()
	pluie_annuelle = grouped.to_dict()
	min_pluie = sorted(pluie_annuelle.items(), key=lambda x: x[1])
	#print(min_pluie)
	return min_pluie


def frequence_pluie(dataset):
	# Initialisation de deux colonnes
	dataset['Jour_pluie'] = 0
	dataset['Jours_totaux'] = 0

	for index, row in dataset.iterrows():
	    if row['Precipitations_dans_les_24_dernieres_heures'] > 1:
	        dataset.at[index, 'Jour_pluie'] = 1
	    dataset.at[index, 'Jours_totaux'] = 1

	coord = dataset.groupby(['Latitude', 'Longitude'])

	# Formule = nombre jours de pluie / nombre jours totaux
	frequence_pluie = coord.apply(lambda x: x['Jour_pluie'].sum()/(x['Jours_totaux'].sum()))
	frequence_pluie = frequence_pluie.to_dict() #dictionnaire des fréquences
	frequ_filtree = {k: v for k, v in frequence_pluie.items() if k[0] >= latitude_min and k[1] >= longitude_min}
	min_freq = sorted(frequ_filtree.items(), key=lambda x: x[1])

	return min_freq


def temperature_moyenne(dataset):
	coord = dataset.groupby(['Latitude', 'Longitude'])
	temp_moyenne = coord['Température (°C)'].mean()
	temp_dict = temp_moyenne.to_dict()
	temp_filtree = {k: v for k, v in temp_dict.items() if k[0] >= latitude_min and k[1] >= longitude_min}
	temp_trie = sorted(temp_filtree.items(), key=lambda x: x[1], reverse=True) # Trie les valeurs en ordre decroissant

	return temp_trie


def location(coord, dataframe):
	# Transforme un couple de coordonnées en le nom de l'endroit
	lat = coord[0]
	lon = coord[1]
	location = dataframe.loc[(dataframe['Latitude'].eq(lat)) & (dataframe['Longitude'].eq(lon)), 'Nom'].values[0]
	return location

def temperature_mois_annee(dataset, mois, annee):
	# data = dataset.loc[dataset["Date"].apply(lambda x: pd.to_datetime(x).year == annee and pd.to_datetime(x).month == mois)]
	data = dataset.loc[dataset["Date"].str.slice(0, 7) == f"{annee}-{mois:02}"]
	temp_trie = temperature_moyenne(data)
	return temp_trie



def main():
	##################################### Création des statistiques
	# Stats de pluie annuelle
	min_pluie = pluie_annuelle(data)
	# Premiere place : GOURDON

	# Stats de fréquence des pluies
	min_freq = frequence_pluie(data)
	# Premiere place : PERPIGNAN

	# Stat de température
	temp_trie = temperature_moyenne(data)
	# Premiere place : Nice



	################################# Affichage des résultats
	print("Coordonnées pour lesquelles il pleut le moins en moyenne : ", location(min_pluie[0][0], data)," avec une fréquence de :",min_pluie[0][1])
	print("Coordonnées pour lesquelles il pleut le moins souvent : ", location(min_freq[0][0], data)," avec une fréquence de :",min_freq[0][1])
	print("Coordonnées pour lesquelles il fait le plus chaud : ", location(temp_trie[0][0], data)," avec une température moyenne de : ",temp_trie[0][1])

# main()