x = 1 # int
y = 2.0 # float

def add(b,c):
    a = b + c
    print(a)

class Test:
    z = 5

p1 = Test
print(p1.z)

my_string = "Hello Worm"

print(my_string)

add(x,y)

#file = open("test_file.txt", "x") # x means create
file = open("./fx_daily/AUDUSD1440.csv", "r") # r - read, w - write, a - append, r+ - r/w
#file.write("Hello World")
for each in file:
    print(each)

file.close()
