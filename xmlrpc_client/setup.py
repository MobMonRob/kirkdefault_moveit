import os

import rospy


def main():
    if rospy.has_param('planning_group'):
        planning_group = rospy.get_param('planning_group')
    else:
        planning_group = 'ur_arm'

    if rospy.has_param('server_name'):
        server_name = rospy.get_param('server_name')
    else:
        server_name = 'http://localhost:8000'

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

    if rospy.has_param('cube_or_joints'):
        cube_or_joints = rospy.get_param('cube_or_joints')
    else:
        cube_or_joints = 0

    if rospy.has_param('all_joint_torque'):
        all_joint_torque = rospy.get_param('all_joint_torque')
    else:
        all_joint_torque = False


    all_parameters = str(planning_group) + " "+ str(server_name) +" "+ str(start_x) + " " + str(start_y) + " " + str(start_z) + " " + str(step_x) + " " + str(step_y) + " " + str(step_z) + " " + str(step_amount_x) + " " + str(step_amount_y) + " " + str(step_amount_z) + " " + str(sleep_time) + " " +str(default_pose) + " " + str(cube_or_joints)
    os.system("python Client.py " + all_parameters)

if __name__ == '__main__':
    main()