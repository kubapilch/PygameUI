import pygame
from UIComponents import Button, Colors

# ---------- PYGAME SETUP ----------
pygame.init()
size = (400, 700)
surface = pygame.display.set_mode(size)
clock = pygame.time.Clock()
stop = False
# ----------------------------------


# ---------- CREATING A BUTTON ----------
def click(): # Simple function ilustrating how to add a function to click
    if button.color == Colors().red:
        button.color = Colors().green
    else:
        button.color = Colors().red

button = Button((125, 100, 150, 50), (0, 0), Colors().red, 255, 'Click Me!', font_size=25, click_function=click)


# Standard game loop
while not stop:
    # Standard event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            stop = True
        # User clicked mouse button (any)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Checking if user has clicked the button and running click_function
            if button.clicked(pygame.mouse.get_pos()):
                print('Clicked!')
                # Do whatever you want to do after user has pressed a button

    surface.fill(Colors().white)
    
    # Drawing a button
    button.draw(surface)

    pygame.display.flip()
    clock.tick(30)

pygame.quit()