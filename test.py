import random
from collections import deque
from anytree import Node, RenderTree


class Counter: # call by ref
    def __init__(self,counter):
        self.counter = counter
        

class Config:
    def __init__(self, key: Counter):
        self.key = key.counter  # 루트는 1이고 자식은 차례대로 1씩 증가한 키값을 갖는다
        self.isMax = True  # max값을 취해야하는 노드인지
        self.line = [] # [(x1,y1),(x2,y2)] 해당 노드가 그리는 엣지 점의 좌표 루트는 []
        self.drawn_lines= [] # 해당 노드에서 그려진 [[(x1,y1),(x2,y2)],[(x1,y1),(x2,y2)],[(x1,y1),(x2,y2)]]
        self.available=[]
        self.value = 0 # value 리프노드의 값이 중요하고 리프까지 가져가기 위한 값
        self.triangle = 0  # 해당 노드에서 새로 완성된 삼각형의 갯수



c = Counter(1)

def InsertNode(key : Counter, parent=None):
    newConf = Config(key)
    newNode = Node(name = str(key.counter), parent=parent,config=newConf)
    if parent is not None:
        newNode.config.isMax = not parent.config.isMax
    key.counter+=1
    return newNode


#config만들어서 넣지말고 넣고나서 만들자 계속 config만드는거 따로하기 귀찮음



# root = InsertNode()
# s0 = InsertNode(parent=root)
# s0b = InsertNode(parent=s0)
# s0a = InsertNode(parent=s0)
# s1 = InsertNode(parent=root)
# s1a = InsertNode(parent=s1)
# s1b = InsertNode(parent=s1)
# s1c = InsertNode(parent=s1)
# s1ca = InsertNode(parent=s1c)


# print(RenderTree(root))
# print(root.children)



# class Node:
#     def __init__(self, parent, key: int):
#         self.key = key  # 루트는 1이고 자식은 차례대로 1씩 증가한 키값을 갖는다
#         self.children = []
#         self.triangle = 0  # 해당 노드에서 새로 완성된 삼각형의 갯수
#         self.isMax = True  # max값을 취해야하는 노드인지
#         self.parent = parent # 부모의 키값 None 이면 루트
#         self.value = 0 # value 리프노드의 값이 중요하고 리프까지 가져가기 위한 값
#         self.line = [] # [(x1,y1),(x2,y2)] 해당 노드가 그리는 엣지 점의 좌표
#         self.drawn_lines= [] # 해당 노드에서 그려진 라인들
        
        
# class Counter: # call by ref
#     def __init__(self,counter):
#         self.counter = counter
        
# def organize_points(self, point_list):
#         point_list.sort(key=lambda x: (x[0], x[1]))
#         return point_list
        
# # root노드에 key값을 갖는 노드를 생성해서 자식으로 넣기, 새로 생성한 노드를 반환
# def insert(parent:Node, key: int):
#     if parent is None:
#         newNode = Node(None, key)
#         newNode.isMax = True
#     else:
#         newNode = Node(parent, key)
#         newNode.isMax = not parent.isMax
#         parent.children.append(newNode)
    
#     return newNode
    
# def insert_wrapper(parent, counter:Counter):
#     counter.counter+=1
#     newNode = insert(parent, counter.counter)
#     return newNode

# # init counter, root
# c = Counter(1)
# r = insert(None, c.counter)
# dq = deque()

# while dq:
#     current = dq.pop()
#     # for 가능한 엣지에대해
#     newNode = insert_wrapper(current,c)
#     dq.append(newNode)



        
    