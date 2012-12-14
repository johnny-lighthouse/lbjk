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

def Read(Sample=5):
	'''return a list of raw unmanipulated measurments'''
        Measurements = []
        while len(Measurements) < Sample :
                Measurements.append(Read_X())
	#accept an optional parameter to turn on an if to print values?
	#should we also somehow append the time? at beinging or end?
	#should Read() return the list and enroll data in the globals and write the raw values to a log file??
	return Measurements

###############
# averaging and analysis functions and associated variables 

Sample_Count = 0
Running_Total = 0

def enroll_data(Samples):
	'''accept list of raw data points and enrolls them into our data set'''
	# USES same variable as Run_Average below so should not be run in combination at this point
	#why should this not be combine with read ??
	#we should have another global like Last_Few below which has a rolling window of a certain size
	global Running_Total
	global Sample_Count
	for measurement in Samples:
		Sample_Count += 1
		Running_Total = Running_Total + measurement
		#print Running_Total, Sample_Count, measurement
	#is it useful to return the unmanipulated input so that we can pass data through this function or is thast confusing??

Def Mean(Samples):
	Samp=Samples[:]
	Sum = 0.0
	Size = len(Samp)
	for s in Samp:
		Sum = Sum + s	
	return Sum / Size

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

def Cumulative_Running_Average(Samples=[]):
	'''return current cumulative running average. assumes Sample_Count is greater than 0'''
	return Running_Total / Sample_Count

def Compute_Deviation(Samples):
	'''look at a set of data and check if it falls inside or outside of deviation'''

###############
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
