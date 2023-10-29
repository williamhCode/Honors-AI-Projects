import collections
import math

import funcs as f

#p = transformed points
#o =  original points
Polygon = collections.namedtuple('Polygon',['p','pos','angle','o']) 

# using Separated Axis Theorem
def overlap_SAT(polygon1, polygon2):
	poly1 = polygon1
	poly2 = polygon2

	for shape in range(2):
		if shape == 1:
			poly1 = polygon2
			poly2 = polygon1

		for a in range(len(poly1.p)):
			b = (a+1) % len(poly1.p)
			axisProj = f.Vec2(-(poly1.p[b].y - poly1.p[a].y), poly1.p[b].x - poly1.p[a].x)

			min_r1, max_r1 = math.inf, -math.inf
			for point in poly1.p:
				q = point.x * axisProj.x + point.y * axisProj.y
				min_r1 = min(min_r1, q)
				max_r1 = max(max_r1, q)

			min_r2, max_r2 = math.inf, -math.inf
			for point in poly2.p:
				q = point.x * axisProj.x + point.y * axisProj.y
				min_r2 = min(min_r2, q)
				max_r2 = max(max_r2, q)

			if not(max_r2 >= min_r1 and max_r1 >= min_r2):
				return False

	return True

# checking edge intersection
def overlap_edge(polygon1, polygon2):
	poly1 = polygon1
	poly2 = polygon2

	for a in range(len(poly1.p)):
		line_r1s = poly1.p[a]
		line_r1e = poly1.p[(a + 1) % len(poly1.p)]

		for b in range(len(poly2.p)):
			line_r2s = poly2.p[b]
			line_r2e = poly2.p[(b + 1) % len(poly2.p)]

			h = (line_r2e.x - line_r2s.x) * (line_r1s.y - line_r1e.y) - (line_r1s.x - line_r1e.x) * (line_r2e.y - line_r2s.y)
			if h == 0:
				continue
			t1 = ((line_r2s.y - line_r2e.y) * (line_r1s.x - line_r2s.x) + (line_r2e.x - line_r2s.x) * (line_r1s.y - line_r2s.y)) / h
			t2 = ((line_r1s.y - line_r1e.y) * (line_r1s.x - line_r2s.x) + (line_r1e.x - line_r1s.x) * (line_r1s.y - line_r2s.y)) / h

			if (t1 >= 0 and t1 < 1 and t2 >= 0 and t2 < 1):
				return True, (line_r2s, line_r2e)

	return False, None

def transform_vector(xy, pos, degrees):
	x, y = xy
	posx, posy = pos
	radians = math.radians(degrees)

	xx = x * math.cos(radians) - y * math.sin(radians) + posx
	yy = x * math.sin(radians) + y * math.cos(radians) + posy

	return xx, yy

def calc_poly_points(polygon):
	return Polygon(tuple(f.Vec2(*transform_vector(point, polygon.pos, polygon.angle)) for point in polygon.o), polygon.pos, polygon.angle, polygon.o)
	# return Polygon(tuple(transform_vector(point,polygon.pos,polygon.angle) for point in polygon.o) if field=='p' else item for item, field in zip(polygon, polygon._fields))

def calc_polys_points(polygons):
	return tuple(map(calc_poly_points, polygons))

def convertPoints(points):
	return tuple(f.Vec2(x,-y) for x,y in points)