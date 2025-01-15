*********
DOMAINS
*********

.. _dds_domain_overview:

=====================
Les domaines en bref
=====================

Comme expliqué dans la précédente section, le middleware par défaut utilisé par ROS 2 pour la communication est DDS. Dans DDS, le principal mécanisme permettant à différents réseaux logiques de partager un réseau physique est appelé l'ID de domaine. Les nœuds ROS 2 sur le même domaine peuvent se découvrir et s'envoyer des messages librement, tandis que les nœuds ROS 2 sur des domaines différents ne le peuvent pas. Tous les nœuds ROS 2 utilisent par défaut l'ID de domaine 0. Pour éviter les interférences entre différents groupes d'ordinateurs exécutant ROS 2 sur le même réseau, un ID de domaine différent doit être défini pour chaque groupe.

.. _choisir-un-id-de-domaine-version-courte:

=========================
Choisir un ID de domaine 
=========================

Pour simplement choisir un ID de domain sûr, sélectionnez un ID de domaine entre ``0`` et ``101`` inclusivement.

Pour des explications détaillées sur la plage d'ID de domaine à utiliser dans ROS 2, veuillez `consulter la documentation officielle de ROS 2 <https://docs.ros.org/en/rolling/Concepts/Intermediate/About-Domain-ID.html>`_.


.. _utiliser-un-domaine-id-en-pratique:
==================================
Utiliser un DOMAIN ID en pratique
==================================

Pour définir l'ID de domaine avant d'exécuter un fichier de lancement dans ROS 2, vous pouvez définir la variable d'environnement ROS_DOMAIN_ID dans votre session terminal.

Ouvrez votre terminal et définissez la variable d'environnement ROS_DOMAIN_ID avec la valeur souhaitée (par exemple, 42) :

.. code-block:: bash

    export ROS_DOMAIN_ID=42

Cette commande configure ROS_DOMAIN_ID pour la session terminal en cours.

Avec ROS_DOMAIN_ID défini, vous pouvez exécuter votre fichier de lancement ROS 2 :

.. code-block:: bash

    ros2 launch <nom_du_paquet> <nom_du_fichier_de_lancement>

Remplacez <nom_du_paquet> par le nom de votre paquet et <nom_du_fichier_de_lancement> par le nom de votre fichier de lancement.

En définissant ROS_DOMAIN_ID avant d'exécuter le fichier de lancement, tous les nœuds initiés par ce fichier fonctionneront dans le domaine spécifié, assurant leur communication avec d'autres nœuds du même domaine.

Pour faire en sorte que le ROS_DOMAIN_ID soit persistant il est possible de l'ajouter dans le fichier .bashrc ou .zshrc de votre utilisateur.

.. code-block:: bash

    echo "export ROS_DOMAIN_ID=42" >> ~/.bashrc