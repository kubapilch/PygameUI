import pygame
from decimal import Decimal
import json

class UIObject():
    def __init__(self, placement:tuple):
        self.placement = placement # (x, y, width, height)
        self._x = placement[0]
        self._y = placement[1]
        self.width = placement[2]
        self.height = placement[3]

        self.__sub_objects = []

    @property
    def placement(self):
        return self._placement

    @placement.setter
    def placement(self, p):
        self._placement = p

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
        self._x = pos[0]
        self._y = pos[1]
        self.placement = (*pos, self.width, self.height)
    
    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, new_x):
        self._x = new_x
        self.placement = (new_x, *self.placement[1:])
    
    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, new_y):
        self._y = new_y
        self.placement = (self.placement[0], new_y, *self.size)

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

        self.__sub_objects = []


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


    # ---- Placeholders has no color and alpha=0 ----
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
    def __init__(self, placement:tuple, reference_position:tuple, color, alpha, text, font="monospace", font_size=None, font_color=(0, 0, 0), click_function=None):
        self.label = None
        super().__init__(placement)
        self.font = font
        self.font_size = font_size
        self.font_color = font_color
        self.color = color
        self.alpha = alpha
        self.reference_position = reference_position
        
        lab_placement = (round(placement[0] + (placement[2]/8)), round(placement[1] + (placement[3]/8)), round(placement[2]* (3/4)), round(placement[3] * (3/4)))
        self.label = Label(lab_placement, text, font_size=font_size, font_color=font_color, alpha=alpha)
        # Make sure that label is centered
        self.label.x = ((placement[2] - self.label.get_width())/2) + placement[0]
        self.label.y = ((placement[3] - self.label.get_height())/2) + placement[1]

        self.text = text
        self.click_function = click_function

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, t):
        # Render new label
        self._text = t
        
        if not self.label is None:
            self.label.text = t

    def draw(self, surface):
        # Draw button
        pygame.draw.rect(surface, (*self.color, self.alpha), self.placement)
        # Draw label
        self.label.draw(surface)

    def clicked(self, pos):
        if pos[0] > self.x + self.reference_position[0] and pos[0] < self.x + self.width + self.reference_position[0]:
            if pos[1] > self.y + self.reference_position[1]  and pos[1] < self.y + self.height + self.reference_position[1] :
                # If user speciefied small function execute it
                if self.click_function is not None:
                    self.click_function()

                return True

        return False
    
    # ---- OVERRING POSITION AND SIZE SETTER TO RELOAD LABEL POSTION AFTER ----
    @property
    def placement(self):
        return self._placement

    @placement.setter
    def placement(self, p):
        self._placement = p

        self.adjust_label()

    @property
    def size(self):
        return (self.placement[2], self.placement[3])
    
    @size.setter
    def size(self, s):
        self.width = s[0]
        self.height = s[1]
        self.placement = (self.x, self.y, *s)

        self.adjust_label()

    @property
    def position(self):
        return (self.placement[0], self.placement[1])
    
    @position.setter
    def position(self, pos):
        self._x = pos[0]
        self._y = pos[1]
        self.placement = (*pos, self.width, self.height)

        self.adjust_label()
    
    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, new_x):
        self._x = new_x
        self.placement = (new_x, *self.placement[1:])

        self.adjust_label()
    
    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, new_y):
        self._y = new_y
        self.placement = (self.placement[0], new_y, *self.size)

        self.adjust_label()
    
    def adjust_label(self):
        if not self.label is None:
            self.label.placement = (((self.placement[2] - self.label.get_width())/2) + self.placement[0], 
                                    ((self.placement[3] - self.label.get_height())/2) + self.placement[1], 
                                    round(self.placement[2]* (3/4)), round(self.placement[3] * (3/4)))


