import copy
import random
import pygame

pygame.init()

#game variables
cards = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
one_deck = 4 * cards
decks = 4
money = 1000 #player starts with $1000
WIDTH = 1200
HEIGHT = 700
background_color = "#1A8A3B"
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('Cat Blackjack!')
fps = 60
timer = pygame.time.Clock()
font = pygame.font.Font('freesansbold.ttf', 44)
smaller_font = pygame.font.Font('freesansbold.ttf', 36)
bigger_font = pygame.font.Font('freesansbold.ttf', 50)
active = False
# win, loss, draw/push
records = [0, 0, 0]
player_score = 0
dealer_score = 0
initial_deal = True
game_deck = copy.deepcopy(decks * one_deck)
my_hand = []
dealer_hand = []
outcome = 0
reveal_dealer = False
hand_active = False
add_score = False
results = ['', 'PLAYERCAT BUSTED', 'PLAYERCAT WINS', 'DEALERCAT WINS', 'TIE GAME']

# generate cats
dealer_cat = pygame.image.load("img/dealercat.png").convert()
happy_cat = pygame.image.load("img/happycat.png").convert()
mad_cat = pygame.image.load("img/madcat.png").convert()
sad_cat = pygame.image.load("img/sadcat.png").convert()
ask_cat = pygame.image.load("img/askcat.png").convert()
very_happy_cat = pygame.image.load("img/veryhappycat.png").convert()
lose_cat = pygame.image.load("img/losecat.png").convert()
win_cat = pygame.image.load("img/wincat.png").convert()

# function to show player cat, mood depending on end-of-round result or current score of end-of-game scenario
def show_cat(key):
    if key == 1 or key == 3:
        screen.blit(sad_cat, (50, 350))
    elif key == 2:
        screen.blit(very_happy_cat, (50, 350))
    elif key == "hit":
        screen.blit(ask_cat, (50, 350))
    elif key == "none" and records[0] >= records[1]:
        screen.blit(happy_cat, (50, 350))
    elif key == "lost":
        screen.blit(lose_cat, (450, 340))
    elif key == "win":
        screen.blit(win_cat, (450, 340))
    elif key == "none" and records[0] < records[1]:
        screen.blit(mad_cat, (55, 350))

# show current money 
def show_money(money):
    screen.blit(smaller_font.render(f'Current money:', True, 'yellow'), (20, 20))
    screen.blit(font.render(f'${money}', True, 'yellow'), (35, 55))


# deal cards by selecting randomly from deck and make function for one card at a time
def deal_cards(current_hand, current_deck):
    card = random.randint(0, len(current_deck))
    current_hand.append(current_deck[card-1])
    current_deck.pop(card-1)
    return current_hand, current_deck

# draw scores for player and dealer on screen
def draw_scores(player, dealer):
    screen.blit(font.render(f'Score[{player}]', True, 'white'), (30, 525))
    if reveal_dealer:
        screen.blit(font.render(f'Score[{dealer}]', True, 'white'), (970, 325))

# draw cards visually onto screen
def draw_cards(player, dealer, reveal):
    for i in range(len(player)):
        pygame.draw.rect(screen, 'white', [250 + (95 * i), 360, 90, 150], 0, 5)
        screen.blit(smaller_font.render(player[i], True, 'black'), (260 + 95 * i, 370))
        screen.blit(smaller_font.render(player[i], True, 'black'), (260 + 95 * i, 470))
        pygame.draw.rect(screen, 'red', [250 + (95 * i), 360, 90, 150], 5, 5)

    # if player hasn't finished turn, dealer will hide one card
    for i in range(len(dealer)):
        pygame.draw.rect(screen, 'white', [825 - (95 * i), 160, 90, 150], 0, 5)
        if i != 0 or reveal:
            screen.blit(smaller_font.render(dealer[i], True, 'black'), (835 - 95 * i, 170))
            screen.blit(smaller_font.render(dealer[i], True, 'black'), (835 - 95 * i, 270))
        else: 
            screen.blit(smaller_font.render('???', True, 'black'), (835 - 95 * i, 170))
            screen.blit(smaller_font.render('???', True, 'black'), (835 - 95 * i, 270))
        pygame.draw.rect(screen, 'blue', [825 - (95 * i), 160, 90, 150], 5, 5)

