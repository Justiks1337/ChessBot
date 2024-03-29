import asyncpg

from config.ConfigValues import ConfigValues


class Connection:

    connection: asyncpg.Connection

    def __new__(cls, *args, **kwargs):
        it = cls.__dict__.get("__it__")
        if it is not None:
            return it
        cls.__it__ = it = object.__new__(cls)
        return it

    @classmethod
    async def connect(cls):
        cls.connection = await asyncpg.connect(
            database=ConfigValues.database_name,
            host=ConfigValues.database_host,
            port=ConfigValues.database_port,
            user=ConfigValues.database_user,
            password=ConfigValues.database_password
        )

        await cls.connection.execute("""CREATE TABLE IF NOT EXISTS "blacklist" (
            "user_id"	INTEGER NOT NULL,
            "username"	TEXT NOT NULL,
            FOREIGN KEY("user_id") REFERENCES "users"("user_id")
        )""")
