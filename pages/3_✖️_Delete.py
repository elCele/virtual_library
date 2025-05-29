import streamlit as st
import pandas as pd
import sqlite3
import os
from utils import logout as lg

st.set_page_config("Add", "✖️", "wide")

if not st.session_state.get("logged_in"):
    st.error("Log in required")
    st.stop()

DB_PATH = st.session_state.dbPath
st.session_state.conn = sqlite3.connect(DB_PATH)

books = pd.read_sql("SELECT * FROM books;", st.session_state.conn)
nBooks = len(books)

st.title("✖️ :red[Delete] a book")

st.dataframe(books, use_container_width = True)

lineToDel = st.number_input(label = "Line selector", min_value = 0, max_value = nBooks - 1 if nBooks != 0 else 0, step = 1)
delButton = st.button(label = "Delete", use_container_width = True)

if delButton:
    title = books.values[lineToDel][1]

    cursor = st.session_state.conn.cursor()

    try:
        cursor.execute(f"DELETE FROM books WHERE title = '{title}'")
        st.success("Row eliminated!", icon ="✅")

        st.session_state.conn.commit()

        st.session_state.conn.close()

        st.rerun()

    except Exception as e:
        st.error(f"Could not proceed wiht the elimination: {e}", icon = "🚨")

if st.session_state.get("logged_in"):
    st.sidebar.button("Log out", on_click = lg, use_container_width = True)