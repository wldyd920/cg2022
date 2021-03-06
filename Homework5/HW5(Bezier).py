"""
Modified on Feb 20 2020
@author: lbg@dongseo.ac.kr
"""

import pygame
from sys import exit
import numpy as np
import math
import time


pygame.init()

width = 800
height = 600
screen = pygame.display.set_mode((width, height), 0, 32)
pygame.display.set_caption("Homework3")
  
# Define the colors we will use in RGB format
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
BLUE =  (  0,   0, 255)
GREEN = (  0, 255,   0)
RED =   (255,   0,   0)
YELLOW = (255, 255, 0)
GRAY = (115, 115, 115)

large_font = pygame.font.SysFont(None, 72)
small_font = pygame.font.SysFont(None, 36)

pts = [] 
knots = []
count = 0
# screen.blit(background, (0,0))
# screen.fill(WHITE)

# https://kite.com/python/docs/pygame.Surface.blit
clock= pygame.time.Clock()


################################################# Functions ###################################################

def drawPoint(pt, color='GREEN', thick=1):
    # pygame.draw.line(screen, color, pt, pt)
    pygame.draw.circle(screen, color, pt, thick)

def drawPoints(pts, color='GREEN', thick=3):
    for i in pts:
        pygame.draw.circle(screen, BLUE, i, 5)
        pygame.draw.circle(screen, WHITE, i, 1)

def drawPolylines(color='GREEN', thick=3):
    if(len(pts) < 2): return
    for i in range(len(pts)-1):
        # drawLine(pts[i], pts[i+1], color)
        pygame.draw.line(screen, color, pts[i], pts[i+1], thick)

def CFS(pt0, pt1, color='GREEN', thick=1):
    # Coordinate-free System (with constraint, a0 = 1-a1 , a1 >= 0)
    for a in range(1000):
        a = a/1000
        c = (1-a)*pt0 + a*pt1
        drawPoint(c, color, thick)

def Euclidean(pt0, pt1):
    # Euclidean Coordinate System (without constraint)
    x0 = pt0[0]
    y0 = pt0[1]
    x1 = pt1[0]
    y1 = pt1[1]
    for x in np.arange(0, 1000):
        if (y1-y0) != 0 and (x1-x0) != 0 and (x-x0) !=0 :
            y = (y1-y0)/(x1-x0)*(x-x0)+y0
            xy = np.array([x,y])
            drawPoint(xy)
    for y in np.arange(0,1000):
        if (x1-x0) != 0 and (y1-y0) != 0 and (y-y0) != 0 :
            x = (x1-x0)/(y1-y0)*(y-y0)+x0
            xy = np.array([x,y])
            drawPoint(xy)

def DrawLines(pts):
    for i in range(len(pts)):
        if i == len(pts)-1 :
            pass
        else:
            pt0=pts[i]
            pt1=pts[i+1]
            CFS(pt0,pt1)

def ContinuousLine(pts):
    for i in range(len(pts)):
        for j in range(len(pts)):
            if j <= i:
                pt0 = pts[i]
                pt1 = pts[j]
                Euclidean(pt0,pt1)
                # CFS(pt0,pt1)

def Barycentric(pts):
    if len(pts) > 2 :
        a = pts[-1]
        b = pts[-2]
        c = pts[-3]
        g = (a+b+c)/3
        pygame.draw.circle(screen, RED, g, 4)
        pygame.draw.circle(screen, WHITE, g, 1)
        centroid = small_font.render('Centroid : ({0},{1})'.format(g[0],g[1]), True, BLACK)
        screen.blit(centroid, (10, 40))
        CFS(g, a)
        CFS(g, b)
        CFS(g, c)
        CFS(a, b)
        CFS(b, c)
        CFS(c, a)

def mul(list):
    res = 1
    for i in list:
        res = i*res
    return res

