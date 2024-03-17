import pygame as pg
import math
import time  # for text entry

# TODO Move these to seperate files


class Element:
    """Generic ui element. Only has a surface"""

    def __init__(self, config):
        self.SURFACE = config["surface"]
        self.type = config["type"]
        self.tag = config.get("tag", None)


class Rectangle(Element):
    """A rectangle UI element

    draws a rectangle, can have transparency and its position
    can be a percentage of its parent surface.
    Every config value with default values:

    """

    def __init__(self, config):
        Element.__init__(self, config)

        ## Coordinate spaces caused problems with percentage anchours so depreicated for now
        ## Would end with pos as a small number
        ## Could be set up to take into account percentage but idrc
        # match config["coordSpace"]:
        # case "Center":
        # config["posX"] -= config["sizeX"] / 2
        # config["posY"] -= config["sizeY"] / 2
        # case "TopLeft":
        # #do nothing
        # pass

        self.anchorSpace = config.get("anchorSpace", "px")

        match self.anchorSpace:
            case "px":
                # do nothing
                pass
            case "%":
                # (str(self.WINDOW.get_height()))
                if self.SURFACE.get_width() == 0 or self.SURFACE.get_height() == 0:
                    # print("test")
                    # stop cryptic dive by zero
                    raise Exception(
                        "surface dimension equals 0 while in percent anchour space"
                        + str(self.SURFACE)
                        + str(config)
                    )
                config["posX"] = self.SURFACE.get_width() * (config["posX"] / 100)
                config["posY"] = self.SURFACE.get_height() * (config["posY"] / 100)

        self.scaleSpace = config.get("scaleSpace", "px")

        match self.scaleSpace:
            case "px":
                # do noting
                pass
            case "%":
                # interestingly the scaling is 1px off in this example
                # posX": 10,
                # "sizeX": 90,
                config["sizeX"] = self.SURFACE.get_width() * (config["sizeX"] / 100)
                config["sizeY"] = self.SURFACE.get_height() * (config["sizeY"] / 100)
                pass

        self.posX = config.get("posX", 0)
        self.posY = config.get("posY", 0)

        self.sizeX = config.get("sizeX", 50)
        self.sizeY = config.get("sizeY", 20)

        self.width = config.get("width", 0)  # Dont see a use but its cool
        self.borderRadius = config.get("borderRadius", 0)

        self.rect = pg.Rect(
            config["posX"], config["posY"], config["sizeX"], config["sizeY"]
        )
        self.colour = config.get("colour", pg.Color(56, 56, 56))

    def update(self):
        self.draw(self)

    def draw(self):
        pg.draw.rect(
            self.SURFACE, self.colour, self.rect, self.width, self.borderRadius
        )


class Button(Rectangle):
    """A button UI element

    Inherits from rectangle
    At its most basic, highlights when mouse is over and runs a function when clicked
    Can have text of varying styles, highlight thickness etc.

    """

    def __init__(self, config):
        Rectangle.__init__(self, config)
        self.fontSize = config.get("fontSize", 50)
        self.em = self.fontSize
        self.text = config.get("text", "")
        self.style = config.get("style", "default")
        self.font = config.get("font", "Hack")
        self.fontColour = config.get("fontColour", "White")
        self.isBold = config.get("isBold", True)
        self.isItalic = config.get("isItalic", False)
        self.textJusify = config.get("textJusify", "centre")

        # Redone here bc i want a different default
        self.borderRadius = config.get("borderRadius", int(self.em / 2))

        self.highlightThickness = config.get("highlightThickness", 0.2)

        self.clickEventHandler = config.get("clickEventHandler", None)

        self.doesHighlighting = config.get("doesHighlighting", True)

        self.prevMouseState = False

        self.fontObj = None

    def isMouseOver(self) -> bool:
        x, y = pg.mouse.get_pos()

        if self.rect.collidepoint(x, y):
            return True
        else:
            return False

    def highlight(self) -> None:
        # match self.style:
        # case "default":
        outlineColour = pg.Color(self.colour + pg.Color(100, 100, 100, 255))
        outlineColour.a = self.colour.a
        outlineSurf = pg.Surface(self.rect.size, pg.SRCALPHA, 32)
        pg.draw.rect(
            outlineSurf,
            outlineColour,
            outlineSurf.get_rect(),
            math.ceil(self.highlightThickness * self.em),
            self.borderRadius,
        )
        self.SURFACE.blit(outlineSurf, self.rect)

    def draw(self) -> pg.Surface:
        Rectangle.draw(self)  # poggers no re-written code

		# optomiseatio  here to only font if text has changed
        if self.fontObj is None:
            self.fontObj = pg.font.SysFont(self.font, self.fontSize, self.isBold, self.isItalic)

        img = self.fontObj.render(self.text, True, self.fontColour)
        # self.fontImg = img

        # this is a very long line of code :/
        # its for centering text btw
        match self.textJusify:
            case "centre":
                self.SURFACE.blit(
                    img,
                    (
                        (self.posX + ((self.sizeX - img.get_width()) / 2)),
                        (self.posY + ((self.sizeY - img.get_height()) / 2)),
                    ),
                )
            case "left":
                self.SURFACE.blit(
                    img,
                    (
                        (self.posX + self.em),
                        (self.posY + ((self.sizeY - img.get_height()) / 2)),
                    ),
                )
            case _:
                raise Exception(f"Invalid text.Justify in {self}")
        # print(img)
        return img

    def update(self) -> None:
        self.draw()
        self.em = self.fontSize
        if self.isMouseOver():
            if self.doesHighlighting:
                self.highlight()
            if pg.mouse.get_pressed()[0] == 1 and not self.prevMouseState:
                if self.clickEventHandler:
                    self.clickEventHandler()
            self.prevMouseState = pg.mouse.get_pressed()[0] == 1

        # self.draw_button_alpha(self.WINDOW, self.colour, self.rect)
        # pg.draw.rect(self.WINDOW, self.colour, self.rect, width=0)
        # if isMouseOver():
        # highlight
        # if isPressed():
        # fire event from Events package
        # pass


