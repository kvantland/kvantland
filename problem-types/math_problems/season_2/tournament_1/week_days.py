def validate(data, answer):
	try:
		choosed_days = []
		day_index = 1

		for day in answer:
			if day['choosed']:
				choosed_days.append(day_index)
			day_index += 1

		return set(choosed_days) == set(data['correct'])
	except:
		return {'answer': "Unknown error"}