def LagrangeInterpolation(pts, color='GREEN', thick=3):
    x_list=[]
    y_list=[]
    for i in range(len(pts)):
        xi = pts[i][0]
        yi = pts[i][1]
        x_list.append(xi)
        y_list.append(yi)
    for x in range(1000):
        # Lagrange Interpolation formula
        right_side=[]
        for i in range(len(y_list)):
            yi = y_list[i]
            xi = x_list[i]
            nume=[]
            deno=[]
            for j in range(len(x_list)):
                xj = x_list[j]
                if i != j:
                    nume.append(x-x_list[j])
                    deno.append(xi-xj)
            term = (mul(nume)/mul(deno))*yi
            right_side.append(term)
        y_hat = sum(right_side)
        # draw it 1000 times per y
        drawPoint((x,y_hat), thick=1)


def DrawController(pts, time_passed, t, b_list):
    pt0 = pts[-1]
    pt1 = pts[-2]

    # CFS(pt0,pt1)
    # Euclidean(pt0,pt1)
    # DrawLines(pts)
    # ContinuousLine(pts)
    # Barycentric(pts)
    # LagrangeInterpolation(pts)

# HW5 : implement cubic bezier
def Bezier(pts, time_passed, t, b1_list, color='GREEN', thick=1):
    if len(pts) >= 2:
        frame = time_passed/5000
        t = t + frame
        if t <= 1:
            pt0 = pts[-2]
            pt1 = pts[-1]
            b1 = ((1-t)*pt0)+(t*pt1)
            b1_list.append(b1)
        for b1 in b1_list:
            drawPoint(b1, color, thick)
    return t, b1_list , b1

def SquareBezier(pts, time_passed, t, b2_list):
    if len(pts) >= 3:
        pt0 = pts[-3]
        pt1 = pts[-2]
        pt2 = pts[-1]
        frame = time_passed/5000
        t = t + frame
        if t <= 1:
            m = ((1-t)*pt0)+(t*pt1)
            n = ((1-t)*pt1)+(t*pt2)
            CFS(m,n, 'GREEN')
            b2 = (1-t)**2*pt0 + 2*(1-t)*t*pt1 + t**2*pt2
            b2_list.append(b2)
        CFS(pt0, pt1, 'GRAY')
        CFS(pt1, pt2, 'GRAY')
        for b2 in b2_list:
            drawPoint(b2, 'RED', 2)
        t_img = small_font.render('t = {0}'.format(t), True, BLACK)
        screen.blit(t_img, (10, 40))
    return t, b2_list, b2

def CubicBezier(pts, time_passed, t, b3_list):
    if len(pts) == 4:
        pt0 = pts[-4]
        pt1 = pts[-3]
        pt2 = pts[-2]
        pt3 = pts[-1]
        frame = time_passed/5000
        t = t + frame
        if t <= 1:
            m = ((1-t)*pt0)+(t*pt1)
            n = ((1-t)*pt1)+(t*pt2)
            o = ((1-t)*pt2)+(t*pt3)
            CFS(m,n, 'GREEN')
            CFS(n,o, 'GREEN')
            p = (1-t)**2*pt0 + 2*(1-t)*t*pt1 + t**2*pt2
            q = (1-t)**2*pt1 + 2*(1-t)*t*pt2 + t**2*pt3
            CFS(p,q, 'YELLOW')
            b3 = (1-t)**3*pt0 + 3*(1-t)**2*t*pt1 + 3*(1-t)*t**2*pt2 + t**3*pt3
            b3_list.append(b3)
        CFS(pt0, pt1, 'GRAY')
        CFS(pt1, pt2, 'GRAY')
        CFS(pt2, pt3, 'GRAY')
        for b3 in b3_list:
            drawPoint(b3, 'RED', 2)
        t_img = small_font.render('t = {0}'.format(t), True, BLACK)
        screen.blit(t_img, (10, 40))
    return t, b3_list, b3


