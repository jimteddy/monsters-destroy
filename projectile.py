import pygame


class Projectile(pygame.sprite.Sprite):
    def __init__(self, player):
        super().__init__()
        self.player = player
        self.velocity = 5
        self.image = pygame.image.load("assets/projectile.png")
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.x = self.player.rect.x + 120
        self.rect.y = self.player.rect.y + 80
        self.origine_image = self.image
        self.angle = 0

    def rotate(self):
        self.angle += 8
        self.image = pygame.transform.rotozoom(self.origine_image, self.angle, 1)
        self.rect = self.image.get_rect(center=self.rect.center)

    def remove(self) -> None:
        self.player.all_projectile.remove(self)

    def move(self):
        self.rect.x += self.velocity
        self.rotate()
        # collision ? entre le projectile et les monstre
        for monster in self.player.game.check_collision(self, self.player.game.all_monsters):
            self.remove()
            # degat infligé
            monster.damage(self.player.attack)
        # sortie d'ecran
        if self.rect.x > 1080:
            self.remove()
