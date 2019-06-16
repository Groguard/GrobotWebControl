import board
import busio
import adafruit_pca9685
import adafruit_motor.servo
import time
import sys
import os

from flask import Flask, render_template, request, redirect, url_for, flash, Response
app = Flask(__name__)


# Initialize I2C
i2c = busio.I2C(board.SCL, board.SDA)

# Initialize I2C PWM Controller
pca = adafruit_pca9685.PCA9685(i2c)

# Set PWM Controller Frequency
pca.frequency = 60

# Servo Assignments
RightRearHip = adafruit_motor.servo.Servo(pca.channels[0])
RightRearFoot = adafruit_motor.servo.Servo(pca.channels[1])

RightFrontHip = adafruit_motor.servo.Servo(pca.channels[2])
RightFrontFoot = adafruit_motor.servo.Servo(pca.channels[3])

LeftFrontFoot = adafruit_motor.servo.Servo(pca.channels[4])
LeftFrontHip = adafruit_motor.servo.Servo(pca.channels[5])

LeftRearFoot = adafruit_motor.servo.Servo(pca.channels[6])
LeftRearHip  = adafruit_motor.servo.Servo(pca.channels[7])

# Servo delay to control the "Speed"
delay = 0.01 

sitting_status = 1

@app.route('/')
def json():
	return render_template('index.html')


@app.route('/actions')
def actions():
	# Get the current action of the button
	action = request.args.get('action')

	if(action == "forward"):
		print('Moving Forward', file=sys.stdout)
		walk_forward_smooth()
		
	if(action == "reverse"):
		print('Moving Reverse', file=sys.stdout)
		walk_backward_smooth()
		
	if(action == "rotate_right"):
		print('Rotating Right', file=sys.stdout)
		rotate_right()
		
	if(action == "rotate_left"):
		print('Rotating Left', file=sys.stdout)
		rotate_left()

	if(action == "sit"):
		print('Sitting', file=sys.stdout)
		zero_servos_smooth()

	if(action == "stand_up"):
		print('Standing Up', file=sys.stdout)
		stand_up_half_smooth()
		
	if(action == "wave"):
		print('Waving', file=sys.stdout)
		wave()
		
	if(action == "enable_servos"):
		print('Enabling Servos', file=sys.stdout)
		enable_all_servos()
		
	if(action == "disable_servos"):
		print('Disabling Servos', file=sys.stdout)
		disable_all_servos()
		
	if(action == "poweroff"):
		os.system("sudo poweroff")

	return ""


def stand_up_half():
	LeftFrontFoot.angle = 90
	RightFrontFoot.angle = 90

	LeftRearFoot.angle = 90
	RightRearFoot.angle = 90

def zero_servos():
	RightRearFoot.angle = 180 # Up
	time.sleep(1)
	RightRearHip.angle = 90
	time.sleep(1)
	
	LeftRearFoot.angle = 0 # up
	time.sleep(1)
	LeftRearHip.angle = 90
	time.sleep(1)

	RightFrontFoot.angle = 0 # up
	time.sleep(1)
	RightFrontHip.angle = 90
	time.sleep(1)

	LeftFrontFoot.angle = 180 # up
	time.sleep(1)
	LeftFrontHip.angle = 90
	time.sleep(1) 
	
	sitting_status = 1
	
def set_servo(Servo, SetAngle):

	CurrentAngle = round(Servo.angle)
		
	if(CurrentAngle < SetAngle):
		for angle in range(CurrentAngle, SetAngle, 5):
			Servo.angle = angle
			time.sleep(delay)
	if(CurrentAngle > SetAngle):
		for angle in range(CurrentAngle, SetAngle, -5):
			Servo.angle = angle
			time.sleep(delay)


def stand_up_half_smooth():
	set_servo(RightFrontHip, 45)
	set_servo(RightFrontFoot, 90)
	
	set_servo(LeftRearHip, 45)
	set_servo(LeftRearFoot, 90)
	
	set_servo(LeftFrontHip, 135)
	set_servo(LeftFrontFoot, 90)
	
	set_servo(RightRearHip, 135)
	set_servo(RightRearFoot, 90)
	
	sitting_status = 0

	
