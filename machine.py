import random
from itertools import combinations
from shapely.geometry import LineString, Point, Polygon

from collections import Counter


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
                
        if len(self.check_triangle(self.drawn_lines)) > 0:               # 현재 턴에 삼각형을 만들 수 있는 선분이 있으면 그 중 랜덤 반환

            return random.choice(self.check_triangle(self.drawn_lines))
        else:                                                            # 없으면 

            # 초반 선분들끼리 만나지 않게 선분 만들기
            available = [[point1, point2] for (point1, point2) in list(combinations(self.whole_points, 2)) if self.check_availability([point1, point2], self.drawn_lines)]        
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
                
                second_available = []

                for second_line in available:
                    
                    dlc = self.drawn_lines.copy()
                    dlc.append(second_line)

                    i = 0
                    while len(self.check_triangle(dlc)) > 0 :

                        l = random.choice(self.check_triangle(dlc))
                        dlc.append(l)
                        i = i + 1
                    
                    if i % 2 == 0:
                        second_available.append(second_line)


                if len(second_available) > 0:

                    return random.choice(second_available)
                
                else:

                    return random.choice(available)


            
    # 현재 턴에 삼각형을 만들 수 있는 선분을 반환
    def check_triangle(self, drawn_lines):

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
                if one_condition == True and self.check_availability(l_candidate, drawn_lines) :      # 삼각형 내부에 점이 없고 check_availability 조건을 만족하면 통과

                    new_list.append([element for element, count in l_counter.items() if count == 1])                  

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

    
