# from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
# from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
# from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, Float
#
# engine = create_async_engine("postgresql+asyncpg://postgres:nikitatnm2@localhost/films")
# async_session = async_sessionmaker(engine, expire_on_commit=False)
#
# class Base(DeclarativeBase):
#     pass
#
# class Users(Base):
#     __tablename__ = 'users'
#
#     id = Column(Integer, primary_key=True, index=True)
#     full_name = Column(String, index=True)
#     username = Column(String, index=True)
#     calorie_allowance = Column(Float)
#     your_calorie = Column(Float)
#     income = Column(Integer)
#     expenses = Column(Integer)


