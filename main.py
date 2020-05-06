import pygame, random, os
pygame.font.init()

# SET WINDOW
WIDTH = 600
HEIGHT = 750
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")
pygame.display.set_icon(pygame.image.load(os.path.join('assets', 'birdNEW.png')))
BG = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'flappy_background.png')), (WIDTH, HEIGHT))
# LOAD IMAGES
PLAYER_IMG = (pygame.image.load(os.path.join('assets', 'birdNEW.png')))
PIPE_IMG = pygame.image.load(os.path.join('assets', 'pipe.png'))
PIPE_BOTTOM_IMG = pygame.image.load(os.path.join('assets', 'pipe_bottom.png'))
PIPE_TOP_IMG = pygame.image.load(os.path.join('assets', 'pipe_top.png'))
# GRAVITY VARIABLE
GRAVITY = 0.5
FLY_GAP = 150

class Player():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.img = PLAYER_IMG
        self.mask = pygame.mask.from_surface(self.img)
    def draw(self, window):
        window.blit(self.img, (self.x, self.y))
    def move(self, vel):
        self.y += vel

class Barrier():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.img = None
        self.end_img = None
    def draw(self, window):
        window.blit(self.img, (self.x, self.y))
    def move(self, vel):
        self.x += vel

class Upper_Barrier(Barrier):
    def __init__(self, x, y, bot_height):
        super().__init__(x, y)
        self.bottom_height = bot_height
        self.img = PIPE_IMG
        self.end_img = PIPE_TOP_IMG
        self.mask = pygame.mask.from_surface(self.img)
    def draw(self, window):
        self.img = pygame.transform.scale(self.img, (50, HEIGHT - FLY_GAP - self.bottom_height))
        window.blit(self.img, (self.x, self.y))
        window.blit(self.end_img, (self.x, HEIGHT - FLY_GAP - self.bottom_height - self.end_img.get_height()))
    def collision(self, obj):
        self.img = pygame.transform.scale(self.img, (50, HEIGHT - FLY_GAP - self.bottom_height))
        self.mask = pygame.mask.from_surface(self.img)
        return collide(self, obj)

class Lower_Barrier(Barrier):
    def __init__(self, x, y, bot_height):
        super().__init__(x, y)
        self.bottom_height = bot_height
        self.img = PIPE_IMG
        self.end_img = PIPE_BOTTOM_IMG
        self.mask = pygame.mask.from_surface(self.img)
    def draw(self, window):
        self.img = pygame.transform.scale(self.img, (50, self.bottom_height))
        window.blit(self.img, (self.x, self.y))
        window.blit(self.end_img, (self.x, self.y))
    def collision(self, obj):
        self.img = pygame.transform.scale(self.img, (50, self.bottom_height))
        self.mask = pygame.mask.from_surface(self.img)
        return collide(self, obj)

def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (int(offset_x), int(offset_y)))

def main():
    running = True
    FPS = 60
    clock = pygame.time.Clock()
    timer = 0
    score = 0
    score_font = pygame.font.Font("score.ttf", 60)
    # BARRIER AND PLAYER PARAMETERS
    barrier_vel = -2
    upper_barriers = []
    lower_barriers = []
    y_vel = 0
    jump_vel = -5
    player = Player(300, 300)

    # REDRAW WINDOW
    def redraw_window():
        WIN.blit(BG, (0,0))
        player.draw(WIN)
        for barrier in upper_barriers:
            barrier.draw(WIN)
        for barrier in lower_barriers:
            barrier.draw(WIN)
        score_label = score_font.render(f'Score: {score}', 1, (255,255,255))
        WIN.blit(score_label, (WIDTH/2 - score_label.get_width()/2, 100))
        pygame.display.update()

    # GAME OVER
    def game_over():
        GO_font = pygame.font.Font("score.ttf", 70)
        run = True
        timer = 0
        while run:
            clock.tick(FPS)
            WIN.blit(BG, (0,0))
            GO_label = GO_font.render("GAME OVER", 1, (255,255,255))
            WIN.blit(GO_label, (WIDTH/2 - GO_label.get_width()/2, HEIGHT/2 - GO_label.get_height()/2 - 20))
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
            timer += 1

            if timer >= 120: # 2 second delay
                main_menu()

    # INFINITE LOOP
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

        # PLAYER VEL + Y CHANGES
        new_y = player.y
        y_vel += GRAVITY
        new_y += y_vel
        player.y = new_y

        # PLAYER MOVEMENT
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            y_vel = jump_vel
            player.move(y_vel)

        # SPAWN BARRIERS
        timer += 1
        if timer >= 95:
            timer = 0
            bottom_height = random.randint(50, HEIGHT - FLY_GAP - 100)
            barrier = Upper_Barrier(600, 0, bottom_height)
            upper_barriers.append(barrier)
            barrier = Lower_Barrier(600, HEIGHT - bottom_height, bottom_height)
            lower_barriers.append(barrier)

        # CHECK FOR COLLISION AND MOVE BARRIERS
        for barrier in upper_barriers:
            if barrier.collision(player):
                game_over()
            barrier.move(barrier_vel)
            if barrier.x <= 0 - barrier.img.get_width():
                upper_barriers.remove(barrier)
        for barrier in lower_barriers:
            if barrier.collision(player):
                game_over()
            barrier.move(barrier_vel)
            if barrier.x <= 0 - barrier.img.get_width():
                lower_barriers.remove(barrier)
        if player.y >= HEIGHT - player.img.get_height():
            game_over()

        # SCORE
        for barrier in upper_barriers:
            if barrier.x == player.x:
                score += 1

        # REDRAW WINDOW
        redraw_window()


def main_menu():
    menu_font = pygame.font.Font("score.ttf", 45)
    run = True

    while run:
        menu_label = menu_font.render("Press SPACE to play!", 1, (255,255,255))
        WIN.blit(BG, (0,0))
        WIN.blit(menu_label, (WIDTH/2 - menu_label.get_width()/2, HEIGHT/2 - menu_label.get_height()/2 - 20))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    main()


main_menu()
