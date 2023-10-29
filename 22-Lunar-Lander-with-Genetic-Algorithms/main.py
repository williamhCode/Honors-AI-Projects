from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import uic

import threading
import time as t
import random

import shipFuncs as sf
import polygonFuncs as pf
import funcs as f


class Window(QMainWindow):
    # pushButton: QPushButton
    # pushButton_2: QPushButton
    # widget: QWidget
    # actionEnter_Full_Screen: QAction
    
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi('app.ui', self)
        self.setFixedSize(self.size())
        
        self.full = False

        self.gridLayout = QGridLayout(self.widget)
        self.gridLayout.setContentsMargins(0,0,0,0)

        self.frame = GraphicsFrame(self.widget)
        self.frame.setFocus()
        self.frame.setFocusPolicy(Qt.ClickFocus)
        self.setFocusProxy(self.frame)

        self.gridLayout.addWidget(self.frame, 0, 0, 1, 1)

        self.pushButton.clicked.connect(self.pushButtonPressed)
        self.pushButton_2.clicked.connect(self.pushButton_2Pressed)
        self.actionEnter_Full_Screen.triggered.connect(self.Enter_Full_Screen)

    def pushButtonPressed(self):
        if self.frame.mode == 'manual':
            self.frame.mode = 'auto'
            self.frame.resetManualMode()
            self.frame.resetAutoMode()
            self.pushButton_2.setText("Start")
        else:
            self.frame.mode = 'manual'
            self.frame.resetAutoMode()
            self.frame.resetManualMode()
            self.pushButton_2.setText("Reset")
        self.pushButton.setText('Mode: '+self.frame.mode)

    def pushButton_2Pressed(self):
        if self.frame.mode == 'manual':
            self.frame.resetManualMode()
        else:
            self.frame.startAutoLoop()
            if self.pushButton_2.text() == 'Start':
                self.pushButton_2.setText('Reset')
            else:
                self.pushButton_2.setText('Start')

    def Enter_Full_Screen(self):
        if self.full:
            self.showNormal()
            self.setFixedSize(1160, 739)
            self.frame.zoom = 0.7
            self.actionEnter_Full_Screen.setText('Enter Full Screen')
            self.frame.update()
            self.full = False
        else:
            
            self.frame.zoom = 1.027
            self.setFixedSize(1680, 1050)
            self.showFullScreen()
            self.actionEnter_Full_Screen.setText('Leave Full Screen')
            self.frame.update()
            self.full = True
            
        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())

    def closeEvent(self, event):
        self.frame.stopAutoTimer = True
        
    
