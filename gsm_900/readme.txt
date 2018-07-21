1) Upload the sketch to arduino
2) Build the ros package gsm_900
3) connect the arduino to pc
4) type roslaunch gsm_900 gsm_launch.launch in terminal
5) check rostopic list for gsm_chatter
6) echo to check the msg received 

if no data recieved go to src folder and open the script, change the 
port.

7) approx frequency is .2hz , one msg received in 5s
8) You can see the msg folder containing the msg format.
