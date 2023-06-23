from db_config import Base
from sqlalchemy import Column, Integer, String

class AppUser(Base):

    __tablename__ = "app_user"

    id = Column(Integer, primary_key=True, autoincrement=True)
    full_name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    password = Column(String(100), nullable=False)

