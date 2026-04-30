---
title: "Bergen vs Paris — The Winter Surprise"
template: index
---

{% header %}

# Bergen is not the frozen north you think it is

In winter, Norway's rainiest city is barely colder than Paris. A decade of weather data tells a surprising story. {% .subtitle %}

{% byline %}
A little side project by [Cédric Lombion](https://linkedin.com/in/cedriclombion)
{% /byline %}

{% /header %}

{% live-legend items="Bergen:#6F4CB8,Paris:#B8843A" /%}

{% section %}

## The gap narrows in winter

Average monthly temperatures over 2016–2025. In summer, Paris pulls ahead by 6°C. But from November to February, the difference shrinks to around 4°C. {% .lead %}

{% chart id="monthlyChart" height=300 /%}

{% /section %}

{% stats id="keyStats" /%}

{% section %}

## A decade, month by month

Each cell shows how much colder Bergen was than Paris. The lighter the cell, the closer they were. Purple means Bergen was warmer. {% .lead %}

{% heatmap /%}

{% /section %}

{% section %}

## When does Bergen actually feel better?

A lower temperature is a disadvantage in winter — but in summer, it's a gift. Each point below is a day Paris exceeded 30°C. The green zone shows the [thermal comfort range](https://link.springer.com/article/10.1007/s00484-019-01694-1) (20–25°C). Bergen stays in it — Paris doesn't. {% .lead %}

{% chart id="comfortChart" height=320 /%}

{% stats id="comfortStats" /%}

{% /section %}

{% section %}

## They move together

When a cold front sweeps across Europe, both cities feel it. Day to day, their temperatures move in sync 81% of the time. Month to month, the match tightens to 94%. {% .lead %}

{% stats id="corrStats" classes="stat-grid-2" /%}

{% chart id="dailyChart" height=320 fixed-height=true /%}

{% year-slider /%}

{% /section %}

{% section id="snowSection" %}

## Bergen's snow days are warmer than you think

Bergen gets noticeable snow on about 14% of days, mostly from November to March. But this isn't Arctic cold. The average temperature on a Bergen snow day is 1.5°C — almost eight in ten snow days are above freezing. On those same days, Tromsø — Norway's largest city above the Arctic Circle, the one with polar nights and northern lights — averages -5.1°C. {% .lead %}

{% stats id="snowStats" /%}

{% stats id="snowGapStats" classes="stat-grid-2" /%}

Even on its snowiest days, Bergen is closer to Paris than to Tromsø. Bergen's snow is wet Atlantic snow — falling at temperatures where Paris would have cold rain. When Paris shivers at 3°C in a winter drizzle, Bergen is at 1°C in a snowfall. Not so different after all. {% .lead %}

{% /section %}

{% section %}

## The Norway you're thinking of is very far from Bergen

When people hear "Norway," they picture the Arctic — polar bears, northern lights, endless ice. But that's Tromsø and the far north, Norway's Arctic capital, 1,200 km from Bergen. Bergen sits on the southwest coast, warmed by the Gulf Stream, closer to the Mediterranean than to the Arctic. {% .lead %}

{% flight-map /%}

### From Bergen to {% capital-select /%}

{% distance-summary /%}

{% chart id="flightChart" height=180 fixed-height=true /%}

{% callout %}
The Gulf Stream carries warm Atlantic water along Norway's west coast, keeping Bergen's winters far milder than its latitude would suggest. At 60°N, Bergen should be as cold as Anchorage, Alaska — instead, its January average is around 1°C, almost Parisian.
{% /callout %}

{% /section %}

{% methodology %}

### Methodology

Daily weather data from **Open-Meteo Historical Weather API** (ERA5 / ECMWF IFS reanalysis), covering 1 Jan 2016 – 31 Dec 2025 (3,653 days). Bergen coordinates: 60.39°N, 5.32°E. Paris: 48.86°N, 2.35°E.

Cross-checked against ECMWF IFS model; Paris data agrees within 1°C on 94% of days. Bergen shows ~1.6°C model uncertainty — noted but not disqualifying. Snow days defined as days with 5mm+ snowfall.

{% /methodology %}
