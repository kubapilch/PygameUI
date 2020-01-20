import pygame
from UIComponents import Background, Colors, Button, Slider

# ---------- PYGAME SETUP ----------
pygame.init()
size = (400, 700)
surface = pygame.display.set_mode(size)
clock = pygame.time.Clock()
stop = False
# ----------------------------------

# ----- CREATING A BACKGROUND -----
background = Background((10, 200, 300, 400), Colors().red, 120)

# Creating sub objects
slider = Slider((100, 100, 100, 5), 0, 100, 2, 50, Colors().red, Colors().black, 'My current value', font_size=20)
button = Button((50, 300, 150, 50), Colors().red, 'Click Me!')

# Adding sub objects
background.add_sub_object(slider)
background.add_sub_object(button)

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
            
            
            if slider.clicked(pygame.mouse.get_pos()): # Checking if user has clicked the slider and running click_function is yes
                print('Clicked!')
                # Do whatever you want to do after user has pressed a slider
           
            elif button.clicked(pygame.mouse.get_pos()): # Checking if user has clicked the button and running click_function is yes
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
    background.draw(surface)

    pygame.display.flip()
    clock.tick(30)

pygame.quit()