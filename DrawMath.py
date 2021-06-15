from Vector import *
import math
import pygame
import numpy as np
import os.path
pygame.init()

class View:
    def __init__(self,equations=[],scale=100,size=(400,400),accuracy=10):
        self.equations=equations
        self.surface=pygame.Surface(size)
        self.eqSurface=self.surface.copy()
        self.visibleRect=[[0,0],[0,0]]
        self.scale=scale
        self.accuracy=accuracy
        self.colorType=0
        self.mouse=(0,0)
        self.mouseLast=None
    def update(self,highlight=None,need=False):
        if need:
            self.Draw()
        self.surface=self.eqSurface.copy()
        self.drawHighlight()
    def drawHighlight(self):
        if self.mouseLast:
            pygame.draw.rect(self.surface,(100,150,200),self.HighlightRect(),1)
            # points=(a,(a[0],b[1]),b,(b[0],a[1]))
            # pygame.draw.polygon(self.surface,(100,200,150),points,1)
            #print(self.coordinate(self.mouse))
    def HighlightRect(self):
        b=Vector([max(Vector(self.mouse)-Vector(self.mouseLast))]*2)*2
        a=Vector(self.mouseLast)-b/2
        return a,b
    def start(self):
        self.Draw()
    def Draw(self):
        self.eqSurface.fill((0,0,0))
        for k in self.equations:
            k.DrawEquation(self.eqSurface,self.visibleRect,self.scale,self.accuracy,self.colorType)
    def Zoom(self):
        a=self.HighlightRect()[1][0]
        self.Move(self.mouseLast)
        self.scale*=self.surface.get_width()/a
    def Move(self,pos,pixel=True):
        if pixel:
            self.visibleRect[0]=list(self.coordinate(pos))
        else:
            self.visibleRect[0]=list(pos)
    def coordinate(self,pos):
        x=(pos[0]-(self.surface.get_width()/2))/self.scale+self.visibleRect[0][0]
        y=-(pos[1]-(self.surface.get_height()/2))/self.scale+self.visibleRect[0][1]
        return x,y
    def save(self):
        pygame.image.save(self.surface,os.path.join('Pictures','New.bmp'))

        
class Equation:
    def __init__(self,equation,XeqY=True,color=(lambda x :bool(x)*(100,200,200))):
        self.equation=equation
        self.XeqY=XeqY      # whether the equation can be expressed as y=f(x)
        self.color=color
    def Redraw(self,center,scale,size,accuracy=10,colorType=0):
        surf=pygame.Surface(size) #rectangle[1][0]*scale//1,rectangle[1][1]*scale//1))
        px=pygame.PixelArray(surf)
        if self.XeqY:
            for i in range(surf.get_width()):
                x=(i-size[0]/2)/scale+center[0]
                a=(self.equation(x)-center[1])*scale+size[1]/2
                if isinstance(a,(float,int)) and 0<a<size[1]:
                    px[i,-int(a)]=self.color(a)
        elif True:
            for ix in range(size[0]):
                for iy in range(size[1]):
                    x=(ix-(size[0]/2))/scale+center[0]
                    y=(iy-(size[1]/2))/scale+center[1]
                    ans=self.equation(x,y,accuracy)
                    px[ix,-iy]=self.color(ans,accuracy,colorType)
            # for i in range(size[1]//2):
            #     px[:,i]=px[:,-i]
        px.close()
        self.surface=surf
    def DrawEquation(self,surface,visibleRect,scale,accuracy=10,colorType=0):
        self.Redraw(visibleRect[0],scale,surface.get_size(),accuracy,colorType)
        self.surface.set_colorkey((0,0,0))
        surface.blit(self.surface,(0,0))



