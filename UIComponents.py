import pygame
from decimal import Decimal

class UIObject():
    def __init__(self, placement:tuple):
        self.placement = placement # (x, y, width, height)
        self.x = placement[0]
        self.y = placement[1]
        self.width = placement[2]
        self.height = placement[3]

        self.__sub_objects = []

    @property
    def size(self):
        return (self.placement[2], self.placement[3])
    
    @size.setter
    def size(self, s):
        self.width = s[0]
        self.height = s[1]
        self.placement = (self.x, self.y, *s)

    @property
    def position(self):
        return (self.placement[0], self.placement[1])
    
    @position.setter
    def position(self, pos):
        self.x = pos[0]
        self.y = pos[1]
        self.placement = (*pos, self.width, self.height)

    def draw(self, surface):
        """
        Draw all sub objects, their sub objects and main object to a given surface
        """
        pass

class Surfaces(UIObject):
    def __init__(self, placement:tuple, color, alpha):
        super().__init__(placement)
        self._color = color
        self._alpha = alpha
        self.__sub_objects = []

        self.createSurface()

    @property
    def color(self):
        return self._color
    
    @color.setter
    def color(self, c):
        self._color = c
        self.surface.fill((*self._color, self._alpha))

    @property
    def alpha(self):
        return self._alpha

    @alpha.setter
    def alpha(self, a):
        self._alpha = a
        self.surface.fill((*self._color, self._alpha))

    def createSurface(self):
        """
        Creates main object surface and sets its color and alpha 
        """
        # Create main surface
        self.surface = pygame.Surface(self.size, pygame.SRCALPHA)

        # Set color and alpha
        self.surface.fill((*self._color, self._alpha))

    def add_sub_object(self, obj):
        """
        Adds sub object to a list and determine if user want the position of the object to be relative to the parent object or tp the entire screen
        """
        self.__sub_objects.append(obj)

    def delete_sub_object(self, obj):
        self.__sub_objects.remove(obj)  

class Placeholder(Surfaces):

    def __init__(self, placement:tuple):
        super().__init__(placement, (0, 0, 0), 0)
        self.placement = placement # (x, y, width, height)
        self.x = placement[0]
        self.y = placement[1]
        self.width = placement[2]
        self.height = placement[3]
        self.__sub_objects = []

        # Create main surface
        self.surface = pygame.Surface(self.size, pygame.SRCALPHA)

    def draw(self, surface):
        # Clear before drawing
        self.surface.fill((0, 0, 0, 0))

        # Check if has sub objects and if so then draw them
        if self.__sub_objects:

            for obj in self.__sub_objects:
                # Draw subobjects and their subobjects to their surface
                obj.draw(self.surface)

        # Blit main surface to given surface
        surface.blit(self.surface, self.position)
    
    def add_sub_object(self, obj):
        # Add sub object to a list
        self.__sub_objects.append(obj)

    def delete_sub_object(self, obj):
        self.__sub_objects.remove(obj)


    # ---- Placeholders has no color and alpha ----
    @property
    def color(self):
        return None

    @color.setter
    def color(self, c):
        pass

    @property
    def alpha(self):
        return 0

    @alpha.setter
    def alpha(self, a):
        pass

class Background(Surfaces):
    def __init__(self, placement:tuple, color, alpha):
        super().__init__(placement, color, alpha)
        self.__sub_objects = []

    def draw(self, surface):
        # Clean before drawing
        self.surface.fill((*self.color, self.alpha))
        
        # Check if has sub objects and if so then draw them
        if self.__sub_objects:

            for obj in self.__sub_objects:
                # Draw subobjects and their subobjects to their surface
                obj.draw(self.surface)

        # Blit main surface to given surface
        surface.blit(self.surface, self.position)
    
    def add_sub_object(self, obj):
        # Add sub object to a list
        self.__sub_objects.append(obj)

    def delete_sub_object(self, obj):
        self.__sub_objects.remove(obj)  


class Button(UIObject):
    def __init__(self, placement:tuple, reference_position:tuple, color, alpha, text, font="monospace", font_size=10, font_color=(0, 0, 0), click_function=None):
        super().__init__(placement)
        self.font = font
        self.font_size = font_size
        self.font_color = font_color
        self.color = color
        self.alpha = alpha
        self.reference_position = reference_position
        self.text = text
        self.click_function = click_function

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, t):
        # Render new label
        self._text = t
        self.label = pygame.font.SysFont(self.font, self.font_size).render(t, 1, (*self.font_color, self.alpha))

    def draw(self, surface):
        # Draw button
        pygame.draw.rect(surface, (*self.color, self.alpha), self.placement)
        # Draw label
        surface.blit(self.label, (self.x + (self.width/2 - self.label.get_width()/2), self.y+(self.height/2 - self.label.get_height()/2)))

    def clicked(self, pos):
        if pos[0] > self.x + self.reference_position[0] and pos[0] < self.x + self.width + self.reference_position[0]:
            if pos[1] > self.y + self.reference_position[1]  and pos[1] < self.y + self.height + self.reference_position[1] :
                # If user speciefied small function execute it
                if self.click_function is not None:
                    self.click_function()
                
                return True

        return False

