==================================================
URDF pour la description de robots non parallèles
==================================================

.. figure:: resources/fig/igraph/scanbot_kinematic_chain/slide003_scanbot_kinematic_chain.svg
   :name: fig_slide003_scanbot_kinematic_chain
   :align: center
   :height: 400px

   Robot Scanbot, et sa chaîne cinmématique.

Dans le cas d'un robot non parallèle, les chaînes cinématiques sont ouvertes et on peut représenter l'ensemble des chaînes cinématiques du robot par un arbre, le chemin en ligne directe de la racine à une feuille de l'arbre correspondant à une chaîne cinématique.

Le format utilisé pour décrire les robots non parallèle dans ROS est l'URDF.
Nous allons maintenant décrire la syntaxe de l'URDF.

-----------------------
Généralités sur le XML
-----------------------

L'URDF est basé sur le format XML, les éléments d'information sont organisés grâce à des balises :code:`<balise> élément </balise>`, qui peuvent être imbriquées. 
En anglais une balise est appelée un **tag**.

**Tag**
Un tag est une construction de balisage qui commence par :code:`<`` et se termine par :code:`>`. Il existe trois types de tag :

#. tag de début, tel que :code:`<section>`,
#. tag de fin, tel que :code:`</section>`,
#. tag sans élément, tel que :code:`<line-break />` (notez le symbole :code:`/` devant le symbole :code:`>` à la fin.

Un tag peut être sans élément, car l'information peut-être contenue dans l'attribut de la balise (attribute en anglais).
En français on utilise souvent le terme **balise** pour désigner un **tag**.

**Attribut**
Un attribut consiste en une paire nom-valeur qui peut apparaître dans un tag de début ou un tag sans élément.
Un exemple est :code:`<link name="base_link">`, où le nom de l'attribut est "name" et sa valeur est "base_link".
Un tag peut avoir plusieurs attributs, mais chaque attribut ne peut apparaître qu'une seule fois dans une balise.

**Élément**
Un élément est une composante logique d'un document qui commence soit par un tag de début et se termine par un tag de fin correspondant, soit consiste uniquement en un tag sans élément. Les caractères entre la balise de début et la balise de fin, s'il y en a, sont le contenu de l'élément, et peuvent contenir du balisage, y compris d'autres éléments, appelés éléments enfants. Dans l'exemple de code suivant, :numref:`example_xml_element`, l'élement ``visual``, lignes 2-10, commence par le tag de début :code:`<visual>`, se finit par le tag de fin :code:`</visual>` et possède les éléments enfants ``origin``, ``geometry`` et ``material``. L'élément  ``mass``, ligne 18, est un élément sans enfant mais qui possède un attribut ``value`` et qui donc consiste en seulement un tag sans élément: :code:`<mass value="18"/>`.

.. literalinclude:: resources/urdf/complete_link_tag.urdf
   :name: example_xml_element
   :language: xml
   :caption: Exemple d'éléments xml
   :linenos:
   :emphasize-lines: 2-10,18

-----------------------
Généralités sur l'URDF
-----------------------

**Dans le format URDF**, il existe de nombreuses balises différentes qu'il est possible d'utiliser.
Elles sont toutes décrites dans la `documentation officielle de ROS du format URDF <http://wiki.ros.org/urdf/XML>`_ .
Il y en a trois principales qu'il faut connaître **robot**, **link** et **joint**.

**Le tag robot et le préambule XML**
Un fichier XML correct doit avoir un préambule XML dans la première ligne, et juste après cela, il contient une balise (appelée la balise racine), dans laquelle toutes les autres balises sont imbriquées. 
Pour un fichier URDF, cette balise racine sera la balise **robot**, et la seule chose à noter ici pour l'instant est que nous pouvons définir l'attribut name qui nous permet de spécifier le nom de notre robot.

.. code-block:: xml

   <?xml version="1.0"?>
   <robot name="my_robot">
      ...
      toutes les autres balises
      ...
   </robot>

Les 2 balises principales de l'URDF sont **link** et **joint** et sont au même niveau d'imbrication à la base de la balise **robot**:

.. code-block:: xml

   <?xml version="1.0"?>
   <?xml-model href="https://raw.githubusercontent.com/ros/urdfdom/master/xsd/urdf.xsd" ?>
   <robot name="my_robot" xmlns="http://www.ros.org">
      <link> ... </link>
      <link> ... </link>
      <link> ... </link>

      <joint>  ....  </joint>
      <joint>  ....  </joint>
      <joint>  ....  </joint>
   </robot>
   

