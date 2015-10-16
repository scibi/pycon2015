import heapq
import sys

import bs4
import urllib2

FIELD_SIZE = 7

__author__ = 'Wini'

def download_lab():
    page_address = 'http://46.101.159.170/A60EHNNQ/amaze/maze'

    response = urllib2.urlopen(page_address)

    html = response.read()

    with open('maze.txt', 'w') as f:
        f.write(html)


class Field(object):
    def __init__(self, x, y, color):
        self._x = x
        self._y = y
        self._color = color

    def __str__(self):
        return '{} {} {}'.format(self._x, self._y, self._color)


def get_lab():
    html = None

    with open('maze.txt', 'r') as f:
        html = f.read()

    soup = bs4.BeautifulSoup(html)
    maze = soup.svg

    labirynth = []
    start = (0,0)
    end = (0,0)

    i = 0

    for field in maze.children:
        if i:
            f= Field(
                    int(field['x']) / int(field['width']),
                    int(field['y']) / int(field['height']),
                    field['fill']
                )
            labirynth.append(f)
            if f._color=='green':
                start = (f._x, f._y)
            if f._color=='red':
                end = (f._x, f._y)
        else:
            i += 1

    print('START {}'.format(start))
    print('END {}'.format(end))
    return {
        'width': max([f._x for f in labirynth]),
        'height': max([f._y for f in labirynth]),
        'start': start,
        'end': end,
        'walls': [(f._x, f._y) for f in labirynth if f._color=='black']
    }


class Cell(object):
    def __init__(self, x, y, reachable):
        """
        Initialize new cell

        @param x cell x coordinate
        @param y cell y coordinate
        @param reachable is cell reachable? not a wall?
        """
        self.reachable = reachable
        self.x = x
        self.y = y
        self.parent = None
        self.g = 0
        self.h = 0
        self.f = 0
        self.on_path = False

class AStar(object):
    def __init__(self):
        self.opened = []
        heapq.heapify(self.opened)
        self.closed = set()
        self.cells = []
        self.grid_height = 6
        self.grid_width = 6

    def init_grid(self):
        lab=get_lab()
        self.grid_height = lab['height']
        self.grid_width = lab['width']
        #print lab
        #walls = ((0, 5), (1, 0), (1, 1), (1, 5), (2, 3), 
        #         (3, 1), (3, 2), (3, 5), (4, 1), (4, 4), (5, 1))
        walls = lab['walls']
        #print walls
        for x in range(self.grid_width):
            for y in range(self.grid_height):
                if (x, y) in walls:
                    reachable = False
                else:
                    reachable = True
                self.cells.append(Cell(x, y, reachable))
        self.start = self.get_cell(*lab['start'])
        self.end = self.get_cell(*lab['end'])
        print('START {}'.format(lab['start']))
        print('END {}'.format(lab['end']))
        print('START {},{}'.format(self.start.x, self.start.y))
        print('END {},{}'.format(self.end.x, self.end.y))

    def get_heuristic(self, cell):
        """
        Compute the heuristic value H for a cell: distance between
        this cell and the ending cell multiply by 10.

        @param cell
        @returns heuristic value H
        """
        return 10 * (abs(cell.x - self.end.x) + abs(cell.y - self.end.y))

    def get_cell(self, x, y):
        """
        Returns a cell from the cells list

        @param x cell x coordinate
        @param y cell y coordinate
        @returns cell
        """
        return self.cells[x * self.grid_height + y]

    def get_adjacent_cells(self, cell):
        """
        Returns adjacent cells to a cell. Clockwise starting
        from the one on the right.

        @param cell get adjacent cells for this cell
        @returns adjacent cells list 
        """
        cells = []
        if cell.x < self.grid_width-1:
            cells.append(self.get_cell(cell.x+1, cell.y))
        if cell.y > 0:
            cells.append(self.get_cell(cell.x, cell.y-1))
        if cell.x > 0:
            cells.append(self.get_cell(cell.x-1, cell.y))
        if cell.y < self.grid_height-1:
            cells.append(self.get_cell(cell.x, cell.y+1))
        return cells

    def display_path(self):
        cell = self.end
        while cell.parent is not self.start:
            cell = cell.parent
            print 'path: cell: %d,%d' % (cell.x, cell.y)

    def update_cell(self, adj, cell):
        """
        Update adjacent cell

        @param adj adjacent cell to current cell
        @param cell current cell being processed
        """
        adj.g = cell.g + 10
        adj.h = self.get_heuristic(adj)
        adj.parent = cell
        adj.f = adj.h + adj.g

    def process(self):
        # add starting cell to open heap queue
        heapq.heappush(self.opened, (self.start.f, self.start))
        while len(self.opened):
            # pop cell from heap queue 
            f, cell = heapq.heappop(self.opened)
            # add cell to closed list so we don't process it twice
            self.closed.add(cell)
            # if ending cell, display found path
            if cell is self.end:
                self.display_path()
                break
            # get adjacent cells for cell
            adj_cells = self.get_adjacent_cells(cell)
            for adj_cell in adj_cells:
                if adj_cell.reachable and adj_cell not in self.closed:
                    if (adj_cell.f, adj_cell) in self.opened:
                        # if adj cell in open list, check if current path is
                        # better than the one previously found for this adj
                        # cell.
                        if adj_cell.g > cell.g + 10:
                            self.update_cell(adj_cell, cell)
                    else:
                        self.update_cell(adj_cell, cell)
                        # add adj cell to open list
                        heapq.heappush(self.opened, (adj_cell.f, adj_cell))

    def display(self):
        cell = self.end
        while cell.parent is not self.start:
            cell = cell.parent
            cell.on_path = True
        print('START {},{}'.format(self.start.x, self.start.y))
        print('END {},{}'.format(self.end.x, self.end.y))
        for y in xrange(self.grid_height):
            for x in xrange(self.grid_width):
                c=self.get_cell(x, y)
                if c.reachable:
                    if ((x==self.start.x) and (y==self.start.y)):
                        sys.stdout.write('S')
                    elif ((x==self.end.x) and (y==self.end.y)):
                        sys.stdout.write('E')
                    elif c.on_path:
                        sys.stdout.write('*')
                    else:
                        sys.stdout.write(' ')
                else:
                    sys.stdout.write('X')
            sys.stdout.write('\n')
    def get_string(self):
        path=[]
        cell = self.end
        while cell is not self.start:
            if cell.x<cell.parent.x:
                path.append('L')
            elif cell.x>cell.parent.x:
                path.append('R')
            elif cell.y>cell.parent.y:
                path.append('B')
            elif cell.y<cell.parent.y:
                path.append('T')
            else:
                print "TO NIE MOZE BYC"
            cell = cell.parent
        
        return ''.join(path[::-1])
        
a = AStar()
a.init_grid()
a.process()
a.display()
path=a.get_string()
#download_lab()

import hashlib

m = hashlib.md5()
m.update(path)
print '>>>>>>>>>>>>>>>>'
print m.hexdigest()
