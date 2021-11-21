

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
eurchf = []
eurgbp = []
eurjpy = []
eurusd = []
gbpjpy = []
gbpusd = []
usdcad = []
usdchf = []
usdjpy = []

make_db(audusd, "./fx_daily/AUDUSD1440.csv") 
make_db(eurchf, "./fx_daily/EURCHF1440.csv") 
make_db(eurgbp, "./fx_daily/EURGBP1440.csv") 
make_db(eurjpy, "./fx_daily/EURJPY1440.csv") 
make_db(eurusd, "./fx_daily/EURUSD1440.csv") 
make_db(gbpjpy, "./fx_daily/GBPJPY1440.csv") 
make_db(gbpusd, "./fx_daily/GBPUSD1440.csv") 
make_db(usdcad, "./fx_daily/USDCAD1440.csv") 
make_db(usdchf, "./fx_daily/USDCHF1440.csv") 
make_db(usdjpy, "./fx_daily/USDJPY1440.csv") 
print(audusd[435][1])
print(usdjpy[435][1])
