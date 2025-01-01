import copy
import random
import pygame

pygame.init()

"""game variables"""
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


"""generate cats"""
dealer_cat = pygame.image.load("img/dealercat.png").convert()
happy_cat = pygame.image.load("img/happycat.png").convert()
mad_cat = pygame.image.load("img/madcat.png").convert()
sad_cat = pygame.image.load("img/sadcat.png").convert()
ask_cat = pygame.image.load("img/askcat.png").convert()
very_happy_cat = pygame.image.load("img/veryhappycat.png").convert()
lose_cat = pygame.image.load("img/losecat.png").convert()
win_cat = pygame.image.load("img/wincat.png").convert()

def set_cat_mood(key):
    if key == 1 or key == 3:
        return sad_cat
    elif key == 2:
        return very_happy_cat
    else:
        if records[0] >= records[1]:
            return happy_cat
        return mad_cat

def show_cat(current_cat_mood):
    """function to show player cat, mood depending on end-of-round result or current score of end-of-game scenario"""
    if current_cat_mood == lose_cat or current_cat_mood == win_cat:
        screen.blit(current_cat_mood, (450, 340))
    else:
        screen.blit(current_cat_mood, (50, 350))


def show_money(money):
    """show current money"""
    screen.blit(smaller_font.render(f'Current money:', True, 'yellow'), (20, 20))
    screen.blit(font.render(f'${money}', True, 'yellow'), (35, 55))


def create_game_deck():
    """create game deck consisting of 4 normal decks of playing cards"""
    cards = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    one_deck = 4 * cards
    decks = 4
    game_deck = copy.deepcopy(decks * one_deck)
    return game_deck


def deal_cards(current_hand, current_deck):
    """deal cards by selecting randomly from deck and make function for one card at a time"""
    card = random.randint(0, len(current_deck) - 1)
    current_hand.append(current_deck.pop(card))
    return current_hand, current_deck


def calculate_score(hand):
    """calculate best score possible for given hand"""
    """calculate hand score fresh every time, check how many aces we have"""
    hand_score = 0
    aces_count = hand.count('A')
    for card in hand:

        """for 2, 3, 4, 5, 6, 7, 8, 9 - just add number to total"""
        if card in ['2', '3', '4', '5', '6', '7', '8', '9']:
            hand_score += int(card)

        """for 10 and face cards, add 10"""
        if card in ['10', 'J', 'Q', 'K']:
            hand_score += 10

        """for aces, start by adding 11, we'll check if we need to reduce afterwards"""
        if card == 'A':
            hand_score += 11
        
        """determine how many aces need to be 1 instead of 11 to get under 21 if possible"""
    while hand_score > 21 and aces_count > 0:
        hand_score -= 10
        aces_count -= 1
    return hand_score


def draw_scores(player, dealer):
    """draw scores for player and dealer on screen"""
    screen.blit(font.render(f'Score[{player}]', True, 'white'), (30, 525))
    if reveal_dealer:
        screen.blit(font.render(f'Score[{dealer}]', True, 'white'), (970, 325))


def draw_cards(player, dealer, reveal):
    """draw cards visually onto screen"""
    for i in range(len(player)):
        pygame.draw.rect(screen, 'white', [250 + (95 * i), 360, 90, 150], 0, 5)
        screen.blit(smaller_font.render(player[i], True, 'black'), (260 + 95 * i, 370))
        screen.blit(smaller_font.render(player[i], True, 'black'), (260 + 95 * i, 470))
        pygame.draw.rect(screen, 'red', [250 + (95 * i), 360, 90, 150], 5, 5)

    """if player hasn't finished turn, dealer will hide one card"""
    for i in range(len(dealer)):
        pygame.draw.rect(screen, 'white', [825 - (95 * i), 160, 90, 150], 0, 5)
        if i != 0 or reveal:
            screen.blit(smaller_font.render(dealer[i], True, 'black'), (835 - 95 * i, 170))
            screen.blit(smaller_font.render(dealer[i], True, 'black'), (835 - 95 * i, 270))
        else: 
            screen.blit(smaller_font.render('???', True, 'black'), (835 - 95 * i, 170))
            screen.blit(smaller_font.render('???', True, 'black'), (835 - 95 * i, 270))
        pygame.draw.rect(screen, 'blue', [825 - (95 * i), 160, 90, 150], 5, 5)    


