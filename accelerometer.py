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
	'''test if device has been set and if not call SetDevice() ???'''
	Open_Device()
	function
	Close_Device()

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

def Read_Median(Sample):
        if Sample % 2 != 0 and type(Sample) == int:
                Median_Index = (Sample / 2)
                '''list indicies start from 0 so rounding of integer division provides required offset'''
                Measurements = []
                while len(Measurements) < Sample :
                        Measurements.append(Read_X())
                Measurements.sort()
                return Measurements[Median_Index]
        else:
                print "Please choose an odd integer sample size for simplicity"

def Read(Sample):
	'''return a sequence of raw measurments for use in different averaging schemes'''
        Measurements = []
        while len(Measurements) < Sample :
                Measurements.append(Read_X())
	'''accept an optional parameter to turn on an if to prinjt values?'''
	'''should we return like this or modify a global variable?'''
	return Measurements

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

def Call_Loop():
	SetDevice()
	import mmTimer
	mmTimer.Major_Payload = Major_Payload
	mmTimer.Loop("Major_Payload()", "Minor_Payload()",1,.5)


