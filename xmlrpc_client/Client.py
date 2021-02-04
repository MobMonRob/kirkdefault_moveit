#!/usr/bin/env python

import sys
import xmlrpclib
import copy

import rospy
import moveit_commander
import moveit_msgs.msg
import geometry_msgs.msg
import time
from tf.transformations import quaternion_from_euler
import Cube



moveit_commander.roscpp_initialize(sys.argv)
rospy.init_node('move_group_python_interface_tutorial',
                anonymous=True)


robot = moveit_commander.RobotCommander()
scene = moveit_commander.PlanningSceneInterface()
group = moveit_commander.MoveGroupCommander("right_arm")
display_trajectory_publisher = rospy.Publisher(
                                    '/move_group/display_planned_path',
                                    moveit_msgs.msg.DisplayTrajectory,
                                    queue_size=5)

server_name = 'http://192.168.12.199:8000' #http://192.168.12.199:8000
server = xmlrpclib.ServerProxy(server_name)

pose_target = geometry_msgs.msg.Pose()



#drives the Robot to the predefined default position and sets all necessary flags
def home():

    group.set_named_target("home")
    plan1 = group.plan()
    group.execute(plan1)
    setFlags()


#sets the necessary flags that need to be set after a valid movemen
def setFlags():
    server.setReady(True)
    x = server.increaseTrialnumber()
    server.setPause(True)
    print(" Trialnumber ", x)


#here you can fill in your routine
# using joint goal
#-----------------------
# you can your robot out of a simgularity with joint goals
# e.g. joint_goal = group.get_current_joint_values() # returns an array of all the joint angles, depending on how much joints you have
#      joint_goal[0] = 0
#      joint_goal[1] = -pi/4
#      joint_goal[2] = 0
#      group.go(joint_goal, wait=True)
#      group.stop()         #ensures that there is no residual movement



# setting up your pose_target
# -------------------------------------------------------------
#to drive the eef to a position specified via carthesian coordinates, you have have to do define a pose_target,
# e.g.  pose_target.position.x = your_x_coordinate
#       pose_target.position.y = your_y_coordinate
#       pose_target.position.z = your_z_coordinate
# the values for the positions are in centimeter

#you can also define the eef orientation for a given pose_target by doing the following:
# pose_target.orientation.x = your_x_orientation
# pose_target.orientation.y = your_y_orientation
# pose_target.orientation.z = your_z_orientation
# pose_target.orientation.w = your_w_orientation
# keep in mind that this orientation is given as a quaternion, the method:
# quaternion_from_euler(your_roll_value, your_pitch_value, your_yaw_value)
# can be used to transform your roll_pitch_yaw value into a quaternion, it returns an array where the order is like the pose_target.orientation
# given above (line 59-62)


#cartesian path
#--------------------------
# if you want to drive to move than one carthesian point you may consider making a list of carthesian waypoints
#           e.g.    waypoints = []
#                   wpose = group.get_current_pose().pose
#                   waypoints.append(copy.deepcopy(wpose))
#                   wpose.position.x += scale * 0.1
#                   waypoints.append(copy.deepcopy(wpose))
#                   (plan, fraction) = group.compute_cartesian_path(
#                                       waypoints,   # waypoints to follow
#                                       0.01,        # eef_step
#                                       0.0)         # jump_threshold
# this plan can be executed like the plan you get from a group.plan()




# planning and executing
# ---------------------------------------------------------------
# if you have set a pose_target, you may use the following method:
# group.set_pose_target(your_pose_target)
# this will set the current pose_target to your_pose_target
# with group.plan() , a plan to your_pose_target will be calculated and returned
# with group.execute(your_plan) your plan should be executed.
#
# using a named_target
#---------
# you can use the moveit setup wizard to predefine some poses with joint angles and name those poses.
# if you want to use such a predefined pose you can use the method:
# group.set_named_target(name_of_the_pose), this method does the same as group.set_pose_target(your_pose_target), hence the rest of the execution is the same




def moveRoutine():
    waypoints = []
    # Cube calculates contains all coordinates within the cube and its edges
    cube = Cube.cube(50,50,25,2,2,2,5,5,5)
    wpose = group.get_current_pose().pose
    #all_coordinates is an array of all the coordinates, the coordinates are a tupel in this form: (x_coordinate,y_coordinate, z_coordinate)
    all_coordinates = cube.random_bottom_up_y_axis_accesses()
    previous_y = 0
    current_y = 0
    for i in range(0, len(all_coordinates)):
        if(previous_y != current_y):
            #wait each time a plain is finished
            server.setPause(True)
            while server.getPause() == True:
                print ("waiting at end of plain ", i)
                time.sleep(5)
                pass
        times = 0
        previous_y = current_y
        current_y = all_coordinates[i][1]
        wpose.position.x = all_coordinates[i][0] * 0.01
        wpose.position.y = all_coordinates[i][1] * 0.01
        wpose.position.z = all_coordinates[i][2] * 0.01
        waypoints.append(copy.deepcopy(wpose))
    (plan, fraction) = group.compute_cartesian_path(
        waypoints,  # waypoints to follow
        0.01,  # eef_step
        0.0)  # jump_threshold
    group.execute((plan))


    #alternativly to waypoints an example using pose_targets
    #pose_target.position.x = all_coordinates[i][0] * 0.01
    #pose_target.position.y = all_coordinates[i][1] * 0.01
    #pose_target.position.z = all_coordinates[i][2] * 0.01
    #group.set_pose_target(pose_target)
    #plan = group.plan()
    #group.execute(plan)



#includes a move the home, setting flags, waiting for master, execution of the Routine and setting of flags for next move.
def cycle():
    home()
    server.setPause(True)
    while server.getPause() == True:
        print "waiting at home"
        time.sleep(5)
        pass
    print "starting Routine"
    moveRoutine()
    setFlags()
    print "cycle finished"


def main():

  
    cycle()

    











if __name__ == '__main__':
    main()



