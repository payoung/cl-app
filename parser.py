#-----------------------------------------------------------------------------#
# Parses the converted html files to find the swell heights and conditions
# and then prints these out into formatted tables
#-----------------------------------------------------------------------------#

def parse_txt(txt):

	# Open File
	in_file = open(txt)

	## Search doc for a list of keywords and record the positions in the file

	# Define keywords
	word = ['Today', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 
		'Friday', 'Saturday', 'Sunday']

	# Initialize itr var to use to track file position
	i = 0
	l_pos = -99

	# Initialize arrays to use to store keyword and file poistion data
	pos_array = []
	word_array = []
	line1_array = []
	line2_array = []
	line3_array = []

	# Loop through doc, search for list of words, and record the line and line #
	for line in in_file:
		for w in word:
			
			if w in line:
				pos_array.append(i)
				word_array.append(w)
				line1_array.append(line)
				l_pos = i
		# Need to pull the extra lines to get the swell height and conditions
		if i == (l_pos + 3):
			line2_array.append(line)
		if i == (l_pos + 4):
			line3_array.append(line)
				
		i += 1
		
	#Seems to be pulling in an extra line from time to time
	# - Remove last item from all arrays if len over 7
	if len(word_array) > 7:
		pos_array.pop()
		word_array.pop()
		line1_array.pop()
		line2_array.pop()
		line3_array.pop()

	# Grab the condition information from the respective lines

	am_cond = []
	am_swell = []
	pm_cond = []
	pm_swell = []

	# Pull AM condition information from line1_array
	for line in line1_array:
		lhs, rhs = line.split("AccordionPanelTab ")
		lhs, rhs = rhs.split("_")
		am_cond.append(lhs)
		
	# Pull AM swell height information from line2_array
	for line in line2_array:
		lhs, rhs = line.split(">", 1)
		lhs, rhs = rhs.split("<")
		am_swell.append(lhs)
		
	# Pull PM conditions and PM Swell from line3_array
	for line in line3_array:
		#Grab Swell Height
		lhs, rhs = line.split(">", 1)
		lhs, rhs = rhs.split("<")
		pm_swell.append(lhs)
		#Grab Conditions
		lhs, mid, rhs = line.split('"')
		pm_cond.append(mid)
		
	# Convert Condition values to readable values

	def conv_cond(cond):
		ret_array = []
		for val in cond:
			if val == 'cond1':
				ret_array.append("Good")
			elif val == 'cond2':
				ret_array.append("Fair")
			elif val == 'cond3':
				ret_array.append("Poor")
			else:
				ret_array.append("!Error!")
		
		return(ret_array)
		
	am_cond = conv_cond(am_cond)
	pm_cond = conv_cond(pm_cond)
	
	#Pull out the Beach Name from the txt file name
	beach, lhs = txt.split('.')
		
	# Print Swell Table
	print "\nSwell Report for %s" % beach
	print "----------------------------------------------"
	print "Day \t\t AM \t\t PM"
	print "----------------------------------------------"
	for j in range(len(word_array)):
		if j == 0:
			print "%s: \t\t %s %s \t %s %s" % (word_array[j], am_swell[j], am_cond[j],
				pm_swell[j], pm_cond[j])
		else:
			print "%s: \t %s %s \t %s %s" % (word_array[j], am_swell[j], am_cond[j],
				pm_swell[j], pm_cond[j])
			
	print "\n"

	in_file.close()

# Set up the arrays to loop through the text files

txt = []
txt.append('Ocean Beach North.txt')
txt.append('Ocean Beach South.txt')
txt.append('Half Moon Bay.txt')
txt.append('Pescadero.txt')
txt.append('Davenport.txt')
txt.append('Santa Cruz.txt')

for i in range(len(txt)):
	parse_txt(txt[i])

