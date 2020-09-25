import random

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six': 6, 'Seven': 7, 'Eight': 8,
          'Nine': 9, 'Ten': 10, 'Jack': 10, 'Queen': 10, 'King': 10, 'Ace': 11}


class Card:

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.value = values[rank]

    def __str__(self):
        return self.rank + " of " + self.suit


class Deck:

    def __init__(self):
        self.all_cards = []

        for suit in suits:
            for rank in ranks:
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

    def get_value_list(self):
        return [x.value for x in self.all_cards]

    def get_balance(self):
        print(f"Your balance is {self.balance}€")


class Dealer:

    def __init__(self, name="Georg"):
        self.name = name
        self.all_cards = []

    def add_cards(self, new_cards):
        self.all_cards.append(new_cards)

    def get_value_list(self):
        return [x.value for x in self.all_cards]


def player_bust_check(cards):
    ace_count = cards.count(11)
    sum_cards = sum(cards)
    if sum_cards > 21:
        while ace_count > 0:
            sum_cards -= 10
            ace_count -= 1
            if sum_cards < 22:
                return False
        return True
    return False


def print_cards(name, all_cards, dealer=False):
    if not dealer:
        print(f"{name} your cards are: ")
    else:
        print(f"Dealer {name} has: ")
    for cards in range(len(all_cards)):
        print(f'{all_cards[cards]}', end='')
        if cards + 1 < len(all_cards):
            print(", ", end='')
        else:
            print("\n")


def hit():
    player_1.add_cards(new_deck.deal_one())
    print_cards(player_1.name, player_1.all_cards)
    if player_bust_check(player_1.get_value_list()):
        print("You are busted! You lost!")
        return False
    return True


def check_lose_win_tie():
    while True:
        if 16 < sum(dealer.get_value_list()) < 22:
            break
        dealer.add_cards(new_deck.deal_one())

        if player_bust_check(dealer.get_value_list()):
            print_cards(dealer.name, dealer.all_cards, True)
            print(f"\nDealer busted! Congrats you have won {bet * 2}€!")
            player_1.player_wins(bet * 2)
            return
    print_cards(dealer.name, dealer.all_cards, True)
    if sum(dealer.get_value_list()) > sum(player_1.get_value_list()):
        print("\nDealer won! You lost!")
        return

    elif sum(dealer.get_value_list()) < sum(player_1.get_value_list()):
        print(f"\nCongrats you have won {bet * 2}€!")
        player_1.player_wins(bet * 2)
        return
    else:
        print("\nTie!")
        player_1.player_wins(bet)
        return


if __name__ == "__main__":
    player_1 = Player("Sebastian", 500)
    dealer = Dealer()
    new_deck = Deck()
    new_deck.shuffle()

    print("Welcome to BlackJack!\n")
    game_on = True
    while game_on:
        print("\n" * 2)
        player_1.get_balance()
        try:
            bet = int(input("Please place your bet: "))
            if not player_1.place_bet(bet):
                continue
        except ValueError:
            print("That was not a valid value!")
            continue
        player_1.add_cards([new_deck.deal_one(), new_deck.deal_one()])
        print_cards(player_1.name, player_1.all_cards)
        dealer.add_cards(new_deck.deal_one())
        print_cards(dealer.name, dealer.all_cards, True)
        while True:

            choice = input("\nStand or Hit:").lower()
            if choice != "stand" and choice != "hit":
                print("Please choose between stand or hit!")
                continue

            if choice == "stand":
                print_cards(dealer.name, dealer.all_cards, True)
                check_lose_win_tie()
                game_on = False
                break

            if choice == "hit":
                if not hit():
                    game_on = False
                    break

        if not game_on:
            player_1.get_balance()
            while True:
                replay = input("Do you want play another round? (YES/NO):").lower()
                if replay == "yes" or "no":
                    break
            if replay == "yes":
                if player_1.balance == 0:
                    print("Sorry you do not have enough money to continue playing!")
                    break
                player_1.all_cards = []
                dealer.all_cards = []
                game_on = True
