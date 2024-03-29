CREATE TABLE IF NOT EXISTS "blacklist" (
			"user_id"	INTEGER NOT NULL,
			"username"	TEXT NOT NULL,
			FOREIGN KEY("user_id") REFERENCES "users"("user_id"));
