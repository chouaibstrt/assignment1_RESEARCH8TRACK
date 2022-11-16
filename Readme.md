
# Python Robotics Simulator  <img src="https://media4.giphy.com/media/dWlLf9EAC8u5Nd0ku4/giphy.gif?cid=ecf05e479junsdcbh0eayqrrx90l4oo4lj83zpqi9yrught2&rid=giphy.gif&ct=s" width="50"></h2>
## First Assignment of the course [Research_Track_1](https://unige.it/en/off.f/2021/ins/51201.html?codcla=10635) , [Robotics Engineering](https://courses.unige.it/10635). 
###  Professor. [Carmine Recchiuto](https://github.com/CarmineD8).

-----------------------

This is a simple, portable robot simulator developed by [Student Robotics](https://studentrobotics.org).

The project aims to make the robot turtle able to sort golden and silver tokens in pairs.Develping the code for this purpose will teach you how to disign an algorithm to let the robot automatically perform a simple task . 




The main difficulties I faced in this project were :

* tuning the robot to finish the task as fast as possible

* find an algorithm that comprimize between being a general solution ,in the same time being very practical to this specific map (tokens orientation)


The robot is able to do this thanks to two motors parallel to each other and the ability to see around itself and recognize in particular golden boxes and silver tokens.

This project introduce me to programing with python in the robotics field.


Installing and running <img src="https://media3.giphy.com/media/LwBuVHh34nnCPWRSzB/giphy.gif?cid=ecf05e47t4j9mb7l8j1vzdc76i2453rexlnv7iye9d4wfdep&rid=giphy.gif&ct=s" width="50"></h2>
-----------------------

The simulator requires a Python 2.7 installation, the [pygame](http://pygame.org/) library, [PyPyBox2D](https://pypi.python.org/pypi/pypybox2d/2.1-r331), and [PyYAML](https://pypi.python.org/pypi/PyYAML/).

Pygame, unfortunately, can be tricky (though [not impossible](http://askubuntu.com/q/312767)) to install in virtual environments. If you are using `pip`, you might try `pip install hg+https://bitbucket.org/pygame/pygame`, or you could use your operating system's package manager. Windows users could use [Portable Python](http://portablepython.com/). PyPyBox2D and PyYAML are more forgiving, and should install just fine using `pip` or `easy_install`.

To run one or more scripts in the simulator, use `run.py`, passing it the file names. 

```bash

$ python run.py assignment.py

```


Robot API
---------

The API for controlling a simulated robot is designed to be as similar as possible to the [SR API][sr-api].

---

<h1 align = "center"> Features </h1>


## Motors ##

The simulated robot has two motors configured for skid steering, connected to a two-output [Motor Board](https://studentrobotics.org/docs/kit/motor_board). The left motor is connected to output `0` and the right motor to output `1`.

The Motor Board API is identical to [that of the SR API](https://studentrobotics.org/docs/programming/sr/motors/), except that motor boards cannot be addressed by serial number. So, to turn on the spot at one quarter of full power, one might write the following:

```python
R.motors[0].m0.power = 25
R.motors[0].m1.power = -25
```

Two main functions have been designed to drive straight and to rotate the robot on its axis:

* `drive(speed , seconds)` : This function gives the robot the ability of move straight for a certain time with a defined speed.

    `Arguments` : 

    * speed : the speed of the motors, that will be equal on each motor in order to move straight.

    * seconds : the time interval in which the robot will move straight.

    This function has no `Returns` .


* `turn(speed , seconds)` : This function gives the robot the ability to turn on its axis.
    
    `Arguments` :

    * speed : the speed of the motors, that will be positive for one and negative for the other in order to make the rotation.

    * seconds : the time interval in which the robot will rotate.
    
    This function has no `Returns` .
    
* `find_silver_token(dist, rot_y)` : This function has been implemented to get closer to the silver token when the robot detects one with its particular visual perception, a feature that I will describe later. At first, the robot checks if it is in the right direction to reach the silver token and if not, it will adapt itself turning left and right. Second, it will call the Routine() function to complete its purpose, take the silver token it saw.

    `Arguments` :
    
    * dist : The distance of the silver token that the robot has detected.
    
    * rot_y : the angle in dregrees of the silver token that the robot has detected 
    
    This function has no `Returns` .
    
    
## The Grabber ##

The robot is equipped with a grabber, capable of picking up a token which is in front of the robot and within 0.4 metres of the robot's centre. To pick up a token, call the `R.grab` method:

```python
success = R.grab()
```

The `R.grab` function returns `True` if a token was successfully picked up, or `False` otherwise. If the robot is already holding a token, it will throw an `AlreadyHoldingSomethingException`.

To drop the token, call the `R.release` method.



## Vision ##

To help the robot find tokens and navigate, each token has markers stuck to it, as does each wall. The `R.see` method returns a list of all the markers the robot can see, as `Marker` objects. The robot can only see markers which it is facing towards.

Each `Marker` object has the following attributes:

* `info`: a `MarkerInfo` object describing the marker itself. Has the following attributes:
  * `code`: the numeric code of the marker.
  * `marker_type`: the type of object the marker is attached to (either `MARKER_TOKEN_GOLD`, `MARKER_TOKEN_SILVER` or `MARKER_ARENA`).
  * `offset`: offset of the numeric code of the marker from the lowest numbered marker of its type. For example, token number 3 has the code 43, but offset 3.
  * `size`: the size that the marker would be in the real game, for compatibility with the SR API.
* `centre`: the location of the marker in polar coordinates, as a `PolarCoord` object. Has the following attributes:
  * `length`: the distance from the centre of the robot to the object (in metres).
  * `rot_y`: rotation about the Y axis in degrees.
* `dist`: an alias for `centre.length`
* `res`: the value of the `res` parameter of `R.see`, for compatibility with the SR API.
* `rot_y`: an alias for `centre.rot_y`
* `timestamp`: the time at which the marker was seen (when `R.see` was called).

For example, the following code lists all of the markers the robot can see:

```python

markers = R.see()
print "I can see", len(markers), "markers:"

for m in markers:
    if m.info.marker_type in (MARKER_TOKEN_GOLD, MARKER_TOKEN_SILVER):
        print " - Token {0} is {1} metres away".format( m.info.offset, m.dist )
    elif m.info.marker_type == MARKER_ARENA:
        print " - Arena marker {0} is {1} metres away".format( m.info.offset, m.dist )
```

Two main functions are designed to recognize the `Marker` object  and whether it is gold or silver. 


* `find_golden_token(dist, rot_y, code)` : This function detects the  golden token facing the robot that has not been detected before (using the data from an array that store the already paired silver token) 

    *  dist = the distance between the center of the robot and the token.
    
    *  rot_y = the angle in degrees between teh robot and the golden token
    


* `find_silver_token()` : This function detects the  silver token facing  the robot in a 140° cone (between -70 ° and 70°) at a maximum distance of 1.2. Furthermore, thanks to the `gold_in_between()` function, the robot ignores the tokens silver behind the walls or that have obstacles that precede them. The main purpose here is to recognise tokens silver to approach.


    *  dist : The distance of the closest silver token, `-1` if no silver tokens are detected or if they are preceded by obstacles (golden boxes).

    *  rot_y : The angle in degrees between the robot and the silver token, `-1` if no silver tokens are detected or if they are preceded by obstacles (golden boxes).




## silver_list and golden_list ##

two lists impleented to store the codes of the tokens already paired,this is essential for thr robot to not grab the same token twice or even continuously.one list store golden token codes and the other list for the silver token codes.

MAIN Function
---------


## peseudocode

while True:
           if the variable  silver is true:

               print"silver token detected"

               find silver_token distance ,rotation and the associated code

           if the silver token already paired:

               turn  right
           else:

                find golden_token distance ,rotation and associated code

                if the golden_token already paired:

                   turn right 

           if dist = -1 :

                          print"i don't see any token"

                           turn clockwise

           elif dist <= d_th:

                               print"found it"

                               if the token is not grabed:

                                    grab the_silver_token

                                    store the code of the silver_token in list 1

                                    print"silver token catched"

                                    declare that you are grabing a token

                                    set the variable silver to false

            else:

                  Release the silver token

                  store the golden token already paired

                  declare that you are nt grabing any token

                  set the silver variable to True

            elif the token is well aligned with the robot:

                                                           go straight forward

            elif the robot is on the left:

                                                           turn right

            elif the robot is on the right:

                                                           turn left
     

 # Results
---------

this video shows the performance of the robot.

https://github.com/chouaibstrt/assignment1_RESEARCH8TRACK/blob/main/test.mp4
------
# discussion :

I focused in my solution to make my system as stable as possible,finishing the task as fast as possible and not crashing the silver_tokens against each other when moving another one. To overcome this chalenges  i spent time tuninig and chosing the speed and the angles suitable to satisfy this specifications.

The project main dificulty is to find a comprimise between a general solution that works for any tokens number and orientation ,in the same time optimize the solution for this specific task.

one of the problems that i faced is when trying to move and turn the robot at maximum speed ,if you move so fast you run into the problem of being not able to align the robot with the token .and somtimes you stuck periodically turning right and left correspending to the line that align the robot and token.this problem is mariginally unstable system from a controle point of view.

Also in my view using a combined movement create more chalenges if we consider a real system specification and dealing with that mathemathically ,require a complex model and it will be out of the scope of the assignment purpose .

# improvement :

1. __always find the nearest token__ : implementig that require the token to turn 360° store every token distance and compute the minimum distance (for our specefic token orientation this will waste more time and decrease efficiency)


2. __time and space complexity__ : I'm not sure if this improvement is feasible but i think that if we have to deal with a very large number of tokens,optimizing run time and the memory space used is vital (iam not sure but  i think in the worst case if we have n tokens ,to optimize the time required to finish the task will grow exponatially "Np hard problems category".

