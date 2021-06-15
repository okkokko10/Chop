from Vector import Vector
from Line import Line

class Polygon:
    def __init__(self,vertices):
        self.vertices=vertices.copy()
        self.center=Vector.Mean(self.vertices)
        #self.vertices.sort(key=self.SortVertices)
        self.edges=[]
        self.FormEdges()
    def SortVertices(self,e):
        return (e-self.center).Angle()
    def FormEdges(self):
        self.edges.clear()
        for i in range(len(self.vertices)):
            self.edges.append(Line(self.vertices[i],self.vertices[(i+1)%len(self.vertices)]))
    def Move(self,amount):
        a=[]
        for i in self.vertices:
            a.append(i+amount)
        self.vertices=a
        self.center=self.center+amount
        self.FormEdges()
    def Intersection(self,other,countInside=False):
        out=[]
        for i in range(len(self.edges)):
            a=other.Intersection(self.edges[i])
            if a:
                if isinstance(a,list):
                    out.append((a,i))
                else:
                    out.append(([a],i))
        if len(out)!=0 and countInside:
            if (other.segment==0 or other.segment==1) and self.Inside(other.b):
                out.append(([other.b],out[0][1]))
            if (other.segment==0 or other.segment==2) and self.Inside(other.a):
                out.append(([other.a],out[0][1]))
        return out
    def PerimeterCut(self,line:Line):
        perimeter=[]    #list of all vertices and intersection points on the perimeter
        indices=[]      #of the point at the same index in perimeter, if an intersection: it's index on the line, starting from 1, if a vertex, 0
        for i in range(len(self.vertices)):
            indices.append(0)
            perimeter.append(self.vertices[i])
            a=line.Intersection(self.edges[i])
            if a:
                indices.append(1)
                perimeter.append(a)
        

        cutsUnsorted=[]
        for i in range(len(indices)):
            if indices[i]:
                cutsUnsorted.append(i)
        if len(cutsUnsorted)==0:
            return perimeter,indices,0      #when the line segment doesn't intersect the edges at all

        
        precision=0.01
        def sortCuts(e):
            return (line.b-line.a)*(perimeter[e]+perimeter[e-2]*precision-line.a*(1+precision))
        cutsSort=[]
        for k in cutsUnsorted:
            cutsSort.append([k,sortCuts(k)])
        #print(cutsSort)
        cuts=cutsUnsorted.copy()
        cuts.sort(key=sortCuts)
        
        # t1=(perimeter[cuts[0]]-line.b)
        # t2=(perimeter[cuts[0]-1]-line.b)
        # if t1.x*t2.y-t1.y*t2.x<0:
        #     t3=False
        # else:
        #     t3=True
        # t3=False
        # if t3:
        #     cuts.sort(key=sortCuts,reverse=True)
        #     cuts.reverse()
        
        


        shallowEnds=[False,False]
        for i in 0,1:
            a=line.Ends()[i]
            if a:
                if self.PointInPolygon(a)==1:
                    shallowEnds[i]=True

        for i in range(len(cuts)):
            indices[cuts[i]]=i+1-shallowEnds[0]

        if shallowEnds[0]:
            a=cuts[0]
            indices[a]=0
            indices.insert(a,0)
            indices.insert(a,0)
            perimeter.insert(a,perimeter[a])
            perimeter.insert(a+1,line.a)
        if shallowEnds[1]:
            a=cuts[-1]
            if cuts[-1]>cuts[0] and shallowEnds[0]:
                a+=2
            indices[a]=0
            indices.insert(a,0)
            indices.insert(a,0)
            perimeter.insert(a,perimeter[a])
            perimeter.insert(a+1,line.b)


        return perimeter,indices,len(cuts)
    @staticmethod
    def CutPieces(indices):
        """returns list of ordered lists containing indices of points on the perimeter"""
        groups=[[]]
        for i in range(len(indices)):
            groups[-1].append(i)
            if indices[i]:
                groups.append([i])
        if len(groups)>1:
            groups[0]=groups[-1]+groups[0]
            del groups[-1]
        else:
            return groups
        def opposite(e):
            return e-1+2*(e%2)
        def continuation(e):
            a=opposite(indices[e[-1]])
            for i in range(len(groups)):
                if indices[groups[i][0]]==a:
                    return i
        #print(groups)
        links=[]    #which groups are connected to each other
        for k in groups:
            links.append([continuation(k),True])
        linked=[]
        for i in range(len(links)):
            if links[i][1]:
                linked.append([])
                a=i
                while links[a][1]:
                    linked[-1].append(a)
                    links[a][1]=False
                    a=links[a][0]
        cutGroups=[]
        for i in range(len(linked)):
            cutGroups.append([])
            for k in linked[i]:
                cutGroups[-1].extend(groups[k])
        return cutGroups
    @staticmethod
    def FormPolygonPieces(perimeter,groups):
        newVertices=[]
        for k in groups:
            newVertices.append([])
            for k1 in k:
                newVertices[-1].append(perimeter[k1])
        newPolygons=[]
        for k in newVertices:
            newPolygons.append(Polygon(k))
        return newPolygons
    def Cutter(self,line:Line):
        a=self.PerimeterCut(line)
        if a[2]>0:
            b=Polygon.CutPieces(a[1])
            return Polygon.FormPolygonPieces(a[0],b)
    def Inside(self,point):
        return len(self.Intersection(Line(point,point+Vector(1,0),2)))%2==1
    def PointInPolygon(self,point):
        crossed=0
        for i in range(len(self.vertices)):
            a=self.vertices[i]-point
            b=self.vertices[(i+1)%len(self.vertices)]-point
            c=((a.x>0)!=(b.x>0))+((a.y>0)!=(b.y>0))
            if c:
                s=(a.y*b.x-a.x*b.y)
                if s>0:
                    sense=-1
                elif s<0:
                    sense=1
                else:
                    return 2
                crossed+=c*sense
        return (crossed!=0)