class Screen:
    def __init__(self,view):
        self.view=view
        self.display=pygame.display.set_mode((800,800))
        self.start()
        self.MainLoop()
    def toView(self,pos):
        return pos[0]*self.view.surface.get_width()/self.display.get_width(),pos[1]*self.view.surface.get_height()/self.display.get_height()
    def MainLoop(self):
        run=True
        while run:
            change=False
            delay=pygame.time.delay(300)
            for event in pygame.event.get():
                #print(event)
                if event.type==pygame.QUIT:
                    run=False
                # if event.type==pygame.MOUSEMOTION:
                #     self.MouseMotion(event.__dict__['pos'],event.__dict__['rel'])
                # if event.type==pygame.MOUSEBUTTONDOWN:
                #     self.MouseDown(event.__dict__['pos'],event.__dict__['button'])
                # if event.type==pygame.MOUSEBUTTONUP:
                #     self.MouseUp(event.__dict__['pos'],event.__dict__['button'])
                if event.type==pygame.KEYDOWN:
                    a=event.__dict__['key']
                    if a==100:
                        self.view.visibleRect[0][0]+=200/self.view.scale
                    elif a==97:
                        self.view.visibleRect[0][0]-=200/self.view.scale
                    elif a==115:
                        self.view.visibleRect[0][1]-=200/self.view.scale
                    elif a==119:
                        self.view.visibleRect[0][1]+=200/self.view.scale
                    elif a==113:
                        self.view.scale*=2
                    elif a==101:
                        self.view.scale/=2
                    elif a==114:
                        self.view.save()
                    elif a==116:
                        self.view.colorType=(self.view.colorType+1)%3
                    change=True
                #print(event)
                if event.type==pygame.MOUSEBUTTONDOWN:
                    pos=event.__dict__['pos']
                    a=event.__dict__['button']
                    if a==1:
                        if self.view.mouseLast:
                            self.view.Zoom()
                            self.view.mouseLast=None
                            change=True
                        else:
                            self.view.mouseLast=self.toView(pos)
                    elif a==3:
                        self.view.Move(self.toView(pos))
                        change=True
                    elif a==5:
                        self.view.accuracy+=2
                        change=True
                    elif a==4:
                        self.view.accuracy-=2
                        change=True
                    if self.view.accuracy<0:
                        self.view.accuracy=0
                if event.type==pygame.MOUSEMOTION:
                    pos=event.__dict__['pos']
                    self.view.mouse=self.toView(pos)
            self.update(delay,change)
            pygame.display.update()
    def start(self):
        self.view.start()
    def update(self,delay,need):
        self.display.fill((50,50,50))
        self.view.update(need=need)
        self.display.blit(pygame.transform.scale(self.view.surface,self.display.get_size()),(0,0))


def Mandelbrot(x,y,extra=30):
    c=complex(x,y)
    z=complex(0,0)
    for i in range(extra):
        z=z**2+c
        if z.imag**2+z.real**2>4:
            return i
    return extra
def MandelbrotColor(x,extra,colorType):
    if x==extra:
        return (0,0,0)
    else:
        if colorType==0:
            a=x*255/extra//1
            return (a,a,a)
        elif colorType==1:
            r=(x)*4
            g=(x%4)*60
            b=(x%13)*16
            return r,g,b
        elif colorType==2:
            a= x**(1/2)*20
            b=x%2 *100
            return (b,a,a)
def Circle(x,y,extra):
    return (x**2+y**2-4)<0 and (((x)**2-y)*20//1==0 or (x**2+y**2-3.5)>0)

def SinColor(x,extra,colorType):
    return (255*(abs(x)) ,0,0)
def SinXsinYx(x,y,extra):
    return math.sin(math.pi*x)*math.sin(math.pi*y)

# A=Equation(lambda x: math.sin(x))
# B=Equation(lambda x: 0)
# C=Equation(lambda x: x)
# D=Equation(Mandelbrot,0,MandelbrotColor)
# E=Equation(Circle,0)
# m=View([D],100,(400,400),50)
# # m.update(need=1)
# # m.save()
# Screen(m)

A=Equation(SinXsinYx,0,SinColor)
m=View([A])
Screen(m)