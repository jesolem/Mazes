import numpy as np
from PIL import Image, ImageDraw
import heapq as hq
import binary_tree as bt


def backtrack(grid, distance, point):
    """ Backtrack from point until the start value is reached. """
    track = [point]

    for step in range(int(distance[point])):
        nbrs = get_nbrs(grid, point)
        d = [(distance[nbr], nbr) for nbr in nbrs]
        d.sort()
        point = d[0][1]
        track.append(point)

    return track


def compute_distances(grid, start=(0,0)):
    """ Compute all distances from start using Dijkstras. """

    visited = np.zeros(grid.shape)
    distance = np.zeros(grid.shape)

    # initialize priority queue of neighbors
    visited[start] = 1
    nbrs = get_nbrs(grid, start)
    q = [(distance[start]+1, n) for n in nbrs]
    hq.heapify(q)

    while q:
        dist, point = hq.heappop(q)
        distance[point] = dist
        visited[point] = 1
        nbrs = get_nbrs(grid, point)
        for nbr in nbrs:
            if visited[nbr] == 0:
                hq.heappush(q, (dist+1, nbr))

    return distance


def get_nbrs(grid, point):
    """ Get all the valid maze neighbors of point. """
    m,n = grid.shape
    nbrs = []

    if point[1]<(n-1) and grid[point] == 1: # if we can go east
        nbrs.append((point[0], point[1]+1))
    if point[0]<(m-1) and grid[point] == 0: # if we can go north
        nbrs.append((point[0]+1, point[1]))
    if point[1]>0 and grid[(point[0], point[1]-1)] == 1: # if we can go west
        nbrs.append((point[0], point[1]-1))
    if point[0]>0 and grid[(point[0]-1, point[1])] == 0: # if we can go south
        nbrs.append((point[0]-1, point[1]))

    return nbrs


def draw_maze_path(grid, track, filename="path.png"):
    """ Draw the path on top of the maze. """
    wid = 40
    im = bt.draw_png(grid, wid=wid)
    draw = ImageDraw.Draw(im)

    for i in range(len(track)-1):
        draw.line( (wid*(track[i][1]+1.5), wid*(track[i][0]+1.5), wid*(track[i+1][1]+1.5), wid*(track[i+1][0]+1.5)), fill=(255, 0, 0), width=5)
    im.save(filename)


def draw_longest_path(grid, filename="longest.png"):
    """ Find a long(est) path. """

    startpoint = (np.random.randint(0, grid.shape[0]), np.random.randint(0, grid.shape[1]))
    d = compute_distances(grid, start=startpoint)
    maxpoint = np.unravel_index(d.argmax(), d.shape) # find largest value
    d = compute_distances(grid, start=maxpoint) # distances from this point
    endpoint = np.unravel_index(d.argmax(), d.shape) # find largest value

    # draw path
    t = backtrack(grid, d, endpoint)
    draw_maze_path(grid, t, filename=filename)


def visualize_distances(d, wid=40, filename="distance_map.png"):
    """ Make an image of the distance map used for Dijkstra. """

    m,n = d.shape
    im = Image.fromarray(np.uint8(d * 255.0/d.max()) , 'L')
    im2 = im.resize((wid*m, wid*n), Image.NEAREST) #Image.ANTIALIAS)
    im2.save(filename)


if __name__ == "__main__":

    toss = bt.create_binary_tree_maze(16)

    draw_longest_path(toss)

    d = compute_distances(toss)
    visualize_distances(d, wid=40)
