---
title: "Bergen vs Paris — La surprise hivernale"
template: index
---

{% header %}

# Bergen n'est pas le grand nord que vous imaginez

En hiver, la ville la plus pluvieuse de Norvège est à peine plus froide que Paris. Une décennie de données météo raconte une histoire surprenante. {% .subtitle %}

{% byline %}
Un petit projet perso de [Cédric Lombion](https://linkedin.com/in/cedriclombion)
{% /byline %}

{% /header %}

{% live-legend items="Bergen:#6F4CB8,Paris:#B8843A" /%}

{% section %}

## L'écart se réduit en hiver

Températures moyennes mensuelles sur 2016–2025. En été, Paris prend 6°C d'avance. Mais de novembre à février, la différence se réduit à environ 4°C. {% .lead %}

{% chart id="monthlyChart" height=300 /%}

{% /section %}

{% stats id="keyStats" /%}

{% section %}

## Une décennie, mois par mois

Chaque cellule montre l'écart de température entre Bergen et Paris. Plus la cellule est claire, plus les températures étaient proches. Une cellule violette signifie que Bergen était plus chaude. {% .lead %}

{% heatmap /%}

{% /section %}

{% section %}

## Quand fait-il meilleur à Bergen qu'à Paris ?

Une température plus basse est un désavantage en hiver — mais en été, c'est un cadeau. Chaque point ci-dessous représente un jour où Paris a dépassé 30°C. La zone verte indique la [zone de confort thermique](https://link.springer.com/article/10.1007/s00484-019-01694-1) (20–25°C). Bergen y reste — pas Paris. {% .lead %}

{% chart id="comfortChart" height=320 /%}

{% stats id="comfortStats" /%}

{% /section %}

{% section %}

## Elles bougent ensemble

Quand une vague de froid balaie l'Europe, les deux villes la ressentent. Au jour le jour, leurs températures évoluent en phase 81 % du temps. Mois par mois, la concordance atteint 94 %. {% .lead %}

{% stats id="corrStats" classes="stat-grid-2" /%}

{% chart id="dailyChart" height=320 fixed-height=true /%}

{% year-slider /%}

{% /section %}

{% section id="snowSection" %}

## Les jours de neige à Bergen sont plus doux qu'on ne le pense

Bergen connaît des chutes de neige notables 14 % des jours, principalement de novembre à mars. Mais ce n'est pas le froid arctique. La température moyenne d'un jour de neige à Bergen est de 1,5°C — près de huit jours de neige sur dix sont au-dessus de zéro. Ces mêmes jours, Tromsø — la plus grande ville norvégienne au-dessus du cercle polaire, celle des nuits polaires et des aurores boréales — affiche -5,1°C en moyenne. {% .lead %}

{% stats id="snowStats" /%}

{% stats id="snowGapStats" classes="stat-grid-2" /%}

Même lors de ses jours les plus enneigés, Bergen est plus proche de Paris que de Tromsø. La neige de Bergen est une neige atlantique humide — elle tombe à des températures où Paris reçoit de la pluie froide. Quand Paris frissonne à 3°C sous la bruine, Bergen est à 1°C sous la neige. Pas si différent, au fond. {% .lead %}

{% /section %}

{% section %}

## La Norvège à laquelle vous pensez est très loin de Bergen

Quand on entend « Norvège », on imagine l'Arctique — ours polaires, aurores boréales, glace à perte de vue. Mais cette image, c'est plutôt celle du Grand Nord. C'est là que l'on trouve Tromsø, la capitale arctique de la Norvège, à 1 200 km de Bergen. Bergen se trouve sur la côte sud-ouest, réchauffée par le Gulf Stream, plus proche de la Méditerranée que de l'Arctique. {% .lead %}

{% flight-map /%}

### De Bergen à {% capital-select /%}

{% distance-summary /%}

{% chart id="flightChart" height=180 fixed-height=true /%}

{% callout %}
Le Gulf Stream transporte des eaux atlantiques chaudes le long de la côte ouest de la Norvège, rendant les hivers de Bergen bien plus doux que sa latitude ne le suggère. À 60°N, Bergen devrait être aussi froide qu'Anchorage en Alaska — au lieu de cela, sa moyenne de janvier est d'environ 1°C, presque parisienne.
{% /callout %}

{% /section %}

{% methodology %}

### Méthodologie

Données météorologiques quotidiennes provenant de l'**API Open-Meteo Historical Weather** (réanalyse ERA5 / ECMWF IFS), couvrant du 1er janvier 2016 au 31 décembre 2025 (3 653 jours). Coordonnées Bergen : 60,39°N, 5,32°E. Paris : 48,86°N, 2,35°E.

Vérifié par croisement avec le modèle ECMWF IFS ; les données de Paris concordent à 1°C près sur 94 % des jours. Bergen présente une incertitude de ~1,6°C entre modèles — noté mais non rédhibitoire. Jours de neige définis comme jours avec 5mm+ de chutes de neige.

{% /methodology %}
