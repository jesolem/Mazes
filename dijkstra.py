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


def draw_maze_path(grid, track, filename="test.png"):
    """ Draw the path on top of the maze. """
    wid = 40
    im = bt.draw_png(grid, wid=wid)
    draw = ImageDraw.Draw(im)

    for i in range(len(track)-1):
        draw.line( (wid*(track[i][1]+1.5), wid*(track[i][0]+1.5), wid*(track[i+1][1]+1.5), wid*(track[i+1][0]+1.5)), fill=(255, 0, 0), width=5)
    im.save(filename)


if __name__ == "__main__":

    sz = 16
    # create a grid of coin tosses 0/1
    toss = np.random.randint(0, 2, (sz, sz)) 
    toss[:,-1] = 0
    toss[-1,:-1] = 1

    d = compute_distances(toss)
    t = backtrack(toss, d, (sz-1, sz-1))
    bt.draw_ascii(toss)
    draw_maze_path(toss, t)
