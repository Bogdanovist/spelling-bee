import streamlit as st
import pandas as pd
import numpy as np
from sqlalchemy import insert
from models import Question, Word
from db.session import engine
from psycopg2.errors import IntegrityError

def commit_sql(stmt):
    with engine.connect() as conn:
        ret = conn.execute(stmt)
        conn.commit()
    
    return ret

def record_guess(result):

    stmt = (
        insert(Question).
        values(word_id=next_word, 
               result=result)
    )
    ret = commit_sql(stmt)

    st.session_state['db_update'] = f"{next_word} success!"

def get_next_word():
   # can use state to speed this up...

   word = pd.read_sql_table('word',engine)
   qs = pd.read_sql_table('question',engine)
   new_words = list(set(word.word).difference(set(qs.word_id)))

   if len(new_words) == 0:
       st.error("No more new words!")
       st.stop()
   else:
       new_word = new_words[0]
       st.write(f"{len(new_words)} words remaining")
       return new_word
       

st.title('Spelling Bee Tester')

next_word = get_next_word()
word = st.header(next_word)

correct = st.button("Correct", key='correct', help=None, on_click=record_guess, args=('correct',))
tricky = st.button("Tricky", key='tricky', help=None, on_click=record_guess, args=('tricky',))
wrong = st.button("Wrong", key='wrong', help=None, on_click=record_guess, args=('wrong',))

if "db_update" in st.session_state:
    st.success(st.session_state['db_update'])