class GraphicsFrame(QWidget):
    def __init__(self, container):
        super().__init__(container)

        self.panx = 0
        self.pany = 0
        self.zoom = 1

        self.starsImg = QPixmap('pics/stars.png')
        rect = QRect(2, 2, 1494, 934)
        self.starsImg = self.starsImg.copy(rect)

        points = (0,0),(0,190),(100,250),(200,350),(300,400),(400,400),(440,340),(500,340),(600,300),(700,250),(800,150),(950,150),(1050,190),(1110,280),(1130,300),(1200,300),(1600,190),(1600,0)
        points = pf.convertPoints(points)
        self.terrain = pf.Polygon(None, f.Vec2(0,950), 0, points)
        self.terrain = pf.calc_poly_points(self.terrain)
        
        self.shipImg = QPixmap('pics/ship.png')
        self.shipSize = 50
        self.ships = ()
        self.xRatio = self.shipSize/self.shipImg.width()
        self.yRatio = self.shipSize/self.shipImg.height()

        self.fuelLength = 30
        self.shipsFrames = ()
        self.shipFuelFrames = (0, 0.1, 0.3, 0.6, 1, 0.8)
        self.shipFuelFrames = tuple(map(lambda ratio:ratio*self.fuelLength, self.shipFuelFrames))
        self.fuelTimer = QTimer()
        self.fuelTimer.timeout.connect(self.fuelLoop)
        
        self.manualTimer = QTimer()
        self.manualTimer.timeout.connect(self.manualLoop)
        self.resetted = True
        self.manualEnd = -1		# None: -1, Landed: 0, Crashed: 1

        self.shipsGenes = ()

        self.stopAutoTimer = True

        self.isUps = ()
        self.isRights = ()
        self.isLefts = ()

        self.mode = 'manual'

        self.resetManualMode()
    
    def resetManualMode(self):
        self.manualTimer.stop()
        self.fuelTimer.stop()
        self.fuel = 1000
        self.score = 0
        self.ships = f.generate_ships((700,200), 1)
        self.shipsPolygons = f.generate_ship_polys(self.ships, self.shipSize)
        self.shipsPolygons = pf.calc_polys_points(self.shipsPolygons)
        self.shipsFrames = 0,
        self.isUps = False,
        self.isRights = False,
        self.isLefts = False,
        self.panx = self.pany = 0
        self.zoom = 1.027 if self.parent().parent().parent().isFullScreen() else 0.7
        self.manualEnd = -1
        self.update()
        self.resetted = True

    def resetAutoMode(self):
        self.fuelTimer.stop()
        self.stopAutoTimer = True

        self.shipAmount = 25
        self.genesAmount = 50

        self.ships = f.generate_ships((700,200), self.shipAmount)
        self.shipsPolygons = f.generate_ship_polys(self.ships, self.shipSize)
        self.shipsPolygons = pf.calc_polys_points(self.shipsPolygons)
        self.shipsFrames = [0,]*self.shipAmount
        self.shipsGenes = f.generate_random_genes(self.genesAmount, self.shipAmount)

        self.generation = 0
        self.landed = 0
        self.amountLanded = 0
        self.similiarGenerations = 0
        
    def startAutoLoop(self):
        self.resetAutoMode()
        try:
            if(self.autoTimer.is_alive()):
                return
        except Exception:
            pass
        self.autoTimer = threading.Thread(target=self.autoLoop)
        self.stopAutoTimer = False
        self.autoTimer.start()
        self.fuelTimer.start(1000/20)

    def rotate(self, img, angle):
        transform = QTransform().rotate(angle)
        return img.transformed(transform, Qt.SmoothTransformation)

    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        # painter.setRenderHint(QPainter.Antialiasing)
        painter.setRenderHint(QPainter.HighQualityAntialiasing)

        pen = QPen(Qt.white)
        pen.setWidth(1)
        painter.setPen(pen)

        painter.scale(self.zoom, self.zoom)
        # painter.translate(-self.panx / self.zoom, -self.pany / self.zoom)
        painter.translate(-self.panx, -self.pany)

        if self.mode == 'manual':
            shiftx = 1600 * ((self.ships[0].pos.x) // (1600))
            shifty = 950 * (self.ships[0].pos.y // (950))
        else:
            shiftx = shifty = 0

        for x in range(-1,2):
            for y in range(-1,2):
                rect = QRect(x*1600 + shiftx, y*950 + shifty, 1600, 950)
                painter.drawPixmap(rect, self.starsImg)

        for i, ship in enumerate(self.ships):
            # print(ship.crashed)
            if ship.crashed is not True:
                img = self.rotate(self.shipImg, ship.angle)
                rect = QRect(0, 0, img.width()*self.xRatio, img.height()*self.yRatio)
                rect.moveCenter(QPoint(ship.pos.x-1, ship.pos.y-1))
                painter.drawPixmap(rect, img)

                topLeft = tuple(map(lambda x,y:x+y, ship.pos, sf.rotate_vector((-self.shipSize/10,self.shipSize/3),ship.angle)))
                topRight = tuple(map(lambda x,y:x+y, ship.pos, sf.rotate_vector((self.shipSize/10,self.shipSize/3),ship.angle)))
                bottom = tuple(map(lambda x,y:x+y, ship.pos, sf.rotate_vector((0,self.shipSize/3+self.shipFuelFrames[self.shipsFrames[i]]),ship.angle)))
                triangle = QPolygon([QPoint(*topLeft),QPoint(*topRight),QPoint(*bottom)])
                painter.drawPolygon(triangle)

        # for polygon in self.shipsPolygons:
        # 	for a in range(len(polygon.p)):
        # 		b = (a+1) % len(polygon.p)
        # 		painter.drawLine(polygon.p[a].x, polygon.p[a].y, polygon.p[b].x, polygon.p[b].y)
        
        pen = painter.pen()
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setBrush(Qt.black)

        for x in range(-1,2):
            terrain = QPolygon()
            for a in range(len(self.terrain.p)):
                terrain.append(QPoint(self.terrain.p[a].x + x*1600 + shiftx, self.terrain.p[a].y))
            painter.drawPolygon(terrain)

        painter.resetTransform()
        painter.scale(self.zoom, self.zoom)
    
        painter.setFont(QFont("Courier", 20, 10))
        if self.mode == 'auto':
            painter.drawText(50, 50, 'Landed: ' + str(self.amountLanded))
            painter.drawText(50, 100, 'Generation: ' + str(self.generation))
            painter.drawText(50, 150, 'Similiar Generation: ' + str(self.similiarGenerations))
        else:
            painter.drawText(50, 50, 'Fuel: ' + str(self.fuel))
            painter.drawText(50, 100, 'Score: ' + str(self.score))

        if(self.manualEnd == -1):
            return 

        painter.setFont(QFont("Courier", 30, 10))	
        if(self.manualEnd == 0):
            painter.drawText(700, 200, "SHIP LANDED")
        else:
            painter.drawText(570, 200, "SHIP CREATED A 10 MILE CRATER")

    def autoLoop(self):
        frameRate = 1000
        notLanded = 0
        while True:
            crashData = [-1]*self.shipAmount
            fitnessData = [0]*self.shipAmount
            surfFlatData = [0]*self.shipAmount
            iteration = 0

            frame_cap = 1.0/frameRate
            time = t.time()
            unprocessed = 0

            self.landed = 0
            while True:
                can_render = False
                time_2 = t.time()
                passed = time_2 - time
                unprocessed += passed
                time = time_2

                while(unprocessed >= frame_cap):
                    unprocessed -= frame_cap
                    can_render = True
                    if self.stopAutoTimer:
                        return
                
                if can_render:
                    if(iteration//6 < self.genesAmount-1):
                        self.isUps, self.isRights, self.isLefts = f.genes_to_inputs(self.shipsGenes, iteration//6)
                    else:
                        self.isUps, self.isRights, self.isLefts = f.empty_input(self.shipsGenes)
                    self.ships = sf.update_ships_crashed(self.ships, self.isUps, self.isRights, self.isLefts, crashData)
                    self.shipsPolygons = f.update_ship_polys(self.ships, self.shipsPolygons)

                    for i in range(len(self.ships)):
                        shiftx = 1600 * (self.ships[i].pos.x // 1600)
                        terrain = f.dup_terrain(self.terrain, shiftx)
                        overlap, edge = pf.overlap_edge(self.shipsPolygons[i], terrain)

                        if overlap:
                            surf_is_flat = f.is_surf_flat(edge)
                            ship_is_in_edge = f.is_ship_in_edge(self.shipsPolygons[i], edge)
                            angle = f.norm_angle(self.ships[i].angle)
                            if surf_is_flat and ship_is_in_edge and -5 < angle < 5 and self.ships[i].vel.y < 100:
                                crashData[i] = False
                                frameRate = 60
                            else:
                                crashData[i] = True
                            surfFlatData[i] = surf_is_flat
                            fitnessData[i] = f.calc_fitness(self.ships[i], crashData[i], surf_is_flat)
                            self.shipsFrames = tuple(0 if x==i else frame for x,frame in enumerate(self.shipsFrames))

                    if -1 not in crashData:
                        break

                    iteration += 1
                    self.update()
            for crashed in crashData:
                if crashed == False:
                    self.landed += 1
            if abs(self.amountLanded-self.landed) < 5 and self.landed > 0 and self.amountLanded > 0:
                self.similiarGenerations += 1
            else:
                self.similiarGenerations = 0
            if self.similiarGenerations == 5:
                self.stopAutoTimer = True
            self.amountLanded = self.landed
            if frameRate == 60 and self.landed == 0:
                notLanded += 1
            if notLanded == 2:
                notLanded = 0
                frameRate = 1000

            self.ships = sf.update_ships_crashed(self.ships, self.isUps, self.isRights, self.isLefts, crashData)
            self.update()
            
            parent_index_1 = fitnessData.index(max(fitnessData))
            fitnessData[parent_index_1] = -1000
            parent_index_2 = fitnessData.index(max(fitnessData))
            gab = self.genesAmount
            self.genesAmount += 1
            shipsGenes = tuple((self.shipsGenes[parent_index_1][i] if i<random.random()*gab else self.shipsGenes[parent_index_2][i] if i < gab else random.randint(0,3) for i in range(self.genesAmount)) for _ in range(self.shipAmount))
            chances = tuple(0.05 for i in range(self.shipAmount))
            self.shipsGenes = tuple(map(f.mutate_genes, shipsGenes, chances))

            self.ships = f.generate_ships((700,200), self.shipAmount)
            self.shipsPolygons = f.generate_ship_polys(self.ships, self.shipSize)
            self.shipsPolygons = pf.calc_polys_points(self.shipsPolygons)
            self.shipsFrames = [0,]*self.shipAmount
            self.generation += 1
            
    def is_out_bounds(self, ship, pan):
        panx, pany = pan
        xmin, xmax, ymin, ymax = 300 + panx, 1300 + panx, 100 + pany, 550 + pany
        shiftx = min(ship.pos.x - xmin, 0) + max(ship.pos.x - xmax, 0)
        shifty = min(ship.pos.y - ymin, 0) + max(ship.pos.y - ymax, 0)
        return shiftx, shifty

    def manualLoop(self):
        if self.fuel == 0:
            self.ships = sf.update_ships(self.ships, (False,), self.isRights, self.isLefts)
        else:
            self.ships = sf.update_ships(self.ships, self.isUps, self.isRights, self.isLefts)
        self.shipsPolygons = f.update_ship_polys(self.ships, self.shipsPolygons)
        if self.ships[0].isAccel:
            self.fuel -= 1
        
        shiftx = 1600 * (self.ships[0].pos.x // 1600)
        terrain = f.dup_terrain(self.terrain, shiftx)
        overlap, edge = pf.overlap_edge(self.shipsPolygons[0], terrain)

        if overlap:
            self.manualTimer.stop()
            self.fuelTimer.stop()

            surf_is_flat = f.is_surf_flat(edge)
            ship_is_in_edge = f.is_ship_in_edge(self.shipsPolygons[0], edge)
            angle = f.norm_angle(self.ships[0].angle)
            if surf_is_flat and ship_is_in_edge and -5 < angle < 5 and self.ships[0].vel.y < 80:
                self.manualEnd = 0
                self.score += 100
            else:
                self.manualEnd = 1
            self.shipsFrames = 0,
        # shiftx, shifty, = self.is_out_bounds(self.ships[0], (self.panx / self.zoom, self.pany / self.zoom))
        shiftx, shifty, = self.is_out_bounds(self.ships[0], (self.panx, self.pany))
        self.panx += shiftx 
        self.pany = min(self.pany + shifty, 0)

        self.update()

    def startManuaLoop(self):
        if not self.manualTimer.isActive():
            if self.fuel == 0:
                self.resetManualMode()
            else:
                fuel = self.fuel
                score = self.score
                self.resetManualMode()
                self.fuel = fuel
                self.score = score
        if self.resetted and not self.manualTimer.isActive():
            self.manualTimer.start(1000/60)
            self.resetted = False

    def fuelLoop(self):
        self.shipsFrames = tuple(map(lambda ship, frame: (frame+1 if frame<5 else frame-1) if ship.isAccel else (frame-1 if frame>0 else 0), self.ships, self.shipsFrames))

    def keyPressEvent(self, event):
        if self.mode == 'manual':
            if not event.isAutoRepeat():
                if event.key() == Qt.Key_Up:
                    self.startManuaLoop()
                    self.isUps = True,
                    self.fuelTimer.start(1000/20)
                if event.key() == Qt.Key_Right:
                    self.startManuaLoop()
                    self.isRights = True,
                if event.key() == Qt.Key_Left:
                    self.startManuaLoop()
                    self.isLefts = True,

    def keyReleaseEvent(self, event):
        if self.mode == 'manual':
            if event.key() == Qt.Key_Up:
                self.isUps = False,
            if event.key() == Qt.Key_Right:
                self.isRights = False,
            if event.key() == Qt.Key_Left:
                self.isLefts = False,

    def wheelEvent(self, event):
        steps = event.angleDelta().y() / 100
        if(steps > 0):
            self.toZoom(event.x(), event.y(), True, abs(steps) + 1)
        elif(steps < 0):
            self.toZoom(event.x(), event.y(), False, abs(steps) + 1)

        self.update()

    def toZoom(self, mousex, mousey, direction, intensity):
        pre_zoom = self.zoom

        if(direction):
            self.zoom *= intensity
        else:
            self.zoom /= intensity

        self.panx = ((mousex + self.panx * pre_zoom)/pre_zoom * self.zoom - mousex) / self.zoom
        self.pany = ((mousey + self.pany * pre_zoom)/pre_zoom * self.zoom - mousey) / self.zoom

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
    
    
