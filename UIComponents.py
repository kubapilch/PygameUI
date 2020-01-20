import pygame
from decimal import Decimal
import json
from typing import Optional, Union, Callable, Type

class UIObject():
    def __init__(self, placement:tuple):
        self.placement = placement # (x, y, width, height)

        # self.__sub_objects = []

        self._parent = None

    @property
    def placement(self) -> tuple:
        return self._placement

    @placement.setter
    def placement(self, p:tuple):
        self._placement = p

    @property
    def size(self) -> tuple:
        return (self.placement[2], self.placement[3])
    
    @size.setter
    def size(self, s:tuple):
        self.placement = (self.x, self.y, *s)
    
    @property
    def width(self) -> int:
        return self.placement[2]
    
    @property
    def height(self) -> int:
        return self.placement[3]

    @property
    def position(self) -> tuple:
        return self.placement[:2]
    
    @position.setter
    def position(self, pos:tuple):
        self.placement = (*pos, self.width, self.height)
    
    @property
    def x(self) -> int:
        return self.placement[0]

    @x.setter
    def x(self, new_x:int):
        self.placement = (new_x, *self.placement[1:])
    
    @property
    def y(self) -> int:
        return self.placement[1]

    @y.setter
    def y(self, new_y:int):
        self.placement = (self.x, new_y, *self.size)

    def draw(self, surface):
        """
        Draw all sub objects, their sub objects and main object to a given surface
        """
        pass

    def get_absolute_pos(self) -> tuple:
        """
        Return the absolute postion of an boject relative to the top left corner of the screen
        """
        if self._parent is None:
            return self.position
        
        parent_x, parent_y = self._parent.get_absolute_pos()

        return (self.x + parent_x, self.y + parent_y)

class Surfaces(UIObject):
    def __init__(self, placement:tuple, color:tuple, alpha:int):
        super().__init__(placement)
        self._color = color
        self._alpha = alpha

        self._createSurface()

    @property
    def color(self) -> tuple:
        return self._color
    
    @color.setter
    def color(self, c:tuple):
        self._color = c
        self.surface.fill((*self._color, self._alpha))

    @property
    def alpha(self) -> int:
        return self._alpha

    @alpha.setter
    def alpha(self, a:int):
        self._alpha = a
        self.surface.fill((*self._color, self._alpha))

    def _createSurface(self):
        """
        Creates main object surface and sets its color and alpha 
        """
        # Create main surface
        self.surface = pygame.Surface(self.size, pygame.SRCALPHA)

        # Set color and alpha
        self.surface.fill((*self._color, self._alpha))

    def add_sub_object(self, obj:Type[UIObject]):
        """
        Adds given object as a subobject 
        """
        self._sub_objects.append(obj)

        obj._parent = self

    def delete_sub_object(self, obj:Type[UIObject]):
        """
        Delets given object from subobjects
        """
        self._sub_objects.remove(obj)

        obj._parent = None  

class Placeholder(Surfaces):
    def __init__(self, placement:tuple):
        super().__init__(placement, (0, 0, 0), 0)

        self._sub_objects = []


    def draw(self, surface):
        """
        Draws itself and its subobjects on a given surface
        """
        # Clear before drawing
        self.surface.fill((0, 0, 0, 0))

        # Check if has sub objects and if so then draw them
        if self._sub_objects:

            for obj in self._sub_objects:
                # Draw subobjects and their subobjects to their surface
                obj.draw(self.surface)

        # Blit main surface to given surface
        surface.blit(self.surface, self.position)

    # ---- Placeholders has no color and alpha=0 ----
    @property
    def color(self) -> None:
        return None

    @color.setter
    def color(self, c:tuple):
        pass

    @property
    def alpha(self) -> 0:
        return 0

    @alpha.setter
    def alpha(self, a:int):
        pass

class Background(Surfaces):
    def __init__(self, placement:tuple, color:tuple, alpha:int):
        super().__init__(placement, color, alpha)
        
        self._sub_objects = []

    def draw(self, surface):
        """
        Draws itself and its subobjects on a given surface
        """
        # Clean before drawing
        self.surface.fill((*self.color, self.alpha))
        
        # Check if has sub objects and if so then draw them
        if self._sub_objects:

            for obj in self._sub_objects:
                # Draw subobjects and their subobjects to their surface
                obj.draw(self.surface)

        # Blit main surface to given surface
        surface.blit(self.surface, self.position)