class Checkbox(UIObject):
    def __init__(self, placement:tuple, reference_position:tuple, checkbox_color, indicator_color, alpha, text, spacing=10, font="monospace", font_size=10, font_color=(0, 0, 0), click_function=None):
        super().__init__(placement)
        self.font = font
        self.font_size = font_size
        self.font_color = font_color
        self.checkbox_color = checkbox_color
        self.indicator_color = indicator_color
        self.alpha = alpha
        self.reference_position = reference_position
        self.spacing = spacing
        self.text = text
        self.click_function = click_function
        self.checked = False

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, t):
        # Render new label
        self._text = t
        self.label = pygame.font.SysFont(self.font, self.font_size).render(t, 1, (*self.font_color, self.alpha))

    def draw(self, surface):
        # Draw button
        pygame.draw.rect(surface, (*self.checkbox_color, self.alpha), self.placement)

        # Draw checked indicator aka circle
        if self.checked:
            pygame.draw.circle(surface, self.indicator_color, (int(self.x + self.width/2), int(self.y + self.height/2)), int(self.width/4))

        # Draw label
        surface.blit(self.label, (self.x + self.width + 10, self.y+(self.height/2 - self.label.get_height()/2)))
    
    def clicked(self, pos):
        if pos[0] > self.x + self.reference_position[0] and pos[0] < self.x + self.width + self.reference_position[0]:
            if pos[1] > self.y + self.reference_position[1]  and pos[1] < self.y + self.height + self.reference_position[1] :
                # Unmark or mark 
                self.checked = not self.checked
                
                # If user speciefied small function execute it
                if self.click_function is not None:
                    self.click_function()

                return True

        return False

class Slider(UIObject):
    def __init__(self, placement:tuple, reference_position:tuple, min_value, max_value, jump, default_value, slider_color, bar_color, slider_radius, alpha, text, spacing=10, font="monospace", font_size=10, font_color=(0, 0, 0), click_function=None):
        super().__init__(placement)
        self.font = font
        self.font_size = font_size
        self.font_color = font_color
        self.slider_color = slider_color
        self.bar_color = bar_color
        self.alpha = alpha
        self.text = text
        self.reference_position = reference_position
        self.spacing = spacing
        self.click_function = click_function
        self.min_value = min_value
        self.max_value = max_value
        self.jump = jump
        self.slider_radius = slider_radius
        self.value = default_value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, v):
        # If the value is a whole number show it like '7' instead of '7.0'
        if float(v).is_integer():
            self._value = int(v)
        else:
            self._value = v

        # Render new label
        self.label = pygame.font.SysFont(self.font, self.font_size).render(f'{self.text}: {self.value}', 1, (*self.font_color, self.alpha))

    def draw(self, surface):
        # Draw a bar
        pygame.draw.rect(surface, (*self.bar_color, self.alpha), self.placement)

        #Draw slider
        pixels_per_one_jump = (self.placement[2]/((self.max_value - self.min_value)/self.jump))
        center = (int(pixels_per_one_jump*((self.value-self.min_value)/self.jump)+self.placement[0]), int(self.placement[1] + self.placement[3]/2))
        pygame.draw.circle(surface, self.slider_color, center, self.slider_radius)

        # Draw label
        surface.blit(self.label, (self.x + (self.width/2 - self.label.get_width()/2), self.y + self.slider_radius*2 + self.label.get_height()/2))

    def clicked(self, pos):
        if pos[0] + self.slider_radius > self.x + self.reference_position[0] and pos[0] - self.slider_radius < self.x + self.width + self.reference_position[0]:
            if pos[1] + self.slider_radius > self.y + self.reference_position[1]  and pos[1] - self.slider_radius  < self.y + self.height + self.reference_position[1] :
                # Set new value
                bar_x_pos = self.position[0] + self.reference_position[0]
                distance = pos[0] - bar_x_pos
                pixels_per_one_jump = (self.placement[2]/((self.max_value - self.min_value)/self.jump))
                round_to = abs(Decimal(str(self.jump)).as_tuple().exponent)
                new_value = round(round(distance/pixels_per_one_jump, round_to)*self.jump, round_to) + self.min_value

                # Make sure it's not out of scale
                if new_value > self.max_value:
                    self.value = self.max_value
                elif new_value < self.min_value:
                    self.value = self.min_value
                else:
                    self.value = new_value

                # If user speciefied small function execute it
                if self.click_function is not None:
                    self.click_function()

                return True

        return False



class Colors():
    @property
    def red(self):
        return (255, 0, 0)

    @property
    def black(self):
        return (0, 0, 0)

    @property
    def white(self):
        return (255, 255, 255)
    
    @property
    def green(self):
        return (0, 255, 0)
    
    @property
    def grey(self):
        return (128, 128, 128)

    @property
    def yellow(self):
        return (255, 255, 0)
    
    @property
    def orange(self):
        return (255, 165, 0)
    
    @property
    def blue(self):
        return (0, 0, 255)