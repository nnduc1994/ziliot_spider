__author__ = 'nnduc_000'

from sqlalchemy.orm import sessionmaker
from models import JobData, db_connect, create_table, JobData_Estonia

# Pipeline for Finland Job
class JobDataPipeLine(object):
    def __init__(self):
        engine = db_connect()
        create_table(engine)
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):
        session = self.Session()
        jobdata = JobData(**item)

        try:
            session.add(jobdata)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()
        return item


# Pipeline for Estonia Job
class JobDataEstoniaPipeLine(object):
    def __init__(self):
        engine = db_connect()
        create_table(engine)
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):
        session = self.Session()
        jobdata = JobData_Estonia(**item)

        try:
            session.add(jobdata)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()
        return item