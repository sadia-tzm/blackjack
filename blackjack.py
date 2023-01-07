import tkinter
from PIL import Image, ImageTk
from tkinter import messagebox
import random

# To start game, deal first cards and start tkinter window
def play():
    first_deal()
    window.mainloop()

# load in card images to be used throughout game
def get_images(card_images):
    suits_for_images = ['hearts', 'clubs', 'diamonds', 'spades']
    face_cards = ['jack', 'queen', 'king']

    for suit in suits_for_images:
        # images for ace to 10
        for card in range(1, 11):
            name = 'images/{}_of_{}.png'.format(str(card), suit)
            image = Image.open(name)
            resize_image = image.resize((100, 200))
            img = ImageTk.PhotoImage(resize_image)
            card_name = '{}_of_{}'.format(str(card), suit)
            card_images.append((card, img, card_name, ))

        # images for face cards, all value 10
        for card in face_cards:
            name = 'images/{}_of_{}.png'.format(str(card), suit)
            image = Image.open(name)
            resize_image = image.resize((100, 200))
            img = ImageTk.PhotoImage(resize_image)
            card_name = '{}_of_{}'.format(str(card), suit)
            card_images.append((10, img, card_name, ))

# first deal of cards at start of game
def first_deal():
    hit()
    dealer_hand.append(deal_card(dealer_cards_frame))
    dealer_score_label.set(score(dealer_hand))
    hit()

# deal single card from top of deck
def deal_card(frame):
    next_card = deck.pop(0)
    deck.append(next_card)
    tkinter.Label(frame, image=next_card[1], relief="raised").pack(side="left")
    return next_card

# score of hand, have to adjust for ace - value either 11 or 1
def score(hand):
    ace = False
    score_value = 0
    for next_card in hand:
        card_value = next_card[0]
        # adjusting for ace, ace value 11
        if card_value == 1 and not ace:
            ace = True
            card_value = 11
        score_value += card_value
        # ace value 1 if scenario leads to bust
        if score_value > 21 and ace:
            score_value -= 10
            ace = False
    return score_value

# Click Hit Button
def hit():
    # Player gets a new card
    player_hand.append(deal_card(player_cards_frame))
    player_score = score(player_hand)
    player_score_label.set(player_score)
    # If player score is more than 21, player busts, display message box
    if player_score > 21:
        winner_text.set("Player Busts! Dealer Wins!")
        messagebox.showinfo("You Lose!", "Player Busts! You Lose")
        new_game()

# Click Stand Button
def stand():
    # Dealer keeps hitting until reaches 17, special 17 rule for dealer
    dealer_score = score(dealer_hand)
    while 0 < dealer_score < 17:
        dealer_hand.append(deal_card(dealer_cards_frame))
        dealer_score = score(dealer_hand)
        dealer_score_label.set(dealer_score)

    # Player scenarios, result displayed in message box
    player_score = score(player_hand)
    if player_score > 21:
        winner_text.set("Dealer Wins!")
        messagebox.showinfo("You Lose!", "Dealer Wins! You Lose")
        new_game()
    elif dealer_score > 21:
        winner_text.set("Dealer Busts! Player Wins!")
        messagebox.showinfo("You Win!", "Dealer Busts! You Win")
        new_game()
    elif dealer_score < player_score:
        winner_text.set("Player Wins!")
        messagebox.showinfo("You Win!", "You Win!")
        new_game()
    elif dealer_score > player_score:
        winner_text.set("Dealer Wins!")
        messagebox.showinfo("You Lose!", "You Lose")
        new_game()
    else:
        winner_text.set("Draw!")
        messagebox.showinfo("Draw!", "Draw")
        new_game()

# Set up a new game
def new_game():
    global dealer_hand
    global player_hand
    global dealer_cards_frame
    global player_cards_frame

    # clears old game, clears player and dealer cards
    dealer_cards_frame.destroy()
    dealer_cards_frame = tkinter.Frame(cards_frame, bg="green")
    dealer_cards_frame.grid(row=0, column=1, rowspan=2, sticky='ew')
    player_cards_frame.destroy()
    player_cards_frame = tkinter.Frame(cards_frame, bg="green")
    player_cards_frame.grid(row=2, column=1, rowspan=2, sticky='ew')

    # resets title box and player hands, deals new cards
    winner_text.set("Blackjack")
    dealer_hand = []
    player_hand = []
    first_deal()

# Shuffle the deck
def shuffle():
    random.shuffle(deck)
    
# Setting up tkinter window and frames for GUI
window = tkinter.Tk()
window.title("Blackjack!")
window.geometry("800x560")
window.configure(bg="green") 

window.columnconfigure(0, weight=2)
window.columnconfigure(1, weight=2)
window.columnconfigure(2, weight=2)
window.columnconfigure(3, weight=5)

# Title Box
winner_text = tkinter.StringVar()
winner_text.set("Blackjack")
title = tkinter.Label(window, textvariable=winner_text, font="Montserrat", padx=10, pady=6, bg="yellow")
title.grid(row=0, column=0, columnspan=3, pady=5)

# Cards Frame
cards_frame = tkinter.Frame(window, bg="green")
cards_frame.grid(row=1, column=0, columnspan=3, rowspan=2, sticky='ew', pady=8)

# Dealer Labels
dealer_score_label = tkinter.IntVar()
tkinter.Label(cards_frame, text="  Dealer  ", bg="green", fg="white", font="Montserrat").grid(row=0, column=0)
tkinter.Label(cards_frame, textvariable=dealer_score_label, bg="green", fg="white", font="Montserrat").grid(row=1, column=0)

# Dealer Cards Frame
dealer_cards_frame = tkinter.Frame(cards_frame, bg="green")
dealer_cards_frame.grid(row=0, column=1, rowspan=2, sticky='ew')

# Player Labels
player_score_label = tkinter.IntVar()
tkinter.Label(cards_frame, text="  Player  ", bg="green", fg="white", font="Montserrat").grid(row=2, column=0)
tkinter.Label(cards_frame, textvariable=player_score_label, bg="green", fg="white", font="Montserrat").grid(row=3, column=0)

# Player Cards Frame
player_cards_frame = tkinter.Frame(cards_frame, bg="green")
player_cards_frame.grid(row=2, column=1, rowspan=2, sticky='ew')

# Buttons Frame
buttons_frame = tkinter.Frame(window)
buttons_frame.grid(row=3, column=1, columnspan=3, sticky='w')

# Hit Button
hit_button = tkinter.Button(buttons_frame, text="Hit", command=hit, padx=10, font="Montserrat")
hit_button.grid(row=0, column=0)

# Stand Button
stand_button = tkinter.Button(buttons_frame, text="Stand", command=stand, padx=10, font="Montserrat")
stand_button.grid(row=0, column=1)

# New Game Button
new_game_button = tkinter.Button(buttons_frame, text="New Game", command=new_game, padx=7, font="Montserrat")
new_game_button.grid(row=0, column=2)

# Setting up Card Deck - card value, image and name
cards = []
get_images(cards)
print(cards)
deck = list(cards)
# Shuffle the deck before beginning
shuffle()

# Set up hands
dealer_hand = []
player_hand = []
    
if __name__ == '__main__':
    play()