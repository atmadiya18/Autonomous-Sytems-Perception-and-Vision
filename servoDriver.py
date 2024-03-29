#!/usr/bin/env python3

import rospy
from gpiozero.pins.pigpio import PiGPIOFactory
from gpiozero.pins.native import NativeFactory
from gpiozero import Device, Servo
from aut_sys.msg import servos

class servoDrive:

    def __init__(self):
      #Device.pin_factory = PiGPIOFactory()
      self.pan = Servo(4,min_pulse_width=1/1000,max_pulse_width=2/1000)
      self.tilt = Servo(25,min_pulse_width=1/1000,max_pulse_width=2/1000)
      # Initialize the servos to an inactive state
      self.pan.value = None
      self.tilt.value = None
      self.rcvd_val = False

    def init_app(self):
      #create the node and subscribe
      rospy.Subscriber('servos',servos,self.__servoUpdate_cbk)
      rospy.init_node('servoDriver',anonymous=True)
      self.rate = rospy.Rate(10)

    def __servoUpdate_cbk(self,data):
      self.pan.value = data.pan
      self.tilt.value = data.tilt
      self.rcvd_val = True
    #as named...
    def main(self):
        ctr = 0
        while not rospy.is_shutdown():
                #read from the sensor
                if self.rcvd_val == True:
                        ctr = ctr + 1
                        if ctr >= 2:
                                self.rcvd = False
                                ctr = 0
                                self.pan.value = None
                                self.tilt.value = None
                self.rate.sleep()

if __name__ == '__main__':
  try:
    s = servoDrive()
    s.init_app()
    s.main()
  except KeyboardInterrupt:
    pass
