import streamlit as st
from dotenv import load_dotenv
import os
import sqlite3
import pandas as pd
from utils import logout as lg

st.set_page_config("Login", "🔑", "wide")

st.title("🔑 Login")

if "logged_in" not in st.session_state.keys():
    st.session_state.logged_in = False

if "wantToRegister" not in st.session_state.keys():
    st.session_state.wantToRegister = False

if "dbPath" not in st.session_state.keys():
    st.session_state.dbPath = ""

DB_PATH = os.path.abspath("files/users.db")
conn = sqlite3.connect(DB_PATH)

users = pd.read_sql(f"SELECT * FROM user;", conn)

user = st.text_input("Username")
pwd = st.text_input("Password", type = "password")

col1, col2, col3 = st.columns(3)

with col2:
    if st.button("Log in", type = "primary", use_container_width = True):
        if user in users['username'].values:
            if pwd == pd.read_sql(f"SELECT password FROM user WHERE username LIKE '{user}'", conn).values[0]:
                st.session_state.logged_in = True
                st.success(f"Ben tornato {user}!")

                st.session_state.dbPath = f"files/{user}.db"
                print(st.session_state.dbPath)

                st.switch_page("pages/1_🔍️_Search.py")
            else:
                st.error("Credenziali non valide")

        else:
            st.warning("Sorry for the inconvenience, you are not registered. We'll implement the register function soon!", icon = "💡")

with col2:
    if not st.session_state.logged_in:
        if st.button("Register", type = "secondary", use_container_width = True):
            st.session_state.wantToRegister = True

if st.session_state.get("logged_in"):
    st.sidebar.button("Log out", on_click = lg, use_container_width = True)

if st.session_state.wantToRegister:
    with st.form("register"):
        user = st.text_input("Username*")
        pwd = st.text_input("Password*", type = "password")
        repeatPwd = st.text_input("Repeat password*", type = "password")

        submitted = st.form_submit_button("Submit")

        if submitted:
            errors = []

            if pwd != repeatPwd:
                errors.append("The passwords don't match")

            if user == "" or pwd == "":
                errors.append("Fill the necessary fields")

            if errors:
                for err in errors:
                    st.error(err, icon = "🚨")
            else:
                new_user = pd.DataFrame([{
                    "username": user,
                    "password": pwd
                }])

                try:
                    new_user.to_sql("user", conn, if_exists = "append", index = False)
                    st.success("Succesfully registered!", icon = "✅")

                    newDB_path = f"files/{user}.db"

                    conn.close()

                    with open(newDB_path, 'w') as f:
                        pass

                    try:
                        conn = sqlite3.connect(newDB_path)

                        cursor = conn.cursor()

                        cursor.execute("CREATE TABLE BOOKS (isbn VARCHAR(17) NOT NULL, title TEXT NOT NULL, author TEXT NOT NULL, beenRead BOOLEAN NOT NULL, rating INTEGER, posX INTEGER, posY INTEGER, ph_name TEXT NOT NULL, PRIMARY KEY (isbn));")
                    
                        st.session_state.dbPath = newDB_path
                    except Exception as x:
                        st.error(x)
                except Exception as e:
                    st.warning(f"Username already in use.", icon = "💡")
