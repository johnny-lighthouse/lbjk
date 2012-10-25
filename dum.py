###############
# periodically poll labjack for current acceleromter voltage and do stuff with it


###############
# set up config file


import ConfigParser

# this needs to be a function that we can call on each loop
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




###############
# set up logging

import logging

LEVELS = {'debug'   : logging.DEBUG,
          'info'    : logging.INFO,
          'warning' : logging.WARNING,
          'error'   : logging.ERROR,
          'critical': logging.CRITICAL}

Log_Filename = "incline.log"
Log_Level = "info"


# this needs to be a function that we can run on each loop

	#test for change in log name and level.  has to be done here to get looging going.
	old_log_name = ()
        if Log_Filename != New_Log_Filename:
                old_log_name = 1
                Log_Filename = New_Log_Filename

#this doesn't work correctly because the names are mapped to numeric values.
#       old_log_level = ()
        if New_level_name != Log_Level:
#               old_log_level = 1
                Log_Level = New_level_name

        #configure logging
        Log_Level = LEVELS.get(Log_Level, logging.NOTSET)
        logging.basicConfig(filename=Log_Filename,level=Log_Level)

        #log any changes to log name and level
        if old_log_name:
                logging.info('Logfile set to:')
#       if old_log_level:
#               logging.info('Log level set to:')

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

logging.debug('This message should go to the log file')


###############
# LabjackPython library calls

import u3

Device = u3.U3(autoOpen = False)

def Open_Device():
	Device.open()

def Close_Device():
	Device.close()

X_Axis = 00	#address of acceleromter, 00 register is AIN

def Read_X():
	return Device.readRegister(X_Axis)

LED = 6004	#address of LED, 6000 register is DIO

def Write_LED():
	Device.writeRegister(LED, LED_State)   


###############
# support functions and variables

LED_State = 0

def Flip_LED():
	global LED_State 
	LED_State = not LED_State
	Write_LED()

def Get_Reading():
     Repeat = 5
     Read_sum = 0
     Loop_count = 0
     while Loop_count < Repeat:
       Read_sum += Read_X() 
       Loop_count += 1
     return Read_sum / Repeat

Last_Few = []
Sample = 5
Average = 0 
def Calc_Average():
	global Last_Few
	if len(Last_Few) >= (Sample +1):
		del Last_Few[0]
	Sum = 0 
	global Average	
	for x in Last_Few:
		Sum = Sum + x
	Average = Sum / Sample

Max_Delta = 0
Max_Diff = 0


###############
# Primary functions

def Major_Payload():

		global Max_Delta
		global Max_Diff
	
		Open_Device()

		Flip_LED()

		#Read and print value of accelerometer
		Accel = Get_Reading() 
		Last_Few.append(Accel)

		Calc_Average()

		Diff = Average - Accel
		if Diff > Max_Diff:
			Max_Diff = Diff	

#		print "%s" % Last_Few
#		print "Acceleromter output is %s Volts" % Accel
#		print "running average is %1.3f Volts" % Average 
#		print "Last sample differs from average by %1.3f Volts" % Diff
		print "Max difference of sample from average is %1.3f Volts" %Max_Diff
		
		Delta = Last_Few[0] - Accel
#		print "Difference from last sample is %1.3f Volts" % Delta

		if Delta > Max_Delta:
			Max_Delta = Delta
		print "Max difference from average is %1.3f Volts" % Max_Delta

		Close_Device()

def Minor_Payload():
	pass


###############
# repeat

import mmTimer

mmTimer.Major_Payload = Major_Payload

mmTimer.Loop("Major_Payload()", "Minor_Payload()",1,.5)
