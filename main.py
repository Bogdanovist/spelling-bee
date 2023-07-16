from db.session import engine
from models import Word, Student, Question
from sqlalchemy import select

def get_all_students():
    pd.read_sql('user',app_events_engine).set_index('user_id')
    stmt = select(Student)
    ret = engine.execute(stmt)
    return ret

if __name__ == '__main__':

    print(get_all_students())