# pass in player or dealer hand and get best score possible
def calculate_score(hand):
    # calculate hand score fresh every time, check how many aces we have
    hand_score = 0
    aces_count = hand.count('A')
    for i in range(len(hand)):
        # for 2, 3, 4, 5, 6, 7, 8, 9 - just add number to total
        for j in range(8):
            if hand[i] == cards[j]:
                hand_score += int(hand[i])
        # for 10 and face cards, add 1°
        if hand[i] in ['10', 'J', 'Q', 'K']:
            hand_score += 10
        # for aces, start by adding 11, we'll check if we need to reduce afterwards
        elif hand[i] == 'A':
            hand_score += 11
        # determine how many aces need to be 1 instead of 11 to get under 21 if possible
    if hand_score > 21 and aces_count > 0:
        for i in range(aces_count):
            if hand_score > 21:
                hand_score -= 10
    return hand_score
    

# draw game conditions and buttons
def draw_game(act, record, result, money):
    button_list = []
    # initially on startup (not active) ask number of decks and deal new hand button to confirm
    if not act:
        deal = pygame.draw.rect(screen, 'white', [450, 20, 300, 100], 0, 5)
        pygame.draw.rect(screen, 'green', [450, 20, 300, 100], 3, 5)
        deal_text = font.render('DEAL HAND', True, 'black')
        screen.blit(deal_text, (465, 50))
        button_list.append(deal)
    # once game started, show hit and stand buttons and win/loss records
    else:
        hit = pygame.draw.rect(screen, 'white', [325 , 550, 250, 75], 0, 5)
        pygame.draw.rect(screen, 'red', [325, 550, 250, 75], 3, 5)
        hit_text = font.render('HIT ME', True, 'black')
        screen.blit(hit_text, (365, 570))
        button_list.append(hit)
        stand = pygame.draw.rect(screen, 'white', [600 , 550, 250, 75], 0, 5)
        pygame.draw.rect(screen, 'red', [600, 550, 250, 75], 3, 5)
        stand_text = font.render('STAND', True, 'black')
        screen.blit(stand_text, (640, 570))
        button_list.append(stand)
        score_text = smaller_font.render(f'Wins: {record[0]}   Losses: {record[1]}   Draws: {record[2]}', True, 'white')
        screen.blit(score_text, (335, 640))
    # if there is an outcome for the hand that was played, display a restart button and tell user what happened
    if result != 0:
        screen.blit(font.render(results[result], True, 'white'), (350, 25))
        deal = pygame.draw.rect(screen, 'white', [450, 270, 300, 100], 0, 5)
        pygame.draw.rect(screen, 'green', [450, 270, 300, 100], 3, 5)
        pygame.draw.rect(screen, 'black', [453, 273, 294, 94], 3, 5)
        deal_text = font.render('NEW HAND', True, 'black')
        screen.blit(deal_text, (475, 298))
        button_list.append(deal)
        
    return button_list, money

# add money on win, substract on loss, nothing on tie
def change_money(input, money):
    if input == 1 or input == 3:
        money -= 100
    elif input == 2:
        money += 200
    elif input == 4:
        pass
    return money