-------------------
La balise **link**
-------------------

La balise **link** est utilisée pour décrire un segment du robot.
La description complète de cette balise est disponible dans la `specification de la balise link <http://wiki.ros.org/urdf/XML/link>`_.


.. grid:: 1 2 2 2

   .. grid-item-card::
  
      .. literalinclude:: resources/urdf/complete_link_tag.urdf
         :language: xml
         :linenos:
         :caption: Balise ``link`` avec les éléments **visual**, **material**, **collision** et **inertial**

   .. grid-item-card::

      .. figure:: resources/img/urdf/urdf_link2.png
         :name: fig_link_element
         :align: center
         :height: 400px

         Élément ``link`` d'un fichier URDF

Nous allons maintenant nous attacher à comprendre les différents repères utilisés dans la description d'un segment d'un robot et comment les définir dans un fichier URDF.

Dans le tag **origin** (tag **visual**s ou **collision**), la position et l'orientation du repère du segment par rapport au repère du parent sont définis par les attributs **xyz** et **rpy**.  |br|

#. La translation est définie par les attributs **xyz** qui sont les coordonnées x, y et z du repère du segment par rapport au repère du parent.
#. La rotation est définie par les attributs **rpy** qui sont les angles de rotation autour des axes x, y et z du repère du segment par rapport au repère du parent. **rpy** désigne «\ **r**\ oll,\ **p**\ itch,\ **y**\ aw» ou en français: «roulis,tangage,lacet».

La rotation est toujours appliquée avant la translation et les rotations sont effectuées dans l'ordre **roll** (roulis), **pitch** (tangage) puis **yaw** (lacet) suivant le schéma ci-dessous:

.. figure:: resources/img/plane_roll_pitch_yaw.png
   :name: fig__plane_roll_pitch_yaw
   :align: center
   :height: 400px

   Rotations roulis, tangage et lacet ou («roll», «pitch» et «yaw» and anglais).

.. grid:: 1 1 1 1

   .. grid-item::

      .. grid:: 1 3 3 3

         .. grid-item-card::
            
            .. figure:: resources/img/roll_plane_animation.gif
               :name: fig_roll_plane_animation
               :align: center
               :height: 300px

               Rotation autour de l'axe x (roulis ou «roll» en anglais)


         .. grid-item-card::
            
            .. figure:: resources/img/pitch_plane_animation.gif
               :name: fig_pitch_plane_animation
               :align: center
               :height: 300px

               Rotation autour de l'axe y (tangage ou «pitch» en anglais)

         .. grid-item-card::

            .. figure:: resources/img/yaw_plane_animation.gif
               :name: fig_yaw_plane_animation
               :align: center
               :height: 300px

               Rotation autour de l'axe z (lacet ou «yaw» en anglais)


----------------
Simple exemple
----------------

Créons une simple description de robot URDF.  |br|
Pour cela nous allons utiliser l'outil de visualisation de modèles URDF fourni par ROS2: **rviz2**.  |br|
Afin de faciliter cette étape nous allons créer un package ROS2 dédié à la visualization en utilisant l'outil développé par IRIS **template2instance**.  |br|
Cet outil permet de créer facilement un package ROS2 à partir d'un template.  |br|
Pour cela nous avons besoin du template **ros2/view_robot** qui est un template de package ROS2 dédié à la visualisation de robots en utilisant rviz2.  |br|

Créons un package ROS2 nommé **simple_bot_description** ayant le fichier de configuration suivant.  |br|

.. literalinclude:: resources/code/template2instance/pkg_gen_cfg_view_simple_bot.json
   :language: json
   :caption: Configuration pour la génération du package simple_bot_description

Créer un répertoire pour sauvegarder vos configurations
.. code-block:: bash

   mkdir -p ~/ros2_ws/system/template2instance/configs

#. :download:`Télécharger le fichier de configuration <resources/code/template2instance/pkg_gen_cfg_view_simple_bot.json>` et le copier dans le répertoire :code:`~/ros2_ws/system/template2instance/configs/pkg_gen_cfg_view_simple_bot.json`.

#. Exécuter la commande suivante: 

.. code-block:: bash

   create ros2/view_robot ~/ros2_ws/src/simple_bot_description --config ~/ros2_ws/system/template2instance/configs/pkg_gen_cfg_view_simple_bot.json

#. Testez le package en le compilant:

