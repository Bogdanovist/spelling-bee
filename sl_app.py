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
        insert(Word).
        values(word=word,
            level = level).
        returning(Word.word)
    )
    try:
        word_id = commit_sql(stmt).first()[0]
        #st.write(word_id)
    except Exception as e:
        st.exception(e)
        st.error(f"word {word} already exists")
        return

    stmt = (
        insert(Question).
        values(word_id=word_id, 
               result=result)
    )
    ret = commit_sql(stmt)

    st.session_state['db_update'] = f"{word} {level} success!"

st.title('Spelling Bee Tester')

with st.sidebar:
    level = st.selectbox("Level selector", [1,2,3,4,5,6], index=0)

word = st.text_input("word")

correct = st.button("Correct", key='correct', help=None, on_click=record_guess, args=('correct',))
tricky = st.button("Tricky", key='tricky', help=None, on_click=record_guess, args=('tricky',))
wrong = st.button("Wrong", key='wrong', help=None, on_click=record_guess, args=('wrong',))

if "db_update" in st.session_state:
    st.success(st.session_state['db_update'])