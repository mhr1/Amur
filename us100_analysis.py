import random

"""
 US100 Analysis

 Using generic .csv data downloaded from HistData.com (find and replace ";" with " ")
 x[0] is date, x[1] time, x[2] is open, x[3] high, x[4] low, x[5] closed, x[6] is zero
 

"""

def make_db(db_list, filename):
    file = open(filename, "r") 

    i = 0
    for eachline in file:
        x = eachline.split()
        my_tuple = (int(x[0]), int(x[1]), float(x[2]), float(x[3]), float(x[4]), float(x[5]))
        db_list.append(my_tuple)
        i += 1
    file.close()
"""
 Normalise
 
 Calculate gradient using mean of the first 100 (a) and the mean of the last 100 (b)
 gradient = (b - a)/size.us100
 normalise: us100[n]-(n * gradient)
"""      
def normalise(db_list, norm):
	size = len(db_list)
	sum1 = 0
	for a in range(0, 100):
		sum1 += db_list[a][2]
		
	mean1 = sum1/100
	
	sum2 = 0
	for a in range(size - 100, size):
		sum2 += db_list[a][2]
		
	mean2 = sum2/100
	gradient = (mean2 - mean1)/(size - 100)

	norm.append(db_list[0][2])
	for x in range(1, size):
	 	a = (db_list[x][2]-(x * gradient))
	 	norm.append(a)
"""
 Deviation
 
 Maximum positive and negative deviations from the mean using normalised data

"""	 	
def deviation(myarray):
	size = len(myarray)
	sum = 0
	for i in range(0, size):
		sum += myarray[i]
		
	mean = sum/size
	plus = 0
	minus = 0
	for i in range(0, size):
		x = myarray[i] - mean
		if(x > plus):
			plus = x
		if(x < minus):
			minus = x
			
	print("Max: ", plus, " min: ", minus)

"""

 One fairly easy analysis is to look at the high and low deviation cf the opening price
 
"""	
def day_move(mylist):
	size = len(mylist)
	plus = 0
	minus = 0
	freq_high = 0
	freq_low = 0
	print(mylist[3])
	for i in range(0, size):
		open1 = float(mylist[i][2])
		high = float(mylist[i][3])
		low = float(mylist[i][4])
		close = float(mylist[i][5])
		mean = round((open1 + close)/2, 2)
		x = high - open1
		if(x > plus): plus = x
		if(x > 30): freq_high += 1; print("High ", mylist[i][1])
		x = low - open1
		if(x < minus): minus = x
		if(x < -30): freq_low += 1; print("Low ", mylist[i][1])
		
	print("Max: ", round(plus, 2), " min: ", round(minus, 2))
	print("Times above 30 pts = ", freq_high, " and below = ", freq_low)
	
"""
 Time Specific data 
 
 Day is 1336 minutes long and trading starts at 9:30 (not 14:30)
 We want 1105 to 14:25 for the 'quiet period'
"""
def time_specific(db, results):
	for i in range(0, len(db)):
		if(db[i][0] == 20211105 and db[i][1] > 90000 and db[i][1] < 162500):
			results.append(db[i])
			
def gaussian_noise():
	x = 0
	for i in range(0, 10):	
		x += random.randrange(0, 11)	
	return x
	
"""	
	Trade Simulator
	
	7/1/22 - This is still not getting it right. Try looking for a gradient inflxion => grad = 0
		followed by grad > 1, but below mean => buy and grad = 0 followed by grad < -1 above mean for a sell

"""			

