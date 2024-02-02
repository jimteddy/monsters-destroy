import random
import pygame
from animation import AnimateSprite


class Monster(AnimateSprite):

    def __init__(self, game, name, size, offset=0):
        super().__init__(name, size)
        self.game = game
        self.health = 100
        self.max_health = 100
        self.attack = 0.3
        self.velocity = 1
        self.default_speed = 1
        self.rect = self.image.get_rect()
        self.rect.x = self._apparition
        self.rect.y = 545 - offset
        self.loot_amount = 10
        self.start_animation()

    @property
    def _apparition(self):
        return 950 + random.randint(0, 100)

    def set_speed(self, speed):
        self.default_speed = speed
        self.velocity = random.randint(1, speed)

    def set_lout_amount(self, amount):
        self.loot_amount = amount

    def damage(self, amount):
        # infliger les degat
        self.health -= amount

        # v
        if self.health <= 0:
            self.rect.x = self._apparition
            self.velocity = random.randint(1, self.default_speed)
            self.health = self.max_health
            self.game.add_score(self.loot_amount)

            # si la barre d'event est chargé à son maximum
            if self.game.comet_fall_event.is_full_loaded():
                # retirer le montre du jeu
                self.game.all_monsters.remove(self)

                # déclancher la pluie de meteor
                self.game.comet_fall_event.attenpt_fall()

    def update_animation(self):
        self.animate(loop=True)

    def update_health_bar(self, surface):
        # dessiner la bar de vie des monstres
        pygame.draw.rect(surface, (60, 63, 60), [self.rect.x + 12, self.rect.y - 20, self.max_health, 5])
        pygame.draw.rect(surface, (111, 210, 46), [self.rect.x + 12, self.rect.y - 20, self.health, 5])

    def forward(self):
        # verifier s'il n'y a pas de collision avec le joueur
        if not self.game.check_collision(self, self.game.all_players):
            self.rect.x -= self.velocity
        # verifier s'il y a collision
        else:
            self.game.player.damage(self.attack)


class Mummy(Monster):
    def __init__(self, game):
        super().__init__(game, "mummy", (130, 130))
        self.set_speed(3)
        self.set_lout_amount(10)


class Alien(Monster):
    def __init__(self, game):
        super().__init__(game, "alien", (300, 300), 145)
        self.health = 250
        self.max_health = 250
        self.attack = 0.5
        self.set_speed(1)
        self.set_lout_amount(20)
