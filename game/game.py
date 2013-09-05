from __future__ import print_function
import os, sys, pygame, random, math, time
from xmlrpclib import MAXINT

class Point(object):
    def __init__(self, pos, cluster=0):
        self.pos = (pos[0], pos[1])
        self.cluster = cluster

def get_dist(pos1, pos2):
    return math.hypot(pos1[0]-pos2[0], pos1[1]-pos2[1])

def get_color(centroids, colors, points):
    pass

def get_random_rgb():
    return random.randint(0, 255)

def get_random_color():
    return pygame.Color(get_random_rgb(), get_random_rgb(), get_random_rgb())

class Joy(object):
    def __init__(self, joystick):
        self.pos = [0, 0]
        self.joystick = joystick
        
    def get_pos(self):
        return self.pos

def run():
    driver = "directfb"
    #if not os.getenv("SDL_VIDEODRIVER"):
    #    os.putenv("SDL_VIDEODRIVER", driver)

    try:
        pygame.display.init()
    except pygame.error:
        print("Driver: {0} failed.".format(driver))

    pygame.joystick.init()

    size = width, height = (pygame.display.Info().current_w, pygame.display.Info().current_h)
    print(size)
    screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
    black = pygame.Color(0, 0, 0)
    
    joysticks = []
    for i in range(0, pygame.joystick.get_count()):
        print("Initializing joystick")
        joysticks.append(Joy(pygame.joystick.Joystick(i)))
        joysticks[-1].joystick.init()
        
    def clamp_width(value):
        return sorted((0, value, width))[1]
    
    def clamp_height(value):
        return sorted((0, value, height))[1]

    positions = []
    centroids = set()
    colors = dict()
    add_time = time.clock()
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        screen.fill(black)
        
        (left, middle, right) = pygame.mouse.get_pressed()
        
        #if time.clock() - add_time > 0.25:
        #    positions.add(Point( (int(width/2+100*math.sin(10*time.clock())),
        #                      int(height/2+100*math.cos(10*time.clock())) ) ) )
        #    add_time = time.clock()
        
        for joy in joysticks:
            joy.pos = [int(clamp_width(joy.pos[0] + 10*joy.joystick.get_axis(0))),
                       int(clamp_height(joy.pos[1] + 10*joy.joystick.get_axis(1)))]
            
            if joy.joystick.get_button(0):
                positions.append(Point(joy.get_pos()))
            if joy.joystick.get_button(5):
                positions.clear()
                centroids.clear()
            if joy.joystick.get_button(6):
                sys.exit()
        
        if left:
            positions.append(Point(pygame.mouse.get_pos()))
        if middle:
            positions.clear()
            centroids.clear()
        if right:
            centroids.add(pygame.mouse.get_pos())
            colors.clear()
            for centroid in centroids:
                colors[centroid] = get_random_color()
            time.sleep(0.25)
        
        if len(positions) > 100:
            positions = [positions[i] for i in range(0, len(positions)) if i%2 == 0]

        for pos in positions:
            color = get_random_color()
            dist = MAXINT
            for centroid in centroids:
                if dist > get_dist(centroid, pos.pos):
                    dist = get_dist(centroid, pos.pos)
                    color = colors[centroid]
            pygame.draw.circle(screen, color, pos.pos, 10)
        pygame.display.flip()