.. code-block:: bash

   cd ~/ros2_ws
   ros2_humble
   ros2_build_only simple_bot_description

Lancez le package:

.. code-block:: bash

   ros2 launch simple_bot_description view_simple_bot.launch.py

Si tout s'est bien passé, vous devriez voir un dans rviz2 le robot par défaut:

.. figure:: resources/img/urdf/scanbot_cam/default_rviz_view.png
   :name: fig_scanbot_cam_rviz_view
   :align: center
   :height: 400px

   Le robot par défaut à l'initialisation d'un package de visualisation à partir du template view_robot_template.

Le fichier URDF qu'il faut étudier se nomme ``simple_bot_macro.xacro`` et se trouve dans le répertoire :code:`~/ros2_ws/src/simple_bot_description/urdf/simple_bot`.  |br|
C'est un fichier de type ``xacro``, c'est-à-dire un fichier XML qui peut contenir des macros. 
Ces macros permettent de définir des éléments qui peuvent être réutilisés plusieurs fois dans le fichier ou déduit par des appels à des fonctions. 
Le format cependant est celui d'un fichier URDF et par abus de language nous parlerons de fichier URDF.  |br|

Ouvrez ce fichier et modifiez le pour qu'il ressemble à ceci:

.. grid:: 1 2 2 2

   .. grid-item-card::
  
      .. literalinclude:: resources/urdf/my01_bot.urdf
         :language: xml
         :linenos:
         :caption: Exemple minimal d'un fichier URDF avec un robot à un seul segment

   .. grid-item-card::

      .. figure:: resources/img/urdf/cylinder_link.png
         :name: fig_cylinder_link
         :align: center
         :height: 400px

         Affichage d'un segment cylindre avec RVIZ correspondant à la précédente description URDF

Fermez toutes les fenêtre et tapez CTRL-C dans le terminal puis relancez le package:

.. code-block:: bash

   ros2 launch simple_bot_description view_simple_bot.launch.py

La :numref:`fig_cylinder_link` montre le segment cylindre tel qu'il devrait s'afficher dans rviz2.

Pour comprendre comment les systèmes de coordonnées fonctionnent, il faut afficher les axes.
Dans rviz:

#. dans le panneau de gauche (''Displays''), dans **RobotModel** modifiez la valeur de **Alpha** à 0.5. Cela change la transparence du modèle du robot et permet de voir les axes.
#. Si vous ne voyez pas les axes, vérifiez que vous avez bien un **TF** et sinon ajoutez un **TF** dans le panneau de gauche (''Displays'') avec le bouton **Add**. Et vérifiez bien que **Show Axes** est coché.

.. figure:: resources/img/urdf/axis_are_visible_in_rviz2_thanks_to_transparency.png
   :name: fig__cylinder_link_with_axes_visible
   :align: center
   :height: 800px

   Affichage d'un segment cylindre avec RVIZ avec les axes visibles (Alpha=0.5, Show Axes : coché)

.. admonition:: Segments définis par des primitives géométriques

   Un segment peut être défini à partir de 3 formes géométriques de base: 
   
   #. pavé droit: :code:`<box size="10 20 40"/>`. Les tailles des côtés (''size'') sont données dans l'ordre x,y,z. Les côtés du pavé droit sont parallèles aux axes x, y et z.
   #. cylindre: :code:`<cylinder radius="10" length="40"/>` l'axe est toujours l'axe z.
   #. sphère: :code:`<sphere radius="10"/>`

   Dans ce cas le repère du segment est par défaut au centre de la forme géométrique (centre de gravité).

Nous allons modifier la forme pour utiliser un pavé droit. Cela nous permettra de bien visualiser l'orientation de la forme dans les 3 dimensions.  |br|
Et nous allons modifier l'élément **origin** pour déplacer le segment par rapport à son origine.  |br|
Modifiez donc le fichier URDF pour qu'il ressemble à ceci:

.. grid:: 1 2 2 2

   .. grid-item-card::
  
      .. literalinclude:: resources/urdf/my02_tr_bot.urdf
         :language: xml
         :linenos:
         :caption: Exemple minimal d'un fichier URDF avec un robot box à un seul segment (pavé droit) dont la position est translatée de 0.5m en x (axe rouge), 1.5m en y (axe vert) et 0m en z (axe bleu) par rapport à l'origine.

   .. grid-item-card::

      .. figure:: resources/img/urdf/my02_tr_bot.png
         :name: fig_box_link_my02_tr_bot
         :align: center
         :height: 400px

         Affichage d'un segment pavé droit avec RVIZ correspondant à la description URDF sur la gauche

