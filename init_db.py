from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from models.models import Base,User
from sqlalchemy.exc import DatabaseError, IntegrityError, OperationalError


BASE_DATABASE_URL = "postgresql://postgres:123456@localhost:5432"
DATABASE_NAME = "MigrationTest"
DATABASE_URL = f'{BASE_DATABASE_URL}/{DATABASE_NAME}'
def create_database():
    try:
        engine = create_engine(BASE_DATABASE_URL)
        # Set AUTOCOMMIT isolation level for database creation
        with engine.connect().execution_options(isolation_level="AUTOCOMMIT") as conn:
            # check if the database already exists
            result = conn.execute(
                text("SELECT 1 FROM pg_database WHERE datname = :dbname"),
                {"dbname": DATABASE_NAME}
            )
            if result.scalar():
                print(f"Database {DATABASE_NAME} already exists.")
            else:
                conn.execute(text(f"CREATE DATABASE \"{DATABASE_NAME}\""))
                print(f"Database {DATABASE_NAME} created successfully.")
        return True
    except (DatabaseError, IntegrityError, OperationalError) as e:
        print(f"Error creating database: {e}")
        return False

def init_table():
    try:
        engine = create_engine(DATABASE_URL)
        Base.metadata.create_all(engine)
        print("Tables created successfully.")
        return engine
    except Exception as e:
        print(f"Error creating tables: {e}")
        return None
    
def init_data():
    try:
        engine = create_engine(DATABASE_URL)
        Session = sessionmaker(bind=engine)
        session = Session()
        
        # Create a new user instance
        if not session.query(User).filter_by(username='admin').first():
            # add a new user
            new_user = User(
                username='admin',
                email='sample@gmail.com',
                password_hash='hashed_password',
                created_at='2023-10-01 12:00:00',
                updated_at= None
            )
            session.add(new_user)
            session.commit()
            print("Sample data added successfully.")
        else:
            print("Sample data already exists.")
        session.close()
    except Exception as e:
        print(f"Error adding sample data: {e}")

if __name__ == "__main__":
    if create_database():
        engine = init_table()
        if engine:
            init_data()
        else:
            print("Failed to initialize tables.")
    else:
        print("Failed to create database.")

