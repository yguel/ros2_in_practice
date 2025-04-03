###########################
ROADMAP
###########################

4 Sessions of 4 hours


#. Robot modeling
   
   #. URDF
   #. reproduce scara model
   #. transformations (tf2) plays programmatically with tf2

     #. 3 points method for manually specifying a coordinate system
     #. how to export matrices, quaternions and euler angles for coordinate systems

   #. play with inertia parameters
   #. see and interact in gazebo (with an obstacle fixed and mobile)
   #. playing with rqt for doing a small user interface (how to add a button to stop the robot)
   
#. Controlling and monitoring a robot

   #. ROS2 control
   #. playing with rqt and rqt_plot and learn how to display graphs with ros2
   #. learn to record and replay stuffs with rosbag
   #. move the real robot (Franka or UR) just with the moveit GUI
   
#. Plannification and manipulation with MoveIt
   
   #. moveit tutorial
   #. manipulation with moveit in simulation
   #. programmatically with moveit (stacking blocks)

      #. how to make a robot angulate its end effector around a point
      #. how to make a robot move its end effector in a straight line

   #. move the real robot (Franka or UR) just with the moveit GUI
   
#. Perception, calibration, environment mapping

   #. robot parameter estimation
   #. perception (introduce SLAM) --> online material with a quizz
   #. laser scanner on the robot in gazebo : detect the cubes and obstacles and stack with moveit
   #. example on the real robot (Franka or UR) with the laser scanner