## **For the youtube video: https://www.youtube.com/watch?v=Xz0j2kR4uDo**
# Abstract Art Generator
Summary: A python program that generates abstract art with variety of styles, shapes, adjustable options and randomization, using pygame.

### Program Info
**Python version**: *3.7.6*,  **Packages used**: *pygame, pygame_gui, tkinter*<br /><br />
In "Abstract Art Generator", we have two layers to work on. Each of these layers have **4** different adjustable options.<br />
These are: *Style, Shape, Complexity and Size*<br />
Also for each artwork, there are **20** unique color palettes to choose from. These color palettes have **4** different colors.<br />
Before any shapes are drawn, one color from the color palette is chosen to be the background color, rest are left for shape colors.<br />

### Style Options
There are **7** style options, these are:<br />
* **Chaotic**: This is the most randomized option.<br />
* **Striped Horizontal**: With this layer style the shapes are forced to *roughly* line up on horizontal lines.<br />
* **Striped Vertical**: Same as the horizontal style but the shapes line up on vertical lines this time.<br />
* **Mosaic**: Whatever the shape is, they cover the screen with same amount of spacing between them.<br />
* **Cornered**: Shapes are forced to be drawn roughly on the corners.<br />
* **Centered**: Shapes are forced to be drawn roughlt on the center.<br />
* **Empty**: This option is there to make *one shape art* possible. Sometimes one shape is enough for an artwork.<br />

### Shape Options
There are **8** shapes to draw on your art, these are:<br />
**Lines, Circles, Sqaures, Hollow Polygons, Filled Polygons, Dots, Curves and Rings**<br />
The shapes are pretty self explanatory.<br />

### Slider Options
For the slider options, we have *Complexity* and *Size*.<br />
**Complexity**: This corresponds to how complex the layer will be. More shapes, more randomization. This option is more absolute.<br />
**Size**: This option changes the **maximum size** that the shapes can have, for that specific layer. This option is more flexible.<br />
* Note: While complexity works with all layer styles, size has an exception. For mosaic style, because the spacing is calculated by how many shapes has to be drawn, size option doesn't affect shapes with that style.<br />

### Extra
I have included an **examples** folder, and inside it there are **5** example abstract artworks. Just to show what can be done. And there is also an info.txt file in the folder that acts as a guide to create the same artworks yourself.<br />
Make sure to have all the packages required installed, and keep the files in the same folder.<br />
It might take a few seconds to fully run for the first time use. Use command prompt to run the .py file like this:
> python art_generator.py
