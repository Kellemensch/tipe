import numpy as np
import random as rd
import pandas as pd

"""
def Est_partition(P, E):
    '''Renvoie True si P est une partition de E
        P: liste de listes Pk qui peuvent être hashables
        E: liste d'elements'''
    D = {}
    for k, Pk in enumerate(P):
        if len(Pk) == 0:
            print("La clause P%s est vide" % (k))
            return False
        for i in Pk:
            if i not in E:
                print("L'lelment %i n'est pas dans E" % (i))
                return False
            if i not in D:
                D[i] = k
            elif D[i] != k:
                print("L'element %s appartient a P%s et P%s a la fois"%(i, D[i], Pk))
                return False
            else:
                print("L'element %s est e double dans P%s"%(i, Pk))
                return False
    for i in E:
        if D.has_key(i):
            return True
        else:
            print("%s n'est present dans aucune classe de P"%(i))
            return False
 """      
        
# n est le nombre de caractéristiques de chaque donnée
# N est le nombre d'élément
        
def kppv(A,D,k,x):
    '''Renvoie une liste de dimension N triée en foction de leur disctance au candidat'''
    L = []
    N,n = A.shape
    for i in range(N):
        dist2 = 0.0
        for j in range(n):
            dist2 = dist2 + (float(A[i,j]) - float(x[j]))**2
        dist = np.sqrt(dist2)
        L.append((D[i], dist))
    Lktriee = sorted(L, key = lambda L: L[1])[0::k] #liste triee limitee aux k premiers elements
    return Etiqu_maj(Lktriee, epsilon=10**(-3))

def Etiqu_maj(L,epsilon):
    '''Recoit la liste triée
        Renvoie l'etiquette première si la dsitance est (presque) nulle
                ou l'etiquette la plus fréquente'''
    if L[0][1] <= epsilon:
        return L[0][0]
    dictiofreq = {}
    freqmax = 0
    nums = len(L)
    for k in range(nums): #iteration sur la liste
        if k in dictiofreq.keys(): #on verifie la presence de la cle dans le dictionnaire
            dictiofreq[k] += 1
        else:
            dictiofreq[k] = 1
        if dictiofreq[k] >= freqmax: #si cette cle est la plus frequente
            clefreqmax = L[k][0]
    return clefreqmax
    
    
def MatConf(X,DictX,SplA,A,DictA,k):
    N,n = A.shape
    nb_etiqu = len(DictX.values())
    M = np.zeros((nb_etiqu,nb_etiqu),dtype = int)
    compt = 0
    liste_i = []
    while compt < N//4: #tests sur 25% du nb total de donnees
        i = rd.randint(0,N-1)
        if i not in SplA and i not in liste_i: #pas tiré dans le set d'apprentissage ni déja tiré
            x = X[i,:].reshape(columns,1) #extraction nouveau candidat, dimensionnement au bon format
            etiqu_vraie = DictX[i] #son etiquette vraie
            etiqu_estim = kppv(A,DictA,k,x) #son etiquette estimee
            print(etiqu_estim,etiqu_vraie)
            M[etiqu_vraie,etiqu_estim] += 1 #incrementation de M[i,j]
            liste_i.append(i)
            compt += 1
    return M


def Proba_i(M,i):
    somme_i = sum([M[i,j] for j in range(M.shape[1])])
    return M[i,i] / somme_i


if __name__ == "__main__":
    data = pd.read_csv("Donnéees_synopopendata_2018-2020/donnees-synop-essentielles-omm.csv",sep=';', encoding='latin-1')
    #dataset = pd.read_csv("Données_kaggle_2018-2020/nr_2018-01.csv",index_col='region', sep=',')
    useless_columns = ["Type de tendance barométrique.1", "Id OMM station", "Date","Coordonnees", "Nom", "Temps passé 1.1", "Temps présent.1", "communes (name)", "communes (code)", "EPCI (name)", "EPCI (code)", "department (name)", "department (code)", "region (name)", "region (code)", "mois_de_l_annee"]
    dataset = data.drop(useless_columns, axis=1)
    rows = len(dataset)-1
    columns = len(data.columns) - len(useless_columns)
    nbdonneesX = 100000
    SplX = rd.sample([i for i in range(rows)], nbdonneesX)
    #X est une matrice dont chaque ligne est un enregistrement du dataset
    X = np.zeros((nbdonneesX, columns), dtype = int).astype(object)
    #DictX[i] est la classe, donc les caractéristiques, de la ligne X[i,:]
    DictX = {}
    try:
        for i,j in enumerate(SplX):
            #print(i,j)
            #X[i] = float(dataset.iloc[j]).to_numpy()
            X[i] = dataset.iloc[j].to_numpy().astype(object)
            #print(type(X))
            DictX[i] = dataset.iloc[j]
            #print(DictX[i])
    except Exception as exception:
        print(f"{exception}")
    else:
        nbdonneesA = 3*nbdonneesX//4
        SplA = rd.sample([i for i in range(nbdonneesX)], nbdonneesA)
        #Set d'apprentissage
        A = np.zeros((nbdonneesA, columns), dtype = int).astype(object)
        DictA = {}
        for i,j in enumerate(SplA):
            for k in range(columns):
                try:
                    int(X[j][k])
                except ValueError:
                    X[j][k] = float(X[j][k])
                else:
                    X[j][k] = 0
                    
            A[i] = np.copy(X[j])
            DictA[i] = DictX[j]
    
        x = dataset.iloc[300].to_numpy().astype(object)#.to_numpy().reshape(1,columns)
        #print(dataset.iloc[300])
        k=10
        reponse = kppv(A,DictA,k,x)
        print(reponse)
        conf = MatConf(X,DictX,SplA,A,DictA,k)
        print(conf)