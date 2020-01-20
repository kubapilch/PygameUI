# Simple pygame UI library
This is small implementation of basic UI components to speed up building pygame projects.
![](https://github.com/kubapilch/PygameUI/blob/master/examples/gifs/showcase.gif)

## Requirements
* `Python 3.5+`
* Pygame `pip install pygame`

## Showscase
### Button
![](https://github.com/kubapilch/PygameUI/blob/master/examples/gifs/button.gif)

You can simply create a button like so 
`Button((X, Y, WIDTH, HEIGHT), COLOR, TEXT)`
and then to draw it `Button.draw(SURFACE)`. 

Obligatory initial arguments:
* `(X, Y, WIDTH, HEIGHT)` - also called as `placement` in code, a tuple representing button position and size. **NOTE: Given cordinates are relative to the surface that you are drawing it on. If you pass a surface and then blit this surface onto the main screen it will be drawn on cordinates on the first surface not the main one, ex. if you set Button position to (10, 0, W, H) draw it on a surface and then blit this surface onto a main screen at (100, 100), button absulute position will be (110, 100)**
* `COLOR` - Color of a button in RGB standard, you can also use my `Colors()` class instead of typing it by yourself
* `TEXT` - Text that will be shown on the button, you can always chenge it later `Button.text=""`

Optional arguments:
* `font=` - If you want to choose different font, default is `monospace`
* `font_size=` - Font size, when set to `None` it will be set dynamically depending on the size of a button
* `font_color=` - Font color, default is black
* `alpha=` - Alpha of the button, 0 means completly transparent and 255 is solid
* `click_function=` If you want to execute a simple function after the button is clicked, although it is not recommended for complex functions, I will show a better way of handling button clicks.

Methods:
* `draw(surface)` - Execute it when drawing a button, it will be drawn on passed surface
* `clicked(pos)` - Returns `True` or `False` if button is clicked for given position. Execute this function in your main event loop and pass `mouse_pos` to check if user has clicked the button. `pos` has to be a tuple like `(X, Y)`. It will also execute a function `click_function=` if you have passed it when creating a button. Check if it returns `True` and then do whatever you want to do after user has pressed a button. 

Properties:
* `size` - Size of a button `(WIDTH, HEIGHT)`
* `position` - Position of a button `(X, Y)`
* `text` - Text
* `x` - X coordinate
* `y` - Y coordinate

### Checkbox
![](https://github.com/kubapilch/PygameUI/blob/master/examples/gifs/checkbox.gif)


You can simply create a checkbox like so 
`Checkbox((X, Y, WIDTH, HEIGHT), BOX_COLOR, INDICATOR_COLOR, TEXT)`
and then to draw it `Checkbox.draw(SURFACE)`.

Obligator initial arguments:
* `(X, Y, WIDTH, HEIGHT)` - also called as `placement` in code, a tuple representing checkbox position and size. The size of a box is indicated by its height, width determine how wide the entire checkbox with a label will be. **NOTE: Given cordinates are relative to the surface that you are drawing it on. If you pass a surface and then blit this surface onto the main screen it will be drawn on cordinates on the first surface not the main one, ex. if you set Checkbox position to (10, 0, W, H) draw it on a surface and then blit this surface onto a main screen at (100, 100), checkbox absulute position will be (110, 100)**
* `BOX_COLOR` - Color of a checkbox box
* `INDICATOR_COLOR` - Color of a circle that indicates that a checkbox is checked
* `TEXT` - Text that will be shown on the checkbox, you can always chenge it later `Checkbox.text=""`

Optional arguments:
* `spacing=` - How many pixels to the right a label will be rednered, when set to `None` it will be dynamically set depending on its size
* `alpha=` - Transparency of the checkbox, 255 is completly drawn and 0 is invisible
* `font=` - If you want to choose different font, default is `monospace`
* `font_size=` - Font size, when set to `None` it will be dynamically set depending on checkbox size to fill the entire avaible space
* `font_color=` - Font color, default is black
* `click_function=` If you want to execute a simple function after a checkbox is checked/unchecked, although it is not recommended for complex functions, I will show a better way of handling checkbox clicks.

Methods:
* `draw(surface)` - Execute it when drawing a checkbox, it will be drawn on passed surface
* `clicked(pos)` - Returns `True` or `False` if checkbox is clicked for given position. Execute this function in your main event loop and pass `mouse_pos` to check if user has clicked the checkbox. `pos` has to be a tuple like `(X, Y)`. It will also execute a function `click_function=` if you have passed it when creating a checkbox.  Check if it returns `True` and then do whatever you want to do after user has checked/unchecked a checkbox.

Properties:
* `checked` - `True` if a checkbox is checked and `False` if not, default `False`
* `size` - Size of a checkbox `(WIDTH, HEIGHT)`
* `position` - Position of a checkbox `(X, Y)`
* `text` - Text
* `x` - X coordinate
* `y` - Y coordinate

### Slider
![](https://github.com/kubapilch/PygameUI/blob/master/examples/gifs/slider.gif)


You can simply create a slider like so 
`Slider((X, Y, WIDTH, HEIGHT), MIN_VALUE, MAX_VALUE, JUMP, DEFAULT_VALUE, SLIDER_COLOR, BAR_COLOR, TEXT)`
and then to draw it `Slider.draw(SURFACE)`.

Obligator initial arguments:
* `(X, Y, WIDTH, HEIGHT)` - also called as `placement` in code, a tuple representing slider position and size. **NOTE: Given cordinates are relative to the surface that you are drawing it on. If you pass a surface and then blit this surface onto the main screen it will be drawn on cordinates on the first surface not the main one, ex. if you set slider position to (10, 0, W, H) draw it on a surface and then blit this surface onto a main screen at (100, 100), slider absulute position will be (110, 100)**
* `MIN_VALUE` - Min value of a slider
* `MAX_VALUE` - Max value of a slider
* `JUMP` - Value that you want your slider to increment by
* `DEFAULT_VALUE` - Starting value of your slider
* `SLIDER_COLOR` - Color of a circle that indicates slider
* `BAR_COLOR` - Main bar color
* `TEXT` - Text that will be shown bellow a slider, you can always chenge it later `slider.text=""`. It will be rendered as `YOUR_TEXT: VALUE`

Optional arguments:
* `slider_radius=` - Radius of a circle that indicates slider, when set to `None` it will be dynamically set depending on the height of a bar
* `spacing=` - How many pixels to the bottom a label will be rednered, default is `10`
* `alpha=` - Transparency of the checkbox, 255 is completly drawn and 0 is invisible
* `font=` - If you want to choose different font, default is `monospace`
* `font_size=` - Font size, default is `10`
* `font_color=` - Font color, default is black
* `click_function=` If you want to execute a simple function after a slider is moved, although it is not recommended for complex functions, I will show a better way of handling slider clicks.

Methods:
* `draw(surface)` - Execute it when drawing a slider, it will be drawn on passed surface
* `clicked(pos)` - Returns `True` or `False` if slider is clicked for given position. Execute this function in your main event loop and pass `mouse_pos` to check if user has clicked the slider. `pos` has to be a tuple like `(X, Y)`. It will also execute a function `click_function=` that you have passed when creating a slider. Check if it returns `True` and then do whatever you want to do after user has moved a slider. 
* `reload_label_pos` - Reloades the position of a label

Properties:
* `value` - Value of a slider
* `size` - Size of a slider `(WIDTH, HEIGHT)`
* `position` - Position of a slider `(X, Y)`
* `text` - Text, it will be rendered as `YOUR_TEXT: VALUE`
* `x` - X coordinate
* `y` - Y coordinate

**If you wnat to get smoth slide effect instead of clicking a slider you have to keep track of pressed buttons and call `Slider.clicked()` function every tick. For my recommended approach look at `slider_example.py`**

### Label
To create a label `Label((X, Y, WIDTH, HEIGHT), TEXT)` and to draw it `Label.draw(SURFACE)`

Obligator initial arguments:
* `(X, Y, WIDTH, HEIGHT)` - also called as `placement` in code, a tuple representing label position and size. **NOTE: Given cordinates are relative to the surface that you are drawing it on. If you pass a surface and then blit this surface onto the main screen it will be drawn on cordinates on the first surface not the main one, ex. if you set label position to (10, 0, W, H) draw it on a surface and then blit this surface onto a main screen at (100, 100), label absulute position will be (110, 100)**
* `TEXT` - Text

Optional arguments:
* `font=` - If you want to choose different font, default is `monospace`
* `font_size=` - Font size, when set to `None` it will be set dynamically depending on the size of a label
* `font_color=` - Font color, default is black
* `alpha=` - Alpha of the button, 0 means completly transparent and 255 is solid

Methods:
* `draw(surface)` - Execute it when drawing a label, it will be drawn on passed surface
* `get_width` - Returns actual width of text
* `get_height` - Returns actual height of text
* `reload_label` - Reloads label, shouldn't be neccessary

Properties:
* `size` - Size of a label `(WIDTH, HEIGHT)`
* `position` - Position of a label `(X, Y)`
* `text` - Text
* `x` - X coordinate
* `y` - Y coordinate
* `max_font` - If `font_size` is set to `None` it will represent current font size inside specified rectengle **Read only!**
* `current_font_size` - It will return current font size, `font_size` if not `None` and if yes then `max_font`

**If font size is not specified and text is too long to fit inside label size it will be blank**


### Placeholder
![](https://github.com/kubapilch/PygameUI/blob/master/examples/gifs/placeholder.gif)


It is invisible surface on which you can draw UI elements instead of main screen. When user resize a window all you have to do is reposition placeholder and all buttons will stay in the same position.
To create: `Placeholder((X, Y, WIDTH, HEIGHT))`

Obligatory initial arguments:
* `(X, Y, WIDTH, HEIGHT)` - also called as `placement` in code, a tuple representing slider position and size.

Methods:
* `add_sub_object(obj)` - Adding an UI object to a placeholder
* `delete_sub_object(obj)` - Deleting an UI object from a placeholder
* `draw(surface)` - Drawing placeholders and all its sub objects on a surface

Properties:
* `size` - Size of a slider `(WIDTH, HEIGHT)`
* `position` - Position of a slider `(X, Y)`

### Background
![](https://github.com/kubapilch/PygameUI/blob/master/examples/gifs/background.gif)


Can act like a placeholder or be added as a separate object to existing placeholder. Basically its a placeholder with a color and transparency.
To create: `Background((X, Y, WIDTH, HEIGHT), COLOR, ALPHA)`

Obligatory initial arguments:
* `(X, Y, WIDTH, HEIGHT)` - also called as `placement` in code, a tuple representing slider position and size.
* `COLOR` - Color of a background in RGB standard, you can also use my `Colors()` class instead of typing it by yourself
* `ALPHA` - Transparency of the background color, 255 is completly drawn and 0 is invisible. **NOTE: It doens't apply to sub objects**

### Colors
You can use my `Color` class to use colors, it has up to 150 html colors and you can easily acces them as properties ex. `.white` or like a dictionary `Color()['white']`. All colors are saved in `colors.json` file and you can add your own in an easy way. 

## Future plans
* Better errors handling
    * ~~Not allowing setting wrong value/jump/min_value/max_value in slider~~
* Auto positiong sub objects for placeholders
    * Aligments left/right/top/bottom
    * Horizontal/Vertical alingment
* ~~Auto detecting absolute postion for clickable elements~~
* More label-rendering options for slider
* Easier and more intuitive functionality
    * ~~Cleaner objects initialization~~
    * ~~More default generated things like better default font size depending on the size of an object, slider radius etc.~~
* ~~More colors~~
* Rewriting `Slider` class to use `Label` class as a label
* More components
    * ~~Labels~~
    * Textboxes
    * Dropdown menus
* Adding `UIManager` that will take care of all inputs etc.