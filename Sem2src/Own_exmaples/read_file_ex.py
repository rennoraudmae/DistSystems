file = open("test.txt", "w")

file.write("Hello World! \n")
file.write("Sisestame veel midagi. \n")
file.write("Sisestame veel midagi teist korda. \n")

file.close()

file = open('test.txt', 'r')

#print file.read()

for line in file:
    print line,





