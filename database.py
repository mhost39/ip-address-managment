from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import IntegrityError
import os

from helper import int_to_ip


engine = create_engine(f'sqlite:////{os.getcwd()}/ipam.db', convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()

class DataBase:

    def __init__(self):
        import models   # import tables from models 
        Base.metadata.create_all(bind=engine)

    def insert_data(self, tablename, **kwargs):
        """ insert to table, if fail return error, if success returns id of the created object """
        try:
            data = tablename(**kwargs)
            db_session.add(data)
            db_session.commit()
        except ValueError as e:
            return "Error while adding data: " + str(e)
        except TypeError as e:
            return "Error while adding data: " + str(e)
        except IntegrityError as e:
            db_session.rollback()
            return "Error while adding data: " + str(e.orig.message) + str(e.params)
        return data.id


    def delete_data(self, tablename, **kwargs):
        """ Delete data from a table, if fail return error, if success return True """
        try:
            data = tablename.query.filter_by(**kwargs).first()
            if data:
                db_session.delete(data)
                db_session.commit()
            else:
                return "data not found"
        except ValueError as e:
            return "Error while deleting data: " + str(e)
        except TypeError as e:
            return "Error while deleting data: " + str(e) 
        except IntegrityError as e:
            db_session.rollback()
            return "Error while deleting data: " + str(e.orig.message) + str(e.params)
        return True


    def select_all(self, tablename):
        data = list()
        data_lit = dict()

        for d in tablename.query.all():
            for value in vars(d):
                if value != '_sa_instance_state':
                    data_lit[value] = vars(d)[value]
                if value == 'ip' and tablename.__tablename__ == 'subnet':
                    data_lit[value] = int_to_ip(vars(d)[value]) + "/" + str(vars(d)['mask'])

            data.append(data_lit)
            data_lit = dict()
        return data


    def select_by_id(self, tablename, **kwargs):
        data_list = dict()
        data = tablename.query.filter_by(**kwargs).first()
        for value in vars(data):
            if value != '_sa_instance_state':
                data_list[value] = vars(data)[value]
            # if value == 'ip' and tablename.__tablename__ == 'subnet':
            #         data_list[value] = int_to_ip(vars(data)[value]) + "/" + str(vars(data)['mask'])
        return data_list

    def update_by_id(self, tablename, id, **kwargs ):
        try:
            num_rows_updated = tablename.query.filter_by(id=id).update(dict(**kwargs))
            db_session.commit()
        except ValueError as e:
            return "Error while updateing: " + str(e)
        except TypeError as e:
            return "Error while updateing: " + str(e)
        except IntegrityError as e:
            db_session.rollback()
            return "Error while updateing: " + str(e.orig.message) + str(e.params)
        return num_rows_updated
