=========
Services
=========

Launch the service A node:

.. code-block:: bash

   ros2_humble_src
   ros2 run rsia_tests_node srv_a_node


Call the service A for testing:

.. code-block:: bash

   ros2_humble_src
   ros2 service call /srv_a_test  rsia_tests_interfaces/srv/SrvAtest   "{request_a: test_A_request! }"

=======
Action
=======

Without timer
--------------

Launch the action node without timer:

.. code-block:: bash

   ros2_humble_src
   ros2 run rsia_tests_node rsia_tests_node

With timer
-----------

Launch the action node with timer:
.. code-block:: bash

   ros2_humble_src
   ros2 run rsia_tests_node rsia_with_timeouts_tests_node

=======================
Test the action server
=======================

The actual action can be tested by sending a goal to the action server:

.. code-block:: bash

   ros2_humble_src
   ros2 action send_goal /action_c_test  rsia_tests_interfaces/action/ActionCtest   "{goal: test }"