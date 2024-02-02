import random
import pygame


class Comet(pygame.sprite.Sprite):
    def __init__(self, comet_fall_event):
        super().__init__()
        self.image = pygame.image.load("assets/comet.png")
        self.rect = self.image.get_rect()
        self.velocity = self._vitesse
        self.rect.x = random.randint(20, 740)
        self.rect.y = - random.randint(0, 100)
        self.comet_fall_event = comet_fall_event

    @property
    def _vitesse(self):
        return random.randint(3, 6)

    def remove(self):
        self.comet_fall_event.all_comets.remove(self)

        # jouer le son
        self.comet_fall_event.game.sound_manager.play("meteorite")

        # verifier si le nombre de comet est à zero
        if len(self.comet_fall_event.all_comets) == 0:
            self.comet_fall_event.reset_percent()
            self.comet_fall_event.game.start()

    def fall(self):
        self.rect.y += self.velocity

        if self.rect.y >= 550:
            self.remove()

            if len(self.comet_fall_event.all_comets) == 0:
                self.comet_fall_event.reset_percent()
                self.comet_fall_event.fall_mode = False

        if self.comet_fall_event.game.check_collision(self, self.comet_fall_event.game.all_players):
            self.remove()
            self.comet_fall_event.game.player.damage(20)
