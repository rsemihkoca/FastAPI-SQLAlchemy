from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.inspection import inspect

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:postgres@localhost/Local"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# secret ve database.ini bak
# postgre bağlandı yazısı
# tekrarlayan user internal server error 'u except ile yakalamak


#Dependency for database: Create a new session for each request and close it after the request is completed
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

def table_exists(name):
    ins = inspect(engine)
    ret = ins.dialect.has_table(engine.connect(),name)
    return ret


"""#Database connection
while True:
    try:
        connection = psycopg2.connect(user = "postgres",
                                    password = "8520",
                                    host = 'localhost',
                                    database= 'db',
                                    port = '5432',s
                                    cursor_factory=RealDictCursor
                                    )
        cursor = connection.cursor()
        print(f"\033[92mPostgreSQL connection is successful \033[0m")
        break
    except (Exception, psycopg2.Error) as error:
        print(f"\033[91mError while connecting to PostgreSQL\n{error}\033[0m")
        time.sleep(3)"""