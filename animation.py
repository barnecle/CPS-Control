import pygame
import time
pygame.init()
  
WHITE=(255,255,255)
BLUE = (0,0,255)

def blitRotate(surf, image, pos, originPos, angle): 
   ###################################
   #
   # I copied this function from stack overflow because I couldn't get the random nodes 
   # look right in pygame after I rotated them.
   # https://stackoverflow.com/questions/4183208/how-do-i-rotate-an-image-around-its-center-using-pygame answer from rabbit76
   #
   # This part of the code does not affect my algorithm implementation in any way. Just helps the visual part.
   #
   ###################################
    image_rect = image.get_rect(topleft = (pos[0] - originPos[0], pos[1]-originPos[1]))
    offset_center_to_pivot = pygame.math.Vector2(pos) - image_rect.center
    rotated_offset = offset_center_to_pivot.rotate(-angle)
    rotated_image_center = (pos[0] - rotated_offset.x, pos[1] - rotated_offset.y)
    rotated_image = pygame.transform.rotate(image, angle)
    rotated_image_rect = rotated_image.get_rect(center = rotated_image_center)
    surf.blit(rotated_image, rotated_image_rect)

# Initializing surface
surface = pygame.display.set_mode((600,600))
surface.fill(WHITE)

pygame.display.flip()

# Drawing Rectangle
running=True

car = pygame.Surface((10,15))
car.fill(BLUE)
i = 0 # iteration number

sol *= 6

while running:
   for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False
   
   surface.fill(WHITE)
   x = sol[i][0]
   y = sol[i][1]
   theta = sol[i][2]
   blitRotate(surface,car,(x,y),(5,7.5),theta*(180/math.pi))
   #surface.blit(car, (x,y))
   pygame.display.update()
   i+=1
   if i == len(sol):
        i=0
   time.sleep(.05)
