CREATE TABLE IF NOT EXISTS "users" (
			"user_id"	BIGINT NOT NULL UNIQUE,
			"games"	INTEGER,
			"points"	INTEGER,
			"nickname"	TEXT,
			"username"	TEXT,
			"session_id"	TEXT,
			"ip_address"	TEXT,
			PRIMARY KEY("user_id"));

CREATE TABLE IF NOT EXISTS "blacklist" (
			"user_id"	BIGINT NOT NULL,
			"username"	TEXT NOT NULL,
			FOREIGN KEY("user_id") REFERENCES "users"("user_id"));
