import random
from itertools import chain, combinations, product
from shapely.geometry import LineString, Point, Polygon
from collections import deque
from anytree import Node, RenderTree
import copy
        
class Counter: # call by ref
    def __init__(self,counter):
        self.counter = counter
        
def organize_points(point_list):
        point_list.sort(key=lambda x: (x[0], x[1]))
        return point_list
        

class Config:
    def __init__(self, key: Counter):
        self.key = key.counter  # 루트는 1이고 자식은 차례대로 1씩 증가한 키값을 갖는다
        self.triangle = 0  # 해당 노드에서 새로 완성된 삼각형의 갯수
        self.isMax = True  # max값을 취해야하는 노드인지
        self.value = 0 # value 리프노드의 값이 중요하고 리프까지 가져가기 위한 값
        self.line = [] # [(x1,y1),(x2,y2)] 해당 노드가 그리는 엣지 점의 좌표
        self.drawn_lines= [] # 해당 노드에서 그려진 라인들
        
def InsertNode(key : Counter, parent=None):
    newConf = Config(key)
    newNode = Node(name = str(key.counter), parent=parent,config=newConf)
    if parent is not None:
        newNode.config.isMax = not parent.config.isMax
    key.counter+=1
    return newNode

def check_triangle(line, drawn_lines, triangles, whole_points):
    point1 = line[0]
    point2 = line[1]
    
    point1_connected = []
    point2_connected = []
    
    for l in drawn_lines:
        if l==line: # 자기 자신 제외
            continue
        if point1 in l:
            point1_connected.append(l)
        if point2 in l:
            point2_connected.append(l)
    
    if point1_connected and point2_connected: # 최소한 2점 모두 다른 선분과 연결되어 있어야 함
        tri = 0
        for line1, line2 in product(point1_connected, point2_connected):
            triangle = organize_points(list(set(chain(*[line, line1, line2]))))
            if len(triangle) != 3 or triangle in triangles:  # 삼각형이 아니거나 이미 그려진 것의 경우
                continue
            
            for point in whole_points:
                if point in triangle:  # 삼각형에 있는 점은 넘어가고
                    continue
                if bool(Polygon(triangle).intersection(Point(point))): # 해당 삼각형을 그릴수없음 안에 점이있어서
                    return -1
            
            tri +=1
        
        return tri
    
    return 0
            
    

class MACHINE():
    """
        [ MACHINE ]
        MinMax Algorithm을 통해 수를 선택하는 객체.
        - 모든 Machine Turn마다 변수들이 업데이트 됨

        ** To Do **
        MinMax Algorithm을 이용하여 최적의 수를 찾는 알고리즘 생성
           - class 내에 함수를 추가할 수 있음
           - 최종 결과는 find_best_selection을 통해 Line 형태로 도출
               * Line: [(x1, y1), (x2, y2)] -> MACHINE class에서는 x값이 작은 점이 항상 왼쪽에 위치할 필요는 없음 (System이 organize 함)
    """
    def __init__(self, score=[0, 0], drawn_lines=[], whole_lines=[], whole_points=[], location=[]):
        self.id = "MACHINE"
        self.score = [0, 0] # USER, MACHINE
        self.drawn_lines = [] # Drawn Lines
        self.board_size = 7 # 7 x 7 Matrix
        self.num_dots = 0
        self.whole_points = []
        self.location = []
        self.triangles = [] # [(a, b), (c, d), (e, f)]

    def find_best_selection(self):
        available = [[point1, point2] for (point1, point2) in list(combinations(self.whole_points, 2)) if self.check_availability([point1, point2], self.drawn_lines)]  # point = (x1,y1), line=[(x1,y1),(x2,y2)]
        
        if len(self.drawn_lines)==0:
            return random.choice(available)
        
        tmp = copy.deepcopy(available)
        
        for l in available: # line=[(x1,y1),(x2,y2)]
            for d in self.drawn_lines:
                if len(set([l[0],l[1],d[0],d[1]]))==3:
                    tmp.remove(l)
                    break

        if tmp:
            return tmp[0]
        
        """-------------------------------------중반 시작-----------------------------------"""
        # root node init
        c = Counter(1)
        rconf = Config(c)
        rconf.drawn_lines = self.drawn_lines
        root = InsertNode(c)
        root.config.drawn_lines = copy.deepcopy(self.drawn_lines)
        root.config.available = copy.deepcopy(available)
        
        #dq
        dq = deque()
        dq.append(root)
        
        #tree expansion
        # 나중에 삼각형안에 도트있는지도 고려해야함  // 고려함
        while dq:
            curNode = dq.pop()
            for l in curNode.config.available:
                ct = check_triangle(l, curNode.config.drawn_lines,self.triangles,self.whole_points)
                if ct == -1:
                    continue
                newNode : Node = InsertNode(c,curNode)
                newNode.config.line = l
                newNode.config.drawn_lines = copy.deepcopy(curNode.config.drawn_lines)
                newNode.config.drawn_lines.append(l)
                newNode.config.available = [[point1, point2] for (point1, point2) in list(combinations(self.whole_points, 2)) if self.check_availability([point1, point2], newNode.config.drawn_lines)]
                newNode.config.triangle = ct
                newNode.config.value = curNode.config.value + ct
                dq.append(newNode)
                
        print(RenderTree(root))
        
        print("return #2")
        return random.choice(available)
    
    def check_availability(self, line, curDrawn_lines):
        line_string = LineString(line)

        # Must be one of the whole points
        condition1 = (line[0] in self.whole_points) and (line[1] in self.whole_points)
        
        # Must not skip a dot
        condition2 = True
        for point in self.whole_points:
            if point==line[0] or point==line[1]:
                continue
            else:
                if bool(line_string.intersection(Point(point))):
                    condition2 = False

        # Must not cross another line
        condition3 = True
        for l in curDrawn_lines:
            if len(list(set([line[0], line[1], l[0], l[1]]))) == 3:
                continue
            elif bool(line_string.intersection(LineString(l))):
                condition3 = False

        # Must be a new line
        condition4 = (line not in curDrawn_lines)

        if condition1 and condition2 and condition3 and condition4:
            return True
        else:
            return False    

    
