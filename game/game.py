from __future__ import print_function
import sys, pygame


def run():
    pygame.init()

    size = width, height = 320, 240
    black = 0, 0, 0

    screen = pygame.display.set_mode(size)

    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()

            screen.fill(black)
            pygame.display.flip()
