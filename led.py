#simple loop to toggle LED on and off forever

import time
import math


MajorPeriod = 1
MinorPeriod = .5
LED = 6004

#Initilize Labjack
import u3
Device = u3.U3(autoOpen = False)

# LED state: null = false = led off
State = ()

#set an initial Target time for first iteration and round up to a whole second
Target = math.ceil(time.time())

while 1 != 0:

	Start = time.time()

	#calculate time to sleep 
	NapTime = MajorPeriod/MinorPeriod

	# round Target up to nearest even time
	Overplus = Target % MajorPeriod
	if Overplus != 0:
		Target = Target + ( MajorPeriod - Overplus )

	if Start >= Target:

		Target = Target + MajorPeriod

		#initialize labjack on each loop
		Device.open()

		#flip current state
		State = not State
		print "LED is %s" % State

		#toggle the LED
		Device.writeRegister(LED, State)

		#close the labjack on eachloop
		Device.close()

	else:
		Remainder = Target - Start

		if Remainder < NapTime:
			time.sleep(Remainder)

		else:

			#Minor Period
			#preforms actions?

			time.sleep(NapTime)
