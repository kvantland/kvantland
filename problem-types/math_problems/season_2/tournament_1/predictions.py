def validate(data, answer):
	try:
		boys_array = answer['boysChoosed']
		girls_array = answer['girlsChoosed']

		print('boys: ', boys_array)
		print('girls: ', girls_array)

		return len(boys_array) == 0 and len(girls_array) == 3
	except:
		return False