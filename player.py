import pygame
from projectile import Projectile
from animation import AnimateSprite


class Player(AnimateSprite):

    def __init__(self, game):
        super().__init__("player")
        self.game = game
        self.health = 100
        self.max_health = 100
        self.attack = 10
        self.velocity = 5
        self.all_projectile = pygame.sprite.Group()
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 500

    def update_health_bar(self, surface):
        # dessiner la bar de vie du joueur
        pygame.draw.rect(surface, (60, 63, 60), [self.rect.x + 50, self.rect.y + 10, self.max_health, 7])
        pygame.draw.rect(surface, (111, 210, 46), [self.rect.x + 50, self.rect.y + 10, self.health, 7])

    def damage(self, amount):
        if self.health - amount > 0:
            self.health -= amount
        else:
            self.game.game_over()

    def update_animation(self):
        self.animate()

    def reset(self):
        self.health = self.max_health
        self.rect.x = 0

    def launch_projectile(self):
        self.start_animation()
        self.all_projectile.add(Projectile(self))

        self.game.sound_manager.play("tir")

    def move_left(self):
        self.rect.x -= self.velocity

    def move_right(self):
        if not self.game.check_collision(self, self.game.all_monsters):
            self.rect.x += self.velocity

    def move_up(self):
        pass
        # self.rect.y -= self.velocity + 5

    def move_down(self):
        pass
        # self.rect.y += self.velocity + 5
