import random

suits = ["♠", "♥", "♦", "♣"]
ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]

deck = [suit + rank for suit in suits for rank in ranks]


def ruler(cards):
    value = 0
    a = 0
    for card in cards:
        rank = card[1:]  
        if rank in ["J", "Q", "K"]:
            value += 10
        elif rank == 'A':
            value += 11
            a += 1
        else:
            value += int(rank)

    while value > 21 and a:
        value -= 10
        a -= 1

    return value

benefit = 0

def bat():
    try:
        money = int(input('How much you want to gamble: $'))
        return money
    except ValueError :
        print('Please type in a number')
        money = int(input('How much you want to gamble: $'))

def gamestate(player_hand, dealer_hand, money, benefit, helper):
    print('player_hand: ', player_hand)
    print('dealer_hand', f'[{dealer_hand[0]}]', 'and [hidden]')

    choice = input('Hit , Stand[H/S]').lower()

    if choice not in ['h','s']:
        print('sorry, please choose between h , s ')
        choice = input('Hit , Stand[H/S]').lower()

    elif choice == 'h':
        helper, benefit = hit(player_hand, money, benefit, helper)
        return helper, benefit 

    else:
        helper, benefit = stand(player_hand, dealer_hand, money, benefit, helper)
        return helper, benefit 

def hit(player_hand, money, benefit, helper):
    player_hand.append(deck.pop())
    print('player_hand: ', player_hand)
    if ruler(player_hand) > 21:
        print("Your hand:", player_hand, "value:", ruler(player_hand))
        print('You bust! Dealer wins.')
        benefit -= money
        helper = False
    return helper, benefit


def stand(player_hand, dealer_hand, money, benefit, helper):
    print(dealer_hand)
    while ruler(dealer_hand) < 17:
        dealer_hand.append(deck.pop())
        print(dealer_hand)
        if ruler(dealer_hand) > 21:
            print("dealer hand:", dealer_hand, "value:", ruler(dealer_hand))
            print(f'Dealer lost! You win ${money}')
            benefit += money
            helper = False
            return helper, benefit 
    helper, benefit = compare(player_hand, dealer_hand, money, benefit, helper)
    return helper, benefit 
    

    
def compare(player_hand, dealer_hand, money, benefit, helper):
    if ruler(player_hand) == ruler(dealer_hand):
        pass

    elif  ruler(dealer_hand) > ruler(player_hand):
        print("Your hand:", player_hand, "value:", ruler(player_hand))
        print("dealer hand:", dealer_hand, "value:", ruler(dealer_hand))
        print('Dealer wins. You lost')
        benefit -= money
            
    else:
        print("Your hand:", player_hand, "value:", ruler(player_hand))
        print("dealer hand:", dealer_hand, "value:", ruler(dealer_hand)) 
        print(f'Dealer lost! You win ${money}')
        benefit += money
    helper = False
    return helper, benefit

while True :
    statement = input('start, quit or benefit: ')
    if statement == 'quit':
        break

    elif statement =='start':
        helper = True
        random.shuffle(deck)

        player_hand = [deck.pop(), deck.pop()]
        dealer_hand = [deck.pop(), deck.pop()]
        money = bat()
        while helper:   
            helper, benefit = gamestate(player_hand, dealer_hand, money, benefit, helper)

    elif statement == 'benefit':
        print(f'${benefit}')

    else:
        print('sorry, invalid input')
        statement = input('start, quit or benefit: ')