def draw_game(active, record, outcome):
    """draw game conditions and buttons"""
    button_list = []
    
    if not active:
        """initially on startup (not active) only option is to deal new hand"""
        deal = pygame.draw.rect(screen, 'white', [450, 20, 300, 100], 0, 5)
        pygame.draw.rect(screen, 'green', [450, 20, 300, 100], 3, 5)
        deal_text = font.render('DEAL HAND', True, 'black')
        screen.blit(deal_text, (465, 50))
        button_list.append(deal)

    else:
        """once game started, show hit and stand buttons and win/loss records"""
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

    if outcome != 0:
        """if there is an outcome for the hand that was played, display a restart button and tell user what happened"""
        screen.blit(font.render(results[outcome], True, 'white'), (350, 25))
        deal = pygame.draw.rect(screen, 'white', [450, 270, 300, 100], 0, 5)
        pygame.draw.rect(screen, 'green', [450, 270, 300, 100], 3, 5)
        pygame.draw.rect(screen, 'black', [453, 273, 294, 94], 3, 5)
        deal_text = font.render('NEW HAND', True, 'black')
        screen.blit(deal_text, (475, 298))
        button_list.append(deal)
        
    return button_list


def change_money(input, money):
    """add money on win, substract on loss, nothing on tie"""
    if input == 1 or input == 3:
        money -= 100
    elif input == 2:
        money += 200
    elif input == 4:
        pass
    return money


def check_endgame(money):
    """check endgame conditions: if money ran out, cat loses, if more than 5000, cat is rich"""
    if money <= 0:
        pygame.draw.rect(screen, '#ED1C24', [50, 50, 1100, 600], 0, 5)
        pygame.draw.rect(screen, 'black', [50, 50, 1100, 600], 5, 0)
        screen.blit(bigger_font.render("Cat lost all his money", True, 'Black'), (310, 60))
        screen.blit(font.render("Sadly, he will be taken by animal control", True, 'Black'), (170, 130))
        screen.blit(font.render("At least he had some fun", True, 'Black'), (310, 200))
        screen.blit(smaller_font.render("(or a new addiction)", True, 'Black'), (410, 270))
        current_cat_mood = lose_cat
        show_cat(current_cat_mood)
    if money >= 5000:
        pygame.draw.rect(screen, '#FFF200', [50, 50, 1100, 600], 0, 5)
        pygame.draw.rect(screen, 'black', [50, 50, 1100, 600], 5, 0)
        screen.blit(bigger_font.render("CAT IS RICH", True, 'Black'), (450, 60))
        screen.blit(font.render("He will go and live his life now", True, 'Black'), (290, 130))
        screen.blit(font.render("As the richest cat in the world", True, 'Black'), (295, 200))
        screen.blit(smaller_font.render("(now get off your pc)", True, 'Black'), (430, 270))
        current_cat_mood = win_cat
        show_cat(current_cat_mood)
    

def check_endround(hand_act, deal_score, play_score, result, totals, add, money, current_cat_mood):
    """check endround scenarios if player has stood, busted or blackjack"""
    """result 1 - player bust, 2 - win, 3 - loss, 4 - push"""
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
            current_cat_mood = set_cat_mood(result)
    check_endgame(money)
    return result, totals, add, money, current_cat_mood

