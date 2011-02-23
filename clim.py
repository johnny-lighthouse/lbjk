#simple loop to toggle LED on and off forever

import time
import math
import ConfigParser
import logging

LEVELS = {'debug'   : logging.DEBUG,
          'info'    : logging.INFO,
          'warning' : logging.WARNING,
          'error'   : logging.ERROR,
          'critical': logging.CRITICAL}

MajorPeriod = 1
MinorPeriod = .5
LED = 6004
Log_Filename = "incline.log"
Log_Level = "info"

#Initilize Labjack
import u3
Device = u3.U3(autoOpen = False)

# LED state: null = false = led off
State = ()

#set an initial Target time for first iteration and round up to a whole second
Target = math.ceil(time.time())

while 1 != 0:

	Start = time.time()

	#
	#read config file and set default values.  default values don't work as intended.
	#
	config = ConfigParser.RawConfigParser()
	config.read('config.file')

	#read config file into temporary variables
	New_LED = config.getint('section 1', 'LED address')
	New_MajorPeriod = config.getfloat('section 1', 'MajorPeriod')
	New_MinorPeriod = config.getfloat('section 1', 'MinorPeriod')
	New_level_name = config.get('section 1', 'LogLevel')
	New_Log_Filename = config.get('section 1', 'LogFile')

	
	#test for change in log name and level.  has to be done here to get looging going.
	old_log_name = ()
	if Log_Filename != New_Log_Filename:
		old_log_name = 1 
		Log_Filename = New_Log_Filename

#this doesn't work correctly because the names are mapped to numeric values.
#	old_log_level = ()
	if New_level_name != Log_Level:
#		old_log_level = 1 
		Log_Level = New_level_name

	#configure logging
	Log_Level = LEVELS.get(Log_Level, logging.NOTSET)
	logging.basicConfig(filename=Log_Filename,level=Log_Level)

	#log any changes to log name and level
	if old_log_name:
 		logging.info('Logfile set to:')
#	if old_log_level:
#		logging.info('Log level set to:')

	#test if other parameters have changed vs new values from file.  if yes then log and update dictionary.
	if New_LED != LED:
		logging.info('LED address set to:')
		LED = New_LED
	if New_MajorPeriod != MajorPeriod:
		logging.info('Major Period set to:')
		MajorPeriod = New_MajorPeriod
	if New_MinorPeriod != MinorPeriod:
		logging.info('Minor Period set to:')
		MinorPeriod = New_MinorPeriod


	#calculate time to sleep 
	NapTime = MajorPeriod/MinorPeriod

	# round Target up to nearest even time
	Overplus = Target % MajorPeriod
	if Overplus != 0:
		Target = Target + ( MajorPeriod - Overplus )


	if Start >= Target:

		logging.debug('This message should go to the log file')

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