# Make sure to set proper "number of Minimum Points needed" that fits to the function which you are going to run.
LeastPoints = 4

################################################# Class ##################################################

class Pt():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.pt = np.array([self.x, self.y])
        self.pts = pts
        self.button1 = button1
        self.button2 = button2
        self.button3 = button3
        self.pressed = pressed
        
        print("({0},{1})".format(self.x, self.y))
    
    def coordinate(self):
        return self.pt

    def create(self):
        pygame.draw.circle(screen, BLUE, self.pt, 5)
        pygame.draw.circle(screen, WHITE, self.pt, 1)
        
    def move(self, x, y):
        if (x,y) in "boundary of point" :
            self.x = x
            self.y = y
        elif (x,y) not in "boundary of point":
            pass

    def remove(self):
        pts.remove(self)
        del(self)
    
################################################ Run ##################################################

#Loop until the user clicks the close button.
done = False
pressed = 0
margin = 6
old_pressed = 0
old_button1 = 0
old_button3 = 0
Points = []
lines = []
t = 0
b_list = []

while not done:   
    # This limits the while loop to a max of 10 times per second.
    # Leave this out and we will use all CPU we can.
    time_passed = clock.tick(30)

    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pressed = -1            
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            pressed = 1
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            pressed = -3
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 3:
            pressed = 3           
        elif event.type == pygame.QUIT:
            done = True
        else:
            pressed = 0

    button1, button2, button3 = pygame.mouse.get_pressed()
    x, y = pygame.mouse.get_pos()
    pt = np.array([x, y])
    cursor_position_image = small_font.render('Mouse Position : ({0},{1})'.format(x,y), True, BLACK)
    
    # Left click
    if old_button1 == 0 and button1 == 1:
        Point = Pt(x, y)
        Point.create()
        Points.append(Point)
        pts.append(Point.coordinate())
        print(pts)
        # print("len:"+repr(len(pts))
        #      +" mouse x:"+repr(x)
        #      +" y:"+repr(y)
        #      +" button1:"+repr(button1)
        #      +" button3:"+repr(button3)
        #      +" pressed:"+repr(pressed)
        #      +" add pts ...")

    # Right click
    if old_button3 == 0 and button3 == 1 :
        Points = []
        pts = [] 
        knots = []
        count = 0
        t = 0
        b_list = []
        screen.fill(WHITE)
        # print("len:"+repr(len(pts))
        #      +" mouse x:"+repr(x)
        #      +" y:"+repr(y)
        #      +" button1:"+repr(button1)
        #      +" button3:"+repr(button3)
        #      +" pressed:"+repr(pressed)
        #      +" erase")

    # Do nothing
    else:
        # print("len:"+repr(len(pts))
        #      +" mouse x:"+repr(x)
        #      +" y:"+repr(y)
        #      +" button1:"+repr(button1)
        #      +" button3:"+repr(button3)
        #      +" pressed:"+repr(pressed))
        pass


################################################ Display ##################################################

    screen.fill(WHITE)

    drawPoints(pts)

    # DrawLines subject to the points
    if len(pts) >= LeastPoints:
        # DrawController(pts)
        # drawPolylines(GREEN, 1)
        # ContinuousLine(pts)
        # EveryLine(pts)
        # Barycentric(pts)
        # LagrangeInterpolation(pts)
    
        # t, b_list, b1 = Bezier(pts, time_passed, t, b_list)
        # t, b_list, b2 = SquareBezier(pts, time_passed, t, b_list)
        t, b_list, b3 = CubicBezier(pts, time_passed, t, b_list)

    screen.blit(cursor_position_image, (10, 10))
    
    # Go ahead and update the screen with what we've drawn.
    # This MUST happen after all the other drawing commands.
    pygame.display.update()
    old_button1 = button1
    old_button3 = button3
    old_pressed = pressed
    old_pts = pts
    
pygame.quit()

