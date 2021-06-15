import pygame
from Vector import Vector
from Line import Line
from Polygon import Polygon
        
class Screen:
    def __init__(self,size=(100,100)):
        self.canvas=pygame.display.set_mode(size)
        self.Clear()
    def DrawLine(self,line,color,width=1):
        a=line.a
        b=line.b
        if line.segment!=0:
            c=line.Extended(((0,0),(self.canvas.get_size())))
            a=c.a
            b=c.b
        pygame.draw.line(self.canvas,color,a.Round(),b.Round(),width)
    def DrawPolygon(self,polygon,color):
        pygame.draw.polygon(self.canvas,color[len(color)-1],polygon.vertices)
        for i in range(len(polygon.edges)):
            self.DrawLine(polygon.edges[i],color[i%(len(color)-1)],1)
            #self.DrawCircle(polygon.vertices[i],1,color[i%3])
        
    def DrawCircle(self,point,radius,color):
        pygame.draw.circle(self.canvas,color,point.Round(),radius)
    def Clear(self):
        col=(0,0,0)
        self.canvas.fill(col)

class State:
    def __init__(self):
        self.lastMouse=(0,0)
        self.screen=Screen((1200,800))
        self.lastClick=Vector()
        self.lines=[]
        self.points=[]
        self.polygons=[]
        self.polygonCreationTrail=[]
        #self.AddPolygon([Vector(0,0),Vector(600,0),Vector(600,600),Vector(0,600)])
    def update(self,delay):
        self.screen.Clear()
        col=(100,100,100)
        for i in self.lines:
            col=(100,100,200)
            self.screen.DrawLine(i,col)
        for i in self.points:
            col=(100,200,100)
            self.screen.DrawCircle(i,5,col)
        col=[(100,0,0),(100,100,0),(0,100,0),(0,100,100),(0,0,100),(100,0,100),(150,150,150)]
        for i in self.polygons:
            self.screen.DrawPolygon(i,col)
    def MouseMotion(self,pos,rel):
        self.mousePos=Vector(pos)
        self.mouseRel=Vector(rel)
        # self.MouseDown(self.mousePos,1)
        # self.MouseUp(self.mouseRel+self.mousePos,1)
    def MouseDown(self,pos,button):
        #pos=(pos[0]//40*40,pos[1]//40*40)
        if button==1:
            self.lastClick=pos
        elif button==3:
            if len(self.polygonCreationTrail)>2:
                self.AddPolygon(self.polygonCreationTrail)
                self.polygonCreationTrail.clear()
                self.points.clear()
        elif button==4:
            self.SeparatePolygons(pos,-10)
        elif button==2:
            self.polygonCreationTrail.append(Vector(pos))
            self.points.append(Vector(pos))
        elif button==5:
            self.SeparatePolygons(Vector(pos))

    def MouseUp(self,pos,button):
        #pos=(pos[0]//40*40,pos[1]//40*40)
        if button==1:
            self.CutPolygons(Line(self.lastClick,pos,0))
    def AddLine(self,line):
        a=[]
        for i in self.lines:
            b=line.Intersection(i)
            if b:
                if isinstance(b,list):
                    a.extend(b)
                else:
                    a.append(b)
        self.lines.append(line)
        self.points.extend(a)
        self.CutPolygons(line)
    def CutPolygons(self,cutter):
        buffer=[]
        removeBuffer=[]
        for i in self.polygons:
            b=i.Cutter(cutter)
            if b:
                buffer.extend(b)
                removeBuffer.append(i)
        for i in removeBuffer:
            self.polygons.remove(i)
        self.polygons.extend(buffer)
    def AddPolygon(self,vertices):
        self.polygons.append(Polygon(vertices))
    def SeparatePolygons(self,pos,amount=10):
        for i in self.polygons:
            i.Move(Vector(0,0)+(i.center-pos).Normalize()*amount)





        

def MainLoop(state):
    run=True
    while run:
        delay=pygame.time.delay(100)
        for event in pygame.event.get():
            #print(event)
            if event.type==pygame.QUIT:
                run=False
            if event.type==pygame.MOUSEMOTION:
                state.MouseMotion(event.__dict__['pos'],event.__dict__['rel'])
            if event.type==pygame.MOUSEBUTTONDOWN:
                state.MouseDown(event.__dict__['pos'],event.__dict__['button'])
            if event.type==pygame.MOUSEBUTTONUP:
                state.MouseUp(event.__dict__['pos'],event.__dict__['button'])
            OverrideControls(event,state)
        state.update(delay)
        pygame.display.update()

def OverrideControls(event,state):
    '''button:
    1:rshift press down to save pos, release to Cut polygons
    2:<   add a point to a not yet created polygon
    3:>   create a polygon if there are more than 2 points created with button 2
    4:^   pull polygons
    5:v   push polygons 
    '''
    if event.type==pygame.KEYDOWN:
        pos=state.mousePos
        key=event.__dict__['key']
        possibilities={
            pygame.K_RSHIFT:1,
            pygame.K_LEFT:2,
            pygame.K_RIGHT:3,
            pygame.K_UP:4,
            pygame.K_DOWN:5,
        }
        if key in possibilities:
            button=possibilities[key]
            state.MouseDown(pos,button)
    elif event.type==pygame.KEYUP:
        pos=state.mousePos
        key=event.__dict__['key']
        if key==pygame.K_RSHIFT:
            state.MouseUp(pos,1)

S=State()

MainLoop(S)