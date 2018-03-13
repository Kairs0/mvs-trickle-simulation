# Modélisation de l'algorithme Trickle

## Résumé

Une implémentation python de l’algorithme Trickle ()

*Entrées* : Une topologie de réseau de capteurs, chaque capteur ayant ses propres caractéristiques. Une description des caractéristiques du réseau (Imax, Imin, k)

*Sorties* : 
Une description de la simulation après un nombre d'itération donné (temps de propagation min, moyen, max et taille des données échangées)

## Description du problème

Un nœud a les attributs suivant: I, tho, c, t, n (numéro de version)
#### Description du cycle:
- à t = 0 : c:=0, Tho est choisi dans [I/2, I]
- à t = Tho : si c < k : broadcast n aux voisins
- à t = I : si on n'a pas reçu de n différent du notre: I:=min(Imax, 2I)
		sinon, I = Imin
		t := 0

Durant tout le cycle, si on reçoit un message (méthode message_received appelée) :
Cas:
- n_ext = n : c:=c+1
- n_ext < n : broadcast n, code
- n_ext > n : boradcast n 
- next < node & code received: boradcast n

## Modélisations

### Première version : une topologie de réseau statique

Structure: Notre modèle est composé de deux objets :

#### Objet Node:

Modélise un nœud avec l'ensemble des ses caractéristiques.

***Attributs***:
- neighbours : set<Node>, ensemble des nœuds présents dans le rayon du nœud
- I : int, représente la durée de intervalle courant
- tau: int, moment de la communication
- c : int, compteur
- t : int, temps (propre au nœud)
- n : int, version actuelle du logiciel
- inconsistent: bool
- buffer: set(), liste des messages reçus à considérer au prochain tick

***Méthodes*** :
- broadcast(n, ?code) : envoie un message (version + éventuellement code) à l'ensemble des voisins
- receive(n, ?code) : ajoute le message reçu au buffer du nœud
- append_neighbour(node)
- remove_neighbour(node)
- update(n, node) : met à jour la version et le code
- tick() : effectue actions (selon messages dans buffer et temps t)

#### Objet Cattle:

Gère le réseau de noeud avec une horloge activant les différents noeuds

***Attributs*** : 
- network : set<Node>
- Imin : int
- Imax : int
- k : int
- 

***Méthodes*** :
- tick() : choisi un noeud au hasard dans la liste de noeuds et appelle la méthode tick() du noeud
- main() : itération de ticks (à chaque tick, le nœud va faire ses actions (recevoir, emmètre, mettre à jour); une fois que toutes ses actions ont été effectuées, le cattle envoie le tick suivant.

### Seconde version

*à venir*

