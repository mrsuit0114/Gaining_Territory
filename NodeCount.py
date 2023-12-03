import tkinter as tk
import random
import networkx as nx
from tkinter import Tk, Canvas, Button, LEFT
from shapely.geometry import Point, LineString

class NodeCount(tk.Canvas):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.board_size = 6
        self.cell_size = 40
        self.outer_gap = 20
        self.nodes = set()  #클릭된 교차점 저장
        self.graph = nx.Graph()  #그래프 생성
        self.draw_board()

        #클릭
        self.bind("<Button-1>", self.on_click)

        #self.run_count = 0  # Run 클릭횟수 / 반복기능 

    def draw_board(self):
        board_size_pixels = self.board_size * self.cell_size
        total_size = board_size_pixels + 2 * self.outer_gap

        for i in range(self.board_size + 1):
            x = i * self.cell_size + self.outer_gap
            self.create_line(x, self.outer_gap, x, board_size_pixels + self.outer_gap)

        for j in range(self.board_size + 1):
            y = j * self.cell_size + self.outer_gap
            self.create_line(self.outer_gap, y, board_size_pixels + self.outer_gap, y)

    def on_click(self, event):
        #클릭된곳 계산ㄴ
        col = (event.x - self.outer_gap) // self.cell_size
        row = (event.y - self.outer_gap) // self.cell_size

        #노드 표시
        x = col * self.cell_size + self.outer_gap
        y = row * self.cell_size + self.outer_gap
        radius = 5
        node = self.create_oval(x - radius, y - radius, x + radius, y + radius, fill="red")

        #클릭된 교차점 저장
        self.nodes.add((col, row))
        self.graph.add_node((col, row))

    def calculate_edges(self):
        # 노드 순서 섞어주기
        shuffled_nodes = list(self.nodes)

        # 그린 셋 초기화
        drawn_edges = set()

        # 반복 횟수 지정 바꿔줘도 됨. 현재 100번.
        for _ in range(100):
            random.shuffle(shuffled_nodes)

            for i in range(len(shuffled_nodes)):
                node1 = shuffled_nodes[i]
                node2 = shuffled_nodes[(i + 1) % len(shuffled_nodes)]  #섞인 거에서 다음 노드 연결

                #그린 선 확인 전 새 선 drawn에 추가 
                new_edge1 = (node1, node2)
                new_edge2 = (node2, node1)

                    
                if len(self.nodes) > 1 and new_edge1 not in drawn_edges and new_edge2 not in drawn_edges and self.check_availability(node1, node2):
                    self.draw_edge(node1, node2)
                    drawn_edges.add(new_edge1)
                    drawn_edges.add(new_edge2)
                    #중복 노드 체크... print(f" {node1} -> {node2}")

        # 그릴 수 있는 엣지의 최대 수를 출력
        max_possible_edges = max(len(self.nodes) * (len(self.nodes) - 1) // 2, 0)  # 음수 확인
        num_edges = len(self.graph.edges)
        print(f"Number of lines: {num_edges}")


        #Repeat 런 카운트 / 반복 기능
        #self.run_count += 1

        # run 한번 하고 나서 자동으로 리셋 / 반복 기능 
        #if self.run_count == 1:
            #self.run_count = 0
            #self.reset_edges()

    def calculate_and_reset_multiple_times(self):
        # run - reset을 10번 반복.
        for _ in range(10):
            self.calculate_edges()

    def draw_edge(self, node1, node2):
        x1, y1 = node1
        x2, y2 = node2
        x1_px = x1 * self.cell_size + self.outer_gap
        y1_px = y1 * self.cell_size + self.outer_gap
        x2_px = x2 * self.cell_size + self.outer_gap
        y2_px = y2 * self.cell_size + self.outer_gap

        # 선 이미 존재하는지 확인
        if (node1, node2) not in self.graph.edges and (node2, node1) not in self.graph.edges:
            # 선 그리기
            self.create_line(x1_px, y1_px, x2_px, y2_px, tags="edge", fill="blue", width=3)

            # 그린 선으로 그래프 업데이트 
            self.graph.add_edge(node1, node2)

    def check_availability(self, node1, node2):
        line_string = LineString([node1, node2])

        # 크로스 X
        condition1 = all(LineString(line).crosses(line_string) is False for line in self.graph.edges)

        # 새 선이여야함 
        condition2 = (node1, node2) not in self.graph.edges and (node2, node1) not in self.graph.edges

        # 선 안에 노드 있으면 X
        condition3 = all(
            not Point(x, y).intersects(line_string) for x, y in self.graph.nodes if (x, y) != node1 and (x, y) != node2
        )


        return condition1 and condition2 and condition3



    def reset_edges(self):
        #선 지우기
        self.delete("edge")
        #그래프 초기화인데 음... 필요없는듯
        self.graph.clear()

def main():
    root = tk.Tk()
    root.title("Line Counting")
    
    board = NodeCount(root, width=280 + 2 * 20, height=280 + 2 * 20, bg="white")
    board.pack()

    #실행
    run_button = tk.Button(root, text="Run", command=board.calculate_edges)
    run_button.pack(side=tk.RIGHT)

    #리셋
    reset_button = tk.Button(root, text="Reset Edges", command=board.reset_edges)
    reset_button.pack(side=tk.RIGHT)

    #반복 기능
    #repeat_button = tk.Button(root, text="Repeat", command=board.calculate_and_reset_multiple_times)
    #repeat_button.pack(side=tk.RIGHT)

    root.mainloop()

if __name__ == "__main__":
    main()