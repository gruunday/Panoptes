import math
import requests
from PIL import Image,ImageDraw
from random import randint

#import config at later date
height = 500
width = 500


class Point():
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __str__(self):
        return f'({x}, {y})'
    
    def dist(self, other):
        return math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)

def point_distance(point, other):
    return math.sqrt((point[0] - other[0])**2 + (point[1] - other[1])**2)

def too_close(node_loc):
    cost = 0
    # Distance that will be too close
    min_dist = 20
    for node in node_loc:
        for other in node_loc:
            if node == other:
                continue
            dist = point_distance(node_loc[node][0], node_loc[other][0])
            if dist < min_dist:
                cost = 5 * (100-dist)
    return cost

def off_map(node_lst, h=500, w=500):
    cost = 0
    for node in node_lst:
        point = node_lst[node][0]
        if point[0] > w or point[0] < 0:
            cost += 600
        if point[1] > h or point[1] < 0:
            cost += 600
    return cost

def cost(node_lst):
    cost = 0
    cost += too_close(node_lst)
    cost += off_map(node_lst)
    return cost

def get_data():
    r = requests.get('http://panoptes.xyz:8080/render?target=*.ping.avg&format=json&from=-1min')
    data = r.json()
    return data

def get_nodes(data):
#    node_lst = []
#    for node in data:
#        distance = node["datapoints"][-1][0]
#        name = node["target"].split('.')[0]
#        node_lst.append((name, distance))
    node_lst = [('anam', 28.127), ('saturn', 30), ('pluto', 5), ('gary', 7), ('dave', 40)]
    return node_lst

def give_points(node_lst):
    points = {}
    for node in node_lst:
        directions = [(1,1),(-1,1),(1,-1),(-1,-1)]
        direction = directions[randint(0,3)]
        step_x = (direction[0] * node[1]) * (randint(0,3) + 3)
        step_y = (direction[1] * node[1]) * (randint(0,3) + 3)
        points[node[0]] = [(250 + step_x,\
                            250 + step_y), (250, 250)]
    return points

def draw_map(point, cost, width=500, height=500):
    img=Image.new('RGB',(width, height),(255,255,255))
    draw=ImageDraw.Draw(img)
    
    for node in point:
        draw.line((point[node][0],point[node][1]),fill=(0,255,0),width=3)

    for node in point:
        draw.text(point[node][0],node,(0,0,0))
   
    # Draw server last to be on top
    server_pos = ((height/2)+3, (width/2)+3)
    draw.text(server_pos,'Server',(0,0,0))

    # Draw stats
    draw.text((5,490),f'Cost {cost}',(0,0,0))

    img.show() 

def main():
    #data = get_data()
    data = ''
    node_lst = get_nodes(data)
    node_loc = give_points(node_lst)
    #print(node_loc)
    score = cost(node_loc)
    draw_map(node_loc, score)

if __name__ == '__main__':
    for _ in range(0,5):
        main()
