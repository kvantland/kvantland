def validate(data, answer):
	def get_dist(star_1, star_2):
		dist_x = abs(star_1['x'] - star_2['x'])
		dist_y = abs(star_1['y'] - star_2['y'])
		dist = dist_x ** 2 + dist_y ** 2
		return dist 
	
	try:
		active_stars = []

		for star in answer:
			if star['active'] == True:
				active_stars.append(star)
		print('here 1')
		
		if len(active_stars) != 4:
			return False
		
		print('here 2')
		
		first_star = active_stars[0]
		second_star = active_stars[1]
		third_star = active_stars[2]
		square_side = min(get_dist(first_star, second_star), get_dist(first_star, third_star))
		print(square_side)
		
		for star_1_index in range(len(active_stars)):
			right_stars = 0
			for star_2_index in range(len(active_stars)):
				if star_1_index == star_2_index:
					continue
				star_1 = active_stars[star_1_index]
				star_2 = active_stars[star_2_index]
				if abs(get_dist(star_1, star_2) - square_side) < 1:
					right_stars += 1
			print(right_stars, star_1_index)
			if right_stars < 2:
				return False

		return True
	except:
		return False