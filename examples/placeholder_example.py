import pygame
from UIComponents import Placeholder, Colors, Button, Slider

# ---------- PYGAME SETUP ----------
pygame.init()
size = (400, 700)
surface = pygame.display.set_mode(size)
clock = pygame.time.Clock()
stop = False
# ----------------------------------

# ----- CREATING A PLACEHOLDER -----
placeholder = Placeholder((10, 200, 300, 400))

# Creating sub objects
slider = Slider((100, 100, 100, 5), placeholder.position, 0, 100, 2, 50, Colors().red, Colors().black, 5, 255, 'My current value', font_size=20)
button = Button((50, 300, 150, 50), placeholder.position, Colors().red, 255, 'Click Me!', font_size=25)

# Adding sub objects
placeholder.add_sub_object(slider)
placeholder.add_sub_object(button)

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
            if slider.clicked(pygame.mouse.get_pos()):
                print('Clicked!')
                 # Do whatever you want to do after user has pressed a slider
            elif button.clicked(pygame.mouse.get_pos()):
                print('Clicked!')
                 # Do whatever you want to do after user has pressed a slider

        elif event.type == pygame.MOUSEBUTTONUP:
            # Keep track of if mouse button is still down
            button_down = False

    # Check if user is slideing
    if button_down:
        slider.clicked(pygame.mouse.get_pos())

    surface.fill(Colors().white)
    
    # Drawing a slider
    placeholder.draw(surface)

    pygame.display.flip()
    clock.tick(30)

pygame.quit()