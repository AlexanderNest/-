import math
from itertools import permutations
from random import randint, random, seed, shuffle
from tkinter import Tk, Canvas, Button


CANVAS_W, CANVAS_H = 800, 800
NODE_R = CANVAS_H * 0.005


class GUI:
    def __init__(self, root):
        self.canvas = Canvas(root, width=CANVAS_W, height=CANVAS_H, bg="white")
        self.canvas.pack()
        self.nodes = None

    def draw(self):
        self.canvas.delete("all")
        for i in range(len(self.nodes)):
            x1, y1 = self.nodes[i]
            x2, y2 = self.nodes[(i + 1) % len(self.nodes)]
            self.canvas.create_line(x1, y1, x2, y2)
            r = NODE_R
            self.canvas.create_oval(x1 - r, y1 - r, x1 + r, y1 + r, fill="red")


def make_random_graph(size):
    nodes = []
    for i in range(size):
        nodes.append((
            randint(NODE_R, CANVAS_W - NODE_R),
            randint(NODE_R, CANVAS_H - NODE_R)
        ))
    return nodes


def distance(n1, n2):
    x1, y1 = n1
    x2, y2 = n2
    dx = x1 - x2
    dy = y1 - y2
    return math.sqrt(dx * dx + dy * dy)


def cost(s):
    tour = distance(s[-1], s[0])
    for i in range(len(s) - 1):
        tour += distance(s[i], s[i + 1])
    return tour


def shuffletransform(s):
    g = s[:]
    shuffle(g)
    return g


def randomsearch(s, steps):
    best = s

    for i in range(steps):
        t = shuffletransform(best)
        if cost(t) < cost(best):
            best = t
            
    return best
            

def swap_transform(s):
    c = s[:]
    first = randint(0, len(s) - 1)
    second = 0
    while True:
        second = randint(0, len(s) - 1)
        if second != first:
            break

    c[first], c[second] = c[second], c[first]

    return c


def rot_transform(s):
    # TODO
    pass


def hill(s, steps):
    
    for i in range(steps):
        t = swap_transform(s)
        if cost(t) <= cost(s):
            s = t

    return s
        
            
def annealing(s, steps):
    T = 1
    for i in range(steps):
        t = swap_transform(s)
        if cost(t) <= cost(s):
            s = t
        else:
            dE = cost(s) - cost(t)
            p = math.exp(dE/T)
            T = 0.99*T
            if p >= random():
                s = t

    return s





seed(42)
g = make_random_graph(10)

#g = randomsearch(g, 10000)
#g = hill(g, 1000)
g = annealing(g, 1000)
root = Tk()
w = GUI(root)
w.nodes = g

w.draw()
root.mainloop()

