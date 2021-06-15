import math

class Vector(tuple):
    def __new__(obj,x=0,y=0):
        if isinstance(x,(tuple,list)):
            return tuple.__new__(obj,x)
        return tuple.__new__(obj,(x,y))
    def __init__(self,x=0,y=0):
        self.x,self.y=self
    def __add__(self, other):
        return Vector(self[0]+other[0],self[1]+other[1])
    def __mul__(self,other):
        if isinstance(other, Vector):
            return self[0]*other[0]+self[1]*other[1]
        return Vector(self[0]*other,self[1]*other)
    def __rmul__(self,other):
        if isinstance(other,int) or isinstance(other,float):
            return Vector(self[0]*other,self[1]*other)
    def __truediv__(self,other):
        return self*(1/other)
    def __neg__(self):
        return Vector(-self[0],-self[1])
    def __sub__(self, other):
        return Vector(self[0]-other[0],self[1]-other[1])
    def __abs__(self):
        return (self[0]**2+self[1]**2)**0.5
    def Normalize(self):
        a=abs(self)
        if a!=0:
            return self/a
        else:
            return Vector(0,0)
    def __floordiv__(self,other):
        if isinstance(other,Vector):
            return self.Scale(other)
    def Scale(self,other):
        return Vector(self[0]*other[0],self[1]*other[1])
    @staticmethod
    def One():
        return Vector(1,1)
    def Round(self):
        return Vector(int(self[0]),int(self[1]))
    #added in Chop
    def Angle(self):
        return math.atan2(self[0],self[1])
    @staticmethod
    def Sum(parts):
        out=Vector(0,0)
        for i in parts:
            out+=i
        return out
    @staticmethod
    def Mean(parts):
        return Vector.Sum(parts)/len(parts)