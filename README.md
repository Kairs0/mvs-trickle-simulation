# Modélisation de l'algorithme Trickle

## Résumé

Une implémentation python de l’algorithme Trickle.

*Entrées* : Une topologie de réseau de capteurs, chaque capteur ayant ses propres caractéristiques. Une description des caractéristiques du réseau (Imax, Imin, k)

*Sorties* :
Une description de la simulation après un nombre d'itération donné (temps de propagation min, moyen, max et taille des données échangées)

## Description du problème

Un nœud a les attributs suivants : `I`, `tau`, `c`, `t`, `n` (numéro de version)

### Description du cycle

- à t = 0 : c:=0, tau est choisi dans [I/2, I]
- à t = tau : si c < k : broadcast n aux voisins
- à t = I : si on n'a pas reçu de n différent du notre: I:=min(Imax, 2I)
		sinon, I = Imin
		t := 0

Durant tout le cycle, si on reçoit un message (méthode `message_received` appelée) :
Cas:

- n_ext = n : c:=c+1
- n_ext < n : broadcast n, code
- n_ext > n : broadcast n
- next < node & code received: broadcast n

## Modélisation

## Première version : une topologie de réseau statique

Structure: Notre modèle est composé de deux objets :

### Objet Node

Modélise un nœud avec l'ensemble des ses caractéristiques.

***Attributs***

| name | type | description |
|:----:|:----:|:----------- |
| `id` | `int` | |
| `name` | `str` | |
| `neighbours` | `set<Node>` | ensemble des nœuds présents dans le rayon du nœud |
| `Imin`, `Imax` | `int` | bornes de la valeur possibles pour I |
| `I` | `int` | représente la durée de l'intervalle courant |
| `tau` | `int` | moment de la communication |
| `c` | `int` | compteur |
| `t` | `int` | temps (propre au nœud) |
| `n` | `int` | version actuelle du logiciel |
| `inconsistent` | `bool` | Détermine le comportement du nœud à la prochaine expiration de l'intervalle : si le paramètre est à False (informations de version consistantes avec l'état initial du nœud), alors on augmente l'intervalle ; dans le cas contraire, on remet le paramètre I à la valeur I min |
| `buffer` | `set()` | liste des messages reçus à considérer au prochain tick. |
| `k` | `int` | constance de redondance |
| `number_of_code_sendings` | `int` | Nombre de communications du code |

***Méthodes***

| signature | description |
|:---------:|:----------- |
| `broadcast(bool)` | envoie un message (version + éventuellement code) à l'ensemble des voisins |
| `receive(int, bool)` | ajoute le message reçu au buffer du nœud |
| `add_neighbour(node)` | |
| `remove_neighbour(node)` | |
| `update(int)` | met à jour la version et le code |
| `tick()`  | effectue actions (selon messages dans buffer et temps t) |
| `reinit()` | réinitialise le nœud |

### Objet Cattle

Gère le réseau de nœuds avec une horloge activant à chaque tour un nœud.

***Attributs***

| name | type | description |
|:----:|:----:|:----------- |
| `nodes` | `set<Node>` | l'ensemble des nœuds du réseau |
| `Imin` | `int` | taille minimale de l'intervalle d'écoute |
| `max` | `int` | valeur servant au calcul de `Imax` |
| `Imax` | `int` |(propriété) taille maximale de l'intervalle d'écoute |
| `k` | `int` | constante de redondance pour paramétrer le comportement des nœuds |
| `time` | `int` | horloge du cattle (horloge globale) |
| `connected_nodes` | `set<Nodes>` | Ensemble des nœuds par lesquels une nouvelle version peut être injectée |
| `current_version` | `int` | (propriété) Version la plus récente du logiciel |
| `coverage` | `double` | (propriété) pourcentage de couverture du réseau pour la version actuelle |

***Méthodes***

| signature | description |
|:---------:|:----------- |
| `new_node(str, int, bool=False)` | ajoute un noeud, connecté ou non |
| `remove_node(node, str)`| Retire un noeud |
| `tick()` | choisit un noeud au hasard dans la liste de nœuds et appelle la méthode `tick()` du noeud |
| `start()` | commence la simulation |
| `get_node_by_name(name)` | retourne un noeud de nom donné|
| `get_versions()` | retourne un dictionaire donnant les versions de chaque noeud |
| `get_number_of_code_sendings()` | retourne le nombre total de message envoyés lors de la simulation |
| `main()` | itération de ticks (à chaque tick, le nœud va faire ses actions (recevoir, émettre, mettre à jour) ; une fois que toutes ses actions ont été effectuées, le cattle envoie le tick suivant. |

## Seconde version: ajout des paramètres dynamiques

### Gestion des mises à jour

Pour la gestion des mises à jour, nous choisissons aléatoirement une date entre deux valeurs possibles. Lorsque l'horloge globale (représentée par un compteur dans le main.py) atteint cette date, une nouvelle version est diffusée dans le réseau à un nœud choisi parmi les nœuds "connectés".
