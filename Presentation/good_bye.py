import pygame
import asyncio
import hand_tracking
import json
from Utils import font_manager, image_manager

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 600

good_bye_image = image_manager.goodbye_screen_image

async def run(screen, ws_client):
    while True:
        
        screen.blit(good_bye_image, (0, 0))
        pygame.display.update()

    return True
