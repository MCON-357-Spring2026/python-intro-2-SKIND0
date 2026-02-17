"""
Exercise 4: Mini-Project - Library Management System
=====================================================
Combine everything: functions, classes, files, and JSON

This exercise brings together all the concepts from the course.
Build a simple library system that tracks books and borrowers.

Instructions:
- Complete all TODOs
- The system should persist data to JSON files
- Run this file to test your implementation

Run with: python exercise_4_project.py
"""

import json
import os
from datetime import datetime


# =============================================================================
# PART 1: HELPER FUNCTIONS
# =============================================================================

def format_date(dt: datetime = None) -> str:
    """
    Format a datetime object as a string "YYYY-MM-DD".
    If no datetime provided, use current date.

    Example:
        format_date(datetime(2024, 1, 15)) -> "2024-01-15"
        format_date() -> "2024-02-04" (today's date)
    """
    if dt is None:
        dt = datetime.now()
    return dt.strftime("%Y-%m-%d")


def generate_id(prefix: str, existing_ids: list) -> str:
    """
    Generate a new unique ID with the given prefix.

    Parameters:
        prefix: String prefix (e.g., "BOOK", "USER")
        existing_ids: List of existing IDs to avoid duplicates

    Returns:
        New ID in format "{prefix}_{number:04d}"

    Example:
        generate_id("BOOK", ["BOOK_0001", "BOOK_0002"]) -> "BOOK_0003"
        generate_id("USER", []) -> "USER_0001"
    """
    if not existing_ids:
        return f"{prefix}_0001"
    numbers = [int(id.split("_")[1]) for id in existing_ids]
    max_num = max(numbers)
    return f"{prefix}_{max_num + 1:04d}"



def search_items(items: list, **criteria) -> list:
    """
    Search a list of dictionaries by matching criteria.
    Uses **kwargs to accept any search fields.

    Parameters:
        items: List of dictionaries to search
        **criteria: Field-value pairs to match (case-insensitive for strings)

    Returns:
        List of matching items

    Example:
        books = [
            {"title": "Python 101", "author": "Smith"},
            {"title": "Java Guide", "author": "Smith"},
            {"title": "Python Advanced", "author": "Jones"}
        ]
        search_items(books, author="Smith") -> [first two books]
        search_items(books, title="Python 101") -> [first book]
    """
    results = []
    for item in items:
        match = True
        for key, value in criteria.items():
            if key not in item:
                match = False
                break
            item_val = item[key]
            if isinstance(item_val, str) and isinstance(value, str):
                if item_val.lower() != value.lower():
                    match = False
                    break
            else:
                if item_val != value:
                    match = False
                    break
        if match:
            results.append(item)
    return results


# =============================================================================
# PART 2: BOOK CLASS
# =============================================================================

