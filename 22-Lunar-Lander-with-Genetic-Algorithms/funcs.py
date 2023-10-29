import collections
import random

import polygonFuncs as pf
import shipFuncs as sf

Vec2 = collections.namedtuple('Vec2',['x','y'])

def update_ship_polys(ships, polygons):
	polygons = tuple(pf.Polygon(polygon.p, ship.pos, ship.angle, polygon.o) for ship, polygon in zip(ships, polygons))
	return pf.calc_polys_points(polygons)

def norm_angle(angle):
	angle = angle % 360
	if angle > 180: angle -= 360
	return angle

def is_surf_flat(edge):
	return True if edge[1].y - edge[0].y == 0 else False

def is_ship_in_edge(shipPolygon, edge):
	return True if shipPolygon.p[3].x >= edge[0].x and shipPolygon.p[2].x <= edge[1].x else False

def dup_terrain(terrain, xtrans):
	return pf.calc_poly_points(pf.Polygon(None, Vec2(xtrans,0), terrain.angle, terrain.p))

def generate_ship_polys(ships, shipSize):
	return tuple(pf.Polygon(None, ship.pos, ship.angle, (Vec2(-shipSize/2.2, -shipSize/2.5), Vec2(shipSize/2.2, -shipSize/2.5), Vec2(shipSize/2.2, shipSize/2.5), Vec2(-shipSize/2.2,shipSize/2.5))) for ship in ships)

def generate_ships(pos, count):
	return tuple(sf.Ship(Vec2(*(pos)), Vec2(0,0), 0, False, False) for _ in range(count))

# Nothing: 0, Up: 1, Right: 2, Left: 3
def generate_random_genes(length, count):
	return tuple(tuple(random.randint(0,3) for _ in range(length)) for _ in range(count))

def genes_to_inputs(shipsGenes, iteration):
	return tuple(True if shipsGenes[i][iteration]==1 else False for i in range(len(shipsGenes))), tuple(True if shipsGenes[i][iteration]==2 else False for i in range(len(shipsGenes))), tuple(True if shipsGenes[i][iteration]==3 else False for i in range(len(shipsGenes)))

def empty_input(shipsGenes):
	list =  tuple(False for i in range(len(shipsGenes)))
	return list, list, list

def calc_fitness(ship, crashed, surf_is_flat):
	crashFitness = 0 if crashed else 100
	surfFlatFitness = 50 if surf_is_flat else 0
	speedFitnessY = -ship.vel.y/20 + 10
	speedFitnessX = -abs(ship.vel.x)/20 + 10
	angleFitness = -abs(norm_angle(ship.angle))/10 + 5
	return crashFitness + surfFlatFitness + speedFitnessY + speedFitnessX + angleFitness

def mutate_genes(genes, chance):
	return tuple(random.randint(0,3) if random.random()<chance else gene for gene in genes)