==================
Robots parallèles
==================

Pour un robot parallèle, il existe des chaînes cinématiques fermées.
Ainsi un segment peut avoir peut avoir 2 articulations comme parents.
Cela rajoute une ou plusieurs contraintes aux mouvements possibles pour le segment.

Il ne s'agit donc plus d'appliquer de manière itérative les transformations associées à chaque articulation qui conduisent au segment pour connaître sa position.

La description URDF, qui n'accepte que des arbres cinématique n'est donc pas adaptée à cette représentation.

ROS et RVIZ ne permettent pas de gérer directement les chaînes cinématiques fermées.

-------------------
Afficher dans RVIZ
-------------------

Pour afficher dans RVIZ, il faut utiliser un format URDF dans lequel les chaînes cinématiques fermées sont représentées par des chaînes cinématiques ouvertes.

Et il faut utiliser du code qui permet de calculer les positions des segments en fonction des articulations en prenant en compte les contraintes de fermeture.


-------------------
Représentation SDF
-------------------

Il existe une solution qui permet de faire automatiquement les calculs de contrainte liés aux chaînes fermés en utilisant Gazebo comme solveur.

La solution est de passer par un format de description de robot plus général, le format SDF, utilisé par Gazebo et qui prend en compte les chaînes cinématiques fermées.