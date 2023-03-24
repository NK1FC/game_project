'''
Creating a game using tutorials
'''
import sys
import pygame
import os

pygame.init()

#colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

#Fonts for game
HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)

#Screen size of the game
WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('NEW Game')
FPS = 60

#Rect object
BORDER = pygame.Rect(WIDTH / 2 - 5, 0, 10, HEIGHT)

#Spaceships Size
SHIP_WIDTH = 55
SHIP_HEIGHT = 40

DURING_GAME = (SHIP_WIDTH, SHIP_WIDTH)
AFTER_WIN = (300, 300)

#Velocity
VELOCITY = 10
BULLET_VEL = 10

#Importing sprites as variables
YELLOW_SHIP = pygame.image.load(os.path.join('Assets', 's_y.png'))
RED_SHIP = pygame.image.load(os.path.join('Assets', 's_r.png'))
BULLET = pygame.image.load(os.path.join('Assets', 'bullet.png'))

#Resize the ship
YELLOW_SHIP = pygame.transform.scale(YELLOW_SHIP, DURING_GAME)
RED_SHIP = pygame.transform.scale(RED_SHIP, DURING_GAME)

#Resize the bullet
BULLET = pygame.transform.scale(BULLET, (20, 40))

#Bullet for red ship
RED_BULLET = pygame.transform.rotate(BULLET, 90)

#Bullet for yellow_ship
YELLOW_BULLET = pygame.transform.rotate(BULLET, -90)

#Bullet list
YELLOW_LIST = []
RED_LIST = []

#Rotate the yellow ship
YELLOW_SHIP = pygame.transform.rotate(YELLOW_SHIP, 90)

#Rotate the red ship
RED_SHIP = pygame.transform.rotate(RED_SHIP, -90)

#Events for Players
RED_HIT = pygame.USEREVENT + 1
YELLOW_HIT = pygame.USEREVENT + 2


def draw_window(rect_red, rect_yellow, red_health, yellow_health):
    '''
    Draw the main window when game startss
    '''
    WIN.fill(BLACK)
    pygame.draw.rect(WIN, WHITE, BORDER)
    WIN.blit(YELLOW_SHIP, (rect_yellow.x, rect_yellow.y))
    WIN.blit(RED_SHIP, (rect_red.x, rect_red.y))
    red_health_text = HEALTH_FONT.render("LIFE:" + str(red_health), 1, WHITE)
    yellow_health_text = HEALTH_FONT.render('LIFE:' + str(yellow_health), 1,
                                            WHITE)
    WIN.blit(red_health_text, (10, 10))
    WIN.blit(yellow_health_text, (700, 10))

    for bullets in YELLOW_LIST:
        bullets.x += BULLET_VEL
        #Post the even on collision.
        if rect_red.colliderect(bullets):
            pygame.event.post(pygame.event.Event(RED_HIT))
            YELLOW_LIST.remove(bullets)
        elif bullets.x > 900:
            YELLOW_LIST.remove(bullets)
        WIN.blit(YELLOW_BULLET, (bullets.x - 1, bullets.y - 6))

    for bullets in RED_LIST:
        bullets.x -= BULLET_VEL
        #Post the even on collision.
        if rect_yellow.colliderect(bullets):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            RED_LIST.remove(bullets)
        elif bullets.x < 0:
            RED_LIST.remove(bullets)
        WIN.blit(RED_BULLET, (bullets.x - 3, bullets.y - 6))
    pygame.display.update()


def draw_winner(winnertext):
    '''
    Draw the winner screen
    '''
    WIN.fill(BLACK)
    playagain = 'Press p to play again'
    play = HEALTH_FONT.render(playagain, 1, WHITE)
    winner = WINNER_FONT.render(winnertext, 1, WHITE)
    WIN.blit(winner, (100, 100))
    WIN.blit(play, (300, 255))
    pygame.display.update()


def move_yellow(rect_yellow, key_pressed):
    '''
    Control the movement of yellow ship
    '''
    if key_pressed[pygame.K_a] and rect_yellow.x - VELOCITY > 0:  #LEFT
        rect_yellow.x -= VELOCITY
    if key_pressed[pygame.K_d] and rect_yellow.x + VELOCITY < 400:  #RIGHT
        rect_yellow.x += VELOCITY
    if key_pressed[pygame.K_w] and rect_yellow.y > 0:  #UP
        rect_yellow.y -= VELOCITY
    if key_pressed[pygame.K_s] and rect_yellow.y < 440:  #DOWN
        rect_yellow.y += VELOCITY


def move_red(rect_red, key_pressed):
    '''
    Control the movement of red ship
    '''
    if key_pressed[pygame.K_LEFT] and rect_red.x + VELOCITY > 455:  #LEFT
        rect_red.x -= VELOCITY
    if key_pressed[pygame.K_RIGHT] and rect_red.x + VELOCITY < 850:  #RIGHT
        rect_red.x += VELOCITY
    if key_pressed[pygame.K_UP] and rect_red.y > 0:  #UP
        rect_red.y -= VELOCITY
    if key_pressed[pygame.K_DOWN] and rect_red.y < 440:  #DOWN
        rect_red.y += VELOCITY


def main():
    '''
    Main game loop.
    '''
    rect_red = pygame.Rect(700, 300, SHIP_WIDTH, SHIP_HEIGHT + 14)
    rect_yellow = pygame.Rect(100, 300, SHIP_WIDTH, SHIP_HEIGHT + 14)
    red_health = 100
    yellow_health = 100

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(YELLOW_LIST) < 10:
                    bullet = pygame.Rect(rect_yellow.x + 50,
                                         rect_yellow.y + 21, 30, 6)
                    YELLOW_LIST.append(bullet)

                if event.key == pygame.K_RCTRL and len(RED_LIST) < 10:
                    bullet = pygame.Rect(rect_red.x - 33, rect_red.y + 26, 30,
                                         6)
                    RED_LIST.append(bullet)
                if event.key == pygame.K_p and (red_health <= 0
                                                or yellow_health <= 0):
                    YELLOW_LIST.clear()
                    RED_LIST.clear()
                    main()

            #Event take place then change the health
            if event.type == RED_HIT:
                yellow_health -= 1
            if event.type == YELLOW_HIT:
                red_health -= 1
        winner_text = ""

        #Deciding on winner
        if red_health <= 0:
            winner_text = "Red wins!!!"
            draw_winner(winner_text)
        if yellow_health <= 0:
            winner_text = "Yellow wins!!!"
            draw_winner(winner_text)

        if red_health >= 1 and yellow_health >= 1:
            key_pressed = pygame.key.get_pressed()
            move_yellow(rect_yellow, key_pressed)
            move_red(rect_red, key_pressed)
            draw_window(rect_red, rect_yellow, red_health, yellow_health)


if __name__ == '__main__':
    main()
