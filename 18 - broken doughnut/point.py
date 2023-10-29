"""
Created on Thu Mar 18 09:31:20 2021

@author: williamhou
"""

class point3D:
    
    def __init__(self, point, label):
        self.point = point
        # null =- 1, top = 0, bottom = 1
        self.label = label
        
    def getColor(self):
        if(self.label == -1):
            return 'grey'
        if(self.label == 0):
            return 'red'
        if(self.label == 1):
            return 'blue'
        