def trade(db, limit, stop, entry):
	state = 0
	spread = 1
	#entry = 1.5 # Enter trade at entry value above or below mean
	#limit = 3
	stop = 100
	waiting_time = 3
	profit = 0
	trades = 0
	gradient = 0
	for i in range(20, len(db)):
		sum = 0
		for j in range(-19, 1):
			sum += db[i+j][2]
		mean = sum/20
		#print(db[i][1], round(mean, 2), round(db[i][2], 2), round(db[i][2] - mean, 2))
		if(state == 0): 
			sum = 0
			for j in range(-19, 1):
				sum += db[i+j][2]
			mean = sum/20
			#print(db[i][1], round(mean, 2), round(db[i][2], 2), round(db[i][2] - mean, 2))
		# Gradient
			suma = 0
			sumb = 0
			for k in range(-9, -4):
				suma += db[i+k][2]
			for k in range(-4, 1):
				sumb += db[i+k][2]
			gradient = (sumb - suma)/5
			print("Gradient", round(gradient, 2))
			
			if(db[i][2] < (mean - entry) and gradient > 1):
				state = 1
				entry_price = db[i][2]
				print(db[i][1], ": Buy @ ", entry_price)
			
			if(db[i][2] > (mean + entry) and gradient < -1):
				state = 2
				entry_price = db[i][2]
				print(db[i][1], ": Sell @ ", entry_price)
		if(state == 1): 
			if(db[i][3] > entry_price + spread + limit):
				print(db[i][1], "Win ", limit, " pts")
				profit += limit
				trades += 1
				state = 3
			if(db[i][4] < entry_price + spread - stop):
				print(db[i][1], "Lose ", stop, " pts")
				profit -= stop
				trades += 1
				state = 3
		if(state == 2): 
			if(db[i][4] < entry_price - spread - limit):
				print(db[i][1], "Win ", limit, " pts")
				profit += limit
				trades += 1
				state = 3
			if(db[i][3] > entry_price - spread + stop):
				print(db[i][1], "Lose ", stop, " pts")
				profit -= stop
				trades += 1
				state = 3
		if(state == 3): 
			#print("Waiting ", waiting_time, " mins")
			waiting_time -= 1
			if(waiting_time == 0):
				state = 0
				waiting_time = 3
				
	print("Limit", limit, "Stop", stop, "entry", entry, "trades", trades, "profit", profit)

def us_open(db):
	reading = 0	
	open_price = 0.0
	hooray = 0
	boo = 0	
	win = 0		
	for i in range(0, len(db)):
		if(db[i][1] == 92700):
			print("Time", db[i][1], "open", db[i][2])
			reading = 1
			open_price = db[i][2]
			# Gradient
			suma = 0
			sumb = 0
			for k in range(-9, -5):
				suma += db[i+k][2]
			for k in range(-4, 0):
				sumb += db[i+k][2]
			gradient = (sumb - suma)/5
			print("Gradient", round(gradient, 2))
		if(reading):
			if(db[i][3] > open_price + 30):
				reading = 0
				hooray += 1
				print("Hooray at", db[i][1], "high", db[i][3])
				if(gradient > 0):
					win += 1
			if(db[i][4] < open_price - 30):
				reading = 0
				boo += 1
				print("Boo at", db[i][1], "low", db[i][4])
				if(gradient < 0):
					win += 1
				
	print("Hoorays", hooray, "Boos", boo, "Wins", win)
		
def main():
	us100 = []
	make_db(us100, "./DAT_ASCII_NSXUSD_M1_202111.csv") 
	#make_db(us500, "./DAT_ASCII_SPXUSD_M1_202111.csv") 

	us_open(us100)
	
	norm = []
	#normalise(us100, norm)
	size = len(us100)


	#print(us100[1][2], us100[size - 1][2])	
	#print(norm[1], norm[size - 1])
	#deviation(norm)

	#day_move(us100)
	"""
	file = open("results.csv", "w")
	for x in range(0, len(norm)):
		print(round(norm[x], 2), file = file)
		#file.write(str(norm[x]), "\n")
	file.close()
	"""

	dummy = []
	time_specific(us100, dummy)	
	#day_move(dummy)

	"""
	noise = 0
	x = 0
	for i in range(1, 101):
		noise = gaussian_noise()
		x += noise
		print(noise)
	y = x/100
	print("Mean", y)
	
	for limit in range(20, 21):
		for stop in range(5, 6):
			for entry in range(1, 11):
				trade(dummy, limit, stop, entry)
"""
main()














