import pygame
from player import Player
from monster import Mummy, Alien
from comet_event import CometFallEvent
from sounds import SoundManager
from score import Scoring


class Game:
    def __init__(self):
        # savoir si le jeu a commencé
        self.is_playing = False

        # generer les evenenment
        self.comet_fall_event = CometFallEvent(self)

        # generer le joueur
        self.all_players = pygame.sprite.Group()
        self.player = Player(self)
        self.all_players.add(self.player)

        # generer les monstres
        self.all_monsters = pygame.sprite.Group()

        self.font = pygame.font.Font("assets/NewYork.ttf", 25)

        self.sound_manager = SoundManager()
        #
        self.score_record = Scoring()
        # mettre le score à zero
        self.score = 0
        self.pressed = {}

    def start(self):
        self.is_playing = True
        self.spawn_monster(Mummy)
        self.spawn_monster(Mummy)
        self.spawn_monster(Alien)

    def add_score(self, points=10):
        self.score += points

    def save_score(self):
        self.score_record.sort_best_score(self.score)
        self.score_record.save()
        self.score = 0

    def check_collision(self, sprite, group):
        return pygame.sprite.spritecollide(sprite, group, False, pygame.sprite.collide_mask)

    def spawn_monster(self, monster_class_name):
        self.all_monsters.add(monster_class_name.__call__(self))

    def game_over(self):
        self.all_monsters = pygame.sprite.Group()
        self.comet_fall_event.all_comets = pygame.sprite.Group()
        self.player.all_projectile = pygame.sprite.Group()
        self.comet_fall_event.reset_percent()
        self.player.reset()
        self.save_score()
        self.is_playing = False
        # jouer le son
        self.sound_manager.play("game_over")

    def update(self, screen):
        # afficher le score sur  l'ecran
        scrore_text = self.font.render(f"Score : {self.score}", 1, (0, 0, 0))
        screen.blit(scrore_text, (20, 20))

        screen.blit(self.player.image, self.player.rect)  # mettre le joueur dans l'ecran

        # dessiner la bar de vie du joueur
        self.player.update_health_bar(screen)

        # gestion de la comet fall event
        self.comet_fall_event.update_bar(screen)

        # actualiser l'animation
        self.player.update_animation()

        # recuprer et activer tous les projectile lancer
        for projectile in self.player.all_projectile:
            projectile.move()

        self.player.all_projectile.draw(screen)  # dessiner l'ensemble des projectile sur l'ecran

        # deplacement
        for monster in self.all_monsters:
            monster.forward()
            monster.update_health_bar(screen)
            monster.update_animation()

        # recuperer toutes les comets
        for comet in self.comet_fall_event.all_comets:
            comet.fall()

        # afficher les monstres
        self.all_monsters.draw(screen)

        # afficher les comets
        self.comet_fall_event.all_comets.draw(screen)

        #  connaitre le mouvement voulu par le joueur
        if self.pressed.get(pygame.K_RIGHT) and self.player.rect.x + self.player.rect.width < screen.get_width():
            self.player.move_right()
        elif self.pressed.get(pygame.K_LEFT) and self.player.rect.x > 0:
            self.player.move_left()
        elif self.pressed.get(pygame.K_UP) and self.player.rect.y > 0:
            self.player.move_up()
        elif self.pressed.get(pygame.K_DOWN) and self.player.rect.y + self.player.rect.width < screen.get_height():
            self.player.move_down()
