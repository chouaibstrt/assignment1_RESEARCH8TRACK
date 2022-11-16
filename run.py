from __future__ import print_function

import time
from sr.robot import *




a_th = 2.0
""" float: Threshold for the control of the linear distance"""

d_th = 0.49
""" float: Threshold for the control of the orientation"""

silver = True
""" boolean: variable for letting the robot know if it has to look for a silver or for a golden marker"""

R = Robot()
""" instance of the class Robot"""

def drive(speed, seconds):
    """
    Function for setting a linear velocity
    
    Args: speed (int): the speed of the wheels
	  seconds (int): the time interval
    """
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0

def turn(speed, seconds):
    """
    Function for setting an angular velocity
    
    Args: speed (int): the speed of the wheels
	  seconds (int): the time interval
    """
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = -speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0

def find_silver_token():
    """
    Function to find the  silver token
    Returns:
	dist (float): distance of the closest silver token (-1 if no silver token is detected)
	rot_y (float): angle between the robot and the silver token (-1 if no silver token is detected)
    """
    dist=100
    for token in R.see():
        #  check for ingoring token already in the list of the grabbed token
        if token.dist < dist and token.info.marker_type is MARKER_TOKEN_SILVER and not(token in silver_list):
            dist=token.dist
            code = token.info.code # added to store also the closest token code
            rot_y=token.rot_y
    if dist==100:
        return -1, -1, -1
    else:
        return dist, rot_y, code # added to return also the closest token code

def find_golden_token():
    """
    Function to find the  golden token
    Returns:
	dist (float): distance of the closest golden token (-1 if no golden token is detected)
	rot_y (float): angle between the robot and the golden token (-1 if no golden token is detected)
    """
    dist=100
    for token in R.see():
        # added additional check for skipping token already in the list of the sorted with a silver token 
        if token.dist < dist and (token.info.marker_type is MARKER_TOKEN_GOLD) and not(token in gold_list):
            dist=token.dist
            code = token.info.code # added to store also the closest token code
            rot_y=token.rot_y
    if dist==100:
        return -1, -1, -1
    else:
        return dist, rot_y, code # added to return also the closest token code

# added flag for differentiate the cycle for grabbing a silver token or
# releasing close to a golden token
grab = False
# added two lists for keeping track of the already grabbed silver token and
# of the already sorted golden token with a silver token
gold_list = []
silver_list = []

while 1:
    if silver == True: # if silver is True, than we look for a silver token, otherwise for a golden one
        print("yes")
        dist, rot_y, code_silver = find_silver_token()
        if  code_silver in silver_list:                      # the robot turn if the token already in the silver_list
            turn(+10, 0.1)
    else:
        dist, rot_y, code = find_golden_token()
        if  code in gold_list: # if the token code is  already in the list,the robot turn
           turn(10, 0.1)
    if dist==-1: # if no token is detected, we make the robot turn 
        print("I don't see any token!!")
        turn(+10, 0.4)
    elif dist <= d_th: # if we are close to the token.
        print("Found it!")
        if not grab and find_silver_token(): # to make sure that we grab a silver token and not grabbed already
            R.grab()
            silver_list.append(code_silver) #update the silver_list
            print("silver token catched!")
            dist, rot_y, code = find_golden_token()
            # look for the not paired golden token
            grab = True
            silver = not silver
        else:
            R.release()
            gold_list.append(code) # update the golden_list with the already paired golden token
            print("yes")
            drive(-80, 0.25)
            turn(60, 1)
            grab = False
            silver = True

    elif -a_th<= rot_y <= a_th: # if the robot is well aligned with the token, we go forward
        print("Ah, that'll do.")
        drive(80, 0.3)
    elif rot_y < -a_th: # if the robot is not well aligned with the token, we move it on the left or on the right
        print("Left a bit...")
        turn(-5, 0.1)
    elif rot_y > a_th:
        print("Right a bit...")
        turn(+5, 0.1)