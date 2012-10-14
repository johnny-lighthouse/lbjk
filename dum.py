#############
# periodically poll labjack for current acceleromter voltage and print to stdout

#############
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
# other setup

import time
import math

MajorPeriod = .01
MinorPeriod = .005

#set an initial Target time for first iteration and round up to a whole second
Target = math.ceil(time.time())

def Increment_Target():
	global Target
	Target = Target + MajorPeriod

Start = ()
NapTime = ()
Remainder = ()

def Set_Timer():
	global Start
	global Naptime
	global Target
 
	Start = time.time()

	#calculate time to sleep 
	NapTime = MajorPeriod/MinorPeriod

	# round Target up to nearest even time
	Overplus = Target % MajorPeriod
	if Overplus != 0:
		Target = Target + ( MajorPeriod - Overplus )

LED_State = ()

def Flip_LED():
	global LED_State 
	LED_State = not LED_State
	Write_LED()

Last_Few = []
Sample = 3
def Calc_Average():
	global Last_Few
	if len(Last_Few) >= (Sample +1):
		del Last_Few[0]
	#take average of Last_Few

###############
# main loop

while 1 != 0:

	Set_Timer()

	if Start >= Target:

		Increment_Target()
	
		Open_Device()

		Flip_LED()

		#Read and print value of accelerometer
		Accel = Read_X()
		Last_Few.append(Accel)

		Calc_Average()

		print "%s" % Last_Few
		print "Acceleromter output is %s Volts" % Accel

		Close_Device()

	else:
		Remainder = Target - Start

		if Remainder < NapTime:
			time.sleep(Remainder)

		else:

			#Minor Period
			#preforms actions?

			time.sleep(NapTime)
