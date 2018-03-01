import xlsxwriter

def docToExcel(inferred_vectors, similar_vectors, title):
	"""
	take in a histogram list and write to Excel to plot
	@param: histogram - a list
	@return: None
	"""
	n = len(inferred_vectors)

	print ("Writing to Excel...")

	#create new excel workbook and worksheet
	workbook = xlsxwriter.Workbook(title + 'xlsx')
	worksheet = workbook.add_worksheet()

	#setup wanted text formatting options
	header = workbook.add_format({'bold': True, 'font_size': 12})

	#set worksheet to start in A1 cell
	row = 0
	col = 0

	
	##Write Histogram##

	worksheet.write(row, col, "Inferred Vector ID", header)
	col += 1
	worksheet.write(row, col, "Similar Vector ID", header)
	col + 1
	worksheet.write(row, col, "Cosine Similarity", header)

	col = 0
	row += 1



	try:
		for i in range(n):
			col = 0
			worksheet.write(row, col, inferred_vectors[i])
			col += 1
			worksheet.write(row, col, similar_vectors[i][index][0])
			col += 1
			worksheet.write(row, col, similar_vectors[i][index][1])
			row += 1

	except:
		print("ERROR WRITING TO EXCEL")


	workbook.close()

	print ("Done writing to Excel")
	print()