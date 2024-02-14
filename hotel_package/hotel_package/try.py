import csv
from geometry_msgs.msg import PoseStamped
from nav2_simple_commander.robot_navigator import BasicNavigator, TaskResult
import rclpy
from rclpy.executors import MultiThreadedExecutor
from std_msgs.msg import Empty,String
from rclpy.duration import Duration
from rclpy.node import Node 
import sys
import select
import os
import threading
i=False
s=False
g=None
room_positions = {
    "kitchen": (5.31,4.49),
    "home": (6.13,-0.62),
    "table1":(0.60,-1.47),
    "table2":(0.50,2.36),
    "table3":(-3.50,2.44)
    # Add more rooms as needed
}
class Hotel(Node):
    def __init__(self):
        super().__init__('connect_to_charging_dock_navigator')
        self.navigator = BasicNavigator()
        self.navigator.waitUntilNav2Active()
        self.room=None
        #self.table_handle()
    def navigate_to_place(self,room_name):
        global room_positions
        self.room=room_name
        if room_name in room_positions:
            x, y = room_positions[room_name]
            a=self.goal(x,y)
            if a=="cancel":
                return "cancel"
        else:
            print("Room not found in the CSV file.")
    def waiting_function(self):
        print("Entering waiting function...")

        # Wait for user input or until 10 seconds have passed
        print("You have 20 seconds to enter 'confirm'...")
        i, _, _ = select.select([sys.stdin], [], [], 20)

        if i:
            user_input = sys.stdin.readline().strip()
            if user_input.lower() == 'confirm':
                print("User confirmed. Returning to calling position.")
                return "Confirmed"
        else:
            print("Timeout reached. Returning to calling position.")
            return "Timeout"
    def goal(self,x,y):
            global i
            global g
            # Go to the specified position
            goal_pose = PoseStamped()
            goal_pose.header.frame_id = 'map'
            goal_pose.header.stamp = self.navigator.get_clock().now().to_msg()
            goal_pose.pose.position.x = x
            goal_pose.pose.position.y = y
            goal_pose.pose.orientation.w = 0.78
            print(self.room)
            self.navigator.goToPose(goal_pose)

            while not self.navigator.isTaskComplete():
                feedback = self.navigator.getFeedback()
                if(i==True)or(self.room==g):
                    i=False
                    self.navigator.cancelTask()
            result = self.navigator.getResult()
            if result == TaskResult.SUCCEEDED:
                print('Goal succeeded!')
            elif result == TaskResult.CANCELED:
                print('Goal was canceled!')
                return "cancel"
            elif result == TaskResult.FAILED:
                print('Goal failed!')
            else:
                print('Goal has an invalid return status!')
    def table_handle(self):
        try:
            while True:
                global s
                global g
                s = False
                g = None
                food = []
                table = []
                k = 0
                i = 0
                for f in range(3):
                    a = input("Enter table no: ")
                    f = input("Enter the food: ")
                    # Check if both table number and food are entered
                    if a.strip() and f.strip():
                        table.append(a)
                        food.append(f)
                print(table)
                if table:
                    b = self.navigate_to_place("kitchen")
                    l = len(table)
                    if (b == "cancel") and l == 1:
                        self.navigate_to_place("home")
                    else:
                        a = self.waiting_function()        #waiting for a conformation from the kitchen
                        if a == "Confirmed":
                            while i < l:
                                if s and g in table:                                        
                                    table.remove(g)        # Remove the current table from the list
                                    l = l - 1
                                    k += 1  
                                    s = False
                                    if (l <= 0) or (i == l):
                                        break  
                                w = self.navigate_to_place(table[i])     # Navigate to the current table
                                if w == "cancel":                        # Wait for confirmation if needed
                                    if i == l - 1:
                                        k = k + 1
                                        break
                                    else:
                                        continue
                                elif self.waiting_function() == "Confirmed":  # Move to the next table if confirmed
                                    i += 1                                 
                                else:
                                    k += 1                              # Handle the case where confirmation is not received
                                    i += 1                             # Move to the next table

                            if k > 0:                                 #if the flag value is <0 then the robot went to kitchen and to home
                                self.navigate_to_place("kitchen")
                                self.navigate_to_place("home")
                            else:                                               
                                self.navigate_to_place("home")
                        else:
                            self.navigate_to_place("home")
        except KeyboardInterrupt:
            print("\nCtrl+C pressed. Exiting...")


            
            
class BatteryStateSubscriber(Node):
    """
    Subscriber node to the current battery state
    """     
    def __init__(self):
   
      super().__init__('battery_state_subscriber')
     
      # Create a subscriber 
      self.subscription_battery_state = self.create_subscription(
        String,
        '/table',
        self.callback,
        10)       
    def callback(self,msg):
        global s,g
        s=True
        g=msg.data
def main(args=None):
  """
  Entry point for the program.
  """
   
  # Initialize the rclpy library
  rclpy.init(args=args)
   
  try: 
    a=Hotel()
    b=BatteryStateSubscriber()
     
    # Set up mulithreading
    executor = MultiThreadedExecutor(num_threads=4)
    executor.add_node(a)
    executor.add_node(b)
    t1=threading.Thread(target=a.table_handle)
    t1.start() 
    try:
      # Spin the nodes to execute the callbacks
      executor.spin()
    finally:
      # Shutdown the nodes
      executor.shutdown()
      connect_to_charging_dock_navigator.destroy_node()
      battery_state_subscriber.destroy_node()
 
  finally:
    # Shutdown
    rclpy.shutdown()

if __name__ == '__main__':
    main()
