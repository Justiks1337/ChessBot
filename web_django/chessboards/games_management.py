from asyncio import get_running_loop
from Game import Game


async def game_start(first_user_id: int, second_user_id: int):

    game = Game((first_user_id, second_user_id))

    loop = get_running_loop()

    loop.create_task(game.start_timers_game())

    return game.tag


def get_event_loop():

    global main_loop

    if not main_loop:
        main_loop = get_running_loop()

    return main_loop


main_loop = None
