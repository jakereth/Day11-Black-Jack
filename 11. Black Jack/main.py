import random
import cards

playerHand = []
dealerHand = []
playerBalance = 1000 # Initial balance for the player

def dealCard():
    card_index = random.randint(0, len(cards.card) - 1)
    card = cards.card[card_index]
    cards.card.remove(card)  # Remove the dealt card from the deck
    return card

def player():
    card = dealCard()
    playerHand.append(card)
    print("Player has:", ", ".join(playerHand))

def dealer():
    card = dealCard()
    dealerHand.append(card)
    if len(dealerHand) == 1:
        print("Dealer has:", dealerHand[0], "and one card face down")
    else:
        print("Dealer has:", ", ".join(dealerHand))

def calculatePlayerHand(playerHand):
    total_value = sum(cards.cards_dict[card] for card in playerHand)
    num_aces = playerHand.count('Ace Hearts') + playerHand.count('Ace Diamonds') + playerHand.count('Ace Clubs') + playerHand.count('Ace Spades')
    # Adjust the total value if there are Aces in the hand
    while total_value > 21 and num_aces > 0:
        total_value -= 10
        num_aces -= 1
    return total_value

def calculateDealerHand(dealerHand):
    total_value = sum(cards.cards_dict[card] for card in dealerHand)
    num_aces = dealerHand.count('Ace Hearts') + dealerHand.count('Ace Diamonds') + dealerHand.count('Ace Clubs') + dealerHand.count('Ace Spades')
    # Adjust the total value if there are Aces in the hand
    while total_value > 21 and num_aces > 0:
        total_value -= 10
        num_aces -= 1
    return total_value

def placeBet():
    global playerBalance
    while True:
        try:
            bet_amount = int(input("Place your bet (current balance: {}): ".format(playerBalance)))
            if bet_amount <= 0:
                print("Please enter a positive bet amount.")
            elif bet_amount > playerBalance:
                print("Insufficient balance. Please enter a bet within your balance.")
            else:
                playerBalance -= bet_amount
                return bet_amount
        except ValueError:
            print("Invalid input. Please enter a valid bet amount.")

def hit():
    player_total = calculatePlayerHand(playerHand)
    if player_total > 21:
        print("Player busts!")
        determine_winner()
    elif player_total == 21:
        print("Player has Blackjack!")
        determine_winner()
    else:
        action = input("Do you want to hit or stand? (h/s): ").lower()
        if action == 'h':
            player()
            hit()
        elif action == 's':
            dealer_turn()
        else:
            print("Invalid input. Please enter 'h' to hit or 's' to stand.")
            hit() 

def dealer_turn():
    print("Dealer has:", ", ".join(dealerHand))  # Reveal the full dealer's hand
    while True:
        dealer_total = calculateDealerHand(dealerHand)
        if dealer_total >= 17:
            break
        dealer()

    if dealer_total > 21:
        print("Dealer busts!")
    else:
        print("Dealer stands.")
    determine_winner()

def determine_winner():
    global playerBalance
    player_total = calculatePlayerHand(playerHand)
    dealer_total = calculateDealerHand(dealerHand)

    if player_total > 21:
        print("Dealer wins!")
    elif dealer_total > 21:
        print("Player wins!")
        playerBalance += 2 * bet_amount
    elif player_total > dealer_total:
        print("Player wins!")
        playerBalance += 2 * bet_amount
    elif player_total < dealer_total:
        print("Dealer wins!")
    else:
        print("It's a tie!")
        playerBalance += bet_amount

# Initial function calls to start the game
while True:
    playerHand.clear()
    dealerHand.clear()
    print("\nNew Round")
    bet_amount = placeBet()
    player()
    player()
    dealer()
    hit()
    play_again = input("Do you want to play again? (y/n): ").lower()
    if play_again != 'y':
        print("Thank you for playing!")
        break