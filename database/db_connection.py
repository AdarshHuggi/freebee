import psycopg2

# database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

class PostgreSQLConnection:
    def __init__(self):
        self.host = "localhost"
        self.port = 5432
        self.database = "postgres"
        self.user = "postgres"
        self.password = "postgres"
        self.connection = None

    def connect(self):
        try:
            self.connection = psycopg2.connect(
                host=self.host,
                port=self.port,
                database=self.database,
                user=self.user,
                password=self.password
            )
            print("Connected to the PostgreSQL database!")
        except Exception as e:
            print(f"Error: Unable to connect to the database - {e}")

    def disconnect(self):
        if self.connection:
            self.connection.close()
            print("Disconnected from the PostgreSQL database.")

    def execute_query(self, query, params=None):
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, params)
            self.connection.commit()
            return cursor.fetchall()
        except Exception as e:
            print(f"Error: Unable to execute query - {e}")
            return None

#*************************************************************#

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/postgres"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

        
Base.metadata.create_all(engine)