class Button(UIObject):
    def __init__(self, placement:tuple, color:tuple, text:str, alpha:int=255, font_size:Optional[int]=None, font_color:tuple=(0, 0, 0), font:str="monospace", click_function:Optional[Callable]=None):
        self.label = None
        super().__init__(placement)
        self.font = font
        self.font_size = font_size
        self.font_color = font_color
        self.color = color
        self.alpha = alpha

        lab_placement = (round(placement[0] + (placement[2]/8)), round(placement[1] + (placement[3]/8)), round(placement[2]* (3/4)), round(placement[3] * (3/4)))
        self.label = Label(lab_placement, text, font_size=font_size, font_color=font_color, alpha=alpha, font=font)
        # Make sure that label is centered
        self.label.x = ((placement[2] - self.label.get_width())/2) + placement[0]
        self.label.y = ((placement[3] - self.label.get_height())/2) + placement[1]

        self.text = text
        self.click_function = click_function

    @property
    def text(self) -> str:
        return self._text

    @text.setter
    def text(self, t:str):
        # Render new label
        self._text = t
        
        if not self.label is None:
            self.label.text = t

    @property
    def alpha(self) -> int:
        return self._alpha

    @alpha.setter
    def alpha(self, a:int):
        self._alpha = a
        if self.label is not None:
            self.label.alpha = a

    def draw(self, surface):
        """
        Draws itself on a given surface
        """
        # Draw button
        pygame.draw.rect(surface, (*self.color, self.alpha), self.placement)
        # Draw label
        self.label.draw(surface)

    def clicked(self, pos:tuple) -> bool:
        """
        Checks if button is clicked for given mouse position and runs specified 'click_function'
        """
        if pos[0] > self.get_absolute_pos()[0] and pos[0] < self.width + self.get_absolute_pos()[0]:
            if pos[1] > self.get_absolute_pos()[1]  and pos[1] < self.height + self.get_absolute_pos()[1] :
                # If user speciefied small function execute it
                if self.click_function is not None:
                    self.click_function()

                return True

        return False
    
    # ---- OVERRING POSITION AND SIZE SETTER TO RELOAD LABEL POSTION AFTER ----
    @property
    def placement(self) -> tuple:
        return self._placement

    @placement.setter
    def placement(self, p:tuple):
        self._placement = p

        self._adjust_label()
    
    def _adjust_label(self):
        """
        Adjust label position after button size or placement has been changed
        """
        if self.label is not None:
            # Change label size to calculate new max font etc.
            self.label.size = (round(self.width* (3/4)), round(self.height * (3/4)))
            self.label.reload_label()

            # Update label position
            self.label.position = (((self.width - self.label.get_width())/2) + self.x, ((self.height - self.label.get_height())/2) + self.y)

class Checkbox(UIObject):
    def __init__(self, placement:tuple, checkbox_color:tuple, indicator_color:tuple, text:str, spacing:Optional[int]=None, alpha:int=255, 
                font:str="monospace", font_size:Optional[int]=None, font_color:tuple=(0, 0, 0), click_function:Optional[Callable]=None):
        self.label = None
        super().__init__(placement)
        
        self.font = font
        self.font_size = font_size
        self.font_color = font_color
        self.checkbox_color = checkbox_color
        self.indicator_color = indicator_color
        self.alpha = alpha
        self.spacing = spacing

        # Just set a label and adjust its position later
        lab_placement = (self.x + self.height, self.y, self.width - self.height - round(self.height/4), self.height - round(self.height/4))
        self.label = Label(lab_placement, text, font_size=font_size, font_color=font_color, alpha=alpha, font=font)
        
        # Adjust labbel position
        if self.spacing is not None:
            self.label.x = self.x + self.height + self.spacing
        else:
            self.label.x = self.x + self.height + self._calculate_spacing()
        
        self.label.y = ((placement[3] - self.label.get_height())/2) + placement[1]

        self.text = text
        self.click_function = click_function
        self.checked = False
    
    def _calculate_spacing(self) -> int:
        """
        Calculates spacing between label nad a box for set font size
        """
        return round(self.height/4) if round(self.height/4) > 1 else 1

    @property
    def text(self) -> str:
        return self._text

    @text.setter
    def text(self, t:str):
        # Render new label
        self._text = t

        if not self.label is None:
            self.label.text = t

    def draw(self, surface):
        """
        Draws itself on a given surface
        """
        # Draw box
        pygame.draw.rect(surface, (*self.checkbox_color, self.alpha), (self.x, self.y, self.height, self.height))

        # Draw checked indicator aka circle
        if self.checked:
            pygame.draw.circle(surface, self.indicator_color, (int(self.x + self.height/2), int(self.y + self.height/2)), int(self.height/4))

        # Draw label
        self.label.draw(surface)

    def clicked(self, pos:tuple) -> bool:
        """
        Checks if checkbox is clicked for given mouse position and runs specified 'click_function'
        """
        if pos[0] > self.get_absolute_pos()[0] and pos[0] < self.height + self.get_absolute_pos()[0]:
            if pos[1] > self.get_absolute_pos()[1]  and pos[1] < self.height + self.get_absolute_pos()[1] :
                # Unmark or mark 
                self.checked = not self.checked

                # If user speciefied small function execute it
                if self.click_function is not None:
                    self.click_function()

                return True

        return False
    
    # ---- OVERRING POSITION AND SIZE SETTER TO RELOAD LABEL POSTION AFTER ----
    @property
    def placement(self) -> tuple:
        return self._placement

    @placement.setter
    def placement(self, p:tuple):
        self._placement = p

        self._adjust_label()
    
    def _adjust_label(self):
        """
        Adjust label position after checkbox size or placement has been changed
        """
        if not self.label is None:
            if self.spacing is not None:
                # Change label size to calculate new max font etc.
                self.label.size = (self.width - self.height - self.spacing, self.height - int(self.height/4))
                self.label.reload_label()

                # Update label position
                self.label.position = (self.x + self.height + self.spacing, ((self.placement[3] - self.label.get_height())/2) + self.placement[1])
            
            else:
                # Change label size to calculate new max font etc.
                self.label.size = (self.width - self.height - self._calculate_spacing(), self.height - int(self.height/4))
                self.label.reload_label()

                # Update label position
                self.label.position = (self.x + self.height + self._calculate_spacing(), ((self.placement[3] - self.label.get_height())/2) + self.placement[1])