def initialize_game():
    """initializes game variables for first game"""
    """returns active (bool), initial_deal (bool), game_deck (list), my_hand (empty list), dealer_hand (empty list), outcome, hand_active, reveal_dealer, add_score, dealer_score, player_score, money, records, results"""
    return False, True, create_game_deck(), [], [], 0, False, False, True, 0, 0, 1000, [0, 0, 0], ['', 'PLAYERCAT BUSTED', 'PLAYERCAT WINS', 'DEALERCAT WINS', 'TIE GAME']

def reset_game():
    """initializes game variables"""
    return True, True, create_game_deck(), [], [], 0, True, False, True, 0, 0, set_cat_mood(0)

def render_game():
    """function to render game elements on screen"""
    screen.fill(background_color)
    show_money(money)
    show_cat(current_cat_mood)
    screen.blit(dealer_cat, (950, 150))

def handle_initial_deal(my_hand, dealer_hand, game_deck):
    """handles the initial deal to player en dealer"""
    for i in range(2):
        my_hand, game_deck = deal_cards(my_hand, game_deck)
        dealer_hand, game_deck = deal_cards(dealer_hand, game_deck)
    return my_hand, dealer_hand, game_deck

def update_scores_and_cards(reveal_dealer, my_hand, dealer_hand, game_deck, player_score, dealer_score):
    player_score = calculate_score(my_hand)
    draw_cards(my_hand, dealer_hand, reveal_dealer)
    if reveal_dealer:
        dealer_score = calculate_score(dealer_hand)
        if dealer_score < 17:
            dealer_hand, game_deck = deal_cards(dealer_hand, game_deck)
    draw_scores(player_score, dealer_score)
    return player_score, dealer_score, dealer_hand, game_deck

"""main game loop"""
run = True
active, initial_deal, game_deck, my_hand, dealer_hand, outcome, hand_active, reveal_dealer, add_score, dealer_score, player_score, money, records, results = initialize_game()
current_cat_mood = set_cat_mood(0)
show_cat(current_cat_mood)
while run:
    """run game at our framerate and render game elements"""
    timer.tick(fps)
    render_game()
    """initial deal to player and dealer"""
    if initial_deal:
        my_hand, dealer_hand, game_deck = handle_initial_deal(my_hand, dealer_hand, game_deck)
        initial_deal = False
    """once game is activated and dealt, calculate scores and display cards"""
    if active:
        player_score, dealer_score, dealer_hand, game_deck = update_scores_and_cards(reveal_dealer, my_hand, dealer_hand, game_deck, player_score, dealer_score)
        
    buttons = draw_game(active, records, outcome)

    """event handling, if quit pressed, then exit game"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONUP:
            if not active:
                if buttons[0].collidepoint(event.pos):
                    active, initial_deal, game_deck, my_hand, dealer_hand, outcome, hand_active, reveal_dealer, add_score, dealer_score, player_score, current_cat_mood = reset_game()
            else:
                if buttons[0].collidepoint(event.pos) and player_score < 21 and hand_active:
                    """if player can hit, allow them to draw a card"""
                    my_hand, game_deck = deal_cards(my_hand, game_deck)
                    current_cat_mood = ask_cat
                    show_cat(current_cat_mood)
                elif buttons[1].collidepoint(event.pos) and not reveal_dealer:
                    """allow player to end turn (stand)"""
                    reveal_dealer = True
                    hand_active = False
                elif len(buttons) == 3:
                    if buttons[2].collidepoint(event.pos):
                        active, initial_deal, game_deck, my_hand, dealer_hand, outcome, hand_active, reveal_dealer, add_score, dealer_score, player_score, current_cat_mood = reset_game()
    
    if hand_active and player_score > 21:
        """if player busts, automatically  end turn - treat like a stand"""
        hand_active = False
        reveal_dealer = True

    outcome, records, add_score, money, current_cat_mood = check_endround(hand_active, dealer_score, player_score, outcome, records, add_score, money, current_cat_mood)

    pygame.display.flip()
pygame.quit()