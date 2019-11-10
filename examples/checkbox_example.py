import pygame
from UIComponents import Checkbox, Colors

# ---------- PYGAME SETUP ----------
pygame.init()
size = (400, 700)
surface = pygame.display.set_mode(size)
clock = pygame.time.Clock()
stop = False
# ----------------------------------

# ------- CREATING A CHECKBOX ------
def checked(): # Simple function ilustrating how to add a function to click
    if checkbox.checked:
        checkbox.text = 'Uncheck Me!'
    else:
        checkbox.text = 'Check Me!'

checkbox = Checkbox((50, 100, 40, 40), (0,0), Colors().black, Colors().red, 255, 'Check Me!', font_size=30, click_function=checked)

# Standard game loop
while not stop:
    # Standard event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            stop = True
        # User clicked mouse button (any)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Checking if user has clicked the checkbox and running click_function
            if checkbox.clicked(pygame.mouse.get_pos()):
                print('Clicked!')
                 # Do whatever you want to do after user has pressed a checkbox

    surface.fill(Colors().white)
    
    # Drawing a checkbox
    checkbox.draw(surface)

    pygame.display.flip()
    clock.tick(30)

pygame.quit()