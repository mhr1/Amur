
def make_db(db_list, filename):
    file = open(filename, "r") 

    i = 0
    for eachline in file:
        x = eachline.split()
        y = round(float(x[5]) - float(x[2]), 5)   
        my_tuple = (i, y)
        db_list.append(my_tuple)
        i += 1
    file.close()

audusd = []

make_db(audusd, "./fx_daily/AUDUSD1440.csv") 
print(audusd[435][1])
