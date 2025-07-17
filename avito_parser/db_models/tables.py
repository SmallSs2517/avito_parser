from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship, DeclarativeBase, mapped_column, Mapped
from datetime import datetime
from typing import List


class Base(DeclarativeBase): 
    pass


class FollowModels(Base):
    __tablename__ = 'follow_models'

    id: Mapped[int] = mapped_column(primary_key=True)
    on_create: Mapped[datetime] = mapped_column(default=datetime.now)
    category: Mapped[str]
    region: Mapped[str]
    brand: Mapped[str]
    model: Mapped[str]
    generation: Mapped[str]
    code: Mapped[str]
    radius: Mapped[str]
    follow: Mapped[bool] = mapped_column(default=True)
    avg_prices: Mapped[List["AveragePrices"]] = relationship(back_populates='model')

    def __init__(self, model: dict):
        self.category = model['CATEGORY']
        self.region = model['REGION']
        self.brand = model['BRAND']
        self.model = model['MODEL']
        self.generation = model['GENERATION']
        self.code = model['CODE']
        self.radius = model['RADIUS']

    def __repr__(self):
        info: str = f'Регион: {self.region},\nМарка: {self.brand},\n' \
            f'Модель: {self.model},\nПоколение: {self.generation}'
        return info


class AveragePrices(Base):
    __tablename__ = 'average_prices'

    id: Mapped[int] = mapped_column(primary_key=True)
    on_create: Mapped[datetime] = mapped_column(default=datetime.now)
    offers: Mapped[int]
    average_price: Mapped[int]
    model_id = mapped_column(ForeignKey("follow_models.id"))

    model: Mapped[FollowModels] = relationship(back_populates="avg_prices")

    def __init__(self, offers: int, average_price: int, model_id: int):
        self.offers = offers
        self.average_price = average_price
        self.model_id = model_id

    def __repr__(self):
        info: str = f'ID: {self.id},\nДата: {self.on_create.isoformat(sep=' ', timespec='minutes')},\nМодель ID: {self.model_id},\nЦена: {self.average_price}'

        return info


# class AllPrices(Base):
#     __tablename__ = 'all_prices'

#     id = Column(Integer, primary_key=True)
#     date = Column(DateTime, default=datetime.now)
#     price = Column(Integer)
#     follow_models_id = Column(Integer, ForeignKey('follow_models.id'))

#     def __init__(self, price: int, follow_models_id: int):
#         self.price = price
#         self.follow_models_id = follow_models_id

#     def __repr__(self):
#         info: dict = {'date': self.date,
#                       'model_id': self.follow_models_id,
#                       'price': self.price}
#         return info