class Slider(UIObject):
    def __init__(self, placement:tuple, min_value:Union[int, float], max_value:Union[int, float], jump:Union[int, float], default_value:Union[int, float], 
                slider_color:tuple, bar_color:tuple, text:str, slider_radius:Optional[int]=None, spacing:int=10, alpha:int=255, 
                font_size:int=10, font_color:tuple=(0, 0, 0), font:str="monospace", click_function:Optional[Callable]=None):
        self.label = None
        super().__init__(placement)
        
        self.font = font
        self.font_size = font_size
        self.font_color = font_color
        
        self.slider_color = slider_color
        self.bar_color = bar_color
        self.alpha = alpha
        self.text = text
        self.spacing = spacing
        self.click_function = click_function
        self.min_value = min_value
        self.max_value = max_value
        self.jump = jump
        self.slider_radius = slider_radius
        self.value = default_value
        
        if self.slider_radius is not None:
            self.label_pos = (self.x + (self.width/2 - self.label.get_width()/2), self.y + self.slider_radius*2 + self.label.get_height()/2)
        else:
            self.label_pos = (self.x + (self.width/2 - self.label.get_width()/2), self.y + self.height*2 + self.label.get_height()/2)
        
        if self.placement[2] < (max_value - min_value)/jump:
            raise ValueError("\033[91m Your total amout of jumps is greater than slider width, ex. you can't set slider width to 100, jump to 1 and max value to 200 because there should be at least 1 pixel per value. You can change jump to 2 to correct it \033[0m")

    @property
    def value(self) -> Union[int, float]:
        return self._value

    @value.setter
    def value(self, v:Union[int, float]):
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

    def reload_label_pos(self):
        """
        Reloads label position
        """
        if self.label is not None:
            if self.slider_radius is not None:
                self.label_pos = (self.x + (self.width/2 - self.label.get_width()/2), self.y + self.slider_radius*2 + self.label.get_height()/2)
            else:
                self.label_pos = (self.x + (self.width/2 - self.label.get_width()/2), self.y + self.height*2 + self.label.get_height()/2)

    def draw(self, surface):
        """
        Draws itself on a given surface
        """
        # Draw a bar
        pygame.draw.rect(surface, (*self.bar_color, self.alpha), self.placement)

        #Draw slider
        pixels_per_one_jump = (self.placement[2]/((self.max_value - self.min_value)/self.jump))
        center = (int(pixels_per_one_jump*((self.value-self.min_value)/self.jump)+self.placement[0]), int(self.placement[1] + self.placement[3]/2))
        if self.slider_radius is not None:
            pygame.draw.circle(surface, self.slider_color, center, self.slider_radius)
        else:
            pygame.draw.circle(surface, self.slider_color, center, self.height)
        
        # Draw label
        surface.blit(self.label, self.label_pos)

    def clicked(self, pos:tuple) -> bool:
        """
        Checks if slider is clicked for given mouse position, updates its value and runs specified 'click_function'
        """

        if self.slider_radius is not None:
            radius = self.slider_radius
        else:
            radius = self.height

        if pos[0] + radius > self.get_absolute_pos()[0] and pos[0] - radius < self.width + self.get_absolute_pos()[0]:
            if pos[1] + radius > self.get_absolute_pos()[1]  and pos[1] - radius  < self.height + self.get_absolute_pos()[1] :
                # Set new value
                bar_x_pos = self.get_absolute_pos()[0]
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
    
    # ---- OVERRING POSITION AND SIZE SETTER TO RELOAD LABEL POSTION AFTER ----
    @property
    def placement(self) -> tuple:
        return self._placement

    @placement.setter
    def placement(self, p:tuple):
        self._placement = p

        self.reload_label_pos()

    @property
    def size(self) -> tuple:
        return self.placement[2:]
    
    @size.setter
    def size(self, s:tuple):
        self.placement = (self.x, self.y, *s)

        self.reload_label_pos()

    @property
    def position(self) -> tuple:
        return self.placement[:2]
    
    @position.setter
    def position(self, pos:tuple):
        self.placement = (*pos, self.width, self.height)

        self.reload_label_pos()
    
    @property
    def x(self) -> int:
        return self.placement[0]

    @x.setter
    def x(self, new_x:int):
        self.placement = (new_x, *self.placement[1:])

        self.reload_label_pos()
    
    @property
    def y(self) -> int:
        return self.placement[1]

    @y.setter
    def y(self, new_y:int):
        self.placement = (self.x, new_y, *self.size)

        self.reload_label_pos()

