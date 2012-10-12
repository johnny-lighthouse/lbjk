

#LabjackPython library calls
import u3
LED = 6004	#address of LED, 6000 register is DIO
X_Axis = 00	#address of acceleromter, 00 register is AIN

Device = u3.U3(autoOpen = False)

def Read_X():
	return Device.readRegister(X_Axis)

LED_State = ()
def Flip_LED():
	global LED_State 
	LED_State = not LED_State
	print "LED is %s" % LED_State
	Device.writeRegister(LED, LED_State)   




import time
import math

MajorPeriod = 1
MinorPeriod = .5

#set an initial Target time for first iteration and round up to a whole second
Target = math.ceil(time.time())

while 1 != 0:

	Start = time.time()

	#calculate time to sleep 
	NapTime = MajorPeriod/MinorPeriod

	# round Target up to nearest even time
	Overplus = Target % MajorPeriod
	if Overplus != 0:
		Target = Target + ( MajorPeriod - Overplus )

	if Start >= Target:

		Target = Target + MajorPeriod

		#initialize labjack on each loop
		Device.open()

		Flip_LED()

		#Read and print value of accelerometer
#		Accel = Device.readRegister(00)
		Accel = Read_X()
		print "Acceleromter output is %s Volts" % Accel

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