# check endgame conditions: if money ran out, cat loses, if more than 5000, cat is rich
def check_endgame(money):
    if money <= 0:
        pygame.draw.rect(screen, '#ED1C24', [50, 50, 1100, 600], 0, 5)
        pygame.draw.rect(screen, 'black', [50, 50, 1100, 600], 5, 0)
        screen.blit(bigger_font.render("Cat lost all his money", True, 'Black'), (310, 60))
        screen.blit(font.render("Sadly, he will be taken by animal control", True, 'Black'), (170, 130))
        screen.blit(font.render("At least he had some fun", True, 'Black'), (310, 200))
        screen.blit(smaller_font.render("(or a new addiction)", True, 'Black'), (410, 270))
        show_cat("lost")
    if money >= 5000:
        pygame.draw.rect(screen, '#FFF200', [50, 50, 1100, 600], 0, 5)
        pygame.draw.rect(screen, 'black', [50, 50, 1100, 600], 5, 0)
        screen.blit(bigger_font.render("CAT IS RICH", True, 'Black'), (450, 60))
        screen.blit(font.render("He will go and live his life now", True, 'Black'), (290, 130))
        screen.blit(font.render("As the richest cat in the world", True, 'Black'), (295, 200))
        screen.blit(smaller_font.render("(now get off your pc)", True, 'Black'), (430, 270))
        show_cat("win")
    
# check endround conditions function
def check_endround(hand_act, deal_score, play_score, result, totals, add, money):
    # check endround scenarios if player has stood, busted or blackjack
    # result 1 - player bust, 2 - win, 3 - loss, 4 - push
    if not hand_act and deal_score >= 17:
        if play_score > 21:
            result = 1
        elif deal_score < play_score <= 21 or deal_score > 21:
            result = 2
        elif play_score < deal_score <= 21:
            result = 3
        else:
            result = 4
        if add:
            if result == 1 or result == 3:
                totals[1] +=1
            elif result == 2:
                totals[0] += 1
            else:
                totals[2] += 1
            money = change_money(result, money)
            add = False
    show_cat(result)
    check_endgame(money)
    return result, totals, add, money


# main game loop
run = True
while run:
    # run game at our framerate and fill screen with bg color
    timer.tick(fps)
    screen.fill(background_color)
    show_money(money)
    show_cat("none")
    screen.blit(dealer_cat, (950, 150))
    # initial deal to player and dealer
    if initial_deal:
        for i in range(2):
            my_hand, game_deck = deal_cards(my_hand, game_deck)
            dealer_hand, game_deck = deal_cards(dealer_hand, game_deck)
        initial_deal = False
    # once game is activated and dealt, calculate scores and display cards
    if active:
        player_score = calculate_score(my_hand)
        draw_cards(my_hand, dealer_hand, reveal_dealer)
        if reveal_dealer:
            dealer_score = calculate_score(dealer_hand)
            if dealer_score < 17:
                dealer_hand, game_deck = deal_cards(dealer_hand, game_deck)
        draw_scores(player_score, dealer_score)
    buttons, money = draw_game(active, records, outcome, money)

    # event handling, if quit pressed, then exit game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONUP:
            if not active:
                if buttons[0].collidepoint(event.pos):
                    active = True
                    initial_deal = True
                    game_deck = copy.deepcopy(decks * one_deck)
                    my_hand = []
                    dealer_hand = []
                    hand_active = True
                    outcome = 0
                    add_score = True
            else:
                # if player can hit, allow them to draw a card
                if buttons[0].collidepoint(event.pos) and player_score < 21 and hand_active:
                    my_hand, game_deck = deal_cards(my_hand, game_deck)
                    show_cat("hit")
                # allow player to end turn (stand)
                elif buttons[1].collidepoint(event.pos) and not reveal_dealer:
                    reveal_dealer = True
                    hand_active = False
                elif len(buttons) == 3:
                    if buttons[2].collidepoint(event.pos):
                        active = True
                        initial_deal = True
                        game_deck = copy.deepcopy(decks * one_deck)
                        my_hand = []
                        dealer_hand = []
                        outcome = 0
                        hand_active = True
                        reveal_dealer = False
                        outcome = 0
                        add_score = True
                        dealer_score = 0
                        player_score = 0


    #if player busts, automatically  end turn - treat like a stand
    if hand_active and player_score > 21:
        hand_active = False
        reveal_dealer = True
    
    outcome, records, add_score, money = check_endround(hand_active, dealer_score, player_score, outcome, records, add_score, money)


    pygame.display.flip()
pygame.quit()