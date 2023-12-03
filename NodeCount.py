import tkinter as tk
import networkx as nx
import random
from shapely.geometry import LineString

class NodeCount(tk.Canvas):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.board_size = 6
        self.cell_size = 40
        self.outer_gap = 20
        self.nodes = set()  #클릭된 교차점 저장
        self.graph = nx.Graph()  #그래프 생성인데 잘 모르겟...
        self.draw_board()

        #클릭
        self.bind("<Button-1>", self.on_click)

        self.run_count = 0  # Run 클릭횟수

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
        #클릭된곳 계산
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
        #노드 순서 섞어주기
        shuffled_nodes = list(self.nodes)
        
        # 반복횟수 지정 바꿔줘도 됨. 현재 300번.
        for _ in range(300):
            random.shuffle(shuffled_nodes)

            #그린 셋 초기화
            drawn_edges = set()

            #더 이상 그릴 엣지가 없을 때까지 엣지를 계산하고 그림
            while True:
                drawn_this_iteration = False  #이 반복에서 새로운 엣지가 그려졌는지 확인

                for i in range(len(shuffled_nodes)):
                    node1 = shuffled_nodes[i]
                    node2 = shuffled_nodes[(i + 1) % len(shuffled_nodes)]  #섞인 목록에서 다음 노드에 연결

                    if self.check_availability(node1, node2) and (node1, node2) not in drawn_edges and (node2, node1) not in drawn_edges:
                        self.draw_edge(node1, node2)
                        drawn_edges.add((node1, node2))
                        drawn_edges.add((node2, node1))
                        drawn_this_iteration = True

                #반복에서 선 그릴거 없으면 스탑
                if not drawn_this_iteration:
                    break

        #그릴 수 있는 엣지의 최대 수를 출력
        #max_possible_edges = len(self.nodes) * (len(self.nodes) - 1)
        num_edges = len(self.find_withtag("edge"))
        print(f"Number of edges: {num_edges} ") #(Max possible: {max_possible_edges}) 넣어도 되고 의미는 없음.

        #Repeat 런 카운트
        self.run_count += 1

        # run 한번 하고 나서 자동으로 리셋
        if self.run_count == 1:
            self.run_count = 0
            self.reset_edges()

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

        # 엣지 그리기
        self.create_line(x1_px, y1_px, x2_px, y2_px, tags="edge", fill="blue")

        #그래프 업데이트
        self.graph.add_edge(node1, node2)

    def check_availability(self, node1, node2):
        line_string = LineString([node1, node2])

        #선 사이에 노드 X
        condition1 = all(LineString(line).crosses(line_string) is False for line in self.graph.edges)

        #새로운 엣지
        condition2 = (node1, node2) not in self.graph.edges and (node2, node1) not in self.graph.edges

        return condition1 and condition2

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

    #반복
    repeat_button = tk.Button(root, text="Repeat", command=board.calculate_and_reset_multiple_times)
    repeat_button.pack(side=tk.RIGHT)

    root.mainloop()

if __name__ == "__main__":
    main()
