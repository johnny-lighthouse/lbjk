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

def Poll_Device(function):
	'''manage open and close of device for a la carte usage outside of Major_Loop_Function below'''
	#test if device has been set and if not call SetDevice() ???
	#not working, nullhandleexception means not finding labjack?  scope deficient??
	#map builtin useful here?
	Open_Device()
	print function
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

Sample_Count = 0
Running_Total = 0
Last_Few = []                   # change to something like recent_readings ?/

def Enroll_Data(Samples):
	'''accept list of raw data points and enrolls them into our data set'''
	#why should this not be combine with read ??
	global Running_Total
	global Sample_Count
	Recent_Values(Samples)
	for measurement in Samples:
		Sample_Count += 1
		Running_Total = Running_Total + measurement
		#print Running_Total, Sample_Count, measurement
	#is it useful to return the unmanipulated input so that we can pass data through this function or is thast confusing??

def Recent_Values(Add, Length=50, Container=Last_Few):
	'''manage sequence of last n values of a measurement.  append new values and drop oldest.  return updated sequence object'''
	#does this have to be a list ??  should we test ??
#	global Container ##### result must be saved for persistence
	for value in Add:
		#validate data in input?  must be list of floats???
		Last_Few.append(value)
	while len(Container) >= Length:
		del Last_Few[0]
	return Container


###############
# averaging and analysis functions and associated variables 
	
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
CRA = Cumulative_Running_Average

def Compute_Deviation(Samples):
	'''look at a set of data and check if it falls inside or outside of deviation'''
	#this needs to be generalized to work on any of the various averages we are working with: mean, median, rolling, cumulative etc
	# input will be a value and a dta set to compare?
	# return will be the difference of the input value to the data set ??

def Rolling_mean():
	'''return mean average of recent readings as defined elsewhere''' 
	return Mean(Last_Few)

def Rolling_Median():
	'''return median average of recent readings as defined elsewhere''' 
	return Median(Last_Few)

###############
# functions arranged for repetative looping
# does not conform to current function structure but retained as place holder

def Major_Loop_Function():
	import time
	'''work to be done periodically: get new data, check it in, evaluate and report avrerages'''
	Open_Device()
	data = Read()
	Enroll_Data(data)
	print "Raw Measurements at", time.time(), "are", data
	print "Mean is", Mean(data), " Median is", Median(data), "      Running Average is", CRA()
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
