import random
from shapely.geometry import LineString, Point, Polygon

from itertools import chain, combinations, product
from collections import Counter
from collections import deque
from anytree import Node, RenderTree, PostOrderIter


class Counter_depth: # call by ref
    def __init__(self,counter):
        self.counter = counter
        
def organize_points(point_list):
        point_list = sorted(point_list, key=lambda x: (x[0], x[1]))
        return point_list
        

class Config:
    def __init__(self, key: Counter_depth):
        self.key = key.counter  # 루트는 1이고 자식은 차례대로 1씩 증가한 키값을 갖는다
        self.triangle = 0  # 해당 노드에서 새로 완성된 삼각형의 갯수
        self.isMax = True  # max값을 취해야하는 노드인지
        self.value = 0 # value 리프노드의 값이 중요하고 리프까지 가져가기 위한 값
        self.line = [] # [(x1,y1),(x2,y2)] 해당 노드가 그리는 엣지 점의 좌표
        self.drawn_lines= [] # 해당 노드에서 그려진 라인들
        self.available = []  # 해당 노드에서 다음에 그릴 수 있는 라인들
        
def InsertNode(key : Counter_depth, parent=None):
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





AVAIL_LIMIT = 9
DEPTH_LIMIT = AVAIL_LIMIT




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

        available = [[point1, point2] for (point1, point2) in list(combinations(self.whole_points, 2)) if self.check_availability([point1, point2], self.drawn_lines)] 

        if len(available) < AVAIL_LIMIT:
            # root node init
            c = Counter_depth(1)
            rconf = Config(c)
            rconf.drawn_lines = self.drawn_lines
            root = InsertNode(c)
            # root.config.drawn_lines = copy.copy(self.drawn_lines)
            # root.config.available = copy.copy(available)
            root.config.drawn_lines = self.drawn_lines[:]
            root.config.available = available[:]
            
            #dq
            dq = deque()
            dq.append(root)
            
            # minMaxDq = deque()
            
            #tree expansion
            # 나중에 삼각형안에 도트있는지도 고려해야함  // 고려함
            # 5개일때는 되는데 10개점인경우 너무 오래걸림
            while dq:
                curNode = dq.pop()
                if curNode.depth < DEPTH_LIMIT:
                    for l in curNode.config.available:
                        ct = check_triangle(l, curNode.config.drawn_lines,self.triangles,self.whole_points)
                        if ct == -1:
                            continue
                        newNode : Node = InsertNode(c,curNode)
                        newNode.config.line = l
                        # newNode.config.drawn_lines = copy.copy(curNode.config.drawn_lines)
                        newNode.config.drawn_lines = curNode.config.drawn_lines[:]
                        newNode.config.drawn_lines.append(l)
                        # newNode.config.available = [[point1, point2] for (point1, point2) in list(combinations(self.whole_points, 2)) if self.check_availability([point1, point2], newNode.config.drawn_lines)]
                        line_string = LineString(l)
                        for i in curNode.config.available:
                            # if len(list(set([i[0], i[1], l[0], l[1]]))) == 3: # 끝에서 만나는선분은 크로스하지않는다
                            #     continue
                            # elif not bool(line_string.intersection(LineString(i))): # 크로스하지 않는 경우의 선분만 자식의 available로 넘겨줌
                            #     newNode.config.available.append((i[0],i[1]))
                                
                            if bool(line_string.intersection(LineString(i)) and len(list(set([i[0], i[1], l[0], l[1]]))) != 3): # 서로겹치는데 점에서 만나는게 아닌 경우
                                continue
                            else:
                                newNode.config.available.append((i[0],i[1]))
                            
                        newNode.config.triangle = ct
                        # newNode의 isMax가 True면 ct를 빼고 False면 ct를 더한값을 계속 가져가기
                        if newNode.config.isMax:
                            newNode.config.value = curNode.config.value - ct
                        else:
                            newNode.config.value = curNode.config.value + ct
                        dq.append(newNode)
            
            for node in PostOrderIter(root):
                if node.parent is None:  # root 예외처리
                    continue
                if node.config.isMax:
                    node.parent.config.value = min(node.config.value, node.parent.config.value)
                else:
                    node.parent.config.value = max(node.config.value, node.parent.config.value)
            
            print(root.config.value)
            tmp = -10000
            minMaxLine=[]
            # for i in root.children:
            #     if root.config.value == i.config.value:
            #         print("#1 minmax")
            #         return i.config.line
            
            for i in root.children:
                if tmp < i.config.value:
                    tmp = i.config.value
                    minMaxLine = i.config.line
                    
            print("#1 minmax")
            return minMaxLine
            

            # nextMinMax = set()
            # # min-max
            # # curNode가 Max이면 parent는 min값을 가져야함
            # while minMaxDq or nextMinMax:
            #     curNode = minMaxDq.popleft()
            #     if curNode.parent is None:  # root 예외처리
            #         continue
            #     if curNode.config.isMax:
            #         curNode.parent.config.value = min(curNode.config.value, curNode.parent.config.value)
            #     else:
            #         curNode.parent.config.value = max(curNode.config.value, curNode.parent.config.value)
            #     nextMinMax.add(curNode.parent)
                
                

        # elif len(self.check_triangle(self.drawn_lines)) > 0:               # 현재 턴에 삼각형을 만들 수 있는 선분이 있으면 그 중 랜덤 반환

        #     return random.choice(self.check_triangle(self.drawn_lines))
        
        # else:
        else:
            print("not triangle, too huge nodes")


            #if len(self.available_triangle(self.drawn_lines)) > 0:               # 현재 턴에 삼각형을 만들 수 있는 선분이 있으면 그 중 랜덤 반환
                              
            two_triangle = []           # 삼각형 2개 만드는 선분 리스트
            one_triangle = []           # 삼각형 1개 만드는 선분 리스트
            minus_triangle = []         # 삼각형 1개를 만들시 다음에 상대가 2개를 만드는 선분 리스트

            for l in self.available_triangle(self.drawn_lines):
                if check_triangle(l, self.drawn_lines, self.triangles, self.whole_points) == 2:         # 삼각형을 만드는 선분이 삼각형 2개를 만들면 two_triangle에 l 추가
                    two_triangle.append(l)
                    
                else:
                    dlc1 = self.drawn_lines.copy()  
                    dlc1.append(l)                                                                      # 삼각형을 1개 만드는 선분을 그려진 선 리스트 복사본에 추가
                    for l2 in self.available_triangle(dlc1):                                            # 그려진 선 리스트 복사본에서 삼각형을 만들 수 있는 선분들 중에
                        if check_triangle(l2, dlc1, self.triangles, self.whole_points) == 2:            # 삼각형 2개를 만드는 놈이 있으면 minus_triangle에 l 추가
                            minus_triangle.append(l)
                            break

                    if l not in minus_triangle:                                                         # l이 minus_triangle에 없으면 one_triangle에 l 추가
                        one_triangle.append(l)


            if len(two_triangle) > 0:                                   # 삼각형 2개를 만드는 선분이 있을시 그 중 랜덤 초이스

                return random.choice(two_triangle)                      
            elif len(one_triangle) > 0:

                return random.choice(one_triangle)
            else:                                                            # 없으면 

                # 초반 선분들끼리 만나지 않게 선분 만들기
                    
                first_available = available.copy()      # available copy 생성

                # 중복 좌표가 있을시 후보에서 제외 
                for first_line in available:                                                        
            
                    for l in self.drawn_lines:
                        if len(list(set([first_line[0], first_line[1], l[0], l[1]]))) == 3:
                            first_available.remove(first_line)
                            break
                
                
                if len(first_available) > 0:   # 겹치지 않는 선분이 있으면 그 중에서 랜덤 초이스

                    return random.choice(first_available)
                
                # 겹치지 않는 선분이 없으면 삼각형을 짝수로 만들 수 있는 선분 중에 랜덤 초이스
                else:                           
                    
                    second_available = []                   # 후보 리스트 생성
                    not_second_available = []               # 후보가 아닌 리스트 생성
                    available_copy = available.copy()
                    available_copy = [sublist for sublist in available_copy if sublist not in minus_triangle]           # 가능한 선분 중 minus_triangle 원소는 제외
                    available_copy2 = [sorted(sublist, key=lambda x: (x[0], x[1])) for sublist in available_copy]       # 선분 조합 정렬
                    

                    for second_line in available_copy2:
                        
                        if second_line not in second_available and second_line not in not_second_available:     # 선분 후보가 후보랑 후보가아닌 리스트면 검사 
                        
                            dlc2 = self.drawn_lines.copy()       # 임시 그려진 선분 리스트 생성
                            dlc2.append(second_line)             # 임시 그려진 선분 리스트에 second line 추가

                            i = 0                               # i 만들어진 삼각형의 개수
                            while len(self.available_triangle(dlc2)) > 0 :   # second line 추가 된 상태에서 삼각형이 만들어질 수 있는 선분이 있으면

                                l = random.choice(self.available_triangle(dlc2))     # 그 중 랜덤 선택
                                dlc2.append(l)                                   # 임시 그려진 선분 리스트에 추가
                                i = i + 1                                       # 삼각형의 개수 + 1 
                            
                            if i % 2 == 0:                                      # 삼각형의 개수가 짝수이면
                                
                                line_set = [sublist for sublist in dlc2 if sublist not in self.drawn_lines]      # 새로 생긴 선분집합
                                
                

                                for j in line_set:
                                    if j not in second_available:             # 후보 리스트에 선분이 없으면
                                        second_available.append(j)            # 후보 리스트에 추가
                            else:
                                
                                line_set = [sublist for sublist in dlc2 if sublist not in self.drawn_lines]      # 새로 생긴 선분집합
                                
                            

                                for j in line_set:
                                    if j not in not_second_available:           # 후보가 아닌 리스트에 선분이 없으면
                                        not_second_available.append(j)          # 후보가 아닌 리스트에 추가

                    if len(second_available) > 0:                           # 후보 리스트가 있으면 그 중 랜덤 반환

                        return random.choice(second_available)
                    
                    elif len(not_second_available) > 0:

                        return random.choice(not_second_available)
                    else:

                        return random.choice(minus_triangle)


            
    # 현재 턴에 삼각형을 만들 수 있는 선분을 반환
    def available_triangle(self, drawn_lines):

        new_list = []       #삼각형 생성 후보 리스트 생성

        for (l1, l2) in list(combinations(drawn_lines, 2)):        # 그려진 선분의 2개를 뽑는 조합
            p_comb = list(set([l1[0], l1[1], l2[0], l2[1]]))            # 중복 좌표 제외 리스트
            p_comb.sort()                                               # 중복 좌표 제외 리스트 정렬
            
            #and LineString(p_comb).is_simple

            if len(p_comb) == 3 and p_comb not in self.triangles :      # 좌표가 3개이고 삼각형에 없으면 통과
             
                triangle = Polygon(list(set([l1[0], l1[1], l2[0], l2[1]])))     # 삼각형 생성


                # 삼각형 내부에 점이 있는지 판단    
                one_condition = True
                for p in self.whole_points:                             
                    point_to_check = Point(p)
                    if triangle.contains(point_to_check):                       # 삼각형 내부에 점이 있으면 one_condition = False
                        one_condition = False                                   
                        break
                
                l_counter = Counter([l1[0], l1[1], l2[0], l2[1]])               
                l_candidate = [element for element, count in l_counter.items() if count == 1]

                # 삼각형 후보 리스트 append
                if one_condition == True and self.check_availability(l_candidate, drawn_lines) and l_candidate not in new_list:      # 삼각형 내부에 점이 없고 check_availability 조건을 만족하면 통과
                    
                    new_list.append(l_candidate)                  

        return new_list

        
    
    def check_availability(self, line, drawn_lines):
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
        for l in drawn_lines:
            if len(list(set([line[0], line[1], l[0], l[1]]))) == 3:
                continue
            elif bool(line_string.intersection(LineString(l))):
                condition3 = False

        # Must be a new line
        condition4 = (line not in drawn_lines)

        if condition1 and condition2 and condition3 and condition4:
            return True
        else:
            return False    
