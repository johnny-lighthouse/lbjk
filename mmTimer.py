###############
# preform specified actions at a specidied Major and Minor period
#
# Call thusly:
#
# import mmTimer.py
# mmTimer.Loop("Major_Payload()", "Minor_Payload()",MajorPeriod,MinorPeriod)
#
#

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