class Book:
    """
    Represents a book in the library.

    Class Attributes:
        GENRES: List of valid genres ["Fiction", "Non-Fiction", "Science", "History", "Technology"]

    Instance Attributes:
        book_id (str): Unique identifier
        title (str): Book title
        author (str): Author name
        genre (str): Must be one of GENRES
        available (bool): Whether book is available for borrowing

    Methods:
        to_dict(): Convert to dictionary for JSON serialization
        from_dict(data): Class method to create Book from dictionary
        __str__(): Return readable string representation
    """

    GENRES = ["Fiction", "Non-Fiction", "Science", "History", "Technology"]

    def __init__(self, book_id: str, title: str, author: str, genre: str, available: bool = True):
        if genre not in Book.GENRES:
            raise ValueError(f"Genre must be one of {Book.GENRES}")
        self.book_id = book_id
        self.title = title
        self.author = author
        self.genre = genre
        self.available = available

    def to_dict(self) -> dict:
        return {
            "book_id": self.book_id,
            "title": self.title,
            "author": self.author,
            "genre": self.genre,
            "available": self.available
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Book":
        return cls(
            data["book_id"],
            data["title"],
            data["author"],
            data["genre"],
            data["available"]
        )

    def __str__(self) -> str:
        status = "Available" if self.available else "Checked Out"
        return f"[{self.book_id}] {self.title} by {self.author} ({self.genre}) - {status}"


# =============================================================================
# PART 3: BORROWER CLASS
# =============================================================================

class Borrower:
    """
    Represents a library member who can borrow books.

    Instance Attributes:
        borrower_id (str): Unique identifier
        name (str): Borrower's name
        email (str): Borrower's email
        borrowed_books (list): List of book_ids currently borrowed

    Methods:
        borrow_book(book_id): Add book to borrowed list
        return_book(book_id): Remove book from borrowed list
        to_dict(): Convert to dictionary
        from_dict(data): Class method to create Borrower from dictionary
    """

    MAX_BOOKS = 3  # Maximum books a borrower can have at once

    def __init__(self, borrower_id: str, name: str, email: str, borrowed_books: list = None):
        self.borrower_id = borrower_id
        self.name = name
        self.email = email
        self.borrowed_books = borrowed_books if borrowed_books else []

    def can_borrow(self) -> bool:
        """Check if borrower can borrow more books."""
        return len(self.borrowed_books) < Borrower.MAX_BOOKS

    def borrow_book(self, book_id: str) -> bool:
        """Add book to borrowed list. Return False if at max limit."""
        if not self.can_borrow():
            return False
        self.borrowed_books.append(book_id)
        return True

    def return_book(self, book_id: str) -> bool:
        """Remove book from borrowed list. Return False if not found."""
        if book_id in self.borrowed_books:
            self.borrowed_books.remove(book_id)
            return True
        return False

    def to_dict(self) -> dict:
        return {
            "borrower_id": self.borrower_id,
            "name": self.name,
            "email": self.email,
            "borrowed_books": self.borrowed_books
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Borrower":
        return cls(
            data["borrower_id"],
            data["name"],
            data["email"],
            data.get("borrowed_books", [])
        )


# =============================================================================
# PART 4: LIBRARY CLASS (Main System)
# =============================================================================

class Library:
    """
    Main library system that manages books and borrowers.
    Persists data to JSON files.

    Attributes:
        name (str): Library name
        books (dict): book_id -> Book
        borrowers (dict): borrower_id -> Borrower
        books_file (str): Path to books JSON file
        borrowers_file (str): Path to borrowers JSON file

    Methods:
        add_book(title, author, genre) -> Book: Add a new book
        add_borrower(name, email) -> Borrower: Add a new borrower
        checkout_book(book_id, borrower_id) -> bool: Borrower checks out a book
        return_book(book_id, borrower_id) -> bool: Borrower returns a book
        search_books(**criteria) -> list: Search books by criteria
        get_available_books() -> list: Get all available books
        get_borrower_books(borrower_id) -> list: Get books borrowed by a borrower
        save(): Save all data to JSON files
        load(): Load data from JSON files
    """

    def __init__(self, name: str, data_dir: str = "."):
        self.name = name
        self.books = {}
        self.borrowers = {}
        self.books_file = os.path.join(data_dir, "library_books.json")
        self.borrowers_file = os.path.join(data_dir, "library_borrowers.json")
        self.load()

    def load(self) -> None:
        """Load books and borrowers from JSON files."""
        try:
            with open(self.books_file, "r") as f:
                books_data = json.load(f)
                self.books = {bid: Book.from_dict(b) for bid, b in books_data.items()}
        except FileNotFoundError:
            self.books = {}

        try:
            with open(self.borrowers_file, "r") as f:
                borrowers_data = json.load(f)
                self.borrowers = {bid: Borrower.from_dict(b) for bid, b in borrowers_data.items()}
        except FileNotFoundError:
            self.borrowers = {}

    def save(self) -> None:
        """Save books and borrowers to JSON files."""
        books_data = {bid: book.to_dict() for bid, book in self.books.items()}
        with open(self.books_file, "w") as f:
            json.dump(books_data, f, indent=2)

        borrowers_data = {bid: b.to_dict() for bid, b in self.borrowers.items()}
        with open(self.borrowers_file, "w") as f:
            json.dump(borrowers_data, f, indent=2)

    def add_book(self, title: str, author: str, genre: str) -> Book:
        """Add a new book to the library."""
        book_id = generate_id("BOOK", list(self.books.keys()))
        book = Book(book_id, title, author, genre)
        self.books[book_id] = book
        self.save()
        return book

    def add_borrower(self, name: str, email: str) -> Borrower:
        """Register a new borrower."""
        borrower_id = generate_id("USER", list(self.borrowers.keys()))
        borrower = Borrower(borrower_id, name, email)
        self.borrowers[borrower_id] = borrower
        self.save()
        return borrower

    def checkout_book(self, book_id: str, borrower_id: str) -> bool:
        """
        Borrower checks out a book.
        Returns False if book unavailable, borrower not found, or at max limit.
        """
        if book_id not in self.books or borrower_id not in self.borrowers:
            return False

        book = self.books[book_id]
        borrower = self.borrowers[borrower_id]

        if not book.available or not borrower.can_borrow():
            return False

        book.available = False
        borrower.borrow_book(book_id)
        self.save()
        return True

    def return_book(self, book_id: str, borrower_id: str) -> bool:
        """
        Borrower returns a book.
        Returns False if book/borrower not found or book wasn't borrowed by this person.
        """
        if book_id not in self.books or borrower_id not in self.borrowers:
            return False

        borrower = self.borrowers[borrower_id]
        if book_id not in borrower.borrowed_books:
            return False

        self.books[book_id].available = True
        borrower.return_book(book_id)
        self.save()
        return True

    def search_books(self, **criteria) -> list:
        """Search books by any criteria (title, author, genre, available)."""
        books_as_dicts = [b.to_dict() for b in self.books.values()]
        return search_items(books_as_dicts, **criteria)

    def get_available_books(self) -> list:
        """Get list of all available books."""
        return [b for b in self.books.values() if b.available]

    def get_borrower_books(self, borrower_id: str) -> list:
        """Get list of books currently borrowed by a borrower."""
        if borrower_id not in self.borrowers:
            return []
        borrower = self.borrowers[borrower_id]
        return [self.books[bid] for bid in borrower.borrowed_books if bid in self.books]

    def get_statistics(self) -> dict:
        """
        Return library statistics.
        Uses the concepts of dict comprehension and aggregation.
        """
        books_by_genre = {}
        for book in self.books.values():
            books_by_genre[book.genre] = books_by_genre.get(book.genre, 0) + 1

        return {
            "total_books": len(self.books),
            "available_books": sum(1 for b in self.books.values() if b.available),
            "checked_out": sum(1 for b in self.books.values() if not b.available),
            "total_borrowers": len(self.borrowers),
            "books_by_genre": books_by_genre
        }


