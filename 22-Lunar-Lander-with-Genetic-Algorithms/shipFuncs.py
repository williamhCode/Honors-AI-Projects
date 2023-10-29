import collections
import math

import funcs as f

Ship = collections.namedtuple('Ship',['pos','vel','angle','isAccel','crashed'])

gravityAccel = 100/60
engineAccel = 300/60
turnSpeedConst = 120/60

def rotate_vector(xy, degrees):
	x, y = xy
	radians = math.radians(degrees)

	xx = x * math.cos(radians) - y * math.sin(radians)
	yy = x * math.sin(radians) + y * math.cos(radians)

	return xx, yy

def cal_turnSpeed(isRight, isLeft):
	turnSpeed = 0
	if isRight:
		turnSpeed += turnSpeedConst
	if isLeft:
		turnSpeed -= turnSpeedConst

	return turnSpeed

def cal_accel(ship, isUp):
	if(isUp):
		xAccel, yAccel = rotate_vector((0,-engineAccel),ship.angle)
	else:
		xAccel, yAccel = 0, 0
	yAccel += gravityAccel

	return (xAccel, yAccel)

def update_ships(ships, isUps, isRights, isLefts):
	return tuple(Ship(f.Vec2(ship.pos.x+ship.vel.x/60, ship.pos.y+ship.vel.y/60), f.Vec2(*map(lambda a,b:a+b,ship.vel,cal_accel(ship,isUp))), ship.angle+cal_turnSpeed(isRight,isLeft), True if isUp else False, ship.crashed) for ship,isUp,isRight,isLeft in zip(ships,isUps,isRights,isLefts))

def update_ships_crashed(ships, isUps, isRights, isLefts, crashData):
	return tuple(Ship(f.Vec2(ship.pos.x+ship.vel.x/60, ship.pos.y+ship.vel.y/60) if crashed==-1 else f.Vec2(*ship.pos), f.Vec2(*map(lambda a,b:a+b,ship.vel,cal_accel(ship,isUp))) if crashed==-1 else f.Vec2(*ship.vel), ship.angle+cal_turnSpeed(isRight,isLeft) if crashed==-1 else ship.angle, (True if isUp else False) if crashed==-1 else False, crashed) for ship,isUp,isRight,isLeft,crashed in zip(ships,isUps,isRights,isLefts,crashData))
