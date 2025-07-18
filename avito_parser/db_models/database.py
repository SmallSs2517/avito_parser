from sqlalchemy import create_engine, select, update, delete
from sqlalchemy.orm import sessionmaker
from db_models.tables import FollowModels, AveragePrices, Base

DB_NAME = 'database.sqlite'
sync_engine = create_engine(f'sqlite:///avito_parser/src/{DB_NAME}', echo=True)
SessionDB = sessionmaker(bind=sync_engine)


class SyncORM:
    
    @staticmethod
    def create_tables(echo: bool = True, drop: bool = False):
        sync_engine.echo = echo
        if drop:
            Base.metadata.drop_all(sync_engine)

        Base.metadata.create_all(sync_engine)
    
    @staticmethod
    def insert_model(model: dict):
        with SessionDB() as session:
            session.add(FollowModels(model=model))
            session.commit()

    @staticmethod
    def insert_average_price(offers: int, average_price: int, model_id: int):
        with SessionDB() as session:
            session.add(AveragePrices(offers, average_price, model_id))
            session.commit()

    @staticmethod
    def select_last_average_price(model_id: int=1) -> str:
        stmt = select(AveragePrices).where(AveragePrices.model_id == model_id).order_by(AveragePrices.id.desc()).limit(1)
        with SessionDB() as session:
            res = session.scalar(stmt)
            result = res.__repr__()
        return result
    
    @staticmethod
    def select_all_average_prices(model_id: int=1) -> str:
        stmt = select(AveragePrices).where(AveragePrices.model_id == model_id)
        with SessionDB() as session:
            res = session.scalars(stmt)
            result = []
            for i in res:
                result.append(i.__repr__())
            result = '\n'.join(result)
        return result

    @staticmethod
    def select_all_models() -> list[dict]:
        stmt = select(FollowModels).where(FollowModels.follow == True)
        result = []

        with SessionDB() as session:
            res = session.scalars(stmt).all()
            for i in res:
                model = {'REGION': '/' + i.region,
                         'CATEGORY': '/' + i.category,
                         'BRAND': '/' + i.brand,
                         'MODEL': '/' + i.model,
                         'GENERATION': '/' + i.generation,
                         'COOKIE': i.code,
                         'RADIUS': i.radius,
                         }
                result.append(model)
        
        return result
    
    @staticmethod
    def delete_by_pk(model: Base, pk: int):
        stmt = delete(model).where(model.id == pk)
        with SessionDB() as session:
            obj = session.execute(stmt)
            session.commit()
