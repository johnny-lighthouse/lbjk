###############
# periodically poll labjack for current acceleromter voltage and do stuff with it


###############
# LabjackPython library calls

import u3

Device = ""   ### Nessasary for current implementation of SetDevice() 
 
def SetDevice():
	'''initialize a labjack object and provide a place to set up a dummy of no labjack is present'''
	global Device
	try:
		Device = u3.U3()
		Close_Device()
	except u3.NullHandleException:
		print "No Labjack device found... "
		from sys import exit
		exit()
	#can this be done as Device = SetDevice() with set device returning with either a labjack object or a dummy ??
		
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

def Read(Sample=5):
	'''return a list of raw unmanipulated measurments'''
        Measurements = []
        while len(Measurements) < Sample :
                Measurements.append(Read_X())
	#should the time get recorded here? makes unpacking results more complicated...
	#should Read() return the list and enroll data in the globals and write the raw values to a log file??
	return Measurements

Sample_Count = 0
Running_Total = 0
Last_Few = []

def Enroll_Data(Samples, Roll_Length=50):
	'''accept list of raw data points and optional length of rolling data list
	enrolls data points into various persistent storage'''
	#why should this not be combine with read ??
	global Running_Total
	global Sample_Count
	Recent_Values(Samples)
	for measurement in Samples:
		Sample_Count += 1
		Running_Total = Running_Total + measurement
		Last_Few.append(measurement)
	while len(Last_Few) >= Roll_Length:
		del Last_Few[0]
	## Do we need to Global Last_Few ?


###############
# averaging functions and associated variables 
	
def Mean(Samples):
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

def Cumulative_Running_Average():
	'''return current cumulative running average. assumes Sample_Count is greater than 0'''
	return Running_Total / Sample_Count

def Rolling_mean():
	'''return mean average of recent readings as defined elsewhere''' 
	return Mean(Last_Few)

def Rolling_Median():
	'''return median average of recent readings as defined elsewhere''' 
	return Median(Last_Few)

###############
# arrangment for repetative looping

def Major_Loop_Function():
	import time
	'''work to be done periodically: get new data, check it in, evaluate and report avrerages'''
	Open_Device()
	data = Read()
	Enroll_Data(data)
	print "Raw Measurements at", time.time(), "are", data
	print "Mean is", Mean(data), " Median is", Median(data), "      Running Average is", Cumulative_Running_Average()
	print "Mean of last 50 measuremnets is", Rolling_mean(), "      Median of last 50 measurments is", Rolling_Median()
	print ""
	Close_Device()

def Minor_Loop_Function():
	pass

def Call_Loop():
	SetDevice()
	import mmTimer
	mmTimer.Major_Loop_Function = Major_Loop_Function
	mmTimer.Loop("Major_Loop_Function()", "Minor_Loop_Function()",1,.5)
