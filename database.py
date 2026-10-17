from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

sqlalchemy_data_url = 'sqlite:///./Todosapp.db'

engine = create_engine( sqlalchemy_data_url, connect_args={'check_same_thread': False})

Sessionlocal = sessionmaker(
    autoflush=False,
    autocommit=False,
    bind=engine  # Fixed: bine -> bind
)

Base = declarative_base()



# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# from sqlalchemy.ext.declarative import declarative_base

# sqlalchemy_data_url = 'postgresql://postgres:password@localhost/database_name'

# engine = create_engine( sqlalchemy_data_url)

# Sessionlocal = sessionmaker(
#     autoflush=False,
#     autocommit=False,
#     bind=engine  # Fixed: bine -> bind
# )

# Base = declarative_base()

# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# from sqlalchemy.ext.declarative import declarative_base

# sqlalchemy_data_url = 'mysql+pymysql://root:password@127.0.0.1:3306/Todosapp.db'

# engine = create_engine( sqlalchemy_data_url, connect_args={'check_same_thread': False})

# Sessionlocal = sessionmaker(
#     autoflush=False,
#     autocommit=False,
#     bind=engine  # Fixed: bine -> bind
# )

# Base = declarative_base()