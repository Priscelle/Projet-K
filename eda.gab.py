import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import rcParams
import geopandas as gpd
import contextily as ctx
import numpy as np 
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import cartopy.crs as ccrs
import matplotlib.patches as patches

rcParams['font.family'] = 'DejaVu Sans'

# Chargement des fichiers CSV pour les années 2021 à 2024
df_2021 = pd.read_csv('resultats_2021-1723625960367.csv')
df_2022 = pd.read_csv('resultats_2022-1723626025027.csv')
df_2023 = pd.read_csv('resultats_2023-1723626045072.csv')
df_2024 = pd.read_csv('resultats_2024-1723626062852.csv')

# Préparation des Données
# Suppression des lignes avec des valeurs manquantes pour chaque DataFrame
df_2021 = df_2021.dropna()
df_2022 = df_2022.dropna()
df_2023 = df_2023.dropna()
df_2024 = df_2024.dropna()

# Ajout d'une colonne d'année à chaque DataFrame
df_2021['année'] = 2021
df_2022['année'] = 2022
df_2023['année'] = 2023
df_2024['année'] = 2024

# Concaténation des DataFrames
df_combined = pd.concat([df_2021, df_2022, df_2023, df_2024], ignore_index=True)

# Filtrage des données pour exclure les séries `5eA`, `3e`, `BEPC`, et `CEP`
df_combined = df_combined[~df_combined['serie'].isin(['5eA', '3e', 'BEPC', 'CEP_CO'])]

# Calcul du Pourcentage d'Admis
admis_par_categorie = df_combined[df_combined['code_decision'] == 'A'].groupby(['année', 'serie', 'code_province', 'nom_etablissement']).size()
total_par_categorie = df_combined.groupby(['année', 'serie', 'code_province', 'nom_etablissement']).size()
pourcentage_admis = (admis_par_categorie / total_par_categorie.replace(0, np.nan)) * 100

# Réinitialisation de l'index pour faciliter la manipulation
df_pourcentage = pourcentage_admis.reset_index(name='Pourcentage Admis')

