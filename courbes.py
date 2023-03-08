import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pandas.api.types import CategoricalDtype
from code3 import location

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





#############################################
# Sélectionner une ville
coord = (44.830667,-0.691333) #Bordeaux
ville = location(coord, data)

data_coord = data.loc[(data['Latitude'] == coord[0]) & (data['Longitude'] == coord[1])]

# # Créer une colonne de mois
# data_coord['Mois'] = pd.Categorical(data_coord['Mois'], month_cat)
data_coord['Date'] = pd.to_datetime(data_coord['Date'])
data_coord['Mois'] = data_coord['Date'].dt.month_name()


# Convertir les températures de Kelvin en Celsius
data_coord['Température'] = data_coord['Température'] - 273.15

# Calculer la moyenne de la température pour chaque mois
temp_moy_mois = data_coord.groupby('Mois')['Température'].mean()

# Créer une liste des mois dans l'ordre chronologique
mois = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

# Trier la moyenne des températures dans l'ordre des mois
temp_moy_mois = temp_moy_mois.reindex(mois)

# Tracer la courbe de la température en fonction des mois
plt.plot(temp_moy_mois.index, temp_moy_mois.values)
plt.xticks(rotation=45)
plt.xlabel('Mois')
plt.ylabel('Température moyenne (°C)')
plt.title(f'Température moyenne pour la coordonnée {ville}')
plt.show()