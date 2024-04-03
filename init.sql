CREATE TABLE IF NOT EXISTS "users" (
			"user_id"	BIGINT NOT NULL UNIQUE,
			"games"	INTEGER,
			"points"	INTEGER,
			"nickname"	TEXT,
			"username"	TEXT,
			"session_id"	TEXT,
			"ip_address"	TEXT,
			PRIMARY KEY("user_id"));

CREATE TABLE IF NOT EXISTS "games" (
    "first_player"	BIGINT NOT NULL,
    "second_player"	BIGINT NOT NULL,
    "winner" BIGINT NOT NULL,
    FOREIGN KEY("second_player") REFERENCES "users"("user_id"),
    FOREIGN KEY("winner") REFERENCES "users"("user_id"),
    FOREIGN KEY("first_player") REFERENCES "users"("user_id"));


CREATE TABLE IF NOT EXISTS "blacklist" (
			"user_id"	BIGINT NOT NULL,
			"username"	TEXT NOT NULL,
			FOREIGN KEY("user_id") REFERENCES "users"("user_id"));
