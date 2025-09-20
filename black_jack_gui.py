import tkinter as tk
import random
from tkinter import messagebox
import re

suits = ["♠", "♥", "♦", "♣"]
ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]

def create_deck():
    return [suit + rank for suit in suits for rank in ranks]

def ruler(cards):
    value = 0
    aces = 0
    for card in cards:
        rank = card[1:]
        if rank in ["J", "Q", "K"]:
            value += 10
        elif rank == 'A':
            value += 11
            aces += 1
        else:
            value += int(rank)
    while value > 21 and aces:
        value -= 10
        aces -= 1
    return value

class BlackjackGui:
    def __init__(self, window):
        self.window = window
        
        window.title("Blackjack")
        
        self.benefit = 0
        self.money = 0
        self.deck = []
        self.player_hand = []
        self.dealer_hand = []

        self.info_label = tk.Label(window, text = "Welcome to Blackjack", font=("Arial", 24, "bold"))
        self.info_label.pack()

        self.bet_entry = tk.Entry(window, font=("Courier", 20))
        self.bet_entry.pack(pady=40)
        self.bet_entry.insert(0, "Enter your bet: $ ")

        self.start_game_button= tk.Button(window, text= "Start game", command= self.start_game, font=("Helvetica", 18))
        self.start_game_button.pack()

        self.hit_button= tk.Button(window, text= "Hit", command= self.hit, state= tk.DISABLED, font=("Helvetica", 18))
        self.hit_button.pack()

        self.stand_button = tk.Button(window, text="Stand", command=self.stand, state=tk.DISABLED, font=("Helvetica", 18))
        self.stand_button.pack()

        self.player_label= tk.Label(window, text="Player hand", font=("Arial", 24, "bold"))                           
        self.player_label.pack()

        self.dealer_label= tk.Label(window, text= "Dealer hand", font=("Arial", 24, "bold"))
        self.dealer_label.pack()

        self.benefit_label = tk.Label(window, text="Benefit: $0", font=("Arial", 24, "bold"))
        self.benefit_label.pack()

    def start_game(self):
        try:
            self.money = int(re.findall(r'$(\d+(?:\.\d+)?)', self.bet_entry.get())[0])
            self.deck= create_deck()
            random.shuffle(self.deck)
            self.player_hand= [self.deck.pop(), self.deck.pop()]
            self.dealer_hand= [self.deck.pop(), self.deck.pop()]

            self.hit_button.config(state=tk.NORMAL)
            self.stand_button.config(state=tk.NORMAL)
            self.bet_entry.config(state= tk.DISABLED)
            self.update_label()

            if self.money <= 0:
                raise ValueError
        except (ValueError,IndexError) as e:
            messagebox.showerror("Invalid Bet", "Please enter a positive integer for your bet.")
        
    def update_label(self):
        self.player_label.config(text=f"Your hand {self.player_hand} Value {ruler(self.player_hand)}")
        self.dealer_label.config(text=f"Dealer's hand: {self.dealer_hand[1]} and [hidden]")

    def hit(self):
        self.player_hand.append(self.deck.pop())
        self.update_label()
        if ruler(self.player_hand)> 21:
            self.info_label.config(text= "You bust!")
            self.benefit =self.benefit - self.money
            self.end_round()

    def stand(self):
        while ruler(self.dealer_hand)< 17:
            self.dealer_hand.append(self.deck.pop())
            self.dealer_label.config(text= f"Dealer's hand: {self.dealer_hand}")
        d = ruler(self.dealer_hand)
        p = ruler(self.player_hand)
        if d> 21 or d< p:
            self.benefit += self.money
            self.info_label.config(text= f'You win! Here is your ${self.money}')
        elif d > p:
            self.benefit =self.benefit - self.money
            self.info_label.config(text= f'You lost ${self.money}')
        else:
            self.info_label.config(text="It's a tie")
        self.end_round()

    def end_round(self):
        self.player_label.config(text=f"Your hand {self.player_hand} Value {ruler(self.player_hand)}")
        self.dealer_label.config(text=f"Dealer's hand: {self.dealer_hand} Value {ruler(self.dealer_hand)}")
        self.hit_button.config(state= tk.DISABLED)
        self.stand_button.config(state=tk.DISABLED)
        self.bet_entry.config(state= tk.NORMAL)
        self.benefit_label.config(text= f'Benefits: ${self.benefit}')

if __name__ == "__main__":
    root = tk.Tk()
    app = BlackjackGui(root)
    root.geometry("800x600+650+300")
    root.mainloop()