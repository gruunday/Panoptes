import math
import requests
from PIL import Image,ImageDraw
from random import randint
from random import seed
import sys
from simulated_aneal import simulated_annealing

"""
This will get data from a graphite database assign it random values and will then proceed
to make it visualy apealing with simulated annealing before drawing the diagram.

"""

# TODO import config at later date

HEIGHT = 500
WIDTH = 500
CENTRE = (HEIGHT/2, WIDTH/2)
seed(randint(1,1000))

#
# Start cost functions
#

def point_distance(point, other):
    """
    Calculates distance between two points

    :point: The co-ordinates of the first point
    :other: The co-ordinates of the other point
    """
    return math.sqrt((point[0] - other[0])**2 + (point[1] - other[1])**2)


def nice_angle(point, other, centre=CENTRE):
    """
    Returns the angle that two points make with eachother and the centre

    :point: Co-ordinates for the first point
    :other: Co-ordinates for the other point
    :centre: Co-ordinates for the centre point
    """
    a = point_distance(point, centre)
    b = point_distance(other, centre)
    c = point_distance(point, other)
    A = a**2
    B = b**2 
    AB = 2 * a * b
    C = c**2
    return math.cos(A + B - (AB - C))

def get_angles(node_loc):
    """
    Gets the angles all the points make with neighbouring points to ensure they are all similar

    :node_loc: List of node locations and their points
    """
    cost = 0
    RADIANS = 6.28319
    ideal_angle = RADIANS / len(node_loc)
    for node in node_loc:
        for other in node_loc:
            if node == other:
                continue
            angle = nice_angle(node_loc[node][0], node_loc[other][0])
            #cost += abs(abs(ideal_angle) - abs(angle))
            if abs(abs(angle) - ideal_angle) < .2:
                cost += 600
    return cost * 2

def same_line(node_loc):
    """
    Ensures two nodes are no on the same line

    :node_loc: List of nodes and their point locations
    """
    cost = 0
    for node in node_loc:
        for other in node_loc:
            if node != other:
                if abs(node_loc[node][0][0] - node_loc[other][0][0]) < 10:
                    cost += 1000
                if abs(node_loc[node][0][1] - node_loc[other][0][1]) < 10:
                    cost += 9000
    return cost * 2
                

def too_close(node_loc, server_loc=CENTRE):
    """
    Calculates if the nodes are too close to eachother 

    :node_loc: List of nodes and their point locations
    :server_loc: Point location of the server piece
    """
    cost = 0
    # Distance that will be too close
    min_dist = 100
    for node in node_loc:
        for other in node_loc:
            if node == other:
                continue
            # Too close to another
            dist = point_distance(node_loc[node][0], node_loc[other][0])
            if dist < min_dist:
                cost += 100 * (100-dist)
            # too close to edge
            if (node_loc[node][0][0] - WIDTH) < min_dist:
                cost += abs(50 * (0.5 * (node_loc[node][0][0] - WIDTH)))
            if (node_loc[node][0][1] - HEIGHT) < min_dist:
                cost += abs(50 * (0.5 * (node_loc[node][0][1] - HEIGHT)))
            if (node_loc[node][0][0]) < min_dist:
                cost += abs(50 * (0.5 * (node_loc[node][0][0])))
            if (node_loc[node][0][1]) < min_dist:
                cost += abs(50 * (0.5 * (node_loc[node][0][1])))
    # too close to server
    if point_distance(server_loc, node_loc[node][0]) < 100:
        cost += 100

    return int(cost / 2)

def off_map(node_lst, h=HEIGHT, w=WIDTH):
    """
    Calculates the cost if a point is off the map

    :node_lst: list of nodes and locations of nodes
    :h: height of canvas
    :w: width of canvas
    """
    cost = 0
    for node in node_lst:
        point = node_lst[node][0]
        if point[0] > w or point[0] < 0:
            cost += 500
        if point[1] > h or point[1] < 0:
            cost += 500
    return int(cost /2) 

