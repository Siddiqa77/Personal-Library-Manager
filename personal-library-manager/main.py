import streamlit as st
import json
import os

# JSON file path
DB_FILE = "library.json"

# Load existing data
def load_data():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as file:
            return json.load(file)
    return {"books": []}

# Save data to JSON file
def save_data(data):
    with open(DB_FILE, "w") as file:
        json.dump(data, file, indent=4)

# Streamlit UI
st.set_page_config(page_title="Bayt al-Hikma: Library Manager", page_icon="📚", layout="wide")

# Heading
st.title("🏛️ Bait al-Hikma Library")

# Sidebar
st.sidebar.title("📚 Library Menu")
menu_option = st.sidebar.radio("Navigate", ["Add Book", "View Library"], index=0)

data = load_data()

if menu_option == "Add Book":
    st.subheader("➕ Add a New Book")
    with st.form("add_book_form"):
        col1, col2 = st.columns(2)
        with col1:
            title = st.text_input("📖 Title")
        with col2:
            author = st.text_input("✍️ Author")
        year = st.number_input("📅 Year", min_value=0, step=1)
        read_status = st.checkbox("✅ Mark as Read")
        submitted = st.form_submit_button("✅ Add Book")
        if submitted:
            if title and author:
                data["books"].append({"title": title, "author": author, "year": year, "read": read_status})
                save_data(data)
                st.success(f"✅ '{title}' by {author} added successfully!")
                st.rerun()
            else:
                st.error("⚠️ Please enter both title and author.")

elif menu_option == "View Library":
    st.subheader("📖 Library Collection")
    if data["books"]:
        updated_books = []
        for index, book in enumerate(data["books"]):
            with st.expander(f"📘 {book['title']} by {book['author']} ({book['year']})"):
                st.write(f"**Title:** {book['title']}")
                st.write(f"**Author:** {book['author']}")
                st.write(f"**Year:** {book['year']}")
                read_status = st.checkbox("✅ Mark as Read", value=book.get("read", False), key=f"read_{index}")
                if st.button("❌ Remove Book", key=f"remove_{index}"):
                    data["books"].pop(index)
                    save_data(data)
                    st.success(f"❌ '{book['title']}' removed successfully!")
                    st.rerun()
                book["read"] = read_status
                updated_books.append(book)
        save_data({"books": updated_books})
    else:
        st.info("📚 No books added yet. Start by adding a new book above!")