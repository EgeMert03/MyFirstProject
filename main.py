import pygame
import random

# Pygame'i başlat
pygame.init()

# Ekran boyutları
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Renkler
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (135, 206, 250)
GREEN = (0, 255, 0)

# FPS ayarı
clock = pygame.time.Clock()
FPS = 60

# Arka plan resmi
background_img = pygame.image.load("Görüntü.jpg")  # Arka plan resmi
background_img = pygame.transform.scale(background_img, (SCREEN_WIDTH, SCREEN_HEIGHT))  # Ekran boyutuna göre ölçeklendir

# Kuş ayarları

# Kuş ayarları
bird_img = pygame.image.load("Gnar.jpg")  # Kuş resmini doğru yol ile koyun
bird_img = pygame.transform.scale(bird_img, (40, 30))  # Kuş boyutlandırma
bird_x = 100
bird_y = SCREEN_HEIGHT // 2
bird_velocity = 0
gravity = 0.5
jump_strength = -8

# Boru ayarları
pipe_width = 70
pipe_gap = 200
pipe_velocity = 3
pipes = []
pipe_frequency = 1500  # Milisaniye (boru ekleme sıklığı)

# Sesler
jump_sound = pygame.mixer.Sound("Yeni Kayıt.wav")  # Zıplama sesi
collision_sound = pygame.mixer.Sound("Yeni Kayıt 4 2.wav")  # Çarpışma sesi

# Skor
score = 0
font = pygame.font.Font(None, 36)

# Oyun durumu
game_over = False

# Boru oluşturma
def create_pipe():
    height = random.randint(100, SCREEN_HEIGHT - pipe_gap - 100)
    return {'x': SCREEN_WIDTH, 'height': height}

# Borular listesine bir başlangıç borusu ekle
pipes.append(create_pipe())

def draw_text(text, x, y, color=BLACK):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))
def main():
    global bird_y, bird_velocity, pipes, game_over, score

    # Zamanlayıcı
    pygame.time.set_timer(pygame.USEREVENT, pipe_frequency)

    while True:
        screen.fill(BLUE)

        # Olayları yakala
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not game_over:
                    bird_velocity = jump_strength
                    jump_sound.play()
                if event.key == pygame.K_r and game_over:
                    # Oyun yeniden başlatılır
                    bird_y = SCREEN_HEIGHT // 2
                    bird_velocity = 0
                    pipes = [create_pipe()]
                    score = 0
                    game_over = False
            if event.type == pygame.USEREVENT and not game_over:
                pipes.append(create_pipe())

        # Kuş hareketi
        if not game_over:
            bird_velocity += gravity
            bird_y += bird_velocity

            # Arka planı çiz
            screen.blit(background_img, (0, 0))

        # Boruları güncelle ve çiz
        for pipe in pipes:
            if not game_over:
                pipe['x'] -= pipe_velocity

            # Üst ve alt boruları çiz
            pygame.draw.rect(screen, GREEN, (pipe['x'], 0, pipe_width, pipe['height']))
            pygame.draw.rect(screen, GREEN, (pipe['x'], pipe['height'] + pipe_gap, pipe_width, SCREEN_HEIGHT - pipe['height'] - pipe_gap))

        # Boruların ekrandan çıktığını kontrol et
        pipes = [pipe for pipe in pipes if pipe['x'] + pipe_width > 0]

        # Çarpışma kontrolü
        bird_rect = pygame.Rect(bird_x, bird_y, 40, 30)
        for pipe in pipes:
            top_rect = pygame.Rect(pipe['x'], 0, pipe_width, pipe['height'])
            bottom_rect = pygame.Rect(pipe['x'], pipe['height'] + pipe_gap, pipe_width, SCREEN_HEIGHT - pipe['height'] - pipe_gap)
            if bird_rect.colliderect(top_rect) or bird_rect.colliderect(bottom_rect) or bird_y >= SCREEN_HEIGHT - 30:
                game_over = True
                collision_sound.play()

        # Skoru güncelle
        if not game_over:
            for pipe in pipes:
                if bird_x > pipe['x'] + pipe_width and not pipe.get('scored', False):
                    pipe['scored'] = True
                    score += 1

        # Kuşu çiz
        screen.blit(bird_img, (bird_x, bird_y))

        # Skoru çiz
        draw_text(f"Score: {score}", 10, 10)

        # Oyun bitti mesajı
        if game_over:
            draw_text("GAME OVER", SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT // 2 - 20, color=BLACK)
            draw_text("Press R to Restart", SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 20, color=BLACK)

        # Ekranı güncelle
        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
