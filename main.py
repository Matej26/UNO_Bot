from Game import Game
from Player import Player


if __name__ == "__main__":
    player = Player('Matej')
    print('My token: ', player.get_token())
    opp = input('Input UID of your opponent: ')
    game = Game(player, opp)
    game.start()

    while True:
        # get a current board
        player.clear_hand()
        game.get_board()
        curr_card = game.current_card
        curr_color = game.current_color

        if player.move:
            # check current game status
            if game.status == 1:
                print('Congrats! You win!')
                break
            if game.status == 2:
                print('Not today :(')
                break

            # log current game situation
            print('Hand: ')
            print(player.print_hand())
            print('--------------------------------------')
            print('Current card: ', curr_card)
            print('--------------------------------------')
            print('Current color: ', curr_color)
            print('--------------------------------------')

            # make a move
            game.send_cards()