Nous allons modifier l'élément **origin** pour tourner le segment de 90 degrées autour de l'axe de roulis: X (roll).  |br|

.. admonition:: Notez l'ordre des transformations géométriques

   Les transformations géométriques sont effectuées dans l'ordre suivant: rotation puis translation.

.. grid:: 1 2 2 2

   .. grid-item-card::
  
      .. literalinclude:: resources/urdf/my02_tr_plus_rot_bot.urdf
         :language: xml
         :name: my02_tr_plus_rot_bot.urdf
         :linenos:
         :caption: Exemple minimal d'un fichier URDF avec un robot box à un seul segment (pavé droit) qui a subit une rotation de 90° suivant l'axe X (roll) puis dont la position est translatée de 0.5m en x (axe rouge), 1.5m en y (axe vert) et 0m en z (axe bleu) par rapport à l'origine.

   .. grid-item-card::

      .. figure:: resources/img/urdf/my02_tr_plus_rot_bot.png
         :name: fig_box_link_my02_tr_plus_rot_bot
         :align: center
         :height: 400px

         Affichage d'un segment pavé droit avec RVIZ correspondant à la description URDF sur la gauche

.. admonition:: Notez bien ce qui est déplacé par les attributs **xyz** et **rpy** de la balise **origin**

   Ce n'est pas l'origine du repère qui est déplacée mais le repère dans lequel la forme géométrique est définie.

En effet si on met le paramètre alpha à 0.5 pour voir en transparence, le centre du pavé ne contient pas de repère.  |br|
On verra dans ce qui suit la différence avec les changements dans la balise **origin** des articulations avec la description du tag **joint**. 

----------------------------------
Un point Xacro et fichiers launch
----------------------------------

Regardons l'organisation du projet ROS2 ``simple_bot_description`` (après y avoir ajouté divers fichiers URDF):

.. _simple_bot_description_tree:

.. container:: tree_simple_bot_description

   .. raw:: html
      :file: resources/html/tree_simple_bot_description.html

 |br|
 |br|

Que se passe-t-il quand nous lançons le package ``simple_bot_description`` avec la commande suivante ?

.. code-block:: bash

   ros2 launch simple_bot_description view_simple_bot.launch.py

Le fichier ``view_simple_bot.launch.py`` est exécuté.  |br|

.. literalinclude:: resources/code/ros2/simple_bot_description/view_simple_bot_01.launch.py
   :language: python
   :caption: Contenu du fichier view_simple_bot.launch.py
   :linenos:
   :emphasize-lines: 45-58

On voit que dans les lignes 45 à 58, le fichier xacro ``simple_bot.urdf.xacro`` qui se trouve dans le répertoire ``~/ros2_ws/src/simple_bot_description/urdf/`` est transformé en fichier URDF.  |br|

.. literalinclude:: resources/code/ros2/simple_bot_description/simple_bot.urdf.xacro
   :language: xml
   :caption: Contenu du fichier simple_bot.urdf.xacro
   :linenos:
   :emphasize-lines: 13

À la ligne 13, on voit une coommande ``xacro`` qui permet d'inclure un autre fichier xacro. 
Cette commande est déclarée grâce à un tag ``xacro:include`` et utilise une autre commande dont le nom est ``find`` qui permet de trouver le chemin d'un package dans le répertoire ``install`` du workspace et dont la valeur de retour est accédée avec la syntaxe ``$(find simple_bot_description)``.  |br|


Dans le :numref:`my02_tr_plus_rot_bot.urdf`, vous avez peut-être remarqué une autre commande xacro bien pratique qui permet de manipuler des angles en degrés et de les convertir en radians: ``${radians(90)}``. 

.. admonition:: Appel de fonction dans une commande xacro
   
   Notez que quand on fait un appel de fonction dans une commande xacro, on utilise des **accolades** au lieu des **paranthèses** pour les premiers délimiteurs de la commande.

Un fichier python ``xxxxx.launch.py`` peut utiliser des arguments en ligne de commande.  |br|
Dans le fichier ci-dessus lignes 23-39 sont définis 2 arguments:

#. le nom par défaut du package (``description_package``)
#. le prefix qui peut être appliqué devant le path de chaque resource, ce qui permet de réutiliser le même fichier de launch pour plusieurs instances d'objets, des robots par exemple, dans le cas d'une flotte de robots.

