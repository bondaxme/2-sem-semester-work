import math
import copy
import matplotlib.pyplot as plt
import networkx as nx


class Graph:

    def __init__(self, matrix=None, size=None):
        self.__matrix = matrix
        self.__cost = None
        self.__path = None
        self.__size = size
        self.__iteration_counter = 0

    @property
    def matrix(self):
        return self.__matrix

    @matrix.setter
    def matrix(self, matrix):
        self.__matrix = matrix

    @property
    def size(self):
        return self.__size

    @size.setter
    def size(self, size):
        self.__size = size

    # АЛГОРИТМ ФЛОЙДА
    def floydMethod(self):
        self.__cost = copy.deepcopy(self.__matrix)
        self.__path = [[x for x in range(self.__size)] for y in range(self.__size)]

        for k in range(self.__size):
            self.minPath(self.__size, k)

        self.writeResult()
        self.__iteration_counter = 0

    # АЛГОРИТМ ДАНЦИГА
    def dantzigMethod(self):
        self.__cost = copy.deepcopy(self.__matrix)
        self.__path = [[x for x in range(self.__size)] for y in range(self.__size)]

        for m in range (2, self.__size):
            for k in range(m):
                self.minPath(m, k)
            self.findMinMj(m)
            self.findMinIm(m)

        for k in range(self.__size):
            self.minPath(self.__size, k)

        self.writeResult()
        self.__iteration_counter = 0

    # ПОРІВНЯННА ШЛЯХІВ ДЛЯ ПОШУКУ НАЙКОРОТШОГО + ПЕРЕВІРКА НА НЕГАТИВНИЙ КОНТУР
    def minPath(self, m, k):
        for i in range(m):
            for j in range(m):
                if self.__cost[i][k] + self.__cost[k][j] < self.__cost[i][j]:
                    self.__cost[i][j] = self.__cost[i][k] + self.__cost[k][j]
                    self.__path[i][j] = k

                self.__iteration_counter += 1

                if self.__cost[i][i] < 0:
                    raise Exception

    # ПОШУК МІНІМАЛЬНОГО, КОЛИ j=m
    def findMinIm(self, m):
        for i in range(m):
            min = self.__cost[i][m]
            for k in range(m):
                if (i != k and self.__cost[i][k] + self.__cost[k][m] < min):
                    self.__path[i][m] = k
                    min = self.__cost[i][k] + self.__cost[k][m]
                self.__iteration_counter += 1
            self.__cost[i][m] = min

    # ПОШУК МІНІМАЛЬНОГО, КОЛИ i=m
    def findMinMj(self, m):
        for j in range(m):
            min = self.__cost[m][j]
            for k in range(m):
                if (j != k and self.__cost[m][k] + self.__cost[k][j] < min):
                    self.__path[m][j] = k
                    min = self.__cost[m][k] + self.__cost[k][j]
                self.__iteration_counter += 1
            self.__cost[m][j] = min

    # ПОБУДОВА НАЙКОРОТОШОГО ШЛЯХУ (ЧЕРЕЗ ЩО ВІН ПРОХОДИТЬ)
    def getWay(self, start, end):
        self.way = ""
        if (self.__cost[start][end] == math.inf):
            self.way = "Неможливо знайти шлях"
            return self.way

        self.way = f'{start + 1}-'
        while (self.__path[start][end] != end):
            new_end = self.__path[start][end]
            while (self.__path[start][new_end] != new_end and self.__cost[start][new_end] != math.inf):
                new_start = self.__path[start][new_end]
                self.way += f"{self.__path[start][new_end] + 1}-"
                start = new_start
            self.way += f'{self.__path[start][end] + 1}-'
            start = self.__path[self.__path[start][end]][end]
        self.way += f'{end + 1}'
        return self.way

    # ЗАПИС РЕЗУЛЬТАТІВ В ФАЙЛ
    def writeResult(self):
        text = "Усі найкоротші шляхи:\n"
        for i in range(self.__size):
            for j in range(self.__size):
                if i != j and self.__path[i][j] != -1:
                    text += f'Найкоротший шлях з {i + 1} в {j + 1} [{str(self.getWay(i, j))}] Length: {self.__cost[i][j]}\n'

        text += "\nМатриця найкоротших довжин:\n"
        for i in range(self.__size):
            for j in range(self.__size):
                text += str(self.__cost[i][j]) + '\t'
            text += '\n'

        text += f"\nКількість ітерацій: {self.__iteration_counter}"

        with open("data.txt", 'w', encoding='utf-8') as file:
            file.write(text)

    # ВИВЕДЕННЯ ГРАФУ
    def drawGraph(self):
        graph = nx.DiGraph()

        for i in range(self.__size):
            graph.add_node(i + 1)

        for i in range(self.__size):
            for j in range(self.__size):
                if self.__matrix[i][j] < math.inf and self.__matrix[i][j] != 0:
                    graph.add_edge(i + 1, j + 1, weight=self.__matrix[i][j])

        pos = nx.spring_layout(graph)
        nx.draw(graph, pos=pos, node_size=500, arrows=True, with_labels=True)
        labels = nx.get_edge_attributes(graph, 'weight')
        nx.draw_networkx_edge_labels(graph, pos, edge_labels=labels)
        plt.savefig('graph.png')
        plt.clf()
