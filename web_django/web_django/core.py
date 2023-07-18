from database_tools.Connection import connect


async def get_data(session_id: str) -> dict:

    database_data = await (
        await connect.request("SELECT user_id, games, points, nickname, username FROM users WHERE session_id = ?",
                              (session_id, ))
    ).fetchone()

    cleaned_data = {"user_id": database_data[0],
                    "games": database_data[1],
                    "points": database_data[2],
                    "nickname": database_data[3],
                    "username": database_data[4]}

    return cleaned_data
