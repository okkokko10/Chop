from Vector import Vector

class Line:
    def __init__(self,a,b,segment=0):                #   segment: 0: a-b 1: -a-b 2: a-b- 3: -a-b-
        self.segment=segment
        self.a=Vector(a)
        self.b=Vector(b)
        self.direction=self.a-self.b
        if self.direction==Vector(0,0):
            self.polynomialType=2
            self.polynomialConstant=0
            self.polynomialSlope=0
        elif self.direction.x==0:
            self.polynomialType=1
            self.polynomialSlope=0
            self.polynomialConstant=self.a.x
        else:
            self.polynomialType=0 
            self.polynomialSlope = self.direction.y/self.direction.x
            self.polynomialConstant=-self.polynomialSlope*self.a.x +self.a.y
                #y=(a.x-b.x)/(a.y-b.y) *(x-a.x)+a.y      y=k*x -k*a.x+a.y   <-- incorrect maybe
    def Intersection(self,other):
        if (self.polynomialSlope==other.polynomialSlope and self.polynomialType==other.polynomialType) or (self.polynomialType==2 or other.polynomialType==2):
            return False
        else:
            if self.polynomialType+other.polynomialType==0:
                x=(self.polynomialConstant-other.polynomialConstant)/(-self.polynomialSlope+other.polynomialSlope)
                y=self.polynomialSlope*x+self.polynomialConstant
            else:
                if self.polynomialType==1 and other.polynomialType==0:
                    x=self.polynomialConstant
                    y=other.polynomialSlope*x+other.polynomialConstant
                    #x=(y-other.polynomialConstant)/other.polynomialSlope
                elif self.polynomialType==0 and other.polynomialType==1:
                    x=other.polynomialConstant
                    y=self.polynomialSlope*x+self.polynomialConstant
                    #x=(y-self.polynomialConstant)/self.polynomialSlope
            a=Vector(x,y)
            if (self.InBounds(a)) and (other.InBounds(a)):
                return a
            else:
                return False
    @staticmethod
    def Polynomial(slope,constant,vertical,edgeRectangle=((0,0),(1,1))):
        if vertical:
            return Line((constant,edgeRectangle[1][1]),(constant,edgeRectangle[1][1]),3)
        else:
            a=Line((edgeRectangle[0][0],0),(edgeRectangle[0][0],1),3)
            c=Line((edgeRectangle[1][0],0),(edgeRectangle[1][0],1),3)
            b=Line((0,0),(0,0),3)
            b.polynomialSlope=slope
            b.polynomialConstant=constant
            b.polynomialType=0
            return Line(b.Intersection(a),b.Intersection(c),3)
    def Extended(self,edgeRectangle=((0,0),(1,1))):
        if self.segment==0:
            return self
        a=Line.Polynomial(self.polynomialSlope,self.polynomialConstant,self.polynomialType,edgeRectangle)
        # if self.segment==1:
        #     a.b=self.b
        # elif self.segment==2:
        #     a.a=self.a
        return a
    def InRectangle(self,point):
        return ((self.a.x<=point.x<=self.b.x) or (self.b.x<=point.x<=self.a.x)) and ((self.a.y<=point.y<=self.b.y) or (self.b.y<=point.y<=self.a.y))
    def InBounds(self,point):
        c=(self.a-self.b)
        if self.segment==3:
            return True
        if self.segment==1 or self.segment==0:
            if 0>(point-self.b)*c:
                return False
        if self.segment==2 or self.segment==0:
            if 0>(self.a-point)*c:
                return False
        return True
    def Ends(self):
        if self.segment==0:
            return [self.a,self.b]
        elif self.segment==1:
            return [None,self.b]
        elif self.segment==2:
            return [None,self.a]
        else:
            return [None,None]