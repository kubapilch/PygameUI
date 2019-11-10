import pygame
from UIComponents import Slider, Colors

# ---------- PYGAME SETUP ----------
pygame.init()
size = (400, 700)
surface = pygame.display.set_mode(size)
clock = pygame.time.Clock()
stop = False
# ----------------------------------

# -------- CREATING A SLIDER -------
def slide():
    pass

slider1 = Slider((100, 100, 100, 5), (0,0), 0, 100, 2, 50, Colors().red, Colors().black, 5, 255, 'My current value', font_size=20, click_function=slide)
slider2 = Slider((100, 300, 200, 5), (0,0), 10, 30, 0.1, 20, Colors().red, Colors().black, 5, 255, 'My current value', font_size=20, click_function=slide)

button_down = False

# Standard game loop
while not stop:
    # Standard event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            stop = True
        # User clicked mouse button (any)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Keep track of if mouse button is still down
            button_down = True
            
            # Checking if user has clicked the slider and running click_function
            if slider1.clicked(pygame.mouse.get_pos()):
                print('Clicked!')
                 # Do whatever you want to do after user has pressed a slider
            elif slider2.clicked(pygame.mouse.get_pos()):
                print('Clicked!')
                 # Do whatever you want to do after user has pressed a slider
        elif event.type == pygame.MOUSEBUTTONUP:
            # Keep track of if mouse button is still down
            button_down = False

    # Check if user is slideing
    if button_down:
        slider1.clicked(pygame.mouse.get_pos())
        slider2.clicked(pygame.mouse.get_pos())

    surface.fill(Colors().white)
    
    # Drawing a slider
    slider1.draw(surface)
    slider2.draw(surface)

    pygame.display.flip()
    clock.tick(30)

pygame.quit()