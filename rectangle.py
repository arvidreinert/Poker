from setup import *
import pygame

class Rectangle():
    def __init__(self, size, position, color, image=False,z_position=0):
        self.image_path = image
        self.rotation = 0
        self.z_position = z_position
        self.is_updating = True
        self.size = size
        self.position = position
        self.transparency = 255
        self.color = color
        
        if image == False:
            self.original_rect = pygame.Surface(size)
            self.original_rect.fill(self.color)
            self.original_rect.set_alpha(self.transparency)
            self.rect = self.original_rect.copy()
            self.rect_rect = self.rect.get_rect(center=position)
        else:
            self.original_image = pygame.image.load(image).convert_alpha()
            self.original_image = pygame.transform.scale(self.original_image, size)
            self.original_image.set_alpha(self.transparency)
            self.image = self.original_image.copy()
            self.image_rect = self.image.get_rect(center=position)
    
    def fill_rect_with_color(self,color):
        self.original_rect.fill(color)
        self.color = color
        self.rect = self.original_rect.copy()
        
    def update(self, surface):
        if self.is_updating:
            if self.image_path != False:
                self.image_rect = self.image.get_rect(center=self.position)
                surface.blit(self.image, self.image_rect)
            else:
                self.rect_rect = self.rect.get_rect(center=self.position)
                surface.blit(self.rect, self.rect_rect)
        
    def set_transparency(self, transparency):
        self.transparency = transparency
        if self.image_path != False:
            self.original_image.set_alpha(transparency)
            self.image.set_alpha(transparency)
        else:
            self.original_rect.set_alpha(transparency)
            self.rect.set_alpha(transparency)

    def set_image(self,image, is_loaded=False):
        if is_loaded == False:
            self.original_image = pygame.image.load(image).convert_alpha()
            self.original_image = pygame.transform.scale(self.original_image, self.size)
            self.original_image.set_alpha(self.transparency)
            self.image = self.original_image.copy()
        else:
            self.original_image = image
            self.image = self.original_image.copy()

    def set_position(self, xc, yc):
        self.position = (xc, yc)
        if self.image_path != False:
            self.image_rect.center = self.position
        else:
            self.rect_rect.center = self.position

    def change_position(self, xc, yc):
        self.position = (self.position[0] + xc, self.position[1] + yc)
        if self.image_path != False:
            self.image_rect.center = self.position
        else:
            self.rect_rect.center = self.position

    def load_costums(self,images):
        l_costums = {}
        for image in images:
            x = pygame.image.load(image).convert_alpha()
            x = pygame.transform.scale(x, self.size)
            x.set_alpha(self.transparency)
            l_costums[image] = x
        return l_costums


    def kill(self):
        self.is_updating = False

    def change_rotation(self, rot):
        self.rotation += rot
        if self.image_path != False:
            self.image = self.original_image
            self.image = pygame.transform.rotate(self.original_image, 0)
            self.image = pygame.transform.rotate(self.original_image, self.rotation)
            self.original_image = self.image.copy()
            self.image_rect = self.image.get_rect(center=self.position)
        else:
            self.rect = self.original_rect
            self.rect = pygame.transform.rotate(self.original_rect, 0)
            self.rect = pygame.transform.rotate(self.original_rect, self.rotation)
            self.rect_rect = self.rect.get_rect(center=self.position)

    def set_rotation(self,rot):
        self.rotation = rot
        if self.image_path != False:
            self.image = self.original_image
            self.image = pygame.transform.rotate(self.original_image, 0)
            self.image = pygame.transform.rotate(self.original_image, self.rotation)
            self.original_image = self.image.copy()
            self.image_rect = self.image.get_rect(center=self.position)
        else:
            self.rect = self.original_rect
            self.rect = pygame.transform.rotate(self.original_rect, 0)
            self.rect = pygame.transform.rotate(self.original_rect, self.rotation)
            self.rect_rect = self.rect.get_rect(center=self.position)
            
    def get_pos(self):
        return self.position

    def get_point_collide(self, point):
        if self.image_path != False:
            return self.image_rect.collidepoint(point)
        else:
            return self.rect_rect.collidepoint(point)
        
    def get_colliding_with(self, colrect):
        if self.image_path != False:
            return self.image_rect.colliderect(colrect.image_rect if colrect.image_path is not None else colrect.rect_rect)
        else:
            return self.rect_rect.colliderect(colrect.rect_rect if colrect.image_path is None else colrect.image_rect)
    
    def set_size(self,size):
        if self.image_path != False:
            self.size = size
            self.original_image = pygame.transform.scale(self.original_image, size)
            self.image = self.original_image.copy()
        else:
            self.size = size
            self.original_rect = pygame.Surface(size)
            self.original_rect.fill(self.color)
            self.original_rect.set_alpha(self.transparency)
            self.rect = self.original_rect.copy()
            self.rect_rect = self.rect.get_rect(center=self.position)
            
    def return_perfect_colission(self,other_rectangle):
        my_mask = pygame.mask.from_surface(self.image)
        other_mask = pygame.mask.from_surface(other_rectangle.image)
        return my_mask.overlap(other_mask,(other_rectangle.get_pos()[0]-self.get_pos()[0],other_rectangle.get_pos()[1]-self.get_pos()[1]))
        