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
		self.length = self.x ** 2 + self.y ** 2 + self.z ** 2

	def normalize(self):
		length = self.length ** 0.5
		self.x = self.x / length
		self.y = self.y / length
		self.z = self.z / length
		return self

	def __str__(self):
		return ' '.join(list(map(str, [self.x, self.y, self.z])))

	def __mul__(self, other):
		return self.x * other.x + self.y * other.y + self.z * other.z


class Point:
	def __init__(self, arr):
		self.x = float(arr[0])
		self.y = float(arr[1])
		self.z = float(arr[2])

	def __str__(self):
		return ' '.join(list(map(str, [self.x, self.y, self.z])))

	def __eq__(self, other):
		return self.x == other.x and self.y == other.y and self.z == other.z


class Point2D:
	def __init__(self, arr):
		self.x = arr[0]
		self.y = arr[1]

	def __str__(self):
		return ' '.join(list(map(str, [self.x, self.y])))

	def l(self, pad):
		self.x -= pad
		return self
	def r(self, pad):
		self.x += pad
		return self
	def u(self, pad):
		self.y -= pad
		return self
	def b(self, pad):
		self.y += pad
		return self


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


class Plain:
	def __init__(self, start):
		k1 = 1 / (3 * (start.x ** 2 + start.y ** 2 + start.z ** 2))
		self.A = start.x * k1
		self.B = start.y * k1
		self.C = start.z * k1
		point_1 = Point([1 / self.A, 0, 0])
		point_2 = Point([0, 1 / self.B, 0])
		point_3 = Point([0, 0, 1 / self.C])
		k2 = 1 / (self.A * start.x + self.B * start.y + self.C * start.z)
		self.O = Point([k2 * start.x, k2 * start.y, k2 * start.z])
		self.v1 = Vector(self.O, point_3).normalize()
		v = Vector(point_1, point_2)
		if v * self.v1 != 0:
			alpha = v * self.v1
			v.x = v.x - self.v1.x * alpha
			v.y = v.y - self.v1.y * alpha
			v.z = v.z - self.v1.z * alpha
		self.v2 = v.normalize()

	def projection(self, p, start):
		x = start.x - p.x
		y = start.y - p.y
		z = start.z - p.z
		k = (1 - p.x * self.A - p.y * self.B - p.z * self.C) / (self.A * x + self.B * y + self.C * z)
		return Point([p.x + k * x, p.y + k * y, p.z + k * z])

	def obj_projection(self, obj, start):
		ans = []
		for edge in obj.edge:
			ans.append([self.projection(edge[0], start), self.projection(edge[1], start)])
		return ans

	def coord(self, p):
		vp = Vector(self.O, p)
		y = vp * self.v1
		x = vp * self.v2
		return Point2D([x, y])


def entry_form(data, kwargs):
	cube = Cube(100)
	start = Point([200, 420, 190])
	plain = Plain(start)
	edge_list = plain.obj_projection(cube, start)
	pad = 10

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

	cub_vert = [
				plain.coord(edge_list[0][0]).r(10).u(5), plain.coord(edge_list[0][1]).u(10).l(5),
				plain.coord(edge_list[1][1]).l(20).b(15), plain.coord(edge_list[3][1]).l(25).b(5),
				plain.coord(edge_list[2][1]).r(5).b(10), plain.coord(edge_list[4][1]).r(5).u(5),
				plain.coord(edge_list[6][1]).l(5).b(20), plain.coord(edge_list[7][1]).u(10).l(10)
				]

	yield '<input name="answer" type="hidden" />'
	yield f'<svg version="1.1" class="plot_area" width="{max_x - min_x}" height="{max_y - min_y}" overflow="visible" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">'
	yield f'<g class="cube" transform="translate({-min_x} {-min_y})">'
	for edge in edge_list:
		if edge[0] == plain.O:
			yield f'<line class="dotted_line" x1="{plain.coord(edge[0]).x}" y1="{plain.coord(edge[0]).y}" x2="{plain.coord(edge[1]).x}" y2="{plain.coord(edge[1]).y}" />'
		else:
			yield f'<line class="line" x1="{plain.coord(edge[0]).x}" y1="{plain.coord(edge[0]).y}" x2="{plain.coord(edge[1]).x}" y2="{plain.coord(edge[1]).y}" />'
		yield f'<circle class="point" num="{edge_list.index(edge)}" cx="{(plain.coord(edge[0]).x + plain.coord(edge[1]).x) / 2}" cy="{(plain.coord(edge[0]).y + plain.coord(edge[1]).y) / 2}" r="5" />'

	for num in data['vert']:
		yield f'<text x="{cub_vert[num - 1].x}" y="{cub_vert[num - 1].y}"> {data["vert_name"][data["vert"].index(num)]} </text>'

	yield '</g>'
	yield '</svg>'

def validate(data, answer):
	return ' '.join(list(map(str, data['correct']))) == answer
