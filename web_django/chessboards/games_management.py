from Game import Game


def game_start(first_user_id: int, second_user_id: int):

    game = Game((first_user_id, second_user_id))

    return game.tag
