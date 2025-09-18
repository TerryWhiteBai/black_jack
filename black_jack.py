import random

SUITS = ["♠", "♥", "♦", "♣"]
RANKS = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]

def create_deck():
    return [suit + rank for suit in SUITS for rank in RANKS]

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

def get_bet():
    while True:
        try:
            money = int(input('How much you want to gamble: $'))
            if money > 0:
                return money
            else:
                print("Bet must be positive.")
        except ValueError:
            print('Please type in a valid number.')

def gamestate(deck, player_hand, dealer_hand, money, benefit):
    while True:
        print('Your hand:', player_hand, 'Value:', ruler(player_hand))
        print('Dealer shows:', dealer_hand[0], 'and [hidden]')
        choice = input('Hit or Stand [H/S]: ').strip().lower()
        if choice == 'h':
            player_hand.append(deck.pop())
            if ruler(player_hand) > 21:
                print("Your hand:", player_hand, "value:", ruler(player_hand))
                print('You bust! Dealer wins.')
                benefit -= money
                return benefit
        elif choice == 's':
            while ruler(dealer_hand) < 17:
                dealer_hand.append(deck.pop())
                print("Dealer draws:", dealer_hand[-1], "Dealer's hand:", dealer_hand)
            player_val = ruler(player_hand)
            dealer_val = ruler(dealer_hand)
            print("Your hand:", player_hand, "value:", player_val)
            print("Dealer's hand:", dealer_hand, "value:", dealer_val)
            if dealer_val > 21 or player_val > dealer_val:
                print(f'You win ${money}!')
                benefit += money
            elif dealer_val > player_val:
                print('Dealer wins. You lost.')
                benefit -= money
            else:
                print("It's a tie!")
            return benefit
        else:
            print('Invalid input. Please choose H or S.')

def main():
    benefit = 0
    while True:
        statement = input('Type "start" to play, "quit" to exit, or "benefit" to see your total: ').strip().lower()
        if statement == 'quit':
            break
        elif statement == 'start':
            deck = create_deck()
            random.shuffle(deck)
            player_hand = [deck.pop(), deck.pop()]
            dealer_hand = [deck.pop(), deck.pop()]
            money = get_bet()
            benefit = gamestate(deck, player_hand, dealer_hand, money, benefit)
        elif statement == 'benefit':
            print(f'Your total benefit: ${benefit}')
        else:
            print('Sorry, invalid input.')

if __name__ == "__main__":
    main()