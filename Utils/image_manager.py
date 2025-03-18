import pygame

# Screen
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 600

empty_screen_image = pygame.image.load("Resources/Images/screen_empty.png")
empty_screen_image = pygame.transform.scale(empty_screen_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

start_screen_image = pygame.image.load("Resources/Images/screen_start.png")
start_screen_image = pygame.transform.scale(start_screen_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

result_screen_image = pygame.image.load("Resources/Images/screen_result.png")
result_screen_image = pygame.transform.scale(result_screen_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

goodbye_screen_image = pygame.image.load("Resources/Images/screen_goodbye.png")
goodbye_screen_image = pygame.transform.scale(goodbye_screen_image, (SCREEN_WIDTH, SCREEN_HEIGHT))


# Button
BUTTON_WIDTH, BUTTON_HEIGHT = 250, 80
BUTTON_RADIUS = 16
button_rect = pygame.Rect((SCREEN_WIDTH - BUTTON_WIDTH) // 2, SCREEN_HEIGHT - 120, BUTTON_WIDTH, BUTTON_HEIGHT)

start_button_image = pygame.image.load("Resources/Images/button_start.png")
start_button_image = pygame.transform.scale(start_button_image, (BUTTON_WIDTH, BUTTON_HEIGHT))

next_button_image = pygame.image.load("Resources/Images/button_next.png")
next_button_image = pygame.transform.scale(next_button_image, (BUTTON_WIDTH, BUTTON_HEIGHT))


# view
PHOTO_WIDTH = 700
PHOTO_HEIGHT = 350
photo_view_image = pygame.image.load("Resources/Images/view_photo.png")
photo_view_image = pygame.transform.scale(photo_view_image, (PHOTO_WIDTH, PHOTO_HEIGHT))
