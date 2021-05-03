#!/usr/bin/env python

import sys
import xmlrpclib
import copy

import rospy
import moveit_commander
import moveit_msgs.msg
import geometry_msgs.msg
import time
from math import pi
from tf.transformations import quaternion_from_euler
import Cube



moveit_commander.roscpp_initialize(sys.argv)
rospy.init_node('moveit_python_application',
                anonymous=True)


robot = moveit_commander.RobotCommander()
scene = moveit_commander.PlanningSceneInterface()


##it is important that you have the correct planning group, you find the correct planning group in the running moveit.rviz application
if rospy.has_param('planning_group'):
    planning_group = rospy.get_param('planning_group')
else:
    planning_group = 'ur_arm'
group = moveit_commander.MoveGroupCommander(planning_group)
display_trajectory_publisher = rospy.Publisher(
                                    '/move_group/display_planned_path',
                                    moveit_msgs.msg.DisplayTrajectory,
                                    queue_size=5)

pose_target = geometry_msgs.msg.Pose()

if rospy.has_param('server_name'):
    server_name = rospy.get_param('server_name')
else:
    server_name = 'http://localhost:8000' #http://192.168.12.199:8000
server = xmlrpclib.ServerProxy(server_name)



if rospy.has_param('start_x'):
    start_x = rospy.get_param('start_x')
else:
    start_x = 50

if rospy.has_param('start_y'):
    start_y = rospy.get_param('start_y')
else:
    start_y = 50

if rospy.has_param('start_z'):
    start_z = rospy.get_param('start_z')
else:
    start_z = 50

if rospy.has_param('step_x'):
    step_x = rospy.get_param('step_x')
else:
    step_x = 2

if rospy.has_param('step_y'):
    step_y = rospy.get_param('step_y')
else:
    step_y = 2

if rospy.has_param('step_z'):
    step_z = rospy.get_param('step_z')
else:
    step_z = 2

if rospy.has_param('step_amount_x'):
    step_amount_x = rospy.get_param('step_amount_x')
else:
    step_amount_x = 2

if rospy.has_param('step_amount_y'):
    step_amount_y = rospy.get_param('step_amount_y')
else:
    step_amount_y = 2

if rospy.has_param('step_amount_z'):
    step_amount_z = rospy.get_param('step_amount_z')
else:
    step_amount_z = 2

if rospy.has_param('sleep_time'):
    sleep_time = rospy.get_param('sleep_time')
else:
    sleep_time = 5

if rospy.has_param('default_pose'):
    default_pose = rospy.get_param('default_pose')
else:
    default_pose = 'home'


#this param decides if we are driving to a carthesian defined cube or to a bunch of joints_states
# if cube_or_joints = 0, the carthesian defined cube will be used
# otherwise the bunch of joint_states will be used
if rospy.has_param('cube_or_joints'):
    cube_or_joints = rospy.get_param('cube_or_joints')
else:
    cube_or_joints = 0

if rospy.has_param('all_joint_torque'):
    all_joint_torque = rospy.get_param('all_joint_torque')
else:
    all_joint_torque = False

#drives the Robot to the predefined default position and sets all necessary flags
def home():

    group.set_named_target(default_pose) #changed to "home" to "zero_pose" due to complications in urdf
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




def moveRoutine(cube):

    # Cube calculates contains all coordinates within the cube and its edges
    pose_target = geometry_msgs.msg.Pose()

    #all_coordinates is an array of all the coordinates, the coordinates are a tupel in this form: (x_coordinate,y_coordinate, z_coordinate)
    all_coordinates = cube.random_bottom_up_y_axis_accesses()
    previous_y = 0
    current_y = 0

    for i in range(0, len(all_coordinates)):

        if(previous_y != current_y):
            server.setPause(True)
            while server.getPause() == True:
                print ("waiting at end of plain ", i)
                #all_parameters[9] keeps the sleep time
                time.sleep(sleep_time)
            #wait each time a plain is finished

        previous_y = current_y
        current_y = all_coordinates[i][1]
        pose_target.position.x = all_coordinates[i][0] * 0.01
        pose_target.position.y = all_coordinates[i][1] * 0.01
        pose_target.position.z = all_coordinates[i][2] * 0.01
        group.set_pose_target(pose_target)
        plan = group.plan()
        group.execute(plan)
        server.setPause(True)



    #alternativly to waypoints
    #pose_target.position.x = all_coordinates[i][0] * 0.01
    #pose_target.position.y = all_coordinates[i][1] * 0.01
    #pose_target.position.z = all_coordinates[i][2] * 0.01
    #group.set_pose_target(pose_target)
    #plan = group.plan()
    #group.execute(plan)


# give an Array with the length of 6, containing different joint configurations(joint angle ? oder einfach Gelenkwinkel)
# the methods checks if the xmlrpc server is paused, and drives to the next configuration if it isn't
def joint_based_move_Routine(all_joint_torque):

    for joint_torque in all_joint_torque:
        server.setPause(True)
        while server.getPause() == True:
            print "to move to next configuration, which is", joint_torque
            time.sleep(sleep_time)
        go_to_joint_state(joint_torque)

def go_to_joint_state(joint_torque):
    #UR has 6 joints
    joint_goal = group.get_current_joint_values()
    print len(joint_goal), "length of joint goal "
    for i in range(0, len(joint_goal)):
        joint_goal[i] = joint_torque[i]

    group.set_joint_value_target(joint_goal)
    plan = group.plan()
    group.execute(plan)

    group.stop()




#includes a move the home, setting flags, waiting for master, execution of the Routine and setting of flags for next move.
#this method includes a full cycle, it needs the positions
def cycle():
    home()
    server.setPause(True)
    while server.getPause() == True:
        print "waiting at home"
        time.sleep(sleep_time)
        pass
    print "starting Routine"

    if cube_or_joints == 0:
        cube = Cube.cube(start_x, start_y, start_z, step_x, step_y, step_z, step_amount_x, step_amount_y, step_amount_z)
        moveRoutine(cube)
    else:
        if(all_joint_torque):
            go_to_joint_state(all_joint_torque)
        else:
            print "Error, 'all_joint_torque is not defined in the rosparam server but you want to use the joint_states, " \
                  "please define all_joint_torque in the rosparam server ! or change the cube_or_joints param to use the carthesian " \
                  "cube "
    setFlags()
    print "cycle finished"


def main():
    cycle()

if __name__ == '__main__':
    main()


