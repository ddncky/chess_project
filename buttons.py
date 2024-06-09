import pygame as p


# button class
class Buton:
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = p.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    def drawButtons(self, surface):
        action = False
        # get mouse position
        pos = p.mouse.get_pos()

        # check mouseover and clecked conditions
        if self.rect.collidepoint(pos):
            if p.mouse.get_pressed()[0] == 1 and not self.clicked:
                self.clicked = True
                action = True

        if p.mouse.get_pressed()[0] == 0:
            self.clicked = False

        # draw button on screen
        surface.blit(self.image, (self.rect.x, self.rect.y))

        return action
