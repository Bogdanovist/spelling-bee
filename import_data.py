from db.session import engine
import pandas as pd
from sqlalchemy import insert
from models import Word

def commit_sql(stmt):
    with engine.connect() as conn:
        ret = conn.execute(stmt)
        conn.commit()
    
    return ret

if __name__ == '__main__':
    
    words = pd.read_csv('data/import_words.csv')

    for indx, row in words.iterrows():
        stmt = (
                insert(Word).
                values(word=row.word,
                    level = row.level).
                returning(Word.word)
            )
        try:
            word_id = commit_sql(stmt).first()[0]
            print(word_id)
        except Exception as e:
            continue
