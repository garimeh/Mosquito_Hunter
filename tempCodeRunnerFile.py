def main():
#     global misses
#     misses = 5
#     mosquito_speed = 2
#     speed_increase_interval = 10  # Increase speed every 10 seconds
#     speed_increase_timer = 0

#     mosquitoes = pygame.sprite.Group()
#     all_sprites = pygame.sprite.Group()

#     racket = Racket()
#     all_sprites.add(racket)

#     score = 0
#     start_time = time.time()
#     mosquito_spawn_interval = 2
#     mosquito_spawn_timer = 0

#     while True:
#         clock.tick(60)
#         window.fill(white)

#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 pygame.quit()
#                 return

#         all_sprites.update()

#         if misses <= 0:
#             draw_score("Game Over", f"Score: {score}", 5)  # Display the game over text
#             misses = 5
#             score = 0
#             mosquitoes.empty()
#             all_sprites.empty()
#             racket.rect.center = (window_width // 2, window_height // 2)
#             start_time = time.time()

#         mosquito_spawn_timer += time.time() - start_time
#         speed_increase_timer += time.time() - start_time
#         start_time = time.time()

#         if speed_increase_timer >= speed_increase_interval:
#             mosquito_speed += 1
#             speed_increase_timer = 0

#         if mosquito_spawn_timer >= mosquito_spawn_interval:
#             new_mosquito = Mosquito(score)
#             mosquitoes.add(new_mosquito)
#             all_sprites.add(new_mosquito)
#             mosquito_spawn_timer = 0

#         hits = pygame.sprite.spritecollide(racket, mosquitoes, True)
#         for hit in hits:
#             score += 1
#             spark = Spark(hit.rect.center)
#             all_sprites.add(spark)

#         for mosquito in mosquitoes:
#             if mosquito.rect.x > window_width:
#                 mosquito.kill()

#         all_sprites.update()

#         # Check if any mosquito has reached the edge of the screen
#         for mosquito in mosquitoes:
#             if mosquito.rect.x > window_width:
#                 decrease_miss(score)  # Decrement misses counter for each missed mosquito
#                 mosquitoes.remove(mosquito)
#                 mosquito.kill()

#         mosquitoes.update()

#         all_sprites.draw(window)

#         score_text = SMALLFONT.render(f"Score: {score}", True, (0, 0, 0))
#         misses_text = SMALLFONT.render(f"Misses: {misses}", True, (0, 0, 0))
#         window.blit(score_text, (window_width - 200, 10))
#         window.blit(misses_text, (10, 10))
#         pygame.display.update()