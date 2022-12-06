from typing import Any
import datetime
import psycopg2
from psycopg2 import Error
from psycopg2.extensions import (
    connection as Connection,
    cursor as Cursor
)

from config import (
    HOST,
    DATABASE,
    PASSWORD,
    PORT,
    USER,
)


class Connection:
    """Class for working to DataBase"""
    
    def get_time(self):
        return datetime.datetime.now()

    def __init__(self) -> None:
        try:
            self.connection: Connection = psycopg2.connect(
                user=USER,
                host=HOST,
                port=PORT,
                password=PASSWORD,
                dbname=DATABASE
            )
            print(f"{self.get_time()} [INFO] Connection is successful")
        except (Exception, Error) as e:
            print("{0} [ERROR] Connection to database is bad: {1}".format(
                datetime.datetime.now(),
                e
            ))

    def __new__(cls: type[Any]) -> Any:
        if not hasattr(cls, 'instance'):
            cls.instance = super(Connection, cls).__new__(cls)

        return cls.instance

    def get_genre_list(self) -> list[dict]:
        data: list[dict] = []
        
        with self.connection.cursor() as cur:
            cur.execute("""
                SELECT id, title  FROM genres;
            """)

            rows = cur.fetchall()
            
            for row in rows:
                g = {}

                g['id'] = row[0]
                g['title'] = row[1]
                
                data.append(g)

        return data  

    def get_platform_list(self) -> list[dict]:
        data: list[dict] = []
        
        with self.connection.cursor() as cur:
            cur.execute("""
                SELECT id, title  FROM platforms;
            """)

            rows = cur.fetchall()
            
            for row in rows:
                g = {}

                g['id'] = row[0]
                g['title'] = row[1]
                
                data.append(g)

        return data  

    def get_publisher_list(self) -> list[dict]:
        data: list[dict] = []
        
        with self.connection.cursor() as cur:
            cur.execute("""
                SELECT id, title  FROM publishers;
            """)

            rows = cur.fetchall()
            
            for row in rows:
                g = {}

                g['id'] = row[0]
                g['title'] = row[1]
                
                data.append(g)

        return data                
    
    def get_language_list(self) -> list[dict]:
        data: list[dict] = []
        
        with self.connection.cursor() as cur:
            cur.execute("""
                SELECT id, title  FROM languages;
            """)

            rows = cur.fetchall()
            
            for row in rows:
                g = {}

                g['id'] = row[0]
                g['title'] = row[1]
                
                data.append(g)

        return data  

    def get_games_list(self) -> list[dict]:
        data: list[dict] = []
        with self.connection.cursor() as cur:
            cur.execute("""
                SELECT g.id, g.title, g.description, g.cost, g.image_path, g.release_date, publishers.title, languages.title  
                FROM games AS g
                INNER JOIN publishers ON publishers.id = g.publisher_id
                INNER JOIN languages ON languages.id = g.language_id
            """)
            rows = cur.fetchall()
            for row in rows:
                g = {}

                g['id'] = row[0]
                g['title'] = row[1]
                g['description'] = row[2]
                g['cost'] = row[3]
                g['image_path'] = row[4]
                g['release_date'] = row[5]
                g['publisher'] = row[6]
                g['language'] = row[7]

                with self.connection.cursor() as cur:
                    cur.execute("""
                        SELECT genres.title FROM game_genre AS t 
                        INNER JOIN genres ON genres.id = t.genre_id
                        WHERE t.game_id = %s
                    """, (g['id'], ))   
                    g['genres'] = cur.fetchall()

                with self.connection.cursor() as cur:
                    cur.execute("""
                        SELECT platforms.title FROM game_platform AS t
                        INNER JOIN platforms ON platforms.id = t.platform_id
                        WHERE t.game_id = %s
                    """, (g['id'], ))   
                    g['platforms'] = cur.fetchall()

                data.append(g)         

        return data

    def save_game(self, g: dict) -> None:
        if g['id']:
            with self.connection.cursor() as cur:
                cur.execute("""
                    UPDATE games SET
                        title = %s,
                        description = %s,
                        cost = %s,
                        image_path = %s,
                        release_date = %s,
                        publisher_id = %s,
                        language_id = %s
                    WHERE id = %s
                """, (
                    g['title'], 
                    g['description'], 
                    g['cost'], 
                    g['image_path'], 
                    g['release_date'], 
                    g['publisher_id'], 
                    g['language_id'], 
                    g['id']
                ))
        else:
            with self.connection.cursor() as cur:
                cur.execute("""
                    INSERT INTO games(title, description, cost, image_path, release_date, publisher_id, language_id)
                    VALUES(%s, %s, %s, %s, %s, %s, %s)
                    RETURNING id
                """, (
                    g['title'], 
                    g['description'], 
                    g['cost'], 
                    g['image_path'], 
                    g['release_date'],
                    g['publisher_id'],
                    g['language_id']
                ))

                g['id'] = cur.fetchone()[0]
        
        self.connection.commit()

        with self.connection.cursor() as cur:
            cur.execute("""
                DELETE FROM game_genre WHERE game_id = %s
            """, (g['id'], ))    

        self.connection.commit()

        with self.connection.cursor() as cur:
            for item in g['genres']:
                cur.execute("""
                    INSERT INTO game_genre(game_id, genre_id) VALUES(%s, %s)
                """, (g['id'], item))

        self.connection.commit()

        with self.connection.cursor() as cur:
            cur.execute("""
                DELETE FROM game_platform WHERE game_id = %s
            """, (g['id'], ))    

        self.connection.commit()

        with self.connection.cursor() as cur:
            for item in g['platforms']:
                cur.execute("""
                    INSERT INTO game_platform(game_id, platform_id) VALUES(%s, %s)
                """, (g['id'], item))
        
        self.connection.commit()