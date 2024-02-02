import pygame

from game import Game
from score import Scoring

pygame.init()

# definir une clock
clock = pygame.time.Clock()
FPS = 60

#  fenetre du jeu
pygame.display.set_caption("My game with pygame")
screen = pygame.display.set_mode((1000, 720))  # ecran principale du jeu

background = pygame.image.load('assets/bg.jpg')
banner = pygame.image.load('assets/banner.png')
banner = pygame.transform.scale(banner, (500, 500))
banner_rect = banner.get_rect()
banner_rect.x = screen.get_width() // 4

# charger le bouton
play_button = pygame.image.load('assets/button.png')
play_button = pygame.transform.scale(play_button, (400, 150))
play_button_rect = play_button.get_rect()
play_button_rect.x = screen.get_width() / 3.33
play_button_rect.y = screen.get_height() / 2


#  charger notre joueur
game = Game()

running = True
print("lancement")
while running:
    screen.blit(background, (0, -200))  # appliquer l"arriere plan

    # commencement du game
    if game.is_playing:
        game.update(screen)
    else:
        screen.blit(play_button, play_button_rect)
        screen.blit(banner, banner_rect)

        scores = Scoring()
        # afficher les meilleurs score sur l'ecran
        scores.scores.reverse()
        if scores.load_score():
            best_scrore_text = game.font.render(f"Best Score : {scores.best_score}", 1, (100, 100, 0))
            screen.blit(best_scrore_text, (425, 500))
            a = 500
            i = 1
            for score in scores.scores:
                best_scrore_text = game.font.render(f"Meilleur score {i} : {score}", 1, (100, 100, 0))
                screen.blit(best_scrore_text, (740, a))
                a += 30
                i +=1

    pygame.display.flip()  # mettre a jour l'ecran

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            print("Fermeture")

        elif event.type == pygame.KEYDOWN:
            game.pressed[event.key] = True

            if event.key == pygame.K_SPACE:  # detecter si on appuis sur la touche espace
                if game.is_playing:
                    game.player.launch_projectile()
                else:
                    game.start()
                    game.sound_manager.play('click')

        elif event.type == pygame.KEYUP:
            game.pressed[event.key] = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if play_button_rect.collidepoint(event.pos):
                game.start()
                game.sound_manager.play('click')

    #
    clock.tick(FPS)
