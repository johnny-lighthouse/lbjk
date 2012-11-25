###############
# preform two arbitrary functions at a specidied Major and Minor period
#
# Call thusly:
#
# import mmTimer
# mmTimer.function1 = function1
# mmTimer.function2 = function2
# mmTimer.Loop("function1()", "function2()",MajorPeriod,MinorPeriod)
#
# NB that function names are quoted in order to pass them as strings
# NB both function must be copied into the mmTimer namespace prior to use
#


def Loop(x,y,a,b):

	import time
	import math
	
	MajorPeriod = a
	MinorPeriod = b

	#set an initial Target time for first iteration and round up to a whole second
	Target = math.ceil(time.time())
	
	while True:
	   try: 
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

			exec(x)	

		else:
			Remainder = Target - Start

			if Remainder < NapTime:
				time.sleep(Remainder)
			else:

				#Minor Period
				#preform actions passed as string in argument y

				exec(y)

				time.sleep(NapTime)

	   except KeyboardInterrupt:
		input = raw_input('  ===> ')
		if input == 'q':
			'''stop loop.  sys.exit() will execute a finally block if defined, it doesn't exit right away'''
			from sys import exit
			exit()
		else:
			pass  
