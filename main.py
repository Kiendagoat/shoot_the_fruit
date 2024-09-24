from random import randint
import pygame
import asyncio

pygame.init()
clock = pygame.time.Clock()
window = pygame.display.set_mode((500, 500))
pygame.display.set_caption('SHOOT THE FRUIT!')

class GameSprite():
    def __init__(self, x, y, width, height, img):
        self.img = pygame.transform.scale(pygame.image.load(img), (width, height))
        self.rect = self.img.get_rect() # get the rectangle area by the img
        self.rect.x = x
        self.rect.y = y

    def draw(self):
        window.blit(self.img, (self.rect.x, self.rect.y))

class TextArea():
    def __init__(self, x, y, width, height, bg_color, text):
        self.rect = pygame.Rect(x, y, width, height) # get the rectangle area by the img
        self.background_color = bg_color
        self.text = text

    def draw(self):
        pygame.draw.rect(window, self.background_color, self.rect)
        txt_font = pygame.font.Font(None, 36)
        window.blit(txt_font.render(self.text, True, (0, 0, 0)), (self.rect.x + 10, self.rect.y + 10))

# Create fruit/bomb
apple = GameSprite(randint(10, 400), randint(10, 400), 100, 100, 'apple.png')
apple_timeout = 45

bomb = GameSprite(randint(10, 400), randint(10, 400), 100, 100,'Pixel Bomb.png')
bomb_timeout = 45

# Create point
point = 0
point_label = TextArea(300, 10, 125, 50, (74, 74, 74), 'Points: ' + str(point))

# Create timer
time_left = 20
start = 0
end = 0
timer_label = TextArea(10, 10, 125, 50, (74, 74, 74), 'Timer: ' + str(time_left))

# Create notificationulation message
notification_label = TextArea(apple.rect.x, apple.rect.y , 100, 50, (74, 74, 74), '')

# Timer algorithm
# start timestamp
# end timestamp
# passing time = end - start
# the time left = amount of time - passing time
# class Fruit(GameSprite):
#     pass

is_running = True


async def main():
    global time_left, end, start, point, bomb_timeout, apple_timeout, is_running
    while True:
        # Update timer
        if point > 3 or int(time_left) == 0:
            is_running = False
            break
            
        time_left -= end - start
        timer_label.text = 'Timer: ' + str(int(time_left))

        # Starting timestamp
        start = pygame.time.get_ticks() / 250

        # Randomize apple's position
        if apple_timeout <= 0:
            apple.rect.x = randint(0, 400)
            apple.rect.y = randint(0, 400)
            apple_timeout = 30
        else:
            if apple_timeout == 15:
                notification_label.text = ''
            apple_timeout -= 1

        # Randomize bomb's position
        if bomb_timeout <= 0:
            bomb.rect.x = randint(0, 400)
            bomb.rect.y = randint(0, 400)
            bomb_timeout = 30
        else:
            if bomb_timeout == 15:
                notification_label.text = ''
            bomb_timeout -= 1

        # Mouse clicked/Keypressed event
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                exit()

            if e.type == pygame.MOUSEBUTTONDOWN:
                # Check if the apple is clicked
                if apple.rect.collidepoint(pygame.mouse.get_pos()):
                    notification_label.text = 'Good Shot!'
                    notification_label.rect.x = apple.rect.x
                    notification_label.rect.y = apple.rect.y + 100

                    # Randomize apple's position
                    apple.rect.x = randint(0, 400)
                    apple.rect.y = randint(0, 400)

                    # Reset timer
                    apple_timeout = 30
                    # Increase points
                    point += 1
                    point_label.text =  'Points: ' + str(point)   

                # Check if the bomb is clicked
                if bomb.rect.collidepoint(pygame.mouse.get_pos()):
                    notification_label.text = 'Be careful!'
                    notification_label.rect.x = bomb.rect.x
                    notification_label.rect.y = bomb.rect.y + 100

                    bomb_timeout = 30

                    #Decrease points
                    point -= 1
                    point_label.text = 'Points:' + str(point)

                        

        # Draw
        window.fill((74, 74, 74))
        point_label.draw()
        timer_label.draw()
        notification_label.draw()
        apple.draw()
        bomb.draw()

        # End timestamp
        end = pygame.time.get_ticks() / 250

        clock.tick(60) # Set FPS
        pygame.display.update()
        await asyncio.sleep(0)

    if point == 3:
        result = 'WIN'
    else:
        result = 'LOL'
    txt_font = pygame.font.SysFont('Comic Sans MC', 100)
    window.fill((199, 253, 253))
    window.blit(txt_font.render(result, True, (0, 0, 0)), (175, 200))

    pygame.display.update()
    await asyncio.sleep(0)    

    # while True:
    #     for e in pygame.event.get():
    #             if e.type ==  pygame.QUIT:
    #                 pygame.quit()
    #                 exit()

    #     if point == 3:
    #         result = 'WIN'
    #     else:
    #         result = 'LOL'
    #     txt_font = pygame.font.SysFont('Comic Sans MC', 100)
    #     window.fill((199, 253, 253))
    #     window.blit(txt_font.render(result, True, (0, 0, 0)), (175, 200))

    #     pygame.display.update()

asyncio.run(main())