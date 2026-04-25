---
title: "Comparaison météo Bergen vs Paris"
template: about
---

[← Retour au site](/)

# Comparaison météo Bergen vs Paris

Ce projet compare 10 ans de données météorologiques quotidiennes (2016–2025) entre Bergen, Norvège et Paris, France.

- Bergen est en moyenne 5°C plus froide que Paris, mais l'écart se réduit à ~4°C en hiver
- Les températures quotidiennes sont corrélées à 81% — quand une ville se refroidit, l'autre aussi
- Les jours de neige à Bergen affichent 1,5°C en moyenne — près de huit sur dix sont au-dessus de zéro
- Bergen est géographiquement plus proche de la Côte d'Azur que de la Norvège arctique
- Quand Paris dépasse 30°C (114 jours sur la décennie), Bergen affiche un agréable 18°C en moyenne

## Explorer les données

{% data-table /%}

## Le processus

Ce projet suit la méthodologie du [pipeline School of Data](https://civicliteraci.es/data-pipeline/) : Define, Find, Get, Verify, Clean, Analyse, Present.

### Define

Parti d'une intuition personnelle : « le climat de Bergen et Paris sont similaires ». Nous l'avons déclinée en quatre hypothèses testables :

1. **H1** : Les températures moyennes quotidiennes sont à moins de 3°C l'une de l'autre
2. **H2** : Les variations de température sont corrélées — quand une ville se refroidit, l'autre aussi
3. **H3** : Les épisodes neigeux coïncident plus souvent que le hasard
4. **H4** : Les journées ensoleillées coïncident plus souvent que le hasard

### Find

{% step-meta items="Method: desk research, Sources compared: 6" /%}

Six sources de données ont été étudiées (Open-Meteo, Meteostat, Frost API, Météo-France, Visual Crossing, NOAA GSOD). Open-Meteo était la seule à proposer les six variables requises (temp moy/min/max, précipitations, neige, ensoleillement) pour les deux villes avec une complétude de 100%, sans clé API.

### Get

{% step-meta items="Tool: Python (fetch_data.py), API: Open-Meteo" /%}

Récupération de 3 653 jours de données quotidiennes par ville depuis l'[API Open-Meteo Historical Weather](https://open-meteo.com/) (réanalyse ERA5/ECMWF IFS). Zéro lacune, zéro valeur nulle.

### Verify

{% step-meta items="Tool: Python (verify_data.py), Cross-check: ERA5 vs ECMWF IFS models" /%}

- **Complétude** : séquences de dates continues, aucune valeur manquante
- **Qualité** : aucune température hors des records climatiques plausibles, aucune précipitation négative, aucune période de valeurs plates suspecte
- **Vérification croisée** : comparaison des modèles ERA5 et ECMWF IFS. Les données de Paris concordent à 1°C près sur 94% des jours. Bergen présente une incertitude de ~1,6°C entre modèles — noté mais non rédhibitoire

### Clean

{% step-meta items="Tool: Python (clean_data.py), Output: data/clean/horizon.csv" /%}

Fusion des deux villes en une table horizon unique (13 colonnes, granularité quotidienne). Standardisation des unités (ensoleillement en heures, neige en mm). Les jours extrêmes (Paris max >35°C, Bergen min <−10°C) avaient été signalés, mais un test de sensibilité a montré que leur suppression ne changeait les résultats que de <0,5°C — le filtrage a donc été abandonné.

### Analyse

{% step-meta items="Tool: Python (analyse.py), Methods: descriptive statistics, Pearson correlation, co-occurrence analysis" /%}

L'analyse a testé chaque hypothèse avec des méthodes statistiques simples : différences de températures quotidiennes et leurs distributions (H1), corrélation de Pearson avec analyse de décalage (H2), et taux de co-occurrence comparés aux probabilités aléatoires (H3, H4). Ni modélisation ni machine learning — le jeu de données est propre et les questions suffisamment directes pour des statistiques descriptives et inférentielles.

|  | Hypothèse | Résultat | Conclusion |
|--|-----------|----------|------------|
| **H1** | Températures quotidiennes à moins de 3°C | Écart moyen de 5,1°C ; seulement 25% des jours sous le seuil | Rejetée |
| **H2** | Les températures sont corrélées au quotidien | r=0,81 quotidien, r=0,94 mensuel | Confirmée |
| **H3** | Les épisodes neigeux coïncident | 2,6× plus que le hasard | Faiblement confirmée |
| **H4** | Les journées ensoleillées coïncident | 1,4× plus que le hasard | Faiblement confirmée |

{% callout %}
Le rejet de H1 s'est avéré être la découverte la plus intéressante. L'écart de 5°C cachait une histoire saisonnière : il se réduit à 4°C en hiver (avec certains mois où Bergen était même plus chaude que Paris) et s'élargit à 6°C en été. Cela a déclenché une boucle Analyse→Define — l'intuition initiale de « températures similaires » était probablement spécifique aux mois froids, où la différence est la moins perceptible, et avait été extrapolée à l'année entière. La question reformulée est devenue : Bergen n'est pas beaucoup plus froide que Paris quand le froid compte le plus (en hiver), et l'écart en été est en fait un *avantage* — Bergen évite totalement les canicules parisiennes.
{% /callout %}

Une leçon supplémentaire sur la sensibilité des seuils : Bergen « a de la neige 20% des jours » selon les données brutes du modèle (toute chute de neige >0mm), mais cela inclut des quantités infimes issues de la réanalyse. Avec un seuil de 5mm+ (« neige notable »), on obtient 14% — ce qui correspondait bien mieux à l'expérience vécue.

### Present

{% step-meta items="Tool: HTML / CSS / JavaScript, Charts: Chart.js, Maps: TopoJSON + Canvas, Data export: Python (export_for_web.py)" /%}

L'objectif était d'aider à dissiper une idée reçue répandue — surtout chez les Français — selon laquelle la Norvège est un pays défini par la neige et le froid extrême. Le site est structuré en deux parties : le *quoi* et le *pourquoi*.

Le **quoi** explore la comparaison des températures sous des angles objectifs et subjectifs. L'angle objectif examine les données brutes : moyennes mensuelles, corrélations quotidiennes, cartes thermiques année par année. L'angle subjectif reformule l'écart comme une expérience vécue : les jours de neige à Bergen sont plus doux qu'on ne le pense, et ses étés se situent dans la zone de confort thermique tandis que Paris dépasse en territoire de canicule.

Le **pourquoi** explore la géographie — les distances entre Bergen, Paris et Tromsø — pour expliquer pourquoi le climat de Bergen est si différent de la Norvège arctique que les gens imaginent. Le Gulf Stream et l'immense longueur de la Norvège sont les facteurs clés.

De nombreux graphiques incluent une petite composante interactive pour maintenir l'engagement : filtrer la carte thermique par niveau de similarité, parcourir les années sur le graphique quotidien, ou choisir une capitale européenne sur la carte des distances aériennes pour rendre le point « la Norvège est un long pays » personnel et parlant.

Le site est bilingue (EN/FR), avec détection automatique des utilisateurs français, car le public français est le premier concerné par cette idée reçue.

## Résumé des outils

L'implémentation technique a été réalisée avec Claude Code, selon une méthodologie axée sur les garde-fous : chaque tâche déléguée au LLM était limitée à une seule phase du pipeline, et sa sortie était vérifiée avant de passer à l'étape suivante. Chaque phase a produit un artefact vérifiable — un script, un jeu de données, un rapport — de sorte que l'ensemble du pipeline peut être reproduit sans aucun LLM, simplement en exécutant les scripts Python dans l'ordre. La structure méthodologique a suivi le [pipeline School of Data](https://civicliteraci.es/data-pipeline/), fournissant le cadre qui a guidé chaque étape.

**Pipeline de données** — cinq scripts Python, un par étape :

```
fetch_data.py     → data/raw/           # Téléchargement depuis l'API Open-Meteo
verify_data.py                          # Vérifications + validation croisée
clean_data.py     → data/clean/         # Fusion et standardisation
analyse.py                              # Test des hypothèses
export_for_web.py → site/data/          # Export JSON pour le site web
```

**Site web** — un site statique mono-page sans étape de build :

- [Chart.js](https://www.chartjs.org/) pour les graphiques interactifs (lollipop, séries temporelles, nuage de points, barres)
- [TopoJSON](https://github.com/topojson/topojson-client) + HTML Canvas pour la carte de fond et la carte des distances aériennes
- [Natural Earth / world-atlas](https://cdn.jsdelivr.net/npm/world-atlas@2) pour les frontières des pays (résolution 50m)
- JavaScript vanilla pour l'i18n, les animations de transition et les statistiques calculées

**Publication** — hébergé sur GitHub Pages, servi directement depuis la racine du dépôt. Code source sur [github.com/clombion/bergen-paris-weather](https://github.com/clombion/bergen-paris-weather).

## Sources

**Source des données** — [Open-Meteo Historical Weather API](https://open-meteo.com/) (réanalyse ERA5 / ECMWF IFS), 3 653 jours de données quotidiennes par ville. Jours de neige définis comme jours avec 5mm+ de chutes de neige. Zone de confort thermique basée sur [Cheung & Jim, 2019](https://link.springer.com/article/10.1007/s00484-019-01694-1).

**Données du projet** — les réponses brutes de l'API et la table horizon nettoyée sont stockées dans le dépôt pour la reproductibilité :

- [data/raw/](https://github.com/clombion/bergen-paris-weather/tree/main/data/raw) — JSON brut d'Open-Meteo (Bergen + Paris, 2016–2025)
- [data/clean/horizon.csv](https://github.com/clombion/bergen-paris-weather/blob/main/data/clean/horizon.csv) — la table horizon fusionnée (3 653 lignes × 13 colonnes)
- [site/data/](https://github.com/clombion/bergen-paris-weather/tree/main/site/data) — sous-ensembles JSON pré-calculés alimentant les graphiques du site
