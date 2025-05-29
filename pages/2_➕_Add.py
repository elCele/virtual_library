import streamlit as st
import pandas as pd
import sqlite3
import re
import os
from utils import logout as lg, search_book

st.set_page_config("Add", "➕", "wide")

'''if not st.session_state.get("logged_in"):
    st.error("Log in required")
    st.stop()'''

st.title("➕ :green[Add] a book")

DB_PATH = st.session_state.dbPath
st.session_state.conn = sqlite3.connect(DB_PATH)

st.text_input(label = "Title*", key = "title")

if st.button("Search book", use_container_width = True):
    titolo = st.session_state.get("title", "").strip()

    if titolo:
        try:
            info = search_book(titolo)
            st.session_state["isbn"] = info.get("ISBN", "")
            st.session_state["author"] = info.get("author", "")
            st.session_state["ph_name"] = info.get("publishing house", "")
            st.success("Book found!")
        except Exception as e:
            st.warning(f"Sorry, there's been an error:: {e}")

with st.form("add", border = False):
    st.text_input("ISBN*", placeholder = "▮▮▮-▮▮-▮▮-▮▮▮▮▮-▮", key = "isbn")
    st.text_input("Author*", placeholder = "Name surname", key = "author")
    read_option = st.radio("Read", ["Read", "Not read"], horizontal = True  )
    rating = st.number_input("Rating", min_value = -1, max_value = 10, step = 1)
    posX = st.number_input("X position", min_value = -1, max_value = 4, step = 1)
    posY = st.number_input("Y position", min_value = -1, max_value = 4, step = 1)
    st.text_input("Publishing house*", key="ph_name")

    submitted = st.form_submit_button("Submit")

    if submitted:
        errors = []

        isbn = st.session_state.get("isbn", "")
        title = st.session_state.get("title", "")
        author = st.session_state.get("author", "")
        ph_name = st.session_state.get("ph_name", "")

        if not isbn.strip():
            errors.append("ISBN field is mandatory.")
        elif not re.match(r"^\d{3}-\d{2}-\d{2}-\d{5}-\d{1}$", isbn):
            errors.append("ISBN non valid. Usa: ▮▮▮-▮▮-▮▮-▮▮▮▮▮-▮")

        if not title.strip():
            errors.append("Title field is mandatory.")
        if not author.strip():
            errors.append("Author field is mandatory.")
        if not ph_name.strip():
            errors.append("Publishing house field is mandatory.")

        if rating == -1:
            rating = "NULL"

        if posX == -1 or posY == -1:
            posX = "NULL"
            posY = "NULL"

        if read_option == "Read":
            beenRead = True
        else:
            beenRead = False

        isbn = str(isbn)

        if errors:
            for err in errors:
                st.error(err, icon="🚨")
        else:
            try:
                cursor = st.session_state.conn.cursor()

                cursor.execute(f"insert into books (isbn, title, author, beenRead, rating, posX, posY, ph_name) values ('{isbn}', '{title}', '{author}', {beenRead}, {rating}, {posX}, {posY}, '{ph_name}');")

                st.success("Libro aggiunto con successo!", icon = "✅")

                st.session_state.conn.commit()

                st.session_state.conn.close()
            except Exception as e:
                st.error(f"Book already in the database", icon = "🚨")

if st.session_state.get("logged_in"):
    st.sidebar.button("Log out", on_click = lg, use_container_width = True)
