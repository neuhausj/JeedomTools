Bonjour à tous,
Voici le script que j'ai réalisé afin d'utiliser Grafana (visualisation) et InfluxDB (stockage) pour visualiser les données de Jeedom.

Introduction
----------
Grafana est une alternative plus flexible et puissante aux pages historiques. 
Il est très facile de mettre des seuils, d'effectuer des calculs sur ses mesures, intégrer d'autres sources de données si besoin. 
Par ailleurs il est aussi possible d'afficher des valeurs seules, des tableaux de bord, ou de créer tes propres plugins de visualisation (camembert, ...). 

Voici un site de démo pour avoir un meilleur aperçu des possibilités: http://play.grafana.org



Prérequis:
----------
* InfluxDB et Grafana : https://influxdata.com/
* Bibliothèque Python InfluxDB : http://influxdb-python.readthedocs.org/en/latest/include-readme.html


Script:
----------
Il suffit de remplir la partie "Script settings" avec les bons paramètres puis de lancer le script.


Description:
----------
Le script permet de récupérer la requête GET envoyée par jeedom (via le paramètre PushURL) et la transmettre à la base de donnée.
Ca fonctionne très bien et ça permet de rapidement enregistrer les valeurs souhaitées.

Voici un schéma de principe de la solution qui fonctionne à présent chez moi (je dispose d'une Jeedom Mini+ ainsi que d'un Raspberry, mais on peux très bien imaginer avoir RPi + InfluxDB + Grafana sur le même système):
[![Schema](http://zupimages.net/up/16/04/q6vb.png)

Exemple de commande Push URL pour un capteur: 

	http://IP_PCScript:1234/updateData?name=#cmd_name#&cmd_id=#cmd_id#&val=#value#&location=exterieur

Et voici un exemple de courbe obtenue avec Grafana:
[![Courbes](http://zupimages.net/up/16/04/3bhe.png)

Le gros avantage de Grafana est de pouvoir visualiser très rapidement plusieurs valeurs. Voici la config de l'exemple ci-dessus (consommation horaire, température, consommation instanée et différence de température sur 1h): 
[![Config](http://zupimages.net/up/16/04/4x1o.png)

On peut ensuite créer différentes vues pour visualiser ses données.


Résumé:
----------
A l'utilisation c'est on ne peut plus simple: 
* dans jeedom, il faut simplement renseigner la PushURL des éléments à logger
* le script se charge de les transmettre à InfluxDB
* Il ne reste plus qu'à définir ses dashboards (vues) dans Grafana



Si vous avez des questions ou remarques, n'hésitez pas à les laisser ci-dessous.
