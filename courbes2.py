import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
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
def courbe_temperature(data,coord):
    ville = location(coord, data)

    data_coord = data.loc[(data['Latitude'] == coord[0]) & (data['Longitude'] == coord[1])]
    data_coord["Date"] = pd.to_datetime(data_coord["Date"])

    # Convertir les températures de Kelvin en Celsius
    data_coord['Température'] = data_coord['Température'] - 273.15


    # Regrouper les données par mois et année et calculer la moyenne des températures
    grouped = data_coord.groupby([data_coord["Date"].dt.year, data_coord["Date"].dt.month])["Température"].mean()

    # Créer une liste de dates à partir des index du groupby
    dates = [pd.Timestamp(year=year, month=month, day=1) for year, month in grouped.index]


    # Tracer la courbe chronologique des températures
    fig, ax = plt.subplots()
    ax.plot(dates, grouped, 'o')
    ax.set_xlabel("Date")
    ax.set_ylabel("Température")
    plt.title(f'Température moyenne pour la coordonnée {ville}')
    plt.show()


def regression_sinus():
    # Créer des données de température simulées
    x = np.linspace(0, 11, 12)
    y = np.array([12, 14, 17, 21, 24, 27, 29, 29, 27, 24, 19, 14])

    # Définir la fonction sinusoidale à ajuster
    def sinusoid(x, A, B, C, D):
        return A * np.sin(B * x + C) + D

    # Ajuster la fonction à nos données de température
    popt, pcov = curve_fit(sinusoid, x, y)

    # Imprimer les paramètres ajustés
    print(popt)

    # Tracer la courbe de température et la régression sinusoidale
    plt.plot(x, y, 'o', label='Données de température')
    plt.plot(x, sinusoid(x, *popt), '-', label='Régression sinusoidale')
    plt.legend()
    plt.show()


# Sélectionner une ville
coord = (44.830667,-0.691333) # Bordeaux
# coord = (44.745000,1.396667) # Gourdon
# courbe_temperature(data,coord)
regression_sinus()