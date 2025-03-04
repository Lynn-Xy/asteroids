import pygame
import sys
from constants import *
from player import Player
from circleshape import CircleShape
from asteroids import Asteroid
from asteroidfield import AsteroidField
from shot import Shot

def main():
    pygame.init()
    clock = pygame.time.Clock()
    print("Starting Asteroids!")
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    background_color = (0, 0, 0)

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shot_group = pygame.sprite.Group()

    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable,)
    Shot.containers = (shot_group, updatable, drawable)
    
    asteroidfield = AsteroidField()
    updatable.add(asteroidfield)

    Player.containers = (updatable, drawable)
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, shot_group)
  
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        screen.fill(color=background_color)
        dt = clock.tick(60) / 1000
        keys = pygame.key.get_pressed()
        updatable.update(dt)
        for asteroid in asteroids:
            for shot in shot_group:
                if asteroid.is_colliding(shot):
                    asteroid.split()
                    shot.kill()
            if asteroid.is_colliding(player):
                print("Game over!")
                sys.exit()
        drawable.draw(screen)
        player.draw(screen)
        pygame.display.flip()

if __name__ == "__main__":
    main()