from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP,text
from app.database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    at_sale = Column(Boolean, server_default=text('false'))
    inventory = Column(Integer,server_default=text('0'), nullable=False)
    added_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))