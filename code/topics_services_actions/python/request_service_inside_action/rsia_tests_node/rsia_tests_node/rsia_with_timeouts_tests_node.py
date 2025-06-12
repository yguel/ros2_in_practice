import time

# ROS2 imports
import rclpy
from rclpy.node import Node
from rclpy.action import ActionServer, GoalResponse, CancelResponse
from rclpy.callback_groups import ReentrantCallbackGroup
from rclpy.executors import MultiThreadedExecutor


from rsia_tests_interfaces.srv import SrvAtest, SrvBtest
from rsia_tests_interfaces.action import ActionCtest

class RSIActionNode(Node):
    def __init__(self, executor):
        super().__init__('rsia_action_node')
        self.executor = executor

        # Publishers and subscribers

        ## Client to service to create motion
        self.srv_a_client = self.create_client( SrvAtest,'srv_a_test')
        self.srv_a_req = SrvAtest.Request()
        while not self.srv_a_client.wait_for_service(timeout_sec=2.0):
            self.get_logger().info('srv_a service not available, waiting again...')
        self.service_a_timeout_s = 2.0  # seconds

        ## Action server to initiate search for sharp images
        self.action_server = ActionServer(
            self,
            ActionCtest,
            'action_c_test',
            execute_callback = self.execute_callback,
            callback_group=ReentrantCallbackGroup(),
            goal_callback = self.goal_callback,
            cancel_callback = self.cancel_callback
        )

        self.action_pending = False

        self.get_logger().info('action_c_test ActionServer is up and running.')

        # sleeper object
        self.sleep_time_s = 10.0

    def destroy(self):
        self.action_server.destroy()
        self.srv_a_client.destroy()
        #self.srv_b_client.destroy()
        super().destroy_node()

    def cancel_callback(self, goal_handle):
        self.get_logger().info("Received request to cancel action_c_test.")
        if self.action_pending:
            self.action_pending = False
            return CancelResponse.ACCEPT
        else:
            self.get_logger().warn("No pending action to cancel.")
            return CancelResponse.REJECT

    def goal_callback(self, goal_handle):
        self.get_logger().info("Received goal")
        if self.action_pending:
            self.get_logger().warn("Action is already pending, rejecting new goal.")
            return GoalResponse.REJECT
        self.action_pending = True
        return GoalResponse.ACCEPT
    
    async def execute_callback(self, goal_handle):
        self.get_logger().info(f"Executing action for action_c_test with goal: {goal_handle.request.goal}.")
        # Create the feedback message
        feedback = ActionCtest.Feedback()
        feedback.feedback = "Action is being processed."
        goal_handle.publish_feedback(feedback)  # Publish feedback

        # Call the service and wait for its answer
        feedback.feedback = "Calling service srv_a_test."
        goal_handle.publish_feedback(feedback)
        self.srv_a_req.request_a = "Requesting service A"
        future = self.srv_a_client.call_async(self.srv_a_req)
        try:
            # response = await future ## < if one wants to wait in a blocking way, indefinitely
            # alternative with a timeout
            rclpy.spin_until_future_complete(self, future, executor=self.executor,timeout_sec=self.service_a_timeout_s)
            if future.result() is None:
                self.get_logger().error("Service A call timed out.")
                goal_handle.abort()
                result = ActionCtest.Result()
                result.result = "Action failed due to service A timeout."
                return result
            response = future.result()
            # Process the response
            feedback.feedback = f"Service A response: {response.response_a}"
            goal_handle.publish_feedback(feedback)
            self.get_logger().info(f"Service A response: {response.response_a}")
            ## end alternative with a timeout
        except Exception as e:
            self.get_logger().error(f"Service call failed: {e}")
            goal_handle.abort()
            result = ActionCtest.Result()
            result.result = "Action failed due to service A call error."
            return result

        # Wait 10s
        feedback.feedback = "Waiting for 10 seconds."
        goal_handle.publish_feedback(feedback)
        self.get_logger().info("Waiting for 10 seconds...")
        self.get_logger().info(f"Test 3")
        time.sleep(self.sleep_time_s)  # Sleep for 10 seconds
        self.get_logger().info("10 seconds passed.")
        feedback.feedback = "10 seconds passed, proceeding with action."
        goal_handle.publish_feedback(feedback)
        
        # Mark the goal as succeeded
        goal_handle.succeed()  # Mark the goal as succeeded

        # Populate the result message
        result = ActionCtest.Result()
        result.result = "Action completed successfully."
        self.get_logger().info(f"Action completed with result: {result.result}")

        # Reset the action pending flag
        self.action_pending = False 
        # Return the result
        return result

def main(args=None):
    rclpy.init(args=args)

    executor = MultiThreadedExecutor()

    node = RSIActionNode(executor=executor)

    try:
        # Spin the node in a separate thread
        rclpy.spin(node,executor=executor)
    except KeyboardInterrupt:
        print("\nKeyboard interrupt received, shutting down...")
        executor.shutdown()
    except Exception as e:
        node.get_logger().error(f"An error occurred: {e}")
        print(f"Exception occurred: {e}")
    
    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)

    try:
        node.destroy()
    except Exception as e:
        print(f"Error during node destruction: {e}")

if __name__ == '__main__':
    main()
