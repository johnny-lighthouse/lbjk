###############
# periodically poll labjack for current acceleromter voltage and do stuff with it


###############
# LabjackPython library calls

import u3

Device = "" 
 
def SetDevice():
	global Device
	try:
		Device = u3.U3()
		Close_Device()
	except u3.NullHandleException:
		print "No Labjack device found... "
		from sys import exit
		exit()
#can this be done as Device = SetDevice() with set device returning wither a labjack object or a dummy ??

		
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

def Poll_Device(function):
	'''manage open and close of device for a la carte usage outside of Major_Payload below'''
	#test if device has been set and if not call SetDevice() ???
	#not working
	#map builtin useful here?
	Open_Device()
	function
	Close_Device()

LED_State = 0

def Flip_LED():
	global LED_State 
	LED_State = not LED_State
	Write_LED()


###############
# averaging and analysis functions and associated variables 


def Get_Reading():
     Repeat = 5
     Read_sum = 0
     Loop_count = 0
     while Loop_count < Repeat:
       Read_sum += Read_X() 
       Loop_count += 1
     return Read_sum / Repeat

def Read_Mean():
        Measurements = []
        Sample = 5
        Sum = 0
        while len(Measurements) < Sample :
                Measurements.append(Read_X())
        for x in Measurements:
                print "%s  " % str(x)
                Sum = Sum + x
        return Sum / Sample


#################################
#    revised for list input     #
#################################


def Median(Samples):
	'''take a list of data points and return the median value as a float'''
	Samp=Samples[:]
	Samp.sort()
	L = len(Samp)
	M = L/2
	if L % 2 != 0:
                return float(Samp[M])
        else:
		return float( Samp[M] + Samp[M-1] ) /2

def Read(Sample=5):
	'''return a list of raw unmanipulated measurments'''
        Measurements = []
        while len(Measurements) < Sample :
                Measurements.append(Read_X())
	#accept an optional parameter to turn on an if to print values?
	#should we also somehow append the time? at beinging or end?
	#should Read() return the list and enroll data in the globals and write the raw values to a log file??
	return Measurements


def Compute_Deviation(Samples):
	'''look at a set of data and check if it falls inside or outside of deviation'''
	
Sample_Count = 0
Running_Total = 0

def enroll_data(Samples):
	'''accept list of data points and enrolls them into our data set'''
	# USES same variable as Run_Average below so should not be run in combination at this point
	#why should this not be combine with read ??
	global Running_Total
	global Sample_Count
	for measurement in Samples:
		Sample_Count += 1
		Running_Total = Running_Total + measurement
		#print Running_Total, Sample_Count, measurement
	#is it useful to return the unmanipulated input so that we can pass data through this function or is thast confusing??

def Cumulative_Running_Average(Samples=[]):
	'''
	return current running average
	optionally takes a list of new data points and adds them into calculation
	assumes Sample_Count is greater than 0
	'''

	#nb global variable is not available in __main__ scope when function imported directly 'from'
	#should i have one function to enroll new data and another to return the current running average?
	#should Read() return the list and enroll data in the globals and write the raw values to a log file??

	#########################
	# duplicated above
	#
	global Running_Total
	global Sample_Count
	#print Samples
	for measurement in Samples:
		Sample_Count += 1
		Running_Total = Running_Total + measurement
		#print Running_Total, Sample_Count, measurement
	#########################

	return Running_Total / Sample_Count



#################################

#older material below

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
# functions arranged for repetative looping

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

def Call_Loop():
	SetDevice()
	import mmTimer
	mmTimer.Major_Payload = Major_Payload
	mmTimer.Loop("Major_Payload()", "Minor_Payload()",1,.5)


