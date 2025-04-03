==================================
URDF par la pratique: le scanbot
==================================

.. figure:: resources/fig/igraph/scanbot_kinematic_chain/slide003_scanbot_kinematic_chain.svg
   :name: fig_slide003_scanbot_kinematic_chain2
   :align: center
   :height: 400px

   Robot Scanbot, le robot d'exemple non parallèle, et sa chaîne cinmématique.

Pour pratiquer nous allons utiliser un robot simple, d'exemple, que nous avons appelé scanbot.
Il se compose d'une partie en translation x,y,z, d'un bras vert capable de pivoter autour de l'axe x et d'un système à 3 degrées de liberté en rotation supportant une caméra à son organe terminal (voir la :numref:`fig_slide003_scanbot_kinematic_chain`).

------------------------
Maillages des segments
------------------------

Pour produire les maillages, nous avons utilisé le logiciel `cadquery <https://github.com/CadQuery/cadquery>`_ (très bien `documenté <https://cadquery.readthedocs.io/en/latest/>`_). Cela permet de créer de manière procédural les formes à partir du language python en utilisant les opérations élémentaires de CAO (sketch, extrusion, combinaisons booléennes de forme). |br|

#. :download:`scanbot.py <resources/3d/scanbot/cadquery/scanbot.py>`,
#. :download:`cq_utils.py <resources/3d/scanbot/cadquery/cq_utils.py>`.

.. exercise:: génération de maillages des segments du scanbot de manière procédurale avec cadquery. [avancé]
   :label: ex_cadquery_scanbot
   :class: toggle

   Installez cq-editor, puis exécutez le programme scanbot.py 
   
   .. code-block:: python

      exec( open('<path_to>/scanbot.py').read() )
   
   en remplaçant <path_to> par le chemin absolu du fichier scanbot.py (n'oubliez pas de mettre dans le même répertoire le fichier cq_utils.py).

   Cela va créer les maillages des segments du scanbot.

Format step
^^^^^^^^^^^^

Les maillages des segments du scanbot au format step sont les suivants:

#. :download:`scanbot_s00_base_link.step <resources/3d/scanbot/scanbot_s00_base_link.step>`,
#. :download:`scanbot_s01_gauntry_link.step <resources/3d/scanbot/scanbot_s01_gauntry_link.step>`,
#. :download:`scanbot_s02_x_cyl_link.step <resources/3d/scanbot/scanbot_s02_x_cyl_link.step>`,
#. :download:`scanbot_s03_z_leg_link.step <resources/3d/scanbot/scanbot_s03_z_leg_link.step>`,
#. :download:`scanbot_s05_ankle_link.step <resources/3d/scanbot/scanbot_s05_ankle_link.step>`,
#. :download:`scanbot_s06_y_cyl_link.step <resources/3d/scanbot/scanbot_s06_y_cyl_link.step>`,
#. :download:`scanbot_s07_toe_link.step <resources/3d/scanbot/scanbot_s07_toe_link.step>`,
#. :download:`scanbot_s08_z_cyl_link.step <resources/3d/scanbot/scanbot_s08_z_cyl_link.step>`,
#. :download:`scanbot_s09_camera_link.step <resources/3d/scanbot/scanbot_s09_camera_link.step>`

.. exercise:: génération de fichier de maillage collada à partir d'autre fichiers de maillage (step,stl,...) [pratique]
   :label: ex_conversion_maillage
   :class: toggle

   À partir des maillages ci-dessus au format step, utilisez un logiciel de CAO pour les convertir au format collada (.dae).
   Indice: Utilisez le logiciel FreeCAD.

.. .. admonition:: Exercice avancé

..    À partir de l'API python de FreeCAD, écrivez un script qui automatise la conversion des fichiers step en fichiers collada.

Format collada (.dae)
^^^^^^^^^^^^^^^^^^^^^

Les maillages des segments du scanbot au format collada sont les suivants:

#. :download:`scanbot_s00_base_link.dae <resources/3d/scanbot/scanbot_s00_base_link.dae>`,
#. :download:`scanbot_s01_gauntry_link.dae <resources/3d/scanbot/scanbot_s01_gauntry_link.dae>`,
#. :download:`scanbot_s02_x_cyl_link.dae <resources/3d/scanbot/scanbot_s02_x_cyl_link.dae>`,
#. :download:`scanbot_s03_z_leg_link.dae <resources/3d/scanbot/scanbot_s03_z_leg_link.dae>`,
#. :download:`scanbot_s05_ankle_link.dae <resources/3d/scanbot/scanbot_s05_ankle_link.dae>`,
#. :download:`scanbot_s06_y_cyl_link.dae <resources/3d/scanbot/scanbot_s06_y_cyl_link.dae>`,
#. :download:`scanbot_s07_toe_link.dae <resources/3d/scanbot/scanbot_s07_toe_link.dae>`,
#. :download:`scanbot_s08_z_cyl_link.dae <resources/3d/scanbot/scanbot_s08_z_cyl_link.dae>`,
#. :download:`scanbot_s09_camera_link.dae <resources/3d/scanbot/scanbot_s09_camera_link.dae>`


-----------------
Produire un URDF
-----------------

Nous allons décrire ce robot en URDF. |br|
Pour cela nous allons utiliser l'outil de visualisation de modèles URDF fourni par ROS2: **rviz2**. |br|
Afin de faciliter cette étape nous allons créer un package ROS2 dédié à la visualization en utilisant l'outil développé par IRIS **template2instance**. |br|
Cet outil permet de créer facilement un package ROS2 à partir d'un template. |br|
Pour cela nous avons besoin du template **ros2/view_robot** qui est un template de package ROS2 dédié à la visualisation de robots en utilisant rviz2. |br|

template2instance est un outil python utilisant le gestionnaire de dépendances **poetry** qui s'utilise de la manière suivante:

.. code-block:: bash

   create path_to_template path_to_new_package [--config path_to_config.json]

Caméra et 3 degrées de liberté en rotation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Commençons simplement par décrire la caméra et les 3 degrées de liberté en rotation. |br|
Pour cela, créons un package ROS2 nommé **scanbot_cam_description** à partir du template **view_robot_template**. |br|

C'est une bonne pratique de mettre les fichiers URDF dans un package ROS2 dédié à la description du robot et appelé my_robot_name_**description**. |br|

Pour cela copier/éditer pour adapter à votre cas le fichier de configuration suivant:

.. literalinclude:: resources/code/template2instance/pkg_gen_cfg_view_scanbot_camera.json
   :language: json
   :caption: Configuration pour la génération du package scanbot_cam_description

Copiez le fichier de configuration à l'emplacement :code:`~/system/template2instance/config/pkg_gen_cfg_view_scanbot_camera.json`. |br|

Puis exécuter la commande suivante:

.. code-block:: bash

   create ros2/view_robot ~/ws_ros2/src/scanbot_cam_description --config ~/system/template2instance/config/pkg_gen_cfg_view_scanbot_camera.json

Compiler le package:

.. code-block:: bash

   cd ~/ws_ros2
   ros2_humble
   ros2_build

Testez le package:

.. code-block:: bash

   ros2 launch scanbot_cam_description view_scanbot_camera.launch.py

.. figure:: resources/img/urdf/scanbot_cam/default_rviz_view.png
   :name: fig_default_rviz_view
   :align: center
   :height: 400px

   Le robot par défaut à l'initialisation d'un package de visualisation à partir du template view_robot_template.

Nous pouvons maintenant éditer le fichier URDF/xacro (``urdf/scanbot_camera/scanbot_camera_macro.xacro``) pour décrire la caméra et les 3 degrées de liberté en rotation. |br|
Nous allons commencer par enlever tous les éléments servant à décrire le robot par défaut. |br|


.. grid:: 1 2 2 2

   .. grid-item-card::

      .. literalinclude:: resources/urdf/scanbot_camera_macro_00_empty.xacro
         :language: xml
         :caption: scanbot_camera_macro.xacro avec un seul élément
         :emphasize-lines: 17-19
   
   .. grid-item-card::

      .. figure:: resources/img/urdf/scanbot_cam/x_cyl_link_only.png
         :name: fig_scanbot_cam_x_cyl_link_only
         :align: center
         :height: 400px

         Le premier segment de la partie caméra du scanbot. Le repère est placé au centre de la face arrière circulaire du cylindre.

L'élément nouveau utilisé dans l'URDF est la balise ``<mesh>`` qui permet de charger un maillage au format collada. Nous avons utilisé le maillage du segment ``scanbot_s02_x_cyl_link.dae``. L'attribut ``filename`` permet de spécifier le chemin du fichier collada, celui-ci est fourni par rapport au package ROS2, c'est pourquoi nous avons le chemin fourni commence par ``package://`` suivi du nom du package (``scanbot_cam_description``) et du path dans ce package: ``package://scanbot_cam_description/meshes/scanbot_s02_x_cyl_link.dae``. |br|
Nous avons aussi spécifiée l'échelle du maillage. ROS2 utilise le mètre comme base unitaire. Notre maillage étant déjà en mètre, nous n'avons en réalité pas besoin d'utiliser l'attribut ``scale``, pour des raisons pédagogique, nous l'avons spécifié avec l'échelle sur chaque axe à ``1.`` . |br|

   .. exercise:: debug ROS2 [avancé]
      :label: ex_debug_ros2_advanced_2_nodes_publishing_robot_state_publisher_on_same_topic
      :class: toggle

      Dans cet exercice, nous allons volontairement faire bugger ROS2 pour apprendre à debugger des problèmes courants. |br|
         
      Comme dans l' :ref:`exercice sur la paramétrisation des fichiers de launch<exercice_xacro_launch_parameterized_urdf>` modifiez les fichiers:
      
      #. ``launch/view_scanbot_camera.launch.py`` de launch
      #. ``urdf/scanbot_camera.urdf.xacro`` de chargement de l'urdf

      pour pouvoir visualiser différentes configuration de robot avec une commande du type:

      .. code-block:: bash

         ros2 launch view_scanbot_camera view_scanbot_camera.launch.py urdf:=scanbot_camera_macro_666_maze.xacro

      Téléchargez les fichiers suivants dans le répertoire ``urdf/scanbot_camera`` du package ``view_scanbot_camera``:

      #. :download:`scanbot_camera_macro_666_maze.xacro <resources/urdf/scanbot_camera_macro_666_maze.xacro>`,
      #. :download:`scanbot_camera_macro_01.xacro <resources/urdf/scanbot_camera_macro_01.xacro>`.

      Réalisez maintenant la séquence d'opérations suivantes:

      #. Exécutez la commande précédente dans un terminal, au niveau du workspace contenant le package ``view_scanbot_camera`` et après avoir sourcé le workspace (:code:`ros2_humble_src`).
      #. Observez toutes les parties du scanbot empilées les unes sur les autres (les transformations ne sont pas correctes).
      #. Dans un autre terminal, toujours dans le même workspace (et après avoir sourcé le workspace), exécutez maintenant la commande:

      .. code-block:: bash

         ros2 launch view_scanbot_camera view_scanbot_camera.launch.py urdf:=scanbot_camera_macro_01.xacro

      Vous devriez observer une deuxième fenêtre rviz s'ouvrir et le segment cheville (``ankle_link``) osciller en position comme dans les images ci-dessous:


      .. grid:: 1 2 2 2

         .. grid-item-card::
      
            .. figure:: resources/img/ros2_strange_robot_flickering.gif
               :name: fig_strange_robot_flickering
               :align: center
               :height: 400px

               Le segment cheville (``ankle_link``) oscille en position.

         .. grid-item-card::

            .. figure:: resources/img/ros2_strange_robot_flickering_position_vue.gif
               :name: fig_strange_robot_flickering_position_vue
               :align: center
               :height: 400px

               En affichant la position du segment cheville (``ankle_link``) on observe bien que la position x oscille.


      (si vous ne l'observez pas, vérifiez que dans le premier terminal, le processus est toujours fonctionnel et sinon relancez-le.)

      Que se passe-t-il et comment pouvez-vous le diagnostiquer ? |br|

      .. solution:: ex_debug_ros2_advanced_2_nodes_publishing_robot_state_publisher_on_same_topic
         :label: sol_debug_ros2_advanced_2_nodes_publishing_robot_state_publisher_on_same_topic
         :class: dropdown

         Il semble donc que la position du segment cheville (``ankle_link``) soit reçue de manière contradictoire. |br|
         Il faut savoir que c'est le nœud ``robot_state_publisher`` qui est responsable de la publication des transformations des segments du robot. |br|
         Si vous effectuez la commande  
         
         .. code-block:: bash
         
            ros2 node list 
         
         vous allez voir un résultat de ce type:
         
         .. code-block:: bash
            :emphasize-lines: 1,4-5
         
            WARNING: Be aware that are nodes in the graph that share an exact name, this can have unintended side effects.
            /joint_state_publisher
            /joint_state_publisher
            /robot_state_publisher
            /robot_state_publisher
            /rviz2
            /transform_listener_impl_5c6fb5eea4e0
         
         ros2 nous prévient, il y a plusieurs nœuds avec exactement le même nom: ici les nœuds ``joint_state_publisher`` et ``robot_state_publisher`` sont dédoublés. |br|
         On ne voit rien par contre quand on examine la liste des topics car chaque nœud a publié sur le même topic: ``robot_description``. En effet, plusieurs nœuds peuvent publier sur le même topic. 
         Attention: quand un publisher se déclare, un nouveau topic n'est pas automatiquement créé. |br|
         Comme nous n'avons pas tué le premier process qui affiche l'urdf ``scanbot_camera_macro_666_maze.xacro`` avant de lancer le deuxième process qui affiche l'urdf ``scanbot_camera_macro_01.xacro``, les 2 nœuds ``robot_state_publisher`` publient en même temps sur le même topic ``robot_description``, mais des descriptions contradictoires (si vous regarder les tags ``<joint>`` qui définissent la position du segment ``ankle_link`` vous verrez en effet cette différence de position (de 20cm). |br|
         Il suffit donc de tuer le premier process pour arrêter le problème. |br|
         Notez que parfois, si on appuie plusieurs fois sur CTRL-C, le processus ne s'arrête pas correctement et on peut avoir un problème de ce type.
         À ce moment-là il faut chercher le processus responsable avec la commande:

         .. code-block:: bash

            ps aux | grep ros2

         puis tuer le processus avec la commande:

         .. code-block:: bash

            kill -9 <pid>
         
         NOTEZ-BIEN: quand vous tuez un processus ROS2 avec CTRL-C dans un terminal, ne tapez bien qu'une seule fois sur CTRL-C et attendez que le processus s'arrête. Cela vous évitera des problèmes de ce type.
         
Nous allons maintenant ajouter les éléments de la caméra et des
2 autres degrées de liberté en rotation. |br|