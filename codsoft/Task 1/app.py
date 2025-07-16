import streamlit as st
import pandas as pd
books_data = [
    {"title": "The Hobbit", "genre": "Fantasy", "popularity": 4.7},
    {"title": "1984", "genre": "Dystopian", "popularity": 4.5},
    {"title": "To Kill a Mockingbird", "genre": "Classic", "popularity": 4.6},
    {"title": "Harry Potter", "genre": "Fantasy", "popularity": 4.8},
    {"title": "Brave New World", "genre": "Dystopian", "popularity": 4.3},
    {"title": "Pride and Prejudice", "genre": "Classic", "popularity": 4.4},
    {"title": "The Lord of the Rings", "genre": "Fantasy", "popularity": 4.9},
    {"title": "Fahrenheit 451", "genre": "Dystopian", "popularity": 4.2},
    {"title": "Jane Eyre", "genre": "Classic", "popularity": 4.5},
    {"title": "The Silmarillion", "genre": "Fantasy", "popularity": 4.6},
]

books_df = pd.DataFrame(books_data)

st.title("📘 Book Recommendation System")
st.markdown("👉 Rate the books from **1 to 5** using the arrows. Books you rate **4 or higher** will influence recommendations.")


user_ratings = {}
st.subheader("🔢 Rate the Books")
for book in books_df['title']:
    user_ratings[book] = st.number_input(
        f"{book}",
        min_value=1,
        max_value=5,
        step=1,
        value=3,
        key=book
    )


liked_books = [title for title, rating in user_ratings.items() if rating >= 4]

if liked_books:
    st.subheader("✅ Books You Liked:")
    for book in liked_books:
        st.markdown(f"- {book}")

    
    liked_genres = books_df[books_df['title'].isin(liked_books)]['genre'].unique()

    
    recommendations = books_df[
        (books_df['genre'].isin(liked_genres)) &
        (~books_df['title'].isin(liked_books))
    ].sort_values(by='popularity', ascending=False)

    st.subheader("📖 Recommended for You:")
    if recommendations.empty:
        st.warning("No other books found in your preferred genres.")
    else:
        for _, row in recommendations.iterrows():
            st.markdown(f"- **{row['title']}** *(Genre: {row['genre']}, ⭐ {row['popularity']})*")
else:
    st.info("Please rate at least one book **4 or 5** to see recommendations.")
