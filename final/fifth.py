import pygame
from typing import List

pygame.init()


class SetPygame:
    def __init__(self):
        self.screen_width = 800
        self.screen_height = 500

        self.burger_list = []
        self.click_count = 0
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Hamburger Kiosk")

        self.text_font = pygame.font.SysFont("Arial", 30)

        self.onion_img = pygame.image.load("onion.PNG").convert_alpha()
        self.pickle_img = pygame.image.load("pickle.PNG").convert_alpha()
        self.cheese_img = pygame.image.load("cheese.PNG").convert_alpha()
        self.tomato_img = pygame.image.load("tomato.PNG").convert_alpha()
        self.lettuce_img = pygame.image.load("lettuce.PNG").convert_alpha()
        self.sauce_img = pygame.image.load("sauce.PNG").convert_alpha()
        self.okay1_img = pygame.image.load("icons8-ok-button-96.png").convert_alpha()
        self.bag_img = pygame.image.load("icons8-bag-80.png").convert_alpha()
        self.okay2_img = pygame.image.load("icons8-okay-96.png").convert_alpha()
        self.back_img = pygame.image.load("icons8-back-100.png").convert_alpha()
        self.pay_img = pygame.image.load("icons8-pay-64.png").convert_alpha()

        self.onion_button = Button(40, 30, self.onion_img, 0.45, self.screen)
        self.pickle_button = Button(290, 30, self.pickle_img, 0.55, self.screen)
        self.cheese_button = Button(550, 30, self.cheese_img, 0.5, self.screen)
        self.tomato_button = Button(40, 180, self.tomato_img, 0.4, self.screen)
        self.lettuce_button = Button(280, 180, self.lettuce_img, 0.35, self.screen)
        self.sauce_button = Button(550, 220, self.sauce_img, 0.5, self.screen)
        self.okay1_button = Button(360, 400, self.okay1_img, 1, self.screen)
        self.bag_button = Button(340, 15, self.bag_img, 1.3, self.screen)
        self.okay2_button = Button(500, 400, self.okay2_img, 0.5, self.screen)
        self.back_button = Button(200, 400, self.back_img, 0.5, self.screen)
        self.pay_button = Button(340, 15, self.pay_img, 1.3, self.screen)

    def draw_text(self, text, font, text_col, x, y, screen):
        img = font.render(text, True, text_col)
        screen.blit(img, (x, y))


class Button:
    def __init__(self, x, y, image, scale, screen):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False
        self.screen = screen

    def draw(self):
        action = False
        # get mouse position
        pos = pygame.mouse.get_pos()

        # check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True

        if pygame.mouse.get_pressed()[0] == 0:  # 마우스가 클릭되지 않았을 때
            self.clicked = False
        # draw button on screen
        self.screen.blit(self.image, (self.rect.x, self.rect.y))

        return action


class Burger(SetPygame):
    # Factory Method Pattern
    def what(self):
        pass

    # Command Pattern
    def coupon(self):
        print("pay using coupon")

    def card(self):
        print("pay using card")


class Factory:
    def create(self, ingredient) -> Burger:
        p = self.createProduct(ingredient)
        return p

    def createProduct(self, ingredient) -> Burger:
        pass


class WhatBurger(Burger, SetPygame):

    def __init__(self, ingredient):
        super().__init__()
        self.ingredient = ingredient

    # Factory Method Pattern
    def what(self):
        print(f"{self.ingredient} 추가 버거가 준비되었습니다.")

    def burgerName(self):
        return self.ingredient

    # Memento Pattern
    def order(self, y):
        text = f"{self.ingredient} added burger is in the shopping bag."
        self.draw_text(text, self.text_font, (0, 0, 0), 140, y, self.screen)

    def createMemento(self):
        burger_memento = BurgerMemento(self.ingredient)
        return burger_memento

    def restore(self, memento):
        self.ingredient = memento.ingredient


class WhatBurgerFactory(Factory):
    def __init__(self):
        self.ingredient = []

    def createProduct(self, ingredient) -> Burger:
        return WhatBurger(ingredient)

    def burgerName(self):
        return self.ingredient


class BurgerMemento:
    def __init__(self, ingredient):
        self.ingredient = ingredient


# Command Pattern
class Command:
    def payMethod(self):
        pass


class BurgerCommand(Command):
    def __init__(self, burger: Burger, commands: List[str]):
        self.burger = burger
        self.commands = commands

    def payMethod(self):
        for command in self.commands:
            if command == "coupon" or command == "쿠폰":
                self.burger.coupon()
            elif command == "card" or command == "카드":
                self.burger.card()


class PlayPygame(SetPygame):
    def __init__(self):
        super().__init__()
        self.user_text = ""
        self.run = True
        self.menu_state = "main"
        self.clock = pygame.time.Clock()
        self.factory = WhatBurgerFactory()

    def setBurger(self, ing):
        burger_ingr = self.factory.create(ing)
        burger_ingr.what()
        self.burger_order = WhatBurger(ing)
        self.burger_list.append(self.burger_order.createMemento())

    def handleEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False
                break

            if self.menu_state == "pay":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        self.user_text = self.user_text[:-1]
                    else:
                        self.user_text += event.unicode

    def updateScreen(self):
        self.screen.fill((255, 255, 255))

        if self.menu_state == "main":
            if self.onion_button.draw():
                self.click_count += 1
                self.setBurger("onion")
                pygame.display.flip()

            if self.pickle_button.draw():
                self.click_count += 1
                self.setBurger("pickle")

            if self.cheese_button.draw():
                self.click_count += 1
                self.setBurger("cheese")

            if self.tomato_button.draw():
                self.click_count += 1
                self.setBurger("tomato")

            if self.lettuce_button.draw():
                self.click_count += 1
                self.setBurger("lettuce")

            if self.sauce_button.draw():
                self.click_count += 1
                self.setBurger("sauce")

            if self.okay1_button.draw():
                self.menu_state = "shopping"

        if self.menu_state == "shopping":
            self.bag_button.draw()
            margin = 40
            y = 130
            for i in range(self.click_count):
                self.burger_order.restore(self.burger_list[i])
                self.burger_order.order(y)
                y += margin

            if self.okay2_button.draw():
                self.menu_state = "pay"

            if self.back_button.draw():
                self.menu_state = "main"

        if self.menu_state == "pay":
            self.pay_button.draw()
            pygame.draw.line(self.screen, (0, 0, 0), (250, 200), (500, 200), 2)

            text_surface = self.text_font.render(self.user_text, True, (0, 0, 0))
            self.screen.blit(text_surface, (280, 165))

            if self.okay2_button.draw():
                user_list = self.user_text.split()
                burger = Burger()
                pay = BurgerCommand(burger, user_list)
                pay.payMethod()

            if self.back_button.draw():
                self.menu_state = "shopping"

            pygame.display.flip()

    def playGame(self):
        while self.run:
            self.handleEvents()
            self.updateScreen()
            pygame.display.update()

        pygame.quit()


play_game = PlayPygame()
play_game.playGame()