<img  style="float: left; margin: 0 10px 0 0; " alt="" src="./others_ressources/icon_logo.png">

# **TRIAL VISUALIZER**

![Language](https://img.shields.io/badge/Language-Python-0052cf)
![Open Source](https://badges.frapsoft.com/os/v2/open-source.svg?v=103)

---

## TRIAL VISUALIZER permet de stocker les données collectées sous forme de publications et d’études cliniques sous forme de deux types (essais contrôlés randomisés et études observationnelles)

#### Entre autre nous avons une base sur mongoDB qui nous permet de stocker toutes ses données puis les utilisés à fin d'avoir un dashboard complet avec des filtres, reporting, overview...

__Partant sur un fichier Excel contenant les données cliniques, les fonctionnalitées sont :__

* L'alimentation automatisée de la base de données 
    * Les affichages graphiques, de tableaux ou de tout autre type de représentation visuelle qui aide à comprendre les données de manière efficace.
    * Capacité de filtrer les données par phase d'essai ou autres critères
    * Possibilité de faire du reporting sur les données


***Les possibilités de reporting***
*  Analyse des revues publiant le plus d'abstracts au total et par trimestre
    *  Détermination des concepts les plus fréquents dans les publications (hors preprints) pour une période donnée
    *  Nombre d'essais en différentes phases (1/2/3/4)
    *  Groupement des essais selon les interventions (colonne "interventions"), en particulier ceux avec un arm_group_label = Drug
    *  Regroupement des essais par mois/année croissant
    *  Correspondance entre les preprints et les articles en fonction de la similarité des titres et des auteurs
