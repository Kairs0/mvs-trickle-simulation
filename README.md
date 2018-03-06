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
- neighbours : set<Node>
- I : int
- Tho : int
- c : int
- t : int
- n : int
- code : str
- is_consistant: bool

***Méthodes*** :
- broadcast(n, ?code)
- receive(n, ?code)
- append_neighbour(node)
- remove_neighbour(node)
- receive_tick()

#### Objet Cattle:

Gère le réseau de noeud avec une horloge activant les différents noeuds

***Attributs*** : 
- network : set<Node>
- Imin : int
- Imax : int
- k : int
- 

***Méthodes*** :
- tick() : choisi un noeud au hasard dans la liste de noeuds et appelle la méthode tick()
- main() : itération de ticks (à chaque tick, le nœud va faire ses actions (recevoir, emmètre, mettre à jour); une fois que toutes ses actions ont été effectuées, le cattle envoie le tick suivant.

### Seconde version

*à venir*

