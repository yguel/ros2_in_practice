*********************
Installation de ROS2
*********************

Il y a plusieurs types d'installation possible:

#. Installation en utilisant docker. C'est la plus simple et qui marche sur windows, mac et linux.
#. Installation en utilisant des paquets précompilés (deb). C'est la plus rapide et qui marche très bien sur linux Ubuntu et qui peut être adaptée pour d'autres distributions linux.
  
  #. Installation en utilisant des paquets précompilés (deb) avec un noyau temps-réel. Celle que l'on doit privilégier pour fonctionner avec un robot et qui marche principalement sur linux Ubuntu, mais qui peut être adaptée pour d'autres distributions linux.

#. Installation en utilisant le code source. C'est la plus compliquée et longue à installer, elle marche sur linux Ubuntu et peut-être adaptée pour d'autres distributions linux, et avec plus de difficultés et des limitations sur windows et mac.

.. tab-set::

    .. tab-item:: Docker 

      .. tab-set::
         :sync-group: docker-install

         .. tab-item:: Docker pour linux
            :sync: linux

            Suivez les instructions à l'adresse suivante: https://docs.docker.com/desktop/setup/install/linux/
         
         .. tab-item:: Docker pour windows
            :sync: windows

            Suivez les instructions à l'adresse suivante: https://docs.docker.com/desktop/setup/install/windows-install/

      
      Créer un répertoire de travail pour le projet ROS2 qui sera partagé entre l'hôte et le conteneur docker:

      .. tab-set::
         :sync-group: docker-install

         .. tab-item:: Docker pour linux
            :sync: linux

            Dans une console

            .. code-block:: bash

               mkdir -p ~/ros2_course_docker_data
            
         .. tab-item:: Docker pour windows
            :sync: windows

            Créer le répertoire: ``C:\Users\<YourUser>\Documents\ros2_course_docker_data``

      Maintenant vous pouvez lancer le conteneur docker:

      .. tab-set::
         :sync-group: docker-install

         .. tab-item:: Docker pour linux
            :sync: linux

            Dans une console

            .. code-block:: bash

               docker run -p 6080:80  -v "/home/YourUser>/ros2_course_docker_data:/home/ubuntu/ros2_course" --shm-size=1064m yguel/ros2_in_practice:humble
            
         .. tab-item:: Docker pour windows
            :sync: windows

            Dans une console du programme docker-desktop:

            .. code-block:: bash

               docker run -p 6080:80  -v "C:\Users\<YourUser>\Documents\ros2_course_docker_data:/home/ubuntu/ros2_course" --shm-size=1064m yguel/ros2_in_practice:humble
      
      Dans une fenêtre de navigateur, ouvrez l'URL suivante: [http://localhost:6080](http://localhost:6080) et vous devriez voir un bureau ubuntu.
      Vous pouvez maintenant ouvrir un terminal et exécuter les commandes ROS2.
      

    .. tab-item:: Paquets précompilés (deb) pour Ubuntu

         Pour installer ROS2, il est recommandé de suivre `les instructions officielles de la documentation ROS2 pour ubuntu <https://docs.ros.org/en/humble/Installation/Ubuntu-Install-Debs.html>`_

         Pour installer template2install:

         .. code-block:: bash

            cd /tmp && wget --content-disposition "https://seafile.unistra.fr/f/af9e58e541c04baba959/?dl=1" &&  apt-get update -q && DEBIAN_FRONTEND=noninteractive apt-get install -f -y ./template2instance_1.0_amd64.deb && rm /tmp/template2instance_1.0_amd64.deb


.. admonition:: Exercice

   Installez ROS2 sur votre machine.

.. admonition:: Exercice 

   Vérifiez que l'installation de ROS2 s'est bien passée en exécutant les commandes suivantes dans un premier terminal pour lancer un nœud **publisher** (talker) écrit en C++:

   .. code-block:: bash

      source /opt/ros/humble/setup.bash
      ros2 run demo_nodes_cpp talker

   et dans un second terminal éxécutez la commande suivante pour lancer un nœud **subscriber** (listener) écrit en Python:

   .. code-block:: bash

      source /opt/ros/humble/setup.bash
      ros2 run demo_nodes_py listener

   Si vous voyez le message "I heard" suivi d'un nombre, c'est que l'installation de ROS2 s'est bien passée.

************************
Création d'un workspace
************************

Un projet ROS2 se compile et s'exécute dans ce que l'on appelle un ``workspace`` souvent abrévié en ``ws`` dans lequel se trouve un répertoire ``src`` qui contient les packages ROS2 que vous allez créer ou que vous allez utiliser.

.. code-block:: bash

   cd ~/ros2_course
   mkdir -p ros2_ws/src

Nous allons maintenant utiliser un package ROS2 que nous allons installer dans le répertoire ``src`` de votre workspace ROS2.

.. code-block:: bash

   cd ~/ros2_course/ros2_ws/src
   git clone https://github.com/yguel/scara_tutorial_ros2.git

Afin d'accélerer les processus de compilation et d'exécution, nous allons utiliser des macros bash qui facilitent la tâche quand on utilise la suite d'outils ROS2 centrée sur ``colcon``.

Ouvrez votre fichier ``~/.bashrc`` avec vscode:

.. code-block:: bash

   code ~/.bashrc

Ajoutez à la fin du fichier les lignes suivantes:

.. literalinclude:: resources/code/_.bashrc
   :language: bash
   :caption: Addons au fichier .bashrc
   :linenos:

Enregistrez le fichier et fermez vscode.

Rechargez votre fichier ``~/.bashrc`` pour prendre en compte les modifications:

.. code-block:: bash

   source ~/.bashrc

Vous pouvez maintenant utiliser les macros bash que vous venez de définir.

****************************
Tests de votre installation
****************************

La commande définie dans le fichier .bashrc **ros2_humble** permet de charger l'environnement ROS2 de la distribution **humble**. Cette commande est à exécuter à chaque fois que vous ouvrez un nouveau terminal.

.. code-block:: bash

   ros2_humble

.. note::

   Vous pouvez vérifier que vous avez bien chargé l'environnement ROS2 de la distribution **humble** en exécutant la commande suivante:

   .. code-block:: bash

      echo $ROS_DISTRO

.. Note::

   Pour charger une autre distribution ROS2, vous pouvez définir une nouvelle commande dans votre fichier .bashrc en remplaçant **humble** par le nom de la distribution que vous souhaitez charger. Cela a déjà été fait pour la distribution **jazzy** (commande :code:`ros2_jazzy`). |br|
   Bien sûr pour que cela marche il faut que la distribution soit installée sur votre machine.

La commande définie dans le fichier .bashrc **ros2_build** permet de compiler les packages de votre workspace ROS2 et de charger les variables d'environnement nécessaires pour exécuter les nœuds de ces packages.

Compilez votre workspace ROS2:

.. code-block:: bash

   ros2_build

Si vous avez des erreurs, vérifiez que vous avez bien suivi les instructions précédentes.