class Checkbox(UIObject):
    def __init__(self, placement:tuple, reference_position:tuple, checkbox_color, indicator_color, alpha, text, spacing=10, font="monospace", font_size=None, font_color=(0, 0, 0), click_function=None):
        self.label = None
        super().__init__(placement)
        self.font = font
        self.font_size = font_size
        self.font_color = font_color
        self.checkbox_color = checkbox_color
        self.indicator_color = indicator_color
        self.alpha = alpha
        self.reference_position = reference_position
        self.spacing = spacing

        lab_placement = (self.x + self.height + self.spacing, self.y, self.width - self.height - self.spacing, self.height - int(self.height/4))
        self.label = Label(lab_placement, text, font_size=font_size, font_color=font_color, alpha=alpha)
        # Make sure that label is centered
        self.label.x = self.x + self.height + self.spacing
        self.label.y = ((placement[3] - self.label.get_height())/2) + placement[1]

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

        if not self.label is None:
            self.label.text = t

    def draw(self, surface):
        # Draw button
        pygame.draw.rect(surface, (*self.checkbox_color, self.alpha), (self.x, self.y, self.height, self.height))

        # Draw checked indicator aka circle
        if self.checked:
            pygame.draw.circle(surface, self.indicator_color, (int(self.x + self.height/2), int(self.y + self.height/2)), int(self.height/4))

        # Draw label
        self.label.draw(surface)

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
    
    # ---- OVERRING POSITION AND SIZE SETTER TO RELOAD LABEL POSTION AFTER ----
    @property
    def placement(self):
        return self._placement

    @placement.setter
    def placement(self, p):
        self._placement = p

        self.adjust_label()

    @property
    def size(self):
        return (self.placement[2], self.placement[3])
    
    @size.setter
    def size(self, s):
        self.width = s[0]
        self.height = s[1]
        self.placement = (self.x, self.y, *s)

        self.adjust_label()

    @property
    def position(self):
        return (self.placement[0], self.placement[1])
    
    @position.setter
    def position(self, pos):
        self._x = pos[0]
        self._y = pos[1]
        self.placement = (*pos, self.width, self.height)

        self.adjust_label()
    
    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, new_x):
        self._x = new_x
        self.placement = (new_x, *self.placement[1:])

        self.adjust_label()
    
    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, new_y):
        self._y = new_y
        self.placement = (self.placement[0], new_y, *self.size)

        self.adjust_label()
    
    def adjust_label(self):
        if not self.label is None:
            self.label.placement = (self.x + self.height + self.spacing, 
                                    ((self.placement[3] - self.label.get_height())/2) + self.placement[1], 
                                    self.width - self.height - self.spacing, self.height - int(self.height/4))


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
        self.label_pos = (self.x + (self.width/2 - self.label.get_width()/2), self.y + self.slider_radius*2 + self.label.get_height()/2)

        if self.placement[2] < (max_value - min_value)/jump:
            raise ValueError("\033[91m Your total amout of jumps is greater than slider width, ex. you can't set slider width to 100, jump to 1 and max value to 200 because there should be at least 1 pixel per value. You can change jump to 2 to correct it \033[0m")

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, v):
        # Make sure it's not out of scale
        if v > self.max_value:
            v = self.max_value
        elif v < self.min_value:
            v = self.min_value
        
        # If the value is a whole number show it like '7' instead of '7.0'
        if float(v).is_integer():
            self._value = int(v)
        else:
            self._value = v

        # Render new label
        self.label = pygame.font.SysFont(self.font, self.font_size).render(f'{self.text}: {self.value}', 1, (*self.font_color, self.alpha))

    @property
    def position(self):
        return (self.placement[0], self.placement[1])

    @position.setter
    def position(self, pos):
        self._x = pos[0]
        self._y = pos[1]
        self.placement = (*pos, self.width, self.height)

        if self.label is not None:
            self.label_pos = (self.x + (self.width/2 - self.label.get_width()/2), self.y + self.slider_radius*2 + self.label.get_height()/2)

    def reload_label_pos(self):
        if self.label is not None:
            self.label_pos = (self.x + (self.width/2 - self.label.get_width()/2), self.y + self.slider_radius*2 + self.label.get_height()/2)

    def draw(self, surface):
        # Draw a bar
        pygame.draw.rect(surface, (*self.bar_color, self.alpha), self.placement)

        #Draw slider
        pixels_per_one_jump = (self.placement[2]/((self.max_value - self.min_value)/self.jump))
        center = (int(pixels_per_one_jump*((self.value-self.min_value)/self.jump)+self.placement[0]), int(self.placement[1] + self.placement[3]/2))
        pygame.draw.circle(surface, self.slider_color, center, self.slider_radius)

        # Draw label
        surface.blit(self.label, self.label_pos)

    def clicked(self, pos):
        if pos[0] + self.slider_radius > self.x + self.reference_position[0] and pos[0] - self.slider_radius < self.x + self.width + self.reference_position[0]:
            if pos[1] + self.slider_radius > self.y + self.reference_position[1]  and pos[1] - self.slider_radius  < self.y + self.height + self.reference_position[1] :
                # Set new value
                bar_x_pos = self.position[0] + self.reference_position[0]
                distance = pos[0] - bar_x_pos
                pixels_per_one_jump = (self.placement[2]/((self.max_value - self.min_value)/self.jump))
                round_to = abs(Decimal(str(self.jump)).as_tuple().exponent)
                new_value = round(round(distance/pixels_per_one_jump, round_to)*self.jump, round_to) + self.min_value

                self.value = new_value

                # If user speciefied small function execute it
                if self.click_function is not None:
                    self.click_function()

                return True

        return False

