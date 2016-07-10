__author__ = 'Sebastian'

import pygame
import tmx

class Presentation(object):
    def main(self, screen):
        pygame.display.set_caption("Welcome")
        image = pygame.image.load("{0}portadaprueba2.gif".format("imgs/"))
        self.background = pygame.mixer.Sound("{0}presentation.wav".format("sound/"))

        while 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    self.background.stop()
                    return True
            self.background.play()
            screen.blit(image, (0,0))
            pygame.display.flip()

class Game1(object):



    def main(self, screen):
        clock = pygame.time.Clock()

        self.blocked = pygame.mixer.Sound("{0}blocked.wav".format("sound/"))
        self.jump = pygame.mixer.Sound("{0}jump.wav".format("sound/"))
        self.respawn = pygame.mixer.Sound("{0}respawn.wav".format("sound/"))
        self.respawn_2 = pygame.mixer.Sound("{0}respawn_2.wav".format("sound/"))
        self.clear = pygame.mixer.Sound("{0}clear.wav".format("sound/"))

        self.tilemap = tmx.load("likeapiepy.tmx", screen.get_size())

        self.sprites = tmx.SpriteLayer()
        start_cell = self.tilemap.layers['triggers'].find('player')[0]
        self.player = Player((start_cell.px, start_cell.py), self.sprites)
        self.tilemap.layers.append(self.sprites)

        pygame.display.set_caption("Like a PiePy")

        while 1:
            clock.tick(30)
            dt = clock.tick(30)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return False

            if self.player.rect.x >= self.tilemap.px_width:
                self.clear.play()
                return True


            self.tilemap.update(dt / 1000., self)
            self.tilemap.draw(screen)
            pygame.display.flip()

class Game2(object):

    def main(self, screen):
        clock = pygame.time.Clock()

        self.blocked = pygame.mixer.Sound("{0}blocked.wav".format("sound/"))
        self.jump = pygame.mixer.Sound("{0}jump.wav".format("sound/"))
        self.respawn = pygame.mixer.Sound("{0}respawn.wav".format("sound/"))
        self.respawn_2 = pygame.mixer.Sound("{0}respawn_2.wav".format("sound/"))
        self.clear = pygame.mixer.Sound("{0}clear.wav".format("sound/"))

        self.tilemap = tmx.load("likeapiepy2.tmx", screen.get_size())

        self.sprites = tmx.SpriteLayer()
        start_cell = self.tilemap.layers['triggers'].find('player')[0]
        self.player = Player((start_cell.px, start_cell.py), self.sprites)
        self.tilemap.layers.append(self.sprites)

        pygame.display.set_caption("Like a PiePy")

        while 1:
            clock.tick(30)
            dt = clock.tick(30)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return False

            if self.player.end:
                self.clear.play()
                return True

            self.tilemap.update(dt / 1000., self)
            self.tilemap.draw(screen)
            pygame.display.flip()

class Game3(object):
    def main(self, screen):
        pygame.display.set_caption("Thank You")
        image = pygame.image.load("{0}end.jpg".format("imgs/"))
        self.background = pygame.mixer.Sound("{0}last.wav".format("sound/"))
        while 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    return
            self.background.play()
            screen.blit(image, (0,0))
            pygame.display.flip()


class Player(pygame.sprite.Sprite):
    def __init__(self, location, *groups):
        super(Player, self).__init__(*groups)
        self.image = pygame.image.load('{0}play-01.png'.format("imgs/"))
        self.image = pygame.transform.smoothscale(self.image, (40,40))
        self.right_image = self.image
        self.left_image = pygame.image.load('{0}backplay-01.png'.format("imgs/"))
        self.left_image = pygame.transform.smoothscale(self.left_image, (40,40))
        self.jump_image = pygame.image.load('{0}jump.png'.format("imgs/"))
        self.jump_image = pygame.transform.smoothscale(self.jump_image, (40,40))
        self.backjump_image = pygame.image.load('{0}backjump.png'.format("imgs/"))
        self.backjump_image = pygame.transform.smoothscale(self.backjump_image, (40,40))
        self.rect = pygame.rect.Rect(location, self.image.get_size())
        self.resting = False
        self.dy = 0
        self.direction = 1
        self.end = False
        self.respawn = False

    def update(self, dt, game):
        last = self.rect.copy()

        key = pygame.key.get_pressed()
        if key[pygame.K_RIGHT]:
            self.rect.x += 300 * dt
            self.direction = 1
        if key[pygame.K_LEFT]:
            self.rect.x -= 300 * dt
            self.direction = -1

        if self.resting and self.direction == 1:
            self.image = self.right_image
        if self.resting and self.direction == -1:
            self.image = self.left_image

        if self.direction == 1 and self.resting == False:
            self.image = self.jump_image
        if self.direction == -1 and self.resting == False:
            self.image = self.backjump_image

        if self.resting and key[pygame.K_SPACE]:
            self.dy = -500
            game.jump.play()
        self.dy = min(400, self.dy + 40)
        self.rect.y += self.dy * dt

        new = self.rect
        self.resting = False
        for cell in game.tilemap.layers['triggers'].collide(new, 'blocker'):
            blockers = cell["blocker"]
            if last.right <= cell.left and new.right > cell.left:
                new.right = cell.left
                game.blocked.play()
            if last.left >= cell.right and new.left < cell.right:
                new.left = cell.right
                game.blocked.play()
            if last.bottom <= cell.top and new.bottom > cell.top:
                self.resting = True
                new.bottom = cell.top
                self.dy = 0
                if "end" in blockers:
                    self.end = True
            if last.top >= cell.bottom and new.top < cell.bottom:
                new.top = cell.bottom
                self.dy = 0
                game.blocked.play()

        for cell in game.tilemap.layers['triggers'].collide(new, 'trap'):
            if last.right <= cell.left and new.right >= cell.left:
                game.player.respawn = True
                game.respawn.play()
            if last.left >= cell.right and new.left <= cell.right:
                game.player.respawn = True
                game.respawn.play()
            if last.bottom <= cell.top and new.bottom > cell.top:
                game.player.respawn = True
                game.respawn.play()
            if last.top >= cell.bottom and new.top < cell.bottom:
                game.player.respawn = True
                game.respawn.play()



        if self.rect.y >= game.tilemap.px_height:
            self.respawn = True
            game.respawn_2.play()

        if self.respawn:
            start_cell = game.tilemap.layers['triggers'].find('player')[0]
            self.rect.x, self.rect.y = (start_cell.px, start_cell.py)
            self.respawn = False

        game.tilemap.set_focus(new.x, new.y)

class Traps(pygame.sprite.Sprite):
    def __init__(self, location, *groups):
        super(Traps, self).__init__(*groups)
        self.rect = pygame.rect.Rect(location, self.image.get_size)


    def update(self, game):
        if self.rect.colliderect(game.player.rect):
            game.player.respawn = True


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((800,600))
    background = pygame.mixer.Sound("{0}background.wav".format("sound/"))
    game_on = Presentation().main(screen)
    background.play()
    if game_on:
        game_on = Game1().main(screen)
    if game_on:
        game_on = Game2().main(screen)
    if game_on:
        game_on = Game3().main(screen)
