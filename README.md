# warmup_project
# git fork and clone

# Draw square script
in order to make the robot move in a square, I decided to make it move foward
and then turn left, and repeat this process forever. this way it will make a
square

Using the example code from class, I setup a publisher for moving the robot
I made a class for drawSquare
  - in this class, there is an init, which initializes the node
  - there is a publisher for publishing the twist commands to move the turtlebot
  - I set the update rate to be 10 Hz
  - I created a default twist instance to move forward and one to turn left
  - the forward twist moves in the x direction and .25 m/s
  - the left rotates about the z axis at 90 degrees per sec
  - I initialized a turn counter
  - I made a while loop that continued until shutdown
      - in the while loop:
      	- I move forward for 40 cycles (4 seconds or 1 meter) by publishing the
	  moveForward msg
	- I stop the robot 
	- I turn left for 10 updates or 1 second by publishing the turn msg
	- I stop the robot
	- log the number of turns and increment the turn counter
  - the run function just does rospy.spin
  - the shutdown function logs that it is stopping and sleeps for 1 sec
  - the skeleton for the program is from the stop at wall in slack.

  - challenges included not having a skeleton for the project. I had trouble
  knowing how to structure the script until the Pouya put the class exmaple in slack
  
  - I had some challenges getting the whole computing setup to work the first time
  - I still have not figured out rosbags or gifs yet

  - the robot drifts over time, so I would like to figure out where it is pointing
  and better control the turns to be exactly 90 degrees and the moves to be exactly
  the same distance.

  - I had trouble getting the rosbag to upload in git at first. It created a 400MB
    file. I had to clear out the workspace, and reclone, and restore to undo the
    bit commit.

  - the gif for this is ![](draw_square.gif)

# wall_follower.py A Wall Following rospy program

The structure of my wall follower is to have a subscriber for the scan
that receives LaserScanner data objects and responds with a
process_scan function. There are 3 states of the program:
1. goto wall
2. turn left
3. follow the wall
These states govern which subfunction is called from the process_scan
function. The basic idea is to find the first wall, turn enough that
the wall is on the right hand side of the robot, then keep the wall
roughly parallel to the robot as it moves fowrad to the next wall. It
then will again turn left, and repeat the process. These functions are
specified more below.

## goto_wall
The goto_wall function moves the robot to the first wall and stops at
the specified distance. This is done by taking the zero value of the
LidarScanner data in data.ranges and checks to see if it is greater
than the desired distance. If it is too far away, drive continues
towards the wall by setting the velocity of the twist object to the speed variable. Otherwise, it
stops by setting my velocity to 0. 

## turn_left
The turn left function has the robot turn left to re-adjust so that it
is in position to follow the wall to its right. It does this by turning
counterclockwise while checking the distance to the wall in front by checking
the zero value of the LidarScanner data in data.ranges. It checks to
see if it is less than 4 times the distance variable, which means that
the robot has rotated by more than about 60 degres and can start to
follow the wall. If it is too close to the wall, it turns left until
by setting the angular velocity on the twist object to rotspeed, which
is published by main process_scan function. Once sufficient rotation
has been achieved, the rotation is stopped and the state is changed to
the wall follower state.  

## follow_wall
The follow_wall function has the robot determine if it is far enough
from the wall in front of it by making sure the zero value in
data.ranges is greater than the desired distance from the wall. Then,
it takes a 90 degree section to the right of the robot and makes sure
that the edges of that first value and last value are both equally
distant from the wall. If they are not, the robot needs to readjust to
be parallel with the wall. It does this by 
taking that difference as an error signal that is used in proportional
feedback for the rotational speed of the robot, while it progresses
foward toward the next wall. At the same time, the Lidar data is
checked to determine if it is too close or too far to the wall at the
point directly to the right of the robot and responding with
proportional feedback either  turning towards or away from the wall with a rotational speed
proportional to the size of the err. Since both of these errors have
the effect of positioning the robot parallel to the wall and at the
right distance from the wall, and their signs align, then when hte
robot is too far from the wall, or pointing away from the wall, the
error is negative, making the robot turn toward the wall. If the robot
is too close to the wall, or pointing toward it, then the error is
positive, making the feedback turn the robot from the wall. This
process continues until the robot sees another wall directly in front
of it at lidardata location 0. then it will stop, and switch states to
turn left again.

## process_scan
The process_scan function looks determines which state the robot is in
as described above and then publishes the data to the correct function
for handeling what must happen according to the state the robot is in.

[The robot running wall_follow.py] ![](wall_follower.gif)

##Challenges
The biggest challenges were figuring out how to
1. read the lidar data
2. find an error signal for proportional feedback to follow the wall
3. make the control stable, and not go out of control.
Reading the Lidar data was overcome by reading some resources  and
looking at the example from class. The error signal was hard to find
that was stable. I first tried just the distance from the wall, but
this would only work sometimes. Looking at the drawing in the class
webpage, the three vectors shown gave me the idea to check at the
side, and 45 degrees in front and behind the robot. This took a long
time to figure out. Making it stable just took some fiddling with the
speeds to find something that worked well.

##Future Work
If I had more time, I would maybe try to implement PID control, with
proportional, integral and derivative feedback, I would also try to
make some other walls to follow.

##Takeaways
- proportional feedback works well once you find the right error
This took some time to figure out but once I got a good error signal,
it was pretty stable. It was helpful to have the class example
from a controller with lidar data for stopping. Scaling the error took
some trial and error.
- It takes some time to figure out the rospy interaction
It took some time to figure out how to fix errors like objects and
number of arguments to functions in rospy. This took some research  and
some guessing based on the error. 
- Some more coding examples would help future students
In some other courses, like computers for learning which was an
introduction to building video games, we had
code examples that gave the overall structure. Over time, we had to
make the skeletons ourselves. This was **really** helpful. Some more
coding examples would be helpful.
