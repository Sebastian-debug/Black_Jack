import random

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Ace1', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Ace1': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six': 6, 'Seven': 7, 'Eight': 8,
          'Nine': 9, 'Ten': 10, 'Jack': 10, 'Queen': 10, 'King': 10, 'Ace': 11}


class Card:

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.value = values[rank]

    def __str__(self):
        return (self.rank if self.rank != "Ace1" else "Ace") + " of " + self.suit


class Deck:

    def __init__(self):
        self.all_cards = []

        for suit in suits:
            for rank in ranks:
                if rank != 'Ace1':
                    self.all_cards.append(Card(suit, rank))

    def shuffle(self):
        random.shuffle(self.all_cards)

    def deal_one(self):
        return self.all_cards.pop()


class Player:

    def __init__(self, name, balance):
        self.name = name
        self.balance = balance
        self.all_cards = []

    def place_bet(self, value):
        if self.balance - value < 0:
            print("Not enough money to place that bet!")
            return False
        else:
            self.balance -= value
            return True

    def player_wins(self, value):
        self.balance += value

    def add_cards(self, new_cards):
        if isinstance(new_cards, list):
            self.all_cards.extend(new_cards)
        else:
            self.all_cards.append(new_cards)

    def get_balance(self):
        print(f"Your balance is {self.balance}€")


class Dealer:

    def __init__(self, name="Georg"):
        self.name = name
        self.all_cards = []

    def add_cards(self, new_cards):
        if isinstance(new_cards, list):
            self.all_cards.extend(new_cards)
        else:
            self.all_cards.append(new_cards)


def get_value_list(card_list):
    return [x.value for x in card_list]


def player_bust_check(real_cards):
    cards = get_value_list(real_cards)
    ace_count = cards.count(11)
    sum_cards = sum(cards)
    if sum_cards > 21:
        while ace_count > 0:
            sum_cards -= 10
            ace_count -= 1
            for real_card in real_cards:
                if real_card.rank == "Ace":
                    real_card.rank = "Ace1"
                    real_card.value = 1
                    break
            if sum_cards < 22:
                return False
        return True
    return False


def print_start_cards():
    print(f"\nDealer {dealer.name}'s Hand:")
    print(" <card hidden>")
    print('', dealer.all_cards[1])
    print(f"\n{player_1.name}'s Hand:", *player_1.all_cards, sep='\n ')


def print_all_cards():
    print(f"\nDealer {dealer.name}'s Hand:", *dealer.all_cards, sep='\n ')
    print(f"Dealer {dealer.name}'s Hand =", sum(get_value_list(dealer.all_cards)))
    print(f"\n{player_1.name}'s Hand:", *player_1.all_cards, sep='\n ')
    print(f"{player_1.name}'s Hand =", sum(get_value_list(player_1.all_cards)))


def hit():
    player_1.add_cards(new_deck.deal_one())
    print_start_cards()
    if player_bust_check(player_1.all_cards):
        print_all_cards()
        print("\nYou are busted! You lost!")
        return False
    return True


def stand_check_lose_win_tie():
    print_all_cards()
    while True:
        if sum(get_value_list(dealer.all_cards)) > 16:
            break
        dealer.add_cards(new_deck.deal_one())
        print_all_cards()
        if player_bust_check(dealer.all_cards):
            print(f"\nDealer busted! Congrats you have won {bet * 2}€!")
            player_1.player_wins(bet * 2)
            return

    if sum(get_value_list(dealer.all_cards)) > sum(get_value_list(player_1.all_cards)):
        print("\nDealer won! You lost!")
        return

    elif sum(get_value_list(dealer.all_cards)) < sum(get_value_list(player_1.all_cards)):
        print(f"\nCongrats you have won {bet * 2}€!")
        player_1.player_wins(bet * 2)
        return
    else:
        print("\nTie!")
        player_1.player_wins(bet)
        return


if __name__ == "__main__":
    player_1 = Player("Max", 500)
    dealer = Dealer()
    new_deck = Deck()
    new_deck.shuffle()

    print("Welcome to BlackJack!")
    game_on = True
    while game_on:
        print("\n")
        player_1.get_balance()
        try:
            bet = int(input("Please place your bet: "))
            if not player_1.place_bet(bet):
                continue
        except ValueError:
            print("That was not a valid value, it must be an integer!")
            continue
        player_1.add_cards([new_deck.deal_one(), new_deck.deal_one()])
        dealer.add_cards([new_deck.deal_one(), new_deck.deal_one()])
        print_start_cards()
        while True:
            choice = input("\nStand or Hit? Enter 's' or 'h: ").lower()

            if choice == "s":
                print("Player stands. Dealer is playing.")
                stand_check_lose_win_tie()
                game_on = False
                break

            elif choice == "h":
                if not hit():
                    game_on = False
                    break
            else:
                print("Please choose between stand or hit! Enter 'h' or 's': ")
                continue

        if not game_on:
            player_1.get_balance()
            while True:
                replay = input("Do you want play another round? (YES/NO):").lower()
                if replay == "yes" or replay == "no":
                    break
            if replay == "yes":
                if player_1.balance == 0:
                    print("Sorry you do not have enough money to continue playing!")
                    break
                player_1.all_cards = []
                dealer.all_cards = []
                game_on = True