La syntaxe est:

.. code-block:: python

   declared_arguments.append(
        DeclareLaunchArgument(
            "name_of_the_argument_for_the_python_launch_file",
            default_value='default argument value',
            description="Description given to the user \
               when he/she is using the --help command \
               or when documentation is automatically generated.",
        )
    )

La valeur d'un paramètre est ensuite récupérée en utilisant la fonction ``LaunchConfiguration`` du module ``launch.substitutions`` (lignes 42-43).

Il est ensuite possible d'utiliser les valeurs récupérées pour réaliser des substitutions dans les fichiers de configuration, par exemple ligne 45-58, la commande ``xacro`` est appelée sur le fichier ``simple_bot.urdf.xacro`` en fournissant comme paramètre ``prefix:=""`` (ici le prefix est la chaîne de caractère vide).

Pour visualiser facilement plusieurs descriptions de robots différentes dans rviz2 et suivre les transformations des repères, il est intéressant de créer plusieurs fichiers xacro sur le modèle du fichier ``simple_bot_macro.xacro``.  |br|
Par exemple nous avons crée les fichiers:

#. simple_bot__my01_bot__macro.xacro
#. simple_bot__my02_tr_bot__macro.xacro
#. simple_bot__my02_tr_plus_rot_bot__macro.xacro
#. simple_bot__my03_bot__macro.xacro
#. simple_bot__my04_bot__macro.xacro

que vous n'avez pas encore et qui apparaissent dans l'arborescence du package ``simple_bot_description`` affichée :ref:`plus haut <simple_bot_description_tree>`.  |br|

pour modifier que quelques paramètres.  |br|

.. _exercice_xacro_launch_parameterized_urdf:

.. container:: exercice

   .. exercise:: Xacro / Launch file
      :label: ex_xacro_launch_file_for_incremental_robot_description
      :class: toggle

      Modifiez les fichiers ``view_simple_bot.launch.py`` et ``simple_bot.urdf.xacro`` pour que le fichier affiché par rviz2 soit paramétrable et par exemple affiche le fichier ``simple_bot__my03_bot__macro.xacro`` quand on lance la commande:

      .. code-block:: bash

         ros2 launch simple_bot_description view_simple_bot.launch.py urdf:=simple_bot__my03_bot__macro.xacro
      
      .. solution:: ex_xacro_launch_file_for_incremental_robot_description
         :label: sol_xacro_launch_file_for_incremental_robot_description
         :class: toggle

         Modifications du fichier ``view_simple_bot.launch.py``:

         .. literalinclude:: resources/code/ros2/simple_bot_description/view_simple_bot_02.launch.py
            :language: python
            :caption: Modification du fichier view_simple_bot.launch.py pour qu'il accepte un argument urdf qui permet de choisir le fichier xacro à afficher dans rviz2
            :linenos:
            :emphasize-lines: 40-46, 51, 65-67
         
         Modifications du fichier ``simple_bot.urdf.xacro``:

         .. literalinclude:: resources/code/ros2/simple_bot_description/simple_bot.urdf_solution.xacro
            :language: xml
            :caption: Modification du fichier simple_bot.urdf.xacro pour qu'il accepte un argument urdf qui permet de choisir le fichier xacro à afficher dans rviz2
            :linenos:
            :emphasize-lines: 13

--------------------
La balise **joint**
--------------------

La balise **joint** est utilisée pour décrire une articulation entre deux segments du robot.
La description complète de cette balise est disponible dans la `specification de la balise joint <http://wiki.ros.org/urdf/XML/joint>`_.


.. grid:: 1 2 2 2

   .. grid-item-card::
  
      .. literalinclude:: resources/urdf/joint_element_revolute.urdf
         :language: xml
         :linenos:
         :caption: Balise ``joint`` de type ``revolute`` avec les éléments  **origin**, **parent**, **child**, **axis** et **limit**
      
      .. literalinclude:: resources/urdf/joint_element_floating.urdf
         :language: xml
         :linenos:
         :caption: Balise ``joint`` de type ``floating`` avec les éléments  **origin**, **parent**, **child**, **limit**, **dynamics**, **calibration**, **safety_controller** et **mimic**


   .. grid-item-card::

      .. figure:: resources/img/urdf/urdf_joint.png
         :name: fig_joint_element
         :align: center
         :height: 400px

         Élément ``joint`` d'un fichier URDF

L'attribut **type** de la balise **joint** permet de définir le type de l'articulation (revolute, prismatic, continuous, fixed, floating ou planar).  |br|

