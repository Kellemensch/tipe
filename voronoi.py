################################Interpolation
#Polygones de Thiessen/Voronoi
coords = np.fliplr(coords) #inverse la latitude et longitude pour que le diagramme de voronoi s'affiche a l'endroit
vor = Voronoi(coords)

#affiche le diagramme
voronoi_plot_2d(vor)
#plt.show()


# # Récupération des coordonnées des villes
# coords = data[['Latitude', 'Longitude']].values

# # Récupération de la liste des régions
# region_list = list(vor.regions)
# print(vor.regions)
# # Calcul des barycentres pour chaque région
# barycenters = []
# for region in region_list:
# 	print("region:", region)

# 	if all(index >= 0 for index in region):
# 		vertices = vor.vertices[region]
# 		barycenter = np.mean(vertices, axis=0)
# 		barycenters.append(barycenter)
# 	else:
# 		barycenters.append(np.nan)

# # Création d'un tableau pour stocker les prévisions
# # dans chaque point de la grille régulière
# lat_min, lat_max = np.min(coords[:, 0]), np.max(coords[:, 0])
# lon_min, lon_max = np.min(coords[:, 1]), np.max(coords[:, 1])
# grid_points = []
# for lat in np.arange(lat_min, lat_max, 0.1):
#     for lon in np.arange(lon_min, lon_max, 0.1):
#         grid_points.append([lat, lon])
# grid_points = np.array(grid_points)
# predictions = np.zeros(grid_points.shape[0])

# # Calcul des prévisions pour chaque point de la grille
# point_regions = [region_list.index(vor.regions[i]) for i in range(len(coords))]
# for i, point in enumerate(grid_points):
#     nearby_regions = [region_list[j] for j in vor.regions[point_regions[i]] if j != -1]
#     distances = [np.linalg.norm(point - barycenters[j]) for j in nearby_regions]
#     weights = 1.0 / np.array(distances)
#     weighted_values = [data.loc[nearby_regions[j], 'Température'] * weights[j] for j in range(len(nearby_regions))]
#     prediction = sum(weighted_values) / sum(weights)
#     predictions[i] = prediction

# # Affichage des résultats sur la carte de la France
# fig, ax = plt.subplots(figsize=(12, 12))
# ax.scatter(data['Longitude'], data['Latitude'], c=data['Température'], cmap='coolwarm')
# voronoi_plot_2d(vor, ax=ax, show_vertices=False)
# ax.scatter(grid_points[:, 1], grid_points[:, 0], c=predictions, cmap='coolwarm', alpha=0.2)
# ax.set_xlabel('Longitude')
# ax.set_ylabel('Latitude')
# plt.show()


#version simple
# Define a class to represent the interpolated points
class InterpolatedPoint:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.min_distance = 999999
        self.value = -1

def distance_between(p1, p2):
    return math.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2)

def voronoi_interpolation(data_set, width, height):
    #tableau 2D des points
    surface = [[InterpolatedPoint(x, y) for y in range(height)] for x in range(width)]
    #appliquer l'interpolation a chaque point de l'espace
    for i in range(width):
        for j in range(height):
            for raw_point in data_set:
                current_distance = distance_between(surface[i][j], raw_point)
                if current_distance < surface[i][j].min_distance:
                    surface[i][j].min_distance = current_distance
                    surface[i][j].value = raw_point.value
    return surface

#essai avec des valeurs arbitraires
data_set = [InterpolatedPoint(0, 0), InterpolatedPoint(0, 10), InterpolatedPoint(10, 0), InterpolatedPoint(10, 10)]
data_set[0].value = 1
data_set[1].value = 2
data_set[2].value = 3
data_set[3].value = 4

#surface de longueur et largeur 100
surface = voronoi_interpolation(data_set, 100, 100)

#valeur du point interpolé a (50,50)
print(surface[50][50].value)

def plot_surface(surface):
    # Create a 2D array of the interpolated point values
    values = [[point.value for point in row] for row in surface]
    # Create a figure and axis object
    fig, ax = plt.subplots()
    # Plot the surface as an image
    im = ax.imshow(values, cmap='viridis', interpolation='nearest')
    # Add a colorbar
    cbar = ax.figure.colorbar(im, ax=ax)
    cbar.ax.set_ylabel('Value', rotation=-90, va='bottom')
    # Set the x and y axis labels
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    # Set the plot title
    ax.set_title('Interpolated Surface')
    # Show the plot
    plt.show()
plot_surface(surface)