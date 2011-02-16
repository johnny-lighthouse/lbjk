#simple loop to toggle LED on and off forever

import time
import math

#Initilize Labjack
import u3

#set output channel on Labjack
LED = 6004

#initialize state as 0 so initial flip is to 1 ie on
State = 0

#set initial Target for first iteration and round up to a whole second
Target = math.ceil(time.time())   
 
while 1 != 0:
 
	# set timing parameters for later.  These are here to catch changes to config file dynamically, without a restart.
	# these should be set from commandline arguments or a config file, with defaults set here?
	Period = 1
	Divisor = .5
 
	NapTime = float(Period)/float(Divisor)
 
	# round Target up to nearest even time
	Odd = Target % Period
	if Odd != 0:
		Target = Target + ( Period - Odd )
 
	#
	# compare current time to Target and act accordingly.
	#
	Start = time.time()
 
	if Start >= Target:
                Target = Target + Period
                print '@ %f seconds from epoch:' % Start

		#initialize labjack
		d = u3.U3()

		#flip current state
		State ^= 1
		print 'LED is %i ' % State

		#toggle the LED
		d.writeRegister(LED, State)
		
		d.close
 
	else:
		Remainder = Target - Start
 
 		if Remainder < NapTime:
			time.sleep(Remainder)
 
		else:
			time.sleep(NapTime)