#. **revolute**: articulation de type pivot d'axe avec des butées.
#. **prismatic**: articulation de type glissière.
#. **continuous**: articulation de type pivot d'axe avec une rotation continue (comme pour une roue).
#. **fixed**: articulation de type encastrement (fixe).
#. **floating**: articulation de type flottante (6 degrés de liberté).
#. **planar**: articulation de type appui plan (2 degrés de liberté en translation et 1 degré de liberté en rotation).

Les éléments de la balise **joint** que nous utiliserons le plus, sont:

#. **origin**: qui définit la position et l'orientation du repère de l'articulation par rapport au repère du parent.
#. **parent**: qui définit le nom du segment parent.
#. **child**: qui définit le nom du segment enfant.
#. **type**: qui définit le type de l'articulation (``revolute``, ``prismatic``, ``continuous``, ``fixed``, ``floating`` ou ``planar``).
#. **axis**: qui définit l'axe de rotation ou de translation de l'articulation utilisée uniquement pour toutes les articulations exceptée ``fixed`` et ``floating``. Sa valeur par défaut est un axe unitaire parallèle à l'axe x du repère de l'articulation :math:`(1,0,0)`. Cet axe correspond: à l'axe de rotation pour les articulations de type ``revolute`` et ``continuous``, à l'axe de translation pour les articulations de type ``prismatic`` et à la normal du plan d'appui pour les articulations de type ``planar``.
#. **limit**: qui définit les limites de l'articulation, nécessaire que pour les articulations de type ``revolute`` ou ``prismatic``. Les limites sont définies par les attributs **lower** et **upper** qui sont les valeurs minimale et maximale de l'articulation (en radians pour l'articulation de type ``revolute`` et en mètres pour l'articulation de type ``prismatic``), par l'attribut **effort** qui est la force maximale que l'articulation peut supporter (en Newtons-mètres pour les articulations de type ``revolute`` et ``continuous``, mesurant donc un couple et en Newtons pour une articulation de type ``prismatic``), et par l'attribut **velocity** qui est la vitesse maximale de l'articulation (en radians par seconde pour les articulations de type ``revolute`` et ``continuous`` et en mètres par seconde pour l'articulation de type ``prismatic``).

Dans le tag **origin** du tag **joint**, la position et l'orientation du repère de l'articulation par rapport au repère du parent sont définis par les attributs **xyz** et **rpy**. 
De la même manière pour les segments (``link``), la rotation est appliquée avant la translation. 
Dans RVIZ2, cette transformation est visible grâce à une arrête jaune terminée par une flêche qui pointe du repère enfant vers le repère parent.  |br|


.. grid:: 1 2 2 2

   .. grid-item-card::
  
      .. literalinclude:: resources/urdf/my03_bot.urdf
         :language: xml
         :linenos:
         :caption: Ajout d'une translation pour le repère de l'articulation par rapport au repère du parent (attribut **xyz** de la balise **origin** du tag **joint**).


   .. grid-item-card::

      .. figure:: resources/img/urdf/my03_bot_rviz.png
         :name: fig_translated_joint_element_my03_bot
         :align: center
         :height: 400px

         Affichage d'une articulation avec RVIZ correspondant à la description URDF sur la gauche. Le lien est modélisé par la flèche jaune de ``base_link`` vers ``world`` (en cochant la case ``Show Arrows``).

Le changement de repère introduit par le tag **origin** de la balise **joint** s'effectue avant la transofrmation du segment (balise **link**).
De même que pour la balise joint, la rotation est effectuée avant la translation (le repère tourne autour de l'origine du repère parent, puis est translaté). La rotation et la translation sont exprimées dans le repère du parent.  |br|

.. grid:: 1 2 2 2

   .. grid-item-card::
  
      .. literalinclude:: resources/urdf/my04_bot.urdf
         :language: xml
         :linenos:
         :caption: Ajout d'une rotation pour le repère de l'articulation par rapport au repère du parent (attribut **rpy** du tag **origin** du tag **joint**).


   .. grid-item-card::

      .. figure:: resources/img/urdf/my04_bot.png
         :name: fig_tr_rot_joint_element_my04_bot
         :align: center
         :height: 400px

         Rotation du repère de l'articulation en plus de la translation. Notez que la rotation est effectuée avant la translation (si cela avait été l'inverse, l'arrête jaune serait alignée avec l'axe vert du repère ``world``).