# Distribution par sexe pour toutes les années avec ajustement
plt.figure(figsize=(12, 6))
sns.countplot(data=df_combined, x='sexe', hue='année', palette='viridis')
plt.title('Distribution des Étudiants par Sexe et Année')
plt.xlabel('Sexe')
plt.ylabel('Nombre d\'Étudiants')
plt.legend(title='Année', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.xticks(rotation=0)
plt.tight_layout()
plt.show()

# Distribution par série pour toutes les années
plt.figure(figsize=(12, 6))
sns.countplot(data=df_combined, y='serie', hue='année', palette='viridis')
plt.title('Distribution des Étudiants par Série et Année')
plt.xlabel('Nombre d\'Étudiants')
plt.ylabel('Série')
plt.legend(title='Année', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()

# Distribution par décision (Admis/Non Admis) pour toutes les années 
plt.figure(figsize=(12, 6))
sns.countplot(data=df_combined, x='code_decision', hue='année', palette='viridis')
plt.title('Distribution des Décisions (Admis/Non Admis) par Année')
plt.xlabel('Décision')
plt.ylabel('Nombre d\'Étudiants')
plt.legend(title='Année', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()

# Distribution par province pour toutes les années
plt.figure(figsize=(12, 6))
sns.countplot(data=df_combined, x='code_province', hue='année', palette='viridis')
plt.title('Distribution des Étudiants par Province et Année')
plt.xlabel('Province')
plt.ylabel('Nombre d\'Étudiants')
plt.legend(title='Année', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Répartition par Tour (1er ou 2ème tour) pour toutes les années
plt.figure(figsize=(12, 6))
sns.countplot(data=df_combined, x='tour', hue='année', palette='viridis')
plt.title('Répartition des Étudiants par Tour et Année')
plt.xlabel('Tour')
plt.ylabel('Nombre d\'Étudiants')
plt.legend(title='Année', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.xticks(rotation=0)
plt.tight_layout()
plt.show()

# Graphiques pour le pourcentage d'admis par année
for year in df_pourcentage['année'].unique():
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=df_pourcentage[df_pourcentage['année'] == year], x='code_province', y='Pourcentage Admis', hue='serie', markers=True, palette='viridis')
    plt.title(f'Pourcentage d\'Admis au Bac par Province et Série pour l\'Année {year}')
    plt.xlabel('Province')
    plt.ylabel('Pourcentage d\'Admis')
    plt.legend(title='Série', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.show()

# Impact par province pour chaque année
plt.figure(figsize=(12, 6))
sns.barplot(data=df_pourcentage, x='code_province', y='Pourcentage Admis', hue='année', palette='viridis')
plt.title('Impact de la Plateforme Kewa par Province et Année')
plt.xlabel('Province')
plt.ylabel('Pourcentage d\'Admis')
plt.legend(title='Année', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
plt.show()

# Heatmap du pourcentage d'admis par province et année
pivot_province = df_pourcentage.pivot_table(values='Pourcentage Admis', index='code_province', columns='année')
plt.figure(figsize=(12, 8))
sns.heatmap(pivot_province, annot=True, cmap='viridis', fmt='.1f')
plt.title('Heatmap du Pourcentage d\'Admis par Province et Année')
plt.xlabel('Année')
plt.ylabel('Province')
plt.show()

# Heatmap du pourcentage d'admis par série et année
pivot_serie = df_pourcentage.pivot_table(values='Pourcentage Admis', index='serie', columns='année')
plt.figure(figsize=(12, 8))
sns.heatmap(pivot_serie, annot=True, cmap='viridis', fmt='.1f')
plt.title('Heatmap du Pourcentage d\'Admis par Série et Année')
plt.xlabel('Année')
plt.ylabel('Série')
plt.show()

# Création de la map pour la visualisation des l'accès internet par provinces
# Définition des provinces et des niveaux d'accès à Internet
provinces = {
    'Estuaire': (9.5, 0.4),
    'Haut-Ogooué': (13.5, -1.5),
    'Moyen-Ogooué': (10.4, -0.6),
    'Ngounié': (11.0, -1.4),
    'Nyanga': (11.3, -2.9),
    'Ogooué-Ivindo': (12.8, 0.6),
    'Ogooué-Lolo': (12.7, -1.0),
    'Ogooué-Maritime': (9.3, -1.0),
    'Woleu-Ntem': (11.5, 1.0)
}

internet_access = {
    'Estuaire': 80,      
    'Haut-Ogooué': 50,
    'Moyen-Ogooué': 40,
    'Ngounié': 30,
    'Nyanga': 20,
    'Ogooué-Ivindo': 70,
    'Ogooué-Lolo': 60,
    'Ogooué-Maritime': 55,
    'Woleu-Ntem': 65
}

# Création d'une figure et un axe avec la projection Mercator
fig, ax = plt.subplots(figsize=(12, 8), subplot_kw={'projection': ccrs.Mercator()})

# Ajout des éléments de carte
ax.add_feature(cfeature.COASTLINE)
ax.add_feature(cfeature.BORDERS, linestyle=':')
ax.add_feature(cfeature.LAND, edgecolor='black')
ax.add_feature(cfeature.OCEAN)
ax.add_feature(cfeature.LAKES, edgecolor='black')
ax.add_feature(cfeature.RIVERS)

# Création d'un colormap
colors = plt.get_cmap('YlOrRd')  # Yellow to Red colormap

# Ajout des points colorés représentant l'accès à Internet
for province, (lon, lat) in provinces.items():
    access_level = internet_access.get(province, 0)
    color = colors(access_level / 100.0)  # Normaliser les niveaux d'accès entre 0 et 1
    ax.plot(lon, lat, 'o', color=color, markersize=10, transform=ccrs.Geodetic())
    ax.text(lon + 0.2, lat, f'{province}\n{access_level}%', fontsize=12, transform=ccrs.Geodetic(), ha='left', bbox=dict(facecolor='white', alpha=0.7))

# Ajouter une barre de couleur pour les pourcentages d'accès
sm = plt.cm.ScalarMappable(cmap=colors, norm=plt.Normalize(vmin=0, vmax=100))
sm.set_array([])
cbar = plt.colorbar(sm, ax=ax, orientation='vertical', pad=0.02)
cbar.set_label('Pourcentage d\'Accès à Internet')
cbar.set_ticks([0, 20, 40, 60, 80, 100])
cbar.ax.yaxis.set_tick_params(color='black')

plt.title('Carte des Provinces du Gabon avec Accès à Internet')
plt.show()



# Analyse des années 2021 à 2023 pour la simulation des résultats du Bac 2024
# Calcul de la moyenne des pourcentages d'admis pour les années 2021 à 2023 par province
historical_data = df_pourcentage[df_pourcentage['année'].isin([2021, 2022, 2023])]
avg_percentages = historical_data.groupby('code_province').agg({'Pourcentage Admis': 'mean'}).reset_index()

avg_percentages.rename(columns={'Pourcentage Admis': 'Pourcentage Simulé'}, inplace=True)

# Fusion des données simulées avec les résultats réels de 2024
simulated_vs_real = df_pourcentage[df_pourcentage['année'] == 2024].merge(avg_percentages, on='code_province', how='left')

# Graphique en barres
simulated_vs_real_melted = simulated_vs_real.melt(id_vars='code_province', 
                                                  value_vars=['Pourcentage Simulé', 'Pourcentage Admis'],
                                                  var_name='Type de Résultat',
                                                  value_name='Pourcentage')

# Graphique en barres comparaison des résultats simulés et réels pour 2024
plt.figure(figsize=(14, 8))
sns.barplot(data=simulated_vs_real_melted, x='code_province', y='Pourcentage', hue='Type de Résultat', palette='viridis')

plt.title('Comparaison des Pourcentages d\'Admis Simulés et Réels au Bac 2024 par Province')
plt.xlabel('Province')
plt.ylabel('Pourcentage')
plt.legend(title='Type de Résultat', loc='upper left')
plt.xticks(rotation=45)
plt.grid(True, axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()

# Ajout du Graphique de l'évolution des résultats par année

# Calcul du pourcentage d'admis combiné pour toutes les séries
evolution_par_annee = df_pourcentage.groupby('année')['Pourcentage Admis'].mean().reset_index()

# Visualisation de l'évolution des résultats
plt.figure(figsize=(12, 6))
sns.lineplot(data=evolution_par_annee, x='année', y='Pourcentage Admis', marker='o', color='b')
plt.title('Évolution des Pourcentages d\'Admis au Bac par Année')
plt.xlabel('Année')
plt.ylabel('Pourcentage d\'Admis')
plt.grid(True)
plt.show()

# Calcul dupPourcentage d'Admis par série et par année
evolution_par_annee_serie = df_pourcentage.groupby(['année', 'serie'])['Pourcentage Admis'].mean().reset_index()

# Visualisation de l'évolution des résultats par Série et par Année
plt.figure(figsize=(12, 6))
sns.lineplot(data=evolution_par_annee_serie, x='année', y='Pourcentage Admis', hue='serie', marker='o', palette='viridis')
plt.title('Évolution des Pourcentages d\'Admis au Bac par Série et par Année')
plt.xlabel('Année')
plt.ylabel('Pourcentage d\'Admis')
plt.legend(title='Série', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(True)
plt.show()

# Calculer le pourcentage moyen d'admis par établissement, par année et par province
avg_admis_par_etablissement_annee = df_pourcentage.groupby(['année', 'nom_etablissement', 'code_province'])['Pourcentage Admis'].mean().reset_index()

# Visualisation des 10 meilleurs établissements par année
for year in sorted(df_pourcentage['année'].unique()):
    # Filtrer les données pour l'année en cours
    top_10_etablissements = avg_admis_par_etablissement_annee[avg_admis_par_etablissement_annee['année'] == year]
    
    # Trier par pourcentage d'admission et sélectionner les 10 premiers
    top_10_etablissements = top_10_etablissements.sort_values(by='Pourcentage Admis', ascending=False).head(10)
    
    # Ajouter une colonne combinée pour nom et province de l'établissement
    top_10_etablissements['etablissement_province'] = top_10_etablissements['nom_etablissement'] + ' (' + top_10_etablissements['code_province'] + ')'
    
    # Créer le graphique
    plt.figure(figsize=(12, 6))
    sns.barplot(data=top_10_etablissements, x='Pourcentage Admis', y='etablissement_province', palette='viridis')
    plt.title(f'Top 10 des Établissements avec les Meilleurs Résultats en {year}')
    plt.xlabel('Pourcentage d\'Admis')
    plt.ylabel('Établissement (Province)')
    plt.grid(True, axis='x', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()
