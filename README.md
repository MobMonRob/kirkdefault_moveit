# sawyer_moveit
This repository is used to controll a robot (tested sawyer and ur_5) with MoveIt!

Right now you can only controll one planning group with this program

To use this Repo you need to have the following ROS, Rviz and Moveit 1 installed.

You will also need a to create a moveit config file for your Robot, or use the default one by the manufacturer.
And test if your moveit installation works by executing roslaunch your_robot_config_file demo.launch
it should open up a Moveit.Rviz window with a simulation of your desired robot.
There you will need to open up the Planning Request tab, and insert the String from Planning group into your Rosparameter server as the parameter 'planning_group'


If you want to use the Program, you will have to do the following:
1.execute "roslaunch your_robot_config_file demo.launch"   (or any other .launch file, the important thing is that we have our robot simulation up and running)
2.settup all parameters in your Rosparam server, a list of all param is listed below
3.execute the Client.py

You'll have to set more parameters in your Rosparam server. Otherwise there will be used a default value. A complete list of all parameters will be listed here:
  1. planning_group, the planning group that you want to control wih moveit. The Default Value is 'ur_arm'.
  2. server_name, the IP address of your xmlrpc server. The Default value is localhost.
 
 The Following parameters are for the cube, The cube is defined by carthesian start coordinates, an amount of steps in each direction and a step size for each direction. 
 Through that the cube is a grid of coordinates, the programm will drive from the bottom up to every y-plain and drive in every plain to a random permutation of all points within   the plain. 
 
    1. start_x the starting coordinate for x
    2. start_y the starting coordinate for y
    3. start_z the starting coordinate for z
    4. step_x the step size of the x-Axis
    5. step_y the step size of the y-Axis
    6. step_z the step size of the z-Axis
    7. step_amount_x the amount of steps taken into x direction, if set to 1 we will have the x values: x_0 = start_x, x_1 = start_x + step_x
    8. step_amount_y the amount of steps taken into y direction
    9. step_amount_z the amount of steps taken into z direction

The following parameters are necessary to decide if you want to use the carthesian grid or different joint_torques to drive the robot 
   1. cube_or_joints, set to 0 the program will use the carthesian grid. Default is 0 
   2. sleep time, minimal waiting time between steps
   3. default_pose, the name of your default pose. Default is 'home'
    

    


