import asyncpg

from config.ConfigValues import ConfigValues


class Connection:

    def __new__(cls, *args, **kwargs):
        it = cls.__dict__.get("__it__")
        if it is not None:
            return it
        cls.__it__ = it = object.__new__(cls)
        return it

    async def connect(self):
        self.connection = await asyncpg.connect(
            host=ConfigValues.database_host,
            port=ConfigValues.database_port,
            user=ConfigValues.database_user,
            password=ConfigValues.database_password,
            database=ConfigValues.database_name
        )

        await self.connection.execute("""CREATE TABLE IF NOT EXISTS "blacklist" (
            "user_id"	INTEGER NOT NULL,
            "username"	TEXT NOT NULL,
            FOREIGN KEY("user_id") REFERENCES "users"("user_id")
        )""")
