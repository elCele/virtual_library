import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
from utils import logout as lg, toggleFilter

st.set_page_config(
    "Virtual library",
    "🔍️",
    "wide"
)

conditions = []
attributes = []

'''if not st.session_state.get("logged_in"):
    st.error("Log in required")
    st.stop()'''

if "showFilter" not in st.session_state.keys():
    st.session_state.showFilter = False

st.title("🔍️ :orange[Search] your book")

DB_PATH = st.session_state.dbPath
st.session_state.conn = sqlite3.connect(DB_PATH)

with st.expander(label = "Filter"):
    col1, col2 = st.columns(2)
    col3, col4 = st.columns(2)
    col5, col6 = st.columns(2)
    col7, col8 = st.columns(2)

    with col1:
        isbnInput = st.text_input(label = "ISBN", placeholder = "▮▮▮-▮▮-▮▮-▮▮▮▮▮-▮")

        conditions.append(f"isbn LIKE '%{isbnInput}%'")

    with col2:
        titleInput = st.text_input(label = "Title", placeholder = "")

        conditions.append(f"title LIKE '%{titleInput}%'")

    with col3:
        authorInput = st.text_input(label = "Author", placeholder = "Name surname")

        conditions.append(f"author LIKE '%{authorInput}%'")

    with col4:
        readInput = st.radio("Read", ["Both", "Read", "Not read"], horizontal = True)

        value = ""

        if readInput == "Read":
            conditions.append(f"beenRead = True")
        elif readInput == "Not read":
            conditions.append(f"beenRead = False")

    with col5:
        xPosInput = st.number_input(label = "X position", min_value = -1, max_value = 4, step = 1, placeholder = "X position")

        if xPosInput != -1:
            conditions.append(f"posX = {xPosInput}")

    with col6:
        yPosInput = st.number_input(label = "Y position", min_value = -1, max_value = 4, step = 1, placeholder = "Y position")

        if yPosInput != -1:
            conditions.append(f"posY = {yPosInput}")

    with col7:
        ratingInput = st.slider(label = "Rating", min_value = -1, max_value = 10, step = 1)

        if ratingInput != -1:
            conditions.append(f"rating = {ratingInput}")

    with col8:
        phInput = st.text_input(label = "Publishing house", placeholder = "")

        conditions.append(f"ph_name LIKE '%{phInput}%'")

    cCol1, cCol2, cCol3, cCol4, cCol5, cCol6, cCol7, cCol8 = st.columns(8)

    with cCol1:
        isbnCheck = st.toggle("isbn", value = True)

        if isbnCheck:
            attributes.append("isbn")

    with cCol2:
        titleCheck = st.toggle("title", value = True)

        if titleCheck:
            attributes.append("title")

    with cCol3:
        authorCheck = st.toggle("author", value = True)

        if authorCheck:
            attributes.append("author")

    with cCol4:
        readCheck = st.toggle("beenRead", value = True)

        if readCheck:
            attributes.append("beenRead")

    with cCol5:
        ratingCheck = st.toggle("rating", value = True)

        if ratingCheck:
            attributes.append("rating")

    with cCol6:
        xPosCheck = st.toggle("posX", value = True)

        if xPosCheck:
            attributes.append("posX")

    with cCol7:
        yPosCheck = st.toggle("posY", value = True)

        if yPosCheck:
            attributes.append("posY")

    with cCol8:
        phCheck = st.toggle("ph_name", value = True)

        if phCheck:
            attributes.append("ph_name")

    attributes = ', '.join(attributes)
    conditions = ' AND '.join(conditions)

if not st.session_state.showFilter:
    books = pd.read_sql("SELECT * FROM books;", st.session_state.conn)
    st.dataframe(books, use_container_width = True)
else:
    try:
        books = pd.read_sql(f"SELECT {attributes} FROM books WHERE {conditions};", st.session_state.conn)
        st.dataframe(books, use_container_width = True)
    except Exception as e:
        st.error(f"Error: {e}", icon = "🚨")

st.session_state.conn.commit()

st.session_state.conn.close()

if st.session_state.get("logged_in"):
    st.sidebar.button("Log out", on_click = lg, use_container_width = True)
