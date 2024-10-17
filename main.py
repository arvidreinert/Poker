from setup import *
from rectangle import Rectangle
class Poker():
    def __init__(self):
        self.cards_image_sheet = SpriteSheet("ace-159857_1280.png")
        positions = [(110,260),(220,260),(width/2-110,115),(width/2,115),(width-220,260),(width-110,260),(110,height-260),(220,height-260),(width/2-110,height-115),(width/2,height-115),(width-220,height-260),(width-110,height-260)]
        self.objects = []
        y = 1
        for i in range(0, 12):
            test =  Rectangle((100,100),positions[i],(250,0,0),"ace-159857_1280.png")
            self.objects.append(test)
            if i%2 == 0:
                y += 1
        
        self.card_rankings = ("2","3","4","5","6","7","8","9","10","J","Q","K","A")
        self.cards = ['hA','h2', 'h3', 'h4', 'h5', 'h6', 'h7', 'h8', 'h9', 'h10', 'hJ', 'hQ', 'hK','sA', 's2', 's3', 's4', 's5', 's6', 's7', 's8', 's9', 's10', 'sJ', 'sQ', 'sK','dA', 'd2', 'd3', 'd4', 'd5', 'd6', 'd7', 'd8', 'd9', 'd10', 'dJ', 'dQ', 'dK','cA', 'c2', 'c3', 'c4', 'c5', 'c6', 'c7', 'c8', 'c9', 'c10', 'cJ', 'cQ',"cK"]
        self.current_cards = self.cards.copy() 
        self.images = []
        y = 0
        x = 0
        for i in range(1,53):
            self.images.append(self.cards_image_sheet.image_at((98.5*x,135.4*y,100,135)))
            x += 1
            if x == 13:
                y += 1
                x = 0

        self.players_cards = {}
        self.give_players_cards()
        print(self.players_cards)
        self.visualize_players_cards()
        self.main_loop()

    def give_players_cards(self):
        for i in range(1,7):
            self.players_good_cards = []
            self.players_cards[f"player{i}"] = []
            for o in range(0,2):
                x = random.randint(0,len(self.current_cards)-1)
                self.players_cards[f"player{i}"].append(self.current_cards[x])
                self.current_cards.remove(self.current_cards[x])

    def visualize_players_cards(self):
        player = 1
        for i in range(0,len(self.objects)):
            self.objects[i].set_image(self.images[self.cards.index(self.players_cards[f"player{player}"][i%2])],True)
            x = i+1
            if x%2 == 0:
                player += 1
        if pygame.mixer.Channel(0).get_busy() == False:
                pygame.mixer.Channel(0).play(pygame.mixer.Sound("Aufzeichnung.mp3"))
                pygame.mixer.Channel(1).set_volume(2)

    def missing_cards_to_straight(self,player, is_flop):
        players_cards = self.players_cards[player]
        players_listed_cards = (list(players_cards[0]),list(players_cards[1]))
        player_cards_ranks = (0,0)
        try:
            player_cards_ranks = (self.card_rankings.index(players_listed_cards[0][1]),self.card_rankings.index(players_listed_cards[1][1]))
        except:
            if "1" in players_listed_cards[1] and "0" in players_listed_cards[1] and "1" in players_listed_cards[0] and "0" in players_listed_cards[0]:
                player_cards_ranks = (8,8)
            else:
                if "1" in players_listed_cards[0] and "0" in players_listed_cards[0]:
                    player_cards_ranks = (8, self.card_rankings.index(players_listed_cards[1][1]))
                if "1" in players_listed_cards[1] and "0" in players_listed_cards[1]:
                    player_cards_ranks = (self.card_rankings.index(players_listed_cards[0][1]),8)

        d = abs(player_cards_ranks[0]-player_cards_ranks[1])
        if d <= 5 and d != 0:
            possible_straights = []
            for x in range(0,2):
                offset = 0
                for i in range(0,5):
                    current_straight = [0,0,0,0,0]
                    current_straight[i] = self.card_rankings[player_cards_ranks[x]]
                    #print("player cards rank index", player_cards_ranks[x], self.card_rankings[player_cards_ranks[x]])
                    for y in range(0,5):
                        if not y == i and player_cards_ranks[x]-offset+y <= len(self.card_rankings)-1 and player_cards_ranks[x]-offset+y >= 0:
                            current_straight[y] = self.card_rankings[player_cards_ranks[x]-offset+y]
                    if len(current_straight) == 5 and 0 not in current_straight:
                        if current_straight not in possible_straights:
                            if self.card_rankings[player_cards_ranks[0]] in current_straight and self.card_rankings[player_cards_ranks[1]] in current_straight:
                                possible_straights.append(current_straight.copy())
                            else:
                                pass
                    offset += 1

            ps = []
            for liste in possible_straights:
                for rank in liste:
                    ps.append(rank)
            possible_straights = []
            for card in self.cards:
                for rank in ps:
                    if rank in card and card not in possible_straights and card not in players_cards:
                        if self.cards.index(card)%6 != 0 and not self.cards.index(card) == 0:
                            possible_straights.append(card)
            return possible_straights
        else:
            return False

    def get_missing_cards_to_pair(self,player,is_flop):
        possible_pairs = []
        players_cards = self.players_cards[player]
        players_listed_cards = (list(players_cards[0]),list(players_cards[1]))
        player_cards_ranks = (0,0)
        try:
            player_cards_ranks = (self.card_rankings.index(players_listed_cards[0][1]),self.card_rankings.index(players_listed_cards[1][1]))
        except:
            if "1" in players_listed_cards[1] and "0" in players_listed_cards[1] and "1" in players_listed_cards[0] and "0" in players_listed_cards[0]:
                player_cards_ranks = (8,8)
            else:
                if "1" in players_listed_cards[0] and "0" in players_listed_cards[0]:
                    player_cards_ranks = (8, self.card_rankings.index(players_listed_cards[1][1]))
                if "1" in players_listed_cards[1] and "0" in players_listed_cards[1]:
                    player_cards_ranks = (self.card_rankings.index(players_listed_cards[0][1]),8)
        if player_cards_ranks[0] == player_cards_ranks[1]:
            return []
        else:
            player_cards_ranks = (self.card_rankings[player_cards_ranks[0]], self.card_rankings[player_cards_ranks[1]])
            for card in self.cards:
                for rank in player_cards_ranks:
                    if rank in card and card not in possible_pairs and card not in players_cards:
                        if self.cards.index(card)%6 != 0 and not self.cards.index(card) == 0:
                            possible_pairs.append(card)
            return possible_pairs

    def get_missing_cards_to_two_pair(self,player,is_flop):
        possible_pairs = []
        players_cards = self.players_cards[player]
        players_listed_cards = (list(players_cards[0]),list(players_cards[1]))
        player_cards_ranks = (0,0)
        try:
            player_cards_ranks = (self.card_rankings.index(players_listed_cards[0][1]),self.card_rankings.index(players_listed_cards[1][1]))
        except:
            if "1" in players_listed_cards[1] and "0" in players_listed_cards[1] and "1" in players_listed_cards[0] and "0" in players_listed_cards[0]:
                player_cards_ranks = (8,8)
            else:
                if "1" in players_listed_cards[0] and "0" in players_listed_cards[0]:
                    player_cards_ranks = (8, self.card_rankings.index(players_listed_cards[1][1]))
                if "1" in players_listed_cards[1] and "0" in players_listed_cards[1]:
                    player_cards_ranks = (self.card_rankings.index(players_listed_cards[0][1]),8)

        player_cards_ranks = (self.card_rankings[player_cards_ranks[0]], self.card_rankings[player_cards_ranks[1]])
        for card in self.cards:
            for rank in player_cards_ranks:
                if rank in card and card not in possible_pairs and card not in players_cards:
                    if self.cards.index(card)%6 != 0 and not self.cards.index(card) == 0:
                        possible_pairs.append(card)
        return possible_pairs, player_cards_ranks[0] == player_cards_ranks[1]

    def get_missing_cards_to_three_of_a_kind(self,player,is_flop):
        possible_pairs = []
        players_cards = self.players_cards[player]
        players_listed_cards = (list(players_cards[0]),list(players_cards[1]))
        player_cards_ranks = (0,0)
        try:
            player_cards_ranks = (self.card_rankings.index(players_listed_cards[0][1]),self.card_rankings.index(players_listed_cards[1][1]))
        except:
            if "1" in players_listed_cards[1] and "0" in players_listed_cards[1] and "1" in players_listed_cards[0] and "0" in players_listed_cards[0]:
                player_cards_ranks = (8,8)
            else:
                if "1" in players_listed_cards[0] and "0" in players_listed_cards[0]:
                    player_cards_ranks = (8, self.card_rankings.index(players_listed_cards[1][1]))
                if "1" in players_listed_cards[1] and "0" in players_listed_cards[1]:
                    player_cards_ranks = (self.card_rankings.index(players_listed_cards[0][1]),8)

        player_cards_ranks = (self.card_rankings[player_cards_ranks[0]], self.card_rankings[player_cards_ranks[1]])
        for card in self.cards:
            for rank in player_cards_ranks:
                if rank in card and card not in possible_pairs and card not in players_cards:
                    if self.cards.index(card)%6 != 0 and not self.cards.index(card) == 0:
                        possible_pairs.append(card)
        return possible_pairs, player_cards_ranks[0] == player_cards_ranks[1]

    def get_missing_cards_to_four_of_a_kind(self,player,is_flop):
        possible_pairs = []
        players_cards = self.players_cards[player]
        players_listed_cards = (list(players_cards[0]),list(players_cards[1]))
        player_cards_ranks = (0,0)
        try:
            player_cards_ranks = (self.card_rankings.index(players_listed_cards[0][1]),self.card_rankings.index(players_listed_cards[1][1]))
        except:
            if "1" in players_listed_cards[1] and "0" in players_listed_cards[1] and "1" in players_listed_cards[0] and "0" in players_listed_cards[0]:
                player_cards_ranks = (8,8)
            else:
                if "1" in players_listed_cards[0] and "0" in players_listed_cards[0]:
                    player_cards_ranks = (8, self.card_rankings.index(players_listed_cards[1][1]))
                if "1" in players_listed_cards[1] and "0" in players_listed_cards[1]:
                    player_cards_ranks = (self.card_rankings.index(players_listed_cards[0][1]),8)

        player_cards_ranks = (self.card_rankings[player_cards_ranks[0]], self.card_rankings[player_cards_ranks[1]])
        for card in self.cards:
            for rank in player_cards_ranks:
                if rank in card and card not in possible_pairs and card not in players_cards:
                    possible_pairs.append(card)
        return possible_pairs, player_cards_ranks[0] == player_cards_ranks[1]

    def get_missing_cards_to_flush(self,player,is_flop):
        possible_pairs = []
        players_cards = self.players_cards[player]
        players_listed_cards = (list(players_cards[0]),list(players_cards[1]))
        player_cards_color = (0,0)
        player_cards_color = (players_listed_cards[0][0],players_listed_cards[1][0])
        for card in self.cards:
            for rank in player_cards_color:
                if rank in card and card not in possible_pairs and card not in players_cards:
                    if self.cards.index(card)%6 != 0 and not self.cards.index(card) == 0:
                        possible_pairs.append(card)
        return possible_pairs

    def get_missing_cards_to_full_house(self,player,is_flop):
        possible_pairs = []
        players_cards = self.players_cards[player]
        players_listed_cards = (list(players_cards[0]),list(players_cards[1]))
        player_cards_ranks = (0,0)
        try:
            player_cards_ranks = (self.card_rankings.index(players_listed_cards[0][1]),self.card_rankings.index(players_listed_cards[1][1]))
        except:
            if "1" in players_listed_cards[1] and "0" in players_listed_cards[1] and "1" in players_listed_cards[0] and "0" in players_listed_cards[0]:
                player_cards_ranks = (8,8)
            else:
                if "1" in players_listed_cards[0] and "0" in players_listed_cards[0]:
                    player_cards_ranks = (8, self.card_rankings.index(players_listed_cards[1][1]))
                if "1" in players_listed_cards[1] and "0" in players_listed_cards[1]:
                    player_cards_ranks = (self.card_rankings.index(players_listed_cards[0][1]),8)

        player_cards_ranks = (self.card_rankings[player_cards_ranks[0]], self.card_rankings[player_cards_ranks[1]])
        for card in self.cards:
            for rank in player_cards_ranks:
                if rank in card and card not in possible_pairs and card not in players_cards:
                        possible_pairs.append(card)
        return possible_pairs

    def get_missing_cards_to_straightflush(self,player,is_flop):
        possible_straights = []
        players_cards = self.players_cards[player]
        players_listed_cards = (list(players_cards[0]),list(players_cards[1]))
        player_cards_color = (0,0)
        player_cards_color = (players_listed_cards[0][0],players_listed_cards[1][0])
        players_cards = self.players_cards[player]
        players_listed_cards = (list(players_cards[0]),list(players_cards[1]))
        player_cards_ranks = (0,0)
        try:
            player_cards_ranks = (self.card_rankings.index(players_listed_cards[0][1]),self.card_rankings.index(players_listed_cards[1][1]))
        except:
            if "1" in players_listed_cards[1] and "0" in players_listed_cards[1] and "1" in players_listed_cards[0] and "0" in players_listed_cards[0]:
                player_cards_ranks = (8,8)
            else:
                if "1" in players_listed_cards[0] and "0" in players_listed_cards[0]:
                    player_cards_ranks = (8, self.card_rankings.index(players_listed_cards[1][1]))
                if "1" in players_listed_cards[1] and "0" in players_listed_cards[1]:
                    player_cards_ranks = (self.card_rankings.index(players_listed_cards[0][1]),8)

        d = abs(player_cards_ranks[0]-player_cards_ranks[1])
        if d <= 5 and d != 0 and player_cards_color[0] == player_cards_color[1]:
            for x in range(0,2):
                offset = 0
                for i in range(0,5):
                    current_straight = [0,0,0,0,0]
                    current_straight[i] = self.card_rankings[player_cards_ranks[x]]
                    #print("player cards rank index", player_cards_ranks[x], self.card_rankings[player_cards_ranks[x]])
                    for y in range(0,5):
                        if not y == i and player_cards_ranks[x]-offset+y <= len(self.card_rankings)-1 and player_cards_ranks[x]-offset+y >= 0:
                            current_straight[y] = self.card_rankings[player_cards_ranks[x]-offset+y]
                    if len(current_straight) == 5 and 0 not in current_straight:
                        if current_straight not in possible_straights:
                            if is_flop == True and self.card_rankings[player_cards_ranks[0]] in current_straight and self.card_rankings[player_cards_ranks[1]] in current_straight:
                                possible_straights.append(current_straight.copy())
                            else:
                                pass
                    offset += 1

            ps = []
            for liste in possible_straights:
                for rank in liste:
                    ps.append(rank)

            possible_straights = []
            for card in self.cards:
                for rank in ps:
                    if player_cards_color[0] in card or player_cards_color[1] in card:
                        if rank in card and card not in possible_straights and card not in players_cards:
                            if self.cards.index(card)%6 != 0 and not self.cards.index(card) == 0:
                                possible_straights.append(card)
            return possible_straights
        else:
            return False
    
    def get_missing_cards_to_royal_Flush(self,player,is_flop):
        needed_ranks = ["A","K","Q","J","10"]
        possible_straights = []
        players_cards = self.players_cards[player]
        players_listed_cards = (list(players_cards[0]),list(players_cards[1]))
        player_cards_color = (0,0)
        player_cards_color = (players_listed_cards[0][0],players_listed_cards[1][0])
        players_cards = self.players_cards[player]
        players_listed_cards = (list(players_cards[0]),list(players_cards[1]))
        player_cards_ranks = (0,0)
        try:
            player_cards_ranks = (self.card_rankings.index(players_listed_cards[0][1]),self.card_rankings.index(players_listed_cards[1][1]))
        except:
            if "1" in players_listed_cards[1] and "0" in players_listed_cards[1] and "1" in players_listed_cards[0] and "0" in players_listed_cards[0]:
                player_cards_ranks = (8,8)
            else:
                if "1" in players_listed_cards[0] and "0" in players_listed_cards[0]:
                    player_cards_ranks = (8, self.card_rankings.index(players_listed_cards[1][1]))
                if "1" in players_listed_cards[1] and "0" in players_listed_cards[1]:
                    player_cards_ranks = (self.card_rankings.index(players_listed_cards[0][1]),8)
        if player_cards_color[0] == player_cards_color[1] and player_cards_ranks[0] in needed_ranks and player_cards_ranks[1] in needed_ranks:
            for rank in needed_ranks:
                possible_straights.append(f"{player_cards_color[0]}{rank}") 
            return possible_straights
        else:
            return False
                
    def get_most_possible_hand(self,player,is_flop):
        if is_flop:
            best = ["",0]
            x = self.get_missing_cards_to_pair(player,True)
            if not x == []:
                best = ["pair",0.5]

            x,y = self.get_missing_cards_to_two_pair(player,True)
            if y:
                x = len(x)/2
                if x > best[1]:
                    best = ["two_pair",x]
            else:
                x = len(x)/3
                if x > best[1]:
                    best = ["two_pair",x]

            x,y = self.get_missing_cards_to_three_of_a_kind(player,True)
            if y:
                x = len(x)/1
                if x > best[1]:
                    best = ["three_of_a_kind",x]
            else:
                x = len(x)/2
                if x > best[1]:
                    best = ["two_pair",x]

            x = self.get_missing_cards_to_straight(player, True)
            if not x == [] or not x == False:
                x = len(x)/3
                if x > best[1]:
                    best = ["straight",x]
            



            
    def main_loop(self):
        print(self.get_most_possible_hand("player1",True))
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            screen.fill((0,0,0))
            for object in self.objects:
                object.update(screen)
            pygame.display.update()

game = Poker()