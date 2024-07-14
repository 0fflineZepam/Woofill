import pygame
from random import randint

pygame.init()
window = pygame.display.set_mode((1280, 720))

class Player:
    def __init__(self):
        self.x_cord = 640  # współrzędna x (środek ekranu)
        self.y_cord = 360  # współrzędna y (środek ekranu)
        self.image = pygame.image.load("MeChampion.png")  # wczytuje grafikę
        self.original_image = self.image  # zapisz oryginalny obraz
        self.flipped_image = pygame.transform.flip(self.image, True, False)  # odwróć obraz w poziomie
        self.width = self.image.get_width()  # szerokość
        self.height = self.image.get_height()  # wysokość
        self.speed = 4  # prędkość
        self.hitbox = pygame.Rect(self.x_cord, self.y_cord, self.width, self.height)
        self.direction = 'left'  # domyślny kierunek

    def tick(self, keys, background_x, background_y):
        if keys[pygame.K_w] and self.y_cord > 0:
            self.y_cord -= self.speed
        if keys[pygame.K_a] and self.x_cord > 0:
            self.x_cord -= self.speed
            self.direction = 'left'
        if keys[pygame.K_s] and self.y_cord < 720 - self.height:
            self.y_cord += self.speed
        if keys[pygame.K_d] and self.x_cord < 1280 - self.width:
            self.x_cord += self.speed
            self.direction = 'right'

        # Poruszanie tłem zamiast postaci
        if keys[pygame.K_w] and background_y < 0:
            background_y += self.speed
        if keys[pygame.K_a] and background_x < 0:
            background_x += self.speed
        if keys[pygame.K_s] and background_y > -(1024 - 720):
            background_y -= self.speed
        if keys[pygame.K_d] and background_x > -(2049 - 1280):
            background_x -= self.speed

        self.hitbox = pygame.Rect(self.x_cord, self.y_cord, self.width, self.height)
        return background_x, background_y

    def draw(self):
        if self.direction == 'right':
            window.blit(self.flipped_image, (self.x_cord, self.y_cord))
        else:
            window.blit(self.original_image, (self.x_cord, self.y_cord))

class Tool:
    def __init__(self):
        self.x_cord = randint(0, 2049)
        self.y_cord = randint(0, 1024)
        self.image = pygame.image.load("klucz1big.png")
        self.width = self.image.get_width()  # szerokość
        self.height = self.image.get_height()  # wysokość
        self.hitbox = pygame.Rect(self.x_cord, self.y_cord, self.width, self.height)

    def draw(self, background_x, background_y):
        window.blit(self.image, (self.x_cord + background_x, self.y_cord + background_y))
        self.hitbox = pygame.Rect(self.x_cord + background_x, self.y_cord + background_y, self.width, self.height)

def draw_score(score):
    font = pygame.font.Font(None, 36)  # Ustawienie czcionki
    text = font.render(f'Zebrane narzędzia: {score}', True, (255, 0, 0))  # Renderowanie tekstu
    window.blit(text, (500, 10))  # Rysowanie tekstu na ekranie

def main():
    run = True
    player = Player()
    clock = 0
    score = 0
    tools = []
    background = pygame.image.load("tlo_czarne.png")
    background_x, background_y = 0, 0
    while run:
        clock += pygame.time.Clock().tick(60) / 1000  # maksymalnie 60 fps
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # jeśli gracz zamknie okienko
                run = False

        keys = pygame.key.get_pressed()
        if clock >= 2:
            clock = 0
            tools.append(Tool())

        background_x, background_y = player.tick(keys, background_x, background_y)

        for tool in tools:
            if player.hitbox.colliderect(tool.hitbox):
                tools.remove(tool)
                score += 1

        window.blit(background, (background_x, background_y))  # rysowanie tła
        for tool in tools:
            tool.draw(background_x, background_y)
        player.draw()

        draw_score(score)  # Wywołanie funkcji rysującej wynik

        pygame.display.update()

    print(f"Brawo zebrałeś: {score} Narzędzi Pawła")

if __name__ == "__main__":
    main()