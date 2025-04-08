Zip file including all files. (largely working, just patching bugs 3:15, 4/8)

Steps:
First Open 2 terminals

Terminal 1:
1) ros2 launch turtlebot3_gazebo empty_world.launch.py headless:=true


Terminal 2:
1) colcon build --packages-select turtlebot_waypoints random_goal
2) source install/setup.bash
3) ros2 run turtlebot_waypoints random_goal

