###############
# periodically poll labjack for current acceleromter voltage and print to stdout

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
# payload setup

LED_State = 0

def Flip_LED():
	global LED_State 
	LED_State = not LED_State
	Write_LED()

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

def Major_Payload():

		global Max_Delta
		global Max_Diff
	
		Open_Device()

		Flip_LED()

		#Read and print value of accelerometer
		Accel = Read_X()
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

import mmTimer

mmTimer.Loop("Major_Payload()", "Minor_Payload()",1,.5)