class bar(Rectangle):
    """A progress bar like element

    Displays a bar with text over the top,
    has min and max values, bar position is determined by current amount
    Displays text over the top with status

    Display text on top right of element?

    """

    def __init__(self, config):
        Rectangle.__init__(self, config)

        self.fontSize = config.get("fontSize", 50)
        self.em = self.fontSize
        self.title = config.get("text", "")
        self.contents = config.get("contents", "balls")
        self.style = config.get("style", "default")
        self.barColour = config.get("barColour", pg.color.Color(50, 255, 186))
        self.barOutlineColour = config.get(
            "barOutlineColour", pg.color.Color(255, 185, 252)
        )
        self.contentFontColour = config.get(
            "contentFontColour", pg.color.Color(255, 90, 248)
        )
        self.font = config.get("font", "Hack")
        self.padding = config.get("padding", 5)
        self.fontColour = config.get("fontColour", "White")
        self.isBold = config.get("isBold", True)
        self.isItalic = config.get("isItalic", False)

        # Redone here bc i want a different default
        self.borderRadius = config.get("borderRadius", int(self.em / 2))

        self.progress = config.get("progress", 0.75)

    def draw(self):
        Rectangle.draw(self)

        # draw title text
        font = None
        font = pg.font.SysFont(self.font, self.fontSize, self.isBold, self.isItalic)
        titleTimg = font.render(self.title, True, self.fontColour)

        a = titleTimg.get_size()
        titleRect = pg.Rect(
            self.posX + self.padding, self.posY + self.padding, a[0], a[1]
        )
        # print(titleRect)
        self.SURFACE.blit(titleTimg, titleRect)

        # draw bar insides.
        ## Draw Rect with dynamic scale

        barPosX = titleRect.x + self.padding
        barPosY = titleRect.y + titleRect.height + self.padding
        barSizeX = (self.sizeX - self.padding * 4) * self.progress
        barSizeY = self.sizeY - titleRect.height - self.padding * 4

        barRect = pg.Rect(barPosX, barPosY, barSizeX, barSizeY)

        # if rounding messes this up im gonna be angy
        borderRadius = int(self.sizeY / 2)

        pg.draw.rect(self.SURFACE, self.barColour, barRect, 0, borderRadius)

        # draw outline

        barSizeX = self.sizeX - self.padding * 4

        barOutlineRect = pg.Rect(barPosX, barPosY, barSizeX, barSizeY)
        pg.draw.rect(
            self.SURFACE,
            self.barOutlineColour,
            barOutlineRect,
            int(self.em / 15),
            borderRadius,
        )

        # draw bar contents

        # font = None

        font = pg.font.SysFont(
            self.font, int(self.fontSize / 1.2), self.isBold, self.isItalic
        )
        contentTimg = font.render(self.contents, True, self.contentFontColour)
        contentRect = (
            (barOutlineRect.x + ((barOutlineRect.width - contentTimg.get_width()) / 2)),
            (
                barOutlineRect.y
                + ((barOutlineRect.height - contentTimg.get_height()) / 2)
            ),
        )
        # print(contentRect)
        # contentRect = barRect
        self.SURFACE.blit(contentTimg, contentRect)

    def update(self):
        self.draw()


class TextEntryBox(Button):
    """# **Dont use this**

    Dont ise this this, doesnt dwork

    """

    def __init__(self, config) -> None:
        Button.__init__(self, config)

        self.selected = False
        self.fontImg = pg.Surface((0, 0))

        self.clickEventHandler = self.toggleSelected

    def update(self) -> None:
        Button.update(self)
        self.fontImg = Button.draw(self)
        print(type(self.fontImg))
        self.draw()

    def draw(self) -> None:
        rect = self.fontImg.get_rect()
        rect.topleft = (20, 20)
        cursor = pg.Rect(rect.topright, (3, rect.height))

        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_BACKSPACE:
                    if len(self.text) > 0:
                        self.text = self.text[:-1]
                else:
                    self.text += event.unicode

        rect.size = self.fontImg.get_size()
        cursor.topleft = rect.topright
        # cursor.topleft += self.posX

        if time.time() % 1 > 0.5:
            pg.draw.rect(self.SURFACE, "red", cursor)

    def toggleSelected(self):
        if self.selected:
            self.selected = False
        else:
            self.selected = True
