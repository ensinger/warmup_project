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

  - the gif for this is !(draw_square.gif)