class Label(UIObject):
    def __init__(self, placement, text, font="monospace", font_size=None, font_color=(0, 0, 0), alpha=1):
        super().__init__(placement)
        self.font = font
        self.font_size = font_size
        self.max_font = None
        self.font_color = font_color
        self.alpha = alpha
        self.text = text
    
    @property
    def text(self):
        return self._text
    
    @text.setter
    def text(self, t):
        self._text = t

        self.reload_label()

    @property
    def font_size(self):
        return self._font_size

    @font_size.setter
    def font_size(self, f):
        self._font_size = f

        self.reload_label()
    
    def get_width(self):
        """
        Gets actual width of text
        """
        if not self.label is None:
            return self.label.get_width()
        
        return 0
    
    def get_height(self):
        """
        Gets actual height of text
        """
        if not self.label is None:
            return self.label.get_height()
        
        return 0

    def reload_label(self):
        # Prevents from error when initializing the oject, reload method is called after font size is set but text is still not set
        try:
            # If font is not specified find the biggest possible font and render label
            if self.font_size is None:
                self.max_font = self._find_biggest_possible_font()

                if self.max_font is None:
                    print("\033[91m Can't render label, too small space \033[0m")
                    self.label = None
                    return

                self.label = pygame.font.SysFont(self.font, self.max_font).render(f'{self.text}', 1, (*self.font_color, self.alpha))
                return
            # Font specified, render normal label
            self.label = pygame.font.SysFont(self.font, self.font_size).render(f'{self.text}', 1, (*self.font_color, self.alpha))
        except AttributeError as err:
            self.label = None

    def draw(self, surface):
        # Draw label
        if self.label is not None:
            surface.blit(self.label, self.position)

    def _find_biggest_possible_font(self):
        max_width = self.placement[2]
        max_height = self.placement[3]
        
        current_max_font = min(max_height, max_width)
        testing_label = pygame.font.SysFont(self.font, current_max_font).render(f'{self.text}', 1, (*self.font_color, self.alpha))

        while current_max_font > 1:

            if testing_label.get_width() <= max_width and testing_label.get_height() <= max_height:
                return current_max_font

            current_max_font -= 1
            testing_label = pygame.font.SysFont(self.font, current_max_font).render(f'{self.text}', 1, (*self.font_color, self.alpha))

        return None

    # ---- OVERRIDE SIZE SETTER TO RELOAD LABEL AFTER CHAINING ITS SIZE ----
    @property
    def placement(self):
        return self._placement

    @placement.setter
    def placement(self, p):
        self._placement = p

        self.reload_label()

    @property
    def size(self):
        return (self.placement[2], self.placement[3])
    
    @size.setter
    def size(self, s):
        self.width = s[0]
        self.height = s[1]
        self.placement = (self.x, self.y, *s)

        self.reload_label()

class Colors():
    def __init__(self):
        try:
            # Load colors from json file
            with open('colors.json', 'r') as f:
                colors = json.load(f)
                # Set them as properties of an object
                for key, item in colors.items():
                    setattr(self, key, tuple(item[:-1]))
        except FileNotFoundError as err:
            print("\033[91m Couldn't find 'colors.json' file inside script directory \033[0m")

    # Allows colors to be accessed like a dictionary
    def __getitem__(self, key):
        try:
            return self.__dict__[key]
        except KeyError as err:
            print(f'\033[91m There is no color named: {key} \033[0m')
            return None
