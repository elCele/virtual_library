import streamlit as st
import requests

def logout():
    st.session_state.logged_in = False

def search_book(titolo):
    url = "https://www.googleapis.com/books/v1/volumes"
    params = {"q": titolo, "maxResults": 1}
    response = requests.get(url, params=params)
    data = response.json()

    if "items" not in data:
        return None

    libro = data["items"][0]["volumeInfo"]

    autore = ", ".join(libro.get("authors", []))
    casa_editrice = libro.get("publisher", "N/D")
    tit = libro.get("title", "N/D")
    isbn = "N/D"

    for id_type in libro.get("industryIdentifiers", []):
        if id_type["type"] == "ISBN_13":
            isbn = id_type["identifier"]
            break

    isbn = list(isbn)

    isbn.insert(3, '-')
    isbn.insert(6, '-')
    isbn.insert(9, '-')
    isbn.insert(15, '-')

    isbn = ''.join(isbn)

    return {
        "title": tit,
        "author": autore,
        "publishing house": casa_editrice,
        "ISBN": isbn
    }

def toggleFilter():
    st.session_state.showFilter = not st.session_state.showFilter