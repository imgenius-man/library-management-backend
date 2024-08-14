
# Library Management System API

This is a Django RESTful API for managing books and authors. The API includes user authentication using JWT, search functionality to find books by title or author, and a recommendation system to suggest books based on user preferences.

## Features

1. **Books Management**:
   - `GET /books`: Retrieve a list of all books.
   - `GET /books/:id`: Retrieve a specific book by ID.
   - `POST /books`: Create a new book (protected).
   - `PUT /books/:id`: Update an existing book (protected).
   - `DELETE /books/:id`: Delete a book (protected).

2. **Authors Management**:
   - `GET /authors`: Retrieve a list of all authors.
   - `GET /authors/:id`: Retrieve a specific author by ID.
   - `POST /authors`: Create a new author (protected).
   - `PUT /authors/:id`: Update an existing author (protected).
   - `DELETE /authors/:id`: Delete an author (protected).

3. **User Authentication**:
   - JWT-based authentication.
   - `POST /register`: Register a new user.
   - `POST /login`: Login an existing user to get a JWT token.

4. **Search Functionality**:
   - `GET /books?search=query`: Search for books by title or author name.

5. **Recommendation System**:
   - Users can add or remove books from their favorites list.
   - The system provides a list of 5 recommended titles when a user adds a book to their favorites.
   - Recommendations are based on a similarity algorithm comparing book titles.

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/imgenius-man/library-management-backend.git

2. **Setup virtual environment**:
    python3 -m venv venv
    activate virtual env "source venv/bin/activate

3. **Run the Server**:
    python3 manage.py runserver