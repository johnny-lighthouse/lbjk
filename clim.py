#simple loop to toggle LED on and off forever

import time
import math
import ConfigParser
import logging

LEVELS = {'debug': logging.DEBUG,
          'info': logging.INFO,
          'warning': logging.WARNING,
          'error': logging.ERROR,
          'critical': logging.CRITICAL}

#Initilize Labjack
import u3
Device = u3.U3(autoOpen = False)

# LED state: null = false = led off
State = ()

#set an initial Target time for first iteration and round up to a whole second
Target = math.ceil(time.time())

MajorPeriod=()

while 1 != 0:

	Start = time.time()

	#
	#read config file and set default values.  default values don't work as intended.
	#
	config = ConfigParser.RawConfigParser({'MajorPeriod': '1', 'MinorPeriod': '.5'})
	config.read('config.file')

	#get periods in seconds	from config file
	NewMajorPeriod = config.getfloat('section 1', 'MajorPeriod')
	MinorPeriod = config.getfloat('section 1', 'MinorPeriod')

	#set output register on Labjack
	LED = config.getint('section 1', 'LED address')

	level_name = config.get('section 1', 'LogLevel')
	LOG_FILENAME = config.get('section 1', 'LogFile')

	#
	#flesh out configuration of logging setup and sleep time
	#
	Level = LEVELS.get(level_name, logging.NOTSET)
	logging.basicConfig(filename=LOG_FILENAME,level=Level)

	#check for change in major period, log and set
#	logging.debug("NewMajorPeriod = %s and MajorPeriod = %s" % NewMajorPeriod MajorPeriod )
	if MajorPeriod != NewMajorPeriod:
		logging.info("config changed for MajorPeriod!")
#		logging.info("%s: detected config change: MajorPeriod changed from %s to %s" % Start MajorPeriod NewMajorPeriod )
		MajorPeriod = NewMajorPeriod

	#calculate time to sleep 
	NapTime = float(MajorPeriod)/float(MinorPeriod)

	# round Target up to nearest even time
	Overplus = Target % MajorPeriod
	if Overplus != 0:
		Target = Target + ( MajorPeriod - Overplus )


	if Start >= Target:

		logging.debug('This message should go to the log filcheived MajorPeriode')

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
