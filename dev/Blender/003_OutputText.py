def outputfile( filename ):
	print("Output: ", filename)
	f = open( filename, "w" )
	f.write("Hello World!!")
	f.close


outputfile( "test.txt" )
print("end of process..")