def same_slope(node_lst, centre=CENTRE):
    """
    Calculates the slope of lines between points to see if they collide

    :node_lst: list of nodes and points they are at
    :centre: centre point of the canvas
    """
    cost = 0
    centre_x = centre[0]
    centre_y = centre[1]
    for node in node_lst:
        for other in node_lst:
            if other != node:
                x = node_lst[node][0][0]
                y = node_lst[node][0][1]
                x1 = node_lst[other][0][0]
                y1 = node_lst[other][0][1]
                # Ensure no div 0
                if (centre_x - x): slope1 = (centre_y - y) / (centre_x - x)
                else: cost += 2000; continue
                # Ensure no div 0
                if (centre_x - x1): slope2 = (centre_y - y1) / (centre_x - x1)
                else: cost += 2000; continue
                # Check same slope
                if slope1 == slope2: cost += 3000
                elif abs(slope1 - slope2) < .5: cost += 2000
    return cost

def cost(node_lst):
    """
    Returns cost of a diagram to see how good it is

    :node_lst: List of nodes on the graph with points
    """
    cost = 0
    cost += too_close(node_lst)
    cost += off_map(node_lst)
    cost += get_angles(node_lst)
    #cost += same_line(node_lst)
    cost += same_slope(node_lst)
    return cost

#
# End cost functions
#


def get_data(query='*.ping.avg', time='-1min', until='', form='json', address='panoptes.xyz:8080'):
    """
    Fetches data from graphite database

    :target: What we want to retrieve from the graphite database
    :form: format for return data
    :address: address of graphite database
    :time: start time for request
    :until: end time for request
    """
    url = f'http://{address}/render?target={query}&format={form}&from={time}&until={until}'
    print(url)
    r = requests.get(url)
    data = r.json()
    return data

def get_nodes(data):
    """
    This will get the data about each of our nodes to be displayed

    :data: raw return data from get_data()
    """
    node_lst = []
    for node in data:
        distance = node["datapoints"][-1][0]
        name = node["target"].split('.')[0]
        if distance != None:
            node_lst.append((name, distance))
    return node_lst

def give_points(node_lst, centre=CENTRE):
    """
    Takes a list of items that need random points accociated with them and does the random 
    generation of them pints

    :centre: centre of the canvas
    """
    points = {}
    for node in node_lst:
        directions = [(1,1),(-1,1),(1,-1),(-1,-1)]
        # Choose a direction
        direction = directions[randint(0,3)]
        # Random X coordinate
        step_x = (direction[0] * node[1]) 
        if step_x > 0: step_x +=  (randint(0,150))
        else: step_x -= (randint(0,150))
        # Random Y coordinate
        step_y = (direction[1] * node[1])
        if step_y > 0: step_y += (randint(0,150))
        else: step_y -= (randint(0,150))
        points[node[0]] = [(250 + step_x,\
                            250 + step_y), centre]
    return points

def draw_map(point, cost, width=WIDTH, height=HEIGHT):
    """
    Takes points and draws them on a diagram

    :point: array of points to be drawn that represent nodes
    :cost: function to calculate cost
    :width: width of canvas
    :height: height of canvas
    """
    img=Image.new('RGB',(width, height),(255,255,255))
    draw=ImageDraw.Draw(img)
    
    for node in point:
        draw.line((point[node][0],point[node][1]),fill=(0,255,0),width=3)

    for node in point:
        msg = node #+ str(point[node][0])
        draw.text(point[node][0],msg,(0,0,0))
   
    # Draw server last to be on top
    server_pos = ((height/2)+3, (width/2)+3)
    draw.text(server_pos,'Server',(0,0,0))

    # Draw stats
    draw.text((5,(HEIGHT-10)),f'Cost {cost}',(0,0,0))

    img.show() 

def main():
    """
    Runs main file
    """
    query = sys.argv[1]
    time = sys.argv[2]
    until = sys.argv[3]
    data = get_data(query, time, until)
    #data = ''
    best_score = 1000000000000
    # Get data from data source
    node_lst = get_nodes(data)
    # make first random guess
    best_guess = give_points(node_lst)
    # Run simulated_annealing on it to get it better (Twice)
    ans = simulated_annealing(best_guess, cost)
    ans = simulated_annealing(ans, cost)
    # Calculate cost
    sim_score = cost(ans)
    # Draw diagram
    draw_map(ans, sim_score)
    

if __name__ == '__main__':
    main()
