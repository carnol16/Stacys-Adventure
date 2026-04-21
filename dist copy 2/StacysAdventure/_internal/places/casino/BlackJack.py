import random

# Card + Deck Utilities

suits = ["♠", "♥", "♦", "♣"]
ranks = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]

def create_shoe(decks=1):
    """Creates a shoe with X decks."""
    return [(rank, suit) for rank in ranks for suit in suits] * decks

def card_value(card):
    rank, _ = card
    if rank in ["J", "Q", "K"]:
        return 10
    if rank == "A":
        return 11
    return int(rank)

def calculate_hand_value(hand):
    total = sum(card_value(card) for card in hand)
    aces = sum(1 for card in hand if card[0] == "A")

    # Adjust Aces from 11→1 if needed
    while total > 21 and aces > 0:
        total -= 10
        aces -= 1

    return total

def print_hand(title, hand, hide_first=False):
    if hide_first:
        print(f"{title}: [??] {hand[1][0]}{hand[1][1]}")
    else:
        cards = " ".join(rank + suit for rank, suit in hand)
        print(f"{title}: {cards}  ({calculate_hand_value(hand)})")

# Blackjack Game


def blackjack(wallet, wager, shoe=None):
    """Play a round of blackjack with real cards."""
    # Make shoe if needed
    if shoe is None or len(shoe) < 10:
        shoe = create_shoe(6)
        random.shuffle(shoe)

    if wager > wallet:
        print(" Not enough money!")
        return wallet, shoe

    # Deal initial hands
    player = [shoe.pop(), shoe.pop()]
    dealer = [shoe.pop(), shoe.pop()]

    print("\n===== 🃏 BLACKJACK 🃏 =====")
    print_hand("Your hand", player)
    print_hand("Dealer", dealer, hide_first=True)

    # Check natural blackjack
    if calculate_hand_value(player) == 21:
        print("\nBLACKJACK! You win 1.5× your bet.")
        return wallet + int(wager * 1.5), shoe

    # Player turn
    while True:
        print("\nChoose: (H)it  (S)tand  (D)ouble")
        move = input("> ").lower()

        if move == "h":
            player.append(shoe.pop())
            print_hand("Your hand", player)

            if calculate_hand_value(player) > 21:
                print("\nYou bust! Dealer wins.")
                return wallet - wager, shoe

        elif move == "d":
            # Double Down = take exactly one more card
            if wager * 2 > wallet:
                print("Not enough money to double down.")
                continue

            wager *= 2
            player.append(shoe.pop())
            print_hand("Your hand", player)

            if calculate_hand_value(player) > 21:
                print("\nYou bust after doubling! Dealer wins.")
                return wallet - wager, shoe
            break

        elif move == "s":
            break

    # Dealer turn
    print("\nDealer reveals:")
    print_hand("Dealer", dealer)

    while calculate_hand_value(dealer) < 17:
        dealer.append(shoe.pop())
        print_hand("Dealer", dealer)

    player_total = calculate_hand_value(player)
    dealer_total = calculate_hand_value(dealer)

    # Determine outcome
    print("\nRESULT")
    print_hand("Your final hand", player)
    print_hand("Dealer final hand", dealer)

    if dealer_total > 21:
        print("Dealer busts! You win!")
        return wallet + wager, shoe

    if player_total > dealer_total:
        print("You win!")
        return wallet + wager, shoe

    if player_total < dealer_total:
        print("Dealer wins:(")
        return wallet - wager, shoe

    print("Push (tie). Bet returned.")
    return wallet, shoe
