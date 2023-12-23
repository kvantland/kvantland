def dist(p1, p2):
	return (p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2 + (p1.z - p2.z) ** 2

def to_point(num, r):
	bin_num = bin(num).split('b')[1]
	bin_num = '0' * (3 - len(bin_num)) + bin_num
	bin_arr = list(bin_num)
	for i in range(len(bin_arr)):
		bin_arr[i] = float(bin_arr[i]) * r
	return Point(bin_arr)

class Vector:
	def __init__(self, point_1, point_2):
		self.x = point_2.x - point_1.x
		self.y = point_2.y - point_1.y
		self.z = point_2.z - point_1.z
	def normalize(self):
		length = (self.x ** 2 + self.y ** 2 + self.z ** 2) ** 0.5
		self.x = self.x / length
		self.y = self.y / length
		self.z = self.z / length

class Point:
	def __init__(self, arr):
		self.x = float(arr[0])
		self.y = float(arr[1])
		self.z = float(arr[2])

	def __str__(self):
		return ' '.join(list(map(str, [self.x, self.y, self.z])))

class Point2D:
	def __init__(self, arr):
		self.x = arr[0]
		self.y = arr[1]

class Cube:
	def __init__(self, r):
		self.r = r
		edge = []
		for point_1 in range(8):
			for point_2 in range(point_1 + 1, 8):
				if (dist(to_point(point_1, r), to_point(point_2, r)) - r ** 2) < 10 ** -3:
					edge.append([to_point(point_1, r), to_point(point_2, r)])
		self.edge = edge

	def __str__(self):
		ans = ''
		for edge in self.edge:
			ans += ' '.join(list(map(str, [edge[0].x, edge[0].y, edge[0].z]))) + ' - ' + ' '.join(list(map(str, [edge[1].x, edge[1].y, edge[1].z])))
			ans += '\n'
		return ans



# Хорошие плоскости, проходящие через (a, 0, 0), (0, b, 0) и (0, 0, c)

class Plain:
	def __init__(self, point_1, point_2, point_3):
		self.A = 1 / point_1.x
		self.B = 1 / point_2.y
		self.C = 1 / point_3.z
		k = (self.A ** 2 + self.B ** 2 + self.C ** 2)
		self.O = Point([self.A / k, self.B / k, self.C / k])
		self.v1 = Vector(point_2, point_1)
		self.v2 = Vector(point_3, self.O)

	def projection(self, p):
		k = (1 - p.x * self.A - p.y * self.B - p.z * self.C) / (self.A ** 2 + self.B ** 2 + self.C ** 2)
		return Point([p.x + k * self.A, p.y + k * self.B, p.z + k * self.C])

	def obj_projection(self, obj):
		ans = []
		for edge in obj.edge:
			ans.append([self.projection(edge[0]), self.projection(edge[1])])
		return ans

	def coord(self, p):
		x = ((p.x - self.O.x) - (p.y - self.O.y) * (self.v2.x / self.v2.y)) / (self.v1.x - self.v1.y * (self.v2.x / self.v2.y))
		y = ((p.x - self.O.x) - x * self.v1.x) / self.v2.x
		return Point2D([x, y])

def entry_form(data, kwargs):
	A = Point([1, 0, 0])
	B = Point([0, 1.5, 0])
	C = Point([0, 0, 2])
	D = Point([1, 1, 1])
	cube = Cube(400)
	plain = Plain(A, B, C)
	edge_list = plain.obj_projection(cube)
	min_x = 10 ** 8
	min_y = 10 ** 8
	max_x = -1
	max_y = -1
	for edge in edge_list:
		min_x = min(plain.coord(edge[0]).x, min_x)
		min_x = min(plain.coord(edge[1]).x, min_x)
		min_y = min(plain.coord(edge[0]).y, min_y)
		min_y = min(plain.coord(edge[1]).y, min_y)
		max_x = max(plain.coord(edge[0]).x, max_x)
		max_x = max(plain.coord(edge[1]).x, max_x)
		max_y = max(plain.coord(edge[0]).y, max_y)
		max_y = max(plain.coord(edge[1]).y, max_y)

	yield f'<svg version="1.1" class="plot_area" width="{max_x - min_x}" height="{max_y - min_y}" overflow="visible" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">'
	yield f'<g class="cube" transform="translate({-min_x} {-min_y})">'
	for edge in edge_list:
		if edge[0].x == plain.O.x and edge[0].y == plain.O.y and edge[0].z == plain.O.z:
			yield f'<line class="dotted_line" x1="{plain.coord(edge[0]).x}" y1="{plain.coord(edge[0]).y}" x2="{plain.coord(edge[1]).x}" y2="{plain.coord(edge[1]).y}" />'
		else:
			yield f'<line class="line" x1="{plain.coord(edge[0]).x}" y1="{plain.coord(edge[0]).y}" x2="{plain.coord(edge[1]).x}" y2="{plain.coord(edge[1]).y}" />'
	yield '</g>'
	yield '</svg>'

def validate(data, answer):
	return True