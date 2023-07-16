from models import Base
from db.session import engine
import pandas as pd

if __name__ == '__main__':

   #word = pd.read_sql(engine, 'word')
   #print(word)
   word = pd.read_sql_table('word',engine)
   word.to_csv('data/word_backup.csv',index=False)

   qs = pd.read_sql_table('question',engine)
   qs.to_csv('data/question_backup.csv',index=False)   
