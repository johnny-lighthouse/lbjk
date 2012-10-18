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

def Get_Reading():
     Read_sum = 0
     Loop_count = 0
     while Loop_count < 5:
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
# Timer Function


def Loop(x,y,a,b):

	import time
	import math
	
	MajorPeriod = a
	MinorPeriod = b

	#set an initial Target time for first iteration and round up to a whole second
	Target = math.ceil(time.time())

	while True:

		Start = time.time()

		#calculate time to sleep 
		NapTime = MajorPeriod/MinorPeriod

		# round Target up to nearest even time
		Overplus = Target % MajorPeriod
		if Overplus != 0:
			Target = Target + ( MajorPeriod - Overplus )


		if Start >= Target:

			Target = Target + MajorPeriod

			#major period
			#preform actions passed as string in argument x

			eval(x)	

		else:
			Remainder = Target - Start

			if Remainder < NapTime:
				time.sleep(Remainder)
			else:

				#Minor Period
				#preform actions passed as string in argument y

				eval(y)

				time.sleep(NapTime)


###############
# main loop

Loop("Major_Payload()", "Minor_Payload()",1,.5)