def stand_up_full_smooth():
	set_servo(LeftFrontFoot, 0)
	set_servo(RightFrontFoot, 180)
	set_servo(LeftRearFoot, 180)
	set_servo(RightRearFoot, 0)


def zero_servos_smooth():
	set_servo(RightRearFoot, 180)
	set_servo(RightRearHip, 90)
	
	set_servo(LeftFrontFoot, 180)
	set_servo(LeftFrontHip, 90)

	set_servo(RightFrontFoot, 0)
	set_servo(RightFrontHip, 90)
	
	set_servo(LeftRearFoot, 0)
	set_servo(LeftRearHip, 90)

def wave():
	set_servo(RightFrontHip, 45)
	set_servo(RightFrontFoot, 90)
	
	set_servo(LeftRearHip, 45)
	set_servo(LeftRearFoot, 90)
	
	set_servo(LeftFrontHip, 135)
	set_servo(LeftFrontFoot, 90)
	
	set_servo(RightRearHip, 135)
	set_servo(RightRearFoot, 90)
	
	set_servo(RightFrontFoot, 0) # Foot Up
	set_servo(RightFrontHip, 20) # Hip Forward
	set_servo(RightFrontFoot, 20) # Foot down
	set_servo(RightFrontHip, 90) # Hip Back
	set_servo(RightFrontFoot, 0) # Foot Up
	set_servo(RightFrontHip, 20) # Hip Forward
	set_servo(RightFrontFoot, 90)# Foot Down
	
def rotate_right():
	
	if sitting_status == 1:
		stand_up_half_smooth()
		
	# First Shift
	set_servo(RightFrontFoot, 50) # Foot Up
	set_servo(LeftRearFoot, 50) # Foot Up
	
	set_servo(LeftRearHip, 90) # Hip Middle
	set_servo(RightFrontHip, 90)# Hip Middle
	
	set_servo(RightFrontFoot, 90) # Foot Down
	set_servo(LeftRearFoot, 90) # Foot Down
	
	# Second Shift
	set_servo(LeftFrontFoot, 130) # Foot Up
	set_servo(RightRearFoot, 130) # Foot Up
	
	set_servo(RightFrontHip, 20)# Hip Forward
	set_servo(LeftRearHip, 20) # Hip Back
	
	set_servo(LeftFrontHip, 180) # Hip Foward
	set_servo(RightRearHip, 180) # Hip Back
	
	set_servo(LeftFrontFoot, 90) # Foot Down
	set_servo(RightRearFoot, 90) # Foot Down
	
	# Third Shift
	set_servo(RightFrontFoot, 50) # Foot Up
	set_servo(LeftRearFoot, 50) # Foot Up
	
	set_servo(LeftFrontHip, 135) # Hip Forward
	set_servo(RightRearHip, 135) # Hip Back
	
	set_servo(RightFrontFoot, 90) # Foot Down
	set_servo(LeftRearFoot, 90) # Foot Down

def rotate_left():
	
	if sitting_status == 1:
		stand_up_half_smooth()
	
	# First Shift
	set_servo(LeftFrontFoot, 130) # Foot Up
	set_servo(RightRearFoot, 130) # Foot Up
	
	set_servo(LeftFrontHip, 90) # Hip Middle
	set_servo(RightRearHip, 90) # Hip Middle
	
	set_servo(LeftFrontFoot, 90) # Foot Down
	set_servo(RightRearFoot, 90) # Foot Down
	
	# Second Shift
	set_servo(RightFrontFoot, 50) # Foot Up
	set_servo(LeftRearFoot, 50) # Foot Up
	
	set_servo(LeftFrontHip, 160) # Hip Back
	set_servo(RightRearHip, 160) # Hip Forward
	
	set_servo(RightFrontHip, 0) # Hip Back
	set_servo(LeftRearHip, 0) # Hip Forward
	
	set_servo(RightFrontFoot, 90) # Foot Down
	set_servo(LeftRearFoot, 90) # Foot Down
	
	# Third Shift
	set_servo(LeftFrontFoot, 130) # Foot Up
	set_servo(RightRearFoot, 130) # Foot Up
	
	set_servo(RightFrontHip, 20) # Hip Forward
	set_servo(LeftRearHip, 20) # Hip Back
	
	set_servo(LeftFrontFoot, 90) # Foot Down
	set_servo(RightRearFoot, 90) # Foot Down
		
