from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from src.domain.entities.models import Base,User
from src.infrastructure.config.settings import settings
from sqlalchemy.exc import DatabaseError, IntegrityError, OperationalError

def create_database():
    try:
        engine = create_engine(settings.SERVER_DATABASE_URL)
        # Set AUTOCOMMIT isolation level for database creation
        with engine.connect().execution_options(isolation_level="AUTOCOMMIT") as conn:
            # check if the database already exists
            result = conn.execute(
                text("SELECT 1 FROM pg_database WHERE datname = :dbname"),
                {"dbname": settings.DB_NAME}
            )
            if result.scalar():
                print(f"Database {settings.DB_NAME} already exists.")
            else:
                conn.execute(text(f"CREATE DATABASE \"{settings.DB_NAME}\""))
                print(f"Database {settings.DB_NAME} created successfully.")
        return True
    except (DatabaseError, IntegrityError, OperationalError) as e:
        print(f"Error creating database: {e}")
        return False

def init_table():
    try:
        engine = create_engine(settings.DATABASE_URL)
        Base.metadata.create_all(engine)
        print("Tables created successfully.")
        return engine
    except Exception as e:
        print(f"Error creating tables: {e}")
        return None
    
def init_data():
    try:
        engine = create_engine(settings.DATABASE_URL)
        Session = sessionmaker(bind=engine)
        session = Session()
        
        # Create a new user instance
        if not session.query(User).filter_by(username='admin').first():
            # add a new user
            # new_user = User(
            #     username='admin',
            #     email='sample@gmail.com',
            #     password_hash='hashed_password',
            #     created_at='2023-10-01 12:00:00',
            #     updated_at= None
            # )
            # session.add(new_user)
            # session.commit()
            print("Sample data added successfully.")
        else:
            print("Sample data already exists.")
        session.close()
    except Exception as e:
        print(f"Error adding sample data: {e}")

if __name__ == "__main__":
    if create_database():
        # engine = init_table()
        # if engine:
        #     init_data()
        # else:
        #     print("Failed to initialize tables.")
        print("Database created successfully. You can now run migrations to create tables.")
    else:
        print("Failed to create database.")

