# hotel_task                                                                                                                                                                                                                                       
mkdir -p ~/ros2_ws/src                #create a workspace                                                                                                                                                                                           
cd ~/ros2_ws/src                      #change the directory to src                                                                                                                                                                          
git clone https://github.com/barathan-mr/hotel_task.git         #clone the repository to the source folder                                                                                                                                         
colcon build                           #build the workspace                                                                                                                                                                                      
source install/setup.bash              #source the workspace


TO LAUNCH THE TASK RUN THE FOLLOWING COMMANDS:                                                                                                                                                                                                  
ros2 launch neuronbot2_gazebo neuronbot2_world.launch.py          #run the command to launch the gaebo world and spawn the urdf                                                                                                                 
ros2 launch neuronbot2_nav localization_launch.py                 #run the command to launch localization                                                                                                                                        
ros2 launch neuronbot2_nav navigation_launch.py                   #run the comand to launch navigation                                                                                                                                           
ros2 launch neuronbot2_nav rviz_view_launch.py                    #run the command to launch rviz                                                                                                                                               

ros2 run hotel_package goal                                       #run the following command to run the task                                                                                                                                     
                                                                                                                                                                                                                                                  
TO CANCEL THE TABLE                                                                                                                                                                                                                             
ros2 topic pub --once /table std_msgs/msg/String data:\ \'table1\'\          #TO CANCE THE TABLE PASS THE TABLE NAME AS ARGUEMENT                                                                                                                                                  