def walk_forward_smooth():
	
	if sitting_status == 1:
		stand_up_half_smooth()
	
	# First Step
	set_servo(RightFrontFoot, 50) # Foot Up
	set_servo(RightFrontHip, 20) # Hip Forward
	set_servo(RightFrontFoot, 90)# Foot Down
	
	# Shift 1
	set_servo(RightRearHip, 135)
	set_servo(RightFrontHip, 45)
	set_servo(LeftFrontHip, 85)
	set_servo(LeftRearHip, 20)
	
	# Step 2
	set_servo(LeftRearFoot, 50) # Foot Up
	set_servo(LeftRearHip, 95) # Hip Foward
	set_servo(LeftRearFoot, 90) # Foot Down

	# Step 3
	set_servo(LeftFrontFoot, 130) # Foot Up
	set_servo(LeftFrontHip, 160) # Hip Foward
	set_servo(LeftFrontFoot, 90) # Foot Down
	
	# Shift 2
	set_servo(RightRearHip, 160)
	set_servo(RightFrontHip, 95)
	set_servo(LeftFrontHip, 135)
	set_servo(LeftRearHip, 45)
	
	# Step 4
	set_servo(RightRearFoot, 130) # Foot Up
	set_servo(RightRearHip, 85) # Hip Forward
	set_servo(RightRearFoot, 90) # Foot Down
	
def walk_backward_smooth():
	
	if sitting_status == 1:
		stand_up_half_smooth()
	
	# First Step
	set_servo(LeftRearFoot, 50) # Foot Up
	set_servo(LeftRearHip, 20) # Hip Forward
	set_servo(LeftRearFoot, 90)# Foot Down
	
	# Shift 1
	set_servo(LeftFrontHip, 135)
	set_servo(LeftRearHip, 45)
	set_servo(RightRearHip, 85)
	set_servo(RightFrontHip, 20)
	
	# Step 2
	set_servo(RightFrontFoot, 50) # Foot Up
	set_servo(RightFrontHip, 95) # Hip Foward
	set_servo(RightFrontFoot, 90) # Foot Down

	# Step 3
	set_servo(RightRearFoot, 130) # Foot Up
	set_servo(RightRearHip, 160) # Hip Foward
	set_servo(RightRearFoot, 90) # Foot Down
	
	# Shift 2
	set_servo(LeftFrontHip, 160)
	set_servo(LeftRearHip, 95)
	set_servo(RightRearHip, 135)
	set_servo(RightFrontHip, 45)
	
	# Step 4
	set_servo(LeftFrontFoot, 130) # Foot Up
	set_servo(LeftFrontHip, 85) # Hip Forward
	set_servo(LeftFrontFoot, 90) # Foot Down
	
def enable_all_servos():
	RightRearFoot.set_pulse_width_range(750, 2250)
	RightRearHip.set_pulse_width_range(750, 2250)

	LeftRearFoot.set_pulse_width_range(750, 2250)
	LeftRearHip.set_pulse_width_range(750, 2250)

	RightFrontFoot.set_pulse_width_range(750, 2250)
	RightFrontHip.set_pulse_width_range(750, 2250)

	LeftFrontFoot.set_pulse_width_range(750, 2250)
	LeftFrontHip.set_pulse_width_range(750, 2250)

def disable_all_servos():
	RightRearFoot.set_pulse_width_range(0, 0)
	RightRearHip.set_pulse_width_range(0, 0)

	LeftRearFoot.set_pulse_width_range(0, 0)
	LeftRearHip.set_pulse_width_range(0, 0)

	RightFrontFoot.set_pulse_width_range(0, 0)
	RightFrontHip.set_pulse_width_range(0, 0)

	LeftFrontFoot.set_pulse_width_range(0, 0)
	LeftFrontHip.set_pulse_width_range(0, 0)
	
def initialize_bot():
	zero_servos()

if __name__ == '__main__':
	initialize_bot()
	app.run(host='0.0.0.0', debug=True)
