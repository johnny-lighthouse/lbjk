#simple loop to toggle LED on and off forever

import time
import math

#Initilize Labjack
import u3

#set output channel on Labjack
LED = 6004

# LED state: null = false = led off
State = ()

#set an initial Target time for first iteration and round up to a whole second
Target = math.ceil(time.time())   
 
while 1 != 0:
 
	#
	#set Periods in seconds and derive implications
	#
	MajorPeriod = 1
	MinorPeriod = .5
 
	NapTime = float(MajorPeriod)/float(MinorPeriod)
 
	# round Target up to nearest even time
	Overplus = Target % MajorPeriod
	if Overplus != 0:
		Target = Target + ( MajorPeriod - Overplus )
 

	#
	# compare current time to Target and act accordingly.
	#
	Start = time.time()
 
	if Start >= Target:

		#MajorPeriod

                Target = Target + MajorPeriod
                print '@ %f seconds from epoch:' % Start

		#initialize labjack on each loop
		Device = u3.U3()

		#flip current state
		State = not State
		print 'LED is %i ' % State

		#toggle the LED
		Device.writeRegister(LED, State)
		
		#close the labjack on eachloop
		Device.close
 
	else:
		Remainder = Target - Start
 
 		if Remainder < NapTime:
			time.sleep(Remainder)
 
		else:

			#Minor Period
			#preforms actions?
			
			time.sleep(NapTime)
