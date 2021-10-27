import numpy as np
from PIL import Image, ImageDraw


def draw_ascii(toss):
    """ Draw the maze in the console. """
    h, v, x, s = "---", "|", "+", "   "

    print(x+len(toss[0])*(h+x))
    for row in toss:
        # east
        print(v + "".join([s+v if i == 1 else " "+s for i in row]))
        # north
        print("".join([x+s if i == 1 else x+h for i in row]) + x)


def draw_png(toss, wid=40, filename='maze.png'):
    """ Draw the maze as a png. """
    rows, cols = toss.shape

    im = Image.new('RGBA', (wid*(rows+2), wid*(cols+2)), (255, 255, 255, 255))
    draw = ImageDraw.Draw(im)
    draw.rectangle([wid, wid, wid*(rows+1), wid*(cols+1)], outline=(0, 0, 0, 255))

    for row in range(rows):
        for col in range(cols):
            if toss[row,col] == 1: # east
                draw.line( (wid*(col+2), wid*(row+1), wid*(col+2), wid*(row+2)), fill=(0, 0, 0))
            else: # north
                draw.line( (wid*(col+1), wid*(row+2), wid*(col+2), wid*(row+2)), fill=(0, 0, 0))

    im.save(filename)


if __name__ == "__main__":

    # create a grid of coin tosses 0/1
    toss = np.random.randint(0, 2, (8,8)) # 0 north, 1 east
    toss[:,-1] = 1
    toss[-1,:-1] = 0

    # visualize
    print(toss)
    draw_ascii(toss)
    draw_png(toss)