class Label(UIObject):
    def __init__(self, placement:tuple, text:str, font_size:Optional[int]=None, font_color:tuple=(0, 0, 0), font:str="monospace", alpha:int=255):
        super().__init__(placement)
        self.font = font
        self.font_size = font_size
        self.max_font = None
        self.font_color = font_color
        self.alpha = alpha
        self.text = text
    
    @property
    def text(self) -> str:
        return self._text
    
    @text.setter
    def text(self, t:str):
        self._text = t

        self.reload_label()

    @property
    def font_size(self) -> int:
        return self._font_size

    @font_size.setter
    def font_size(self, f:int):
        self._font_size = f

        self.reload_label()
    
    def get_width(self) -> int:
        """
        Gets actual width of text
        """
        if not self.label is None:
            return self.label.get_width()
        
        return 0
    
    def get_height(self) -> int:
        """
        Gets actual height of text
        """
        if not self.label is None:
            return self.label.get_height()
        
        return 0

    def reload_label(self):
        """
        Renders pygame label
        """
        # Prevents from error when initializing the oject, reload method is called after font size is set but text is still not set
        try:
            # If font is not specified find the biggest possible font and render label
            if self.font_size is None:
                self.max_font = self._find_biggest_possible_font()

                if self.max_font is None:
                    print("\033[91m Can't render label, too small space \033[0m")
                    self.label = None
                    return

                self.label = pygame.font.SysFont(self.font, self.max_font).render(f'{self.text}', 1, (*self.font_color, self.alpha/255))
                return
            # Font specified, render normal label
            self.label = pygame.font.SysFont(self.font, self.font_size).render(f'{self.text}', 1, (*self.font_color, self.alpha/255))
        except AttributeError as err:
            self.label = None

    def draw(self, surface):
        """
        Draws itself on a given surface
        """
        # Draw label
        if self.label is not None:
            surface.blit(self.label, self.position)

    def _find_biggest_possible_font(self) -> Optional[int]:
        """
        Finds the biggest possible font for set text, height and width
        """
        max_width = self.placement[2]
        max_height = self.placement[3]
        
        current_max_font = min(max_height, max_width)
        testing_label = pygame.font.SysFont(self.font, current_max_font).render(f'{self.text}', 1, (*self.font_color, 1))

        while current_max_font > 1:

            if testing_label.get_width() <= max_width and testing_label.get_height() <= max_height:
                return current_max_font

            current_max_font -= 1
            testing_label = pygame.font.SysFont(self.font, current_max_font).render(f'{self.text}', 1, (*self.font_color, 1))

        return None

    @property
    def current_font_size(self) -> int:
        return self.max_font if self.font_size is None else self.font_size

    # ---- OVERRIDE SIZE SETTER TO RELOAD LABEL AFTER CHAINING ITS SIZE ----
    @property
    def placement(self) -> tuple:
        return self._placement

    @placement.setter
    def placement(self, p:tuple):
        self._placement = p

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
