from os import getenv

import psycopg2
from dotenv import load_dotenv

load_dotenv()


def main():
    db_url = getenv("DB_URL")

    with psycopg2.connect(db_url) as conn:
        print("Connected to PostgreSQL database.")
        cursor = conn.cursor()
        query = "CREATE TYPE accesslevel AS ENUM ('GUEST', 'USER', 'ADMIN');"

        try:
            cursor.execute(query)
            conn.commit()
            print("Created enum type accesslevel.")
        except (Exception, psycopg2.DatabaseError) as error:
            print(f"Error: {error}")


if __name__ == "__main__":
    main()
