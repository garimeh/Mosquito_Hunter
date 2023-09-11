import pygame
import random
import time
import math
pygame.init()
pygame.mixer.init()
pygame.font.init()

window_width = 700
window_height = 700
WIN = pygame.display.set_mode((window_width, window_height))
RACKETHEIGHT, RACKETWIDTH = 100, 250
MOSQUITOHEIGHT, MOSQUITOWIDTH = 55, 40
SPARKHEIGHT, SPARKWIDTH = 55, 40
SCOREFONT = pygame.font.SysFont('timesroman', 100)
SMALLFONT = pygame.font.SysFont('timesroman', 36)
MOSQUITOHITSOUND = pygame.mixer.Sound('/Users/garimaminocha/Projects/Pygame/Mosquito game/Assets/zapsplat_cartoon_anime_hit_zap_laser_001_71431.mp3')
SPACE = pygame.transform.scale(pygame.image.load('/Users/garimaminocha/Projects/Pygame/Mosquito game/Assets/diy floating desk for wasted corner space_.jpeg'), (window_width, window_height))

window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Mosquito Hunter")

mosquito_img = pygame.image.load("/Users/garimaminocha/Projects/Pygame/Mosquito game/Assets/mosquito1.png")
mosquito_s = pygame.transform.scale(mosquito_img, (MOSQUITOHEIGHT, MOSQUITOWIDTH))
racket_img = pygame.image.load("Mosquito game/Assets/racker2.png")
racket_s = pygame.transform.scale(racket_img, (RACKETHEIGHT, RACKETWIDTH))
spark_img = pygame.image.load("/Users/garimaminocha/Projects/Pygame/Mosquito game/Assets/spark.png")
spark_s = pygame.transform.scale(spark_img, (SPARKHEIGHT, SPARKWIDTH))

clock = pygame.time.Clock()

class Mosquito(pygame.sprite.Sprite):
    def __init__(self, speed, main_game): 
        super().__init__()
        self.image = mosquito_s
        self.rect = self.image.get_rect()
        self.spawn_x = 0
        self.spawn_y = random.randint(0, window_height - self.rect.height)
        self.rect.x = self.spawn_x
        self.rect.y = self.spawn_y
        self.speed = speed
        self.angle = random.uniform(0, math.pi * 2)
        self.main_game = main_game  

    def update(self):
        self.rect.x += self.speed
        self.rect.y = self.spawn_y + int(50 * math.sin(self.angle))
        self.angle += 0.1
        if self.rect.x > window_width:
            self.kill()
            decrease_miss(self.main_game)  

class Spark(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        self.image = spark_s
        self.rect = self.image.get_rect()
        self.rect.center = position
        self.time_created = time.time()

    def update(self):
        if time.time() - self.time_created > 1:
            self.kill()

def decrease_miss(main_game):
    main_game.misses -= 1  
    if main_game.misses <= 0:
        game_over(main_game.score)

class Racket(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = racket_s
        self.rect = self.image.get_rect()
        self.rect.center = (window_width // 2, window_height // 2)

    def update(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        self.rect.center = (mouse_x, mouse_y)

def game_over(score):
    game_over_font = pygame.font.Font(None, 48)
    game_over_text = game_over_font.render("Game Over", True, (0, 0, 0))
    score_text = game_over_font.render(f"Your Score: {score}", True, (0, 0, 0))

    window.blit(game_over_text, (window_width // 2 - 150, window_height // 2 - 20))
    window.blit(score_text, (window_width // 2 - 150, window_height // 2 + 30))
    pygame.display.flip()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

def main():
    class MainGame:
        def __init__(self):
            self.misses = 5
            self.score = 0

    main_game = MainGame()

    mosquito_speed = 2
    speed_increase_interval = 10
    speed_increase_timer = 0
    last_score_checkpoint = 0  

    mosquitoes = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()

    racket = Racket()
    all_sprites.add(racket)

    start_time = time.time()
    mosquito_spawn_interval = 2
    mosquito_spawn_timer = 0

    while True:
        clock.tick(60)
        WIN.blit(SPACE, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        all_sprites.update()

        if main_game.misses <= 0:
            game_over(main_game.score)

        mosquito_spawn_timer += time.time() - start_time
        speed_increase_timer += time.time() - start_time
        start_time = time.time()

        if speed_increase_timer >= speed_increase_interval:
            mosquito_speed += 1
            speed_increase_timer = 0

        if main_game.score // 10 > last_score_checkpoint:
            last_score_checkpoint = main_game.score // 10
            mosquito_spawn_interval *= 0.9  
            speed_increase_interval *= 0.9  

        if mosquito_spawn_timer >= mosquito_spawn_interval:
            new_mosquito = Mosquito(mosquito_speed, main_game)
            mosquitoes.add(new_mosquito)
            all_sprites.add(new_mosquito)
            mosquito_spawn_timer = 0

        hits = pygame.sprite.spritecollide(racket, mosquitoes, True)
        for hit in hits:
            main_game.score += 1
            spark = Spark(hit.rect.center)
            all_sprites.add(spark)
            MOSQUITOHITSOUND.play()

        all_sprites.draw(window)

        score_text = SMALLFONT.render(f"Score: {main_game.score}", True, (0, 0, 0))
        misses_text = SMALLFONT.render(f"Misses: {main_game.misses}", True, (0, 0, 0))
        window.blit(score_text, (window_width - 200, 10))
        window.blit(misses_text, (10, 10))
        pygame.display.update()

        if main_game.misses <= 0:
            game_over(main_game.score)


if __name__ == "__main__":
    main()