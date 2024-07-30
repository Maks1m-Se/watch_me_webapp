# /// script
# dependencies = [
#  "pygame-ce",
#  "pygame",
#  "sys",
#  "asyncio"
# ]
# ///

import pygame
import sys
import asyncio

# Button class definition
class Button:
    def __init__(self, x, y, width, height, text, color, hover_color, text_color, font):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.font = font

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        mouse_clicked = pygame.mouse.get_pressed()

        # Change color on hover
        if self.rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, self.hover_color, self.rect)
            if mouse_clicked[0]:
                return True
        else:
            pygame.draw.rect(screen, self.color, self.rect)

        # Render text
        text_surf = self.font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

        return False

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Watch Me WebApp')

# Font for button text
font = pygame.font.SysFont(None, 40)

# Create a quit button
quit_button = Button(300, 250, 200, 100, 'Quit', (200, 0, 0), (255, 0, 0), (255, 255, 255), font)

running = True
async def main():
    global running

    pygame.display.set_caption("Test App")

    while running:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((255, 255, 255))

        # Draw the quit button and check for clicks
        if quit_button.draw(screen):
            running = False

        pygame.display.flip()
        await asyncio.sleep(0)
    pygame.quit()
    sys.exit()
    


asyncio.run(main())
