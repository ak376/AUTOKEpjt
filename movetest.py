#!/usr/bin/python
from Raspi_MotorHAT import Raspi_MotorHAT, Raspi_DCMotor
from Raspi_PWM_Servo_Driver import PWM


import time
import atexit

# create a default object, no changes to I2C address or frequency
mh = Raspi_MotorHAT(addr=0x6f)

# recommended for auto-disabling motors on shutdown!
def turnOffMotors():
	mh.getMotor(1).run(Raspi_MotorHAT.RELEASE)
	mh.getMotor(2).run(Raspi_MotorHAT.RELEASE)
	mh.getMotor(3).run(Raspi_MotorHAT.RELEASE)
	mh.getMotor(4).run(Raspi_MotorHAT.RELEASE)

atexit.register(turnOffMotors)

################################# DC motor test!
myMotor = mh.getMotor(2)

# set the speed to start, from 0 (off) to 255 (max speed)
myMotor.setSpeed(150)
myMotor.run(Raspi_MotorHAT.FORWARD);
# turn on motor
myMotor.run(Raspi_MotorHAT.RELEASE);


pwm = PWM(0x6F);
pwm.setPWMFreq(60);

# while (True):

# # 앞으로 직진이 backward로 구동
#     print ("mid gogo! ")
#     pwm.setPWM(0, 0, 375)
#     myMotor.run(Raspi_MotorHAT.BACKWARD)

#     print ("\tSpeed up...")
#     for i in range(255):
#         myMotor.setSpeed(i)
#         time.sleep(0.01)

#     print ("\tSlow down...")
#     for i in reversed(range(255)):
#         myMotor.setSpeed(i)
#         time.sleep(0.01)

# #440 이 우회전
#     print ("right gogo! ")
#     pwm.setPWM(0, 0, 440)
#     myMotor.run(Raspi_MotorHAT.BACKWARD)

#     print ("\tSpeed up...")
#     for i in range(255):
#         myMotor.setSpeed(i)
#         time.sleep(0.01)


#     print ("\tSlow down...")
#     for i in reversed(range(255)):
#         myMotor.setSpeed(i)
#         time.sleep(0.01)


# ## 좌회전이 270
#     print ("left gogo! ")
#     pwm.setPWM(0, 0, 270)
#     myMotor.run(Raspi_MotorHAT.BACKWARD)

#     print ("\tSpeed up...")
#     for i in range(255):
#         myMotor.setSpeed(i)
#         time.sleep(0.01)

#     print ("\tSlow down...")
#     for i in reversed(range(255)):
#         myMotor.setSpeed(i)
#         time.sleep(0.01)


    

    
# #뒤로가기가 forward
#     print ("Backward! ")
#     pwm.setPWM(0, 0, 375)
#     myMotor.run(Raspi_MotorHAT.FORWARD)

#     print ("\tSpeed up...")
#     for i in range(255):
#         myMotor.setSpeed(i)
#         time.sleep(0.01)
#     print ("\tSlow down...")
#     for i in reversed(range(255)):
#         myMotor.setSpeed(i)
#         time.sleep(0.01)


#     print ("Release")
#     myMotor.run(Raspi_MotorHAT.RELEASE)
#     time.sleep(1.0)
