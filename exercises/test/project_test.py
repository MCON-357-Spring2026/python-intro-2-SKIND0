import pytest
import os
from exercises.src.project import *


class TestHelperFunctions:
    """Test suite for helper functions"""

    def test_format_date(self):
        """Test format_date function"""
        assert format_date(datetime(2024, 1, 15)) == "2024-01-15"
        assert len(format_date()) == 10  # Current date

    def test_generate_id(self):
        """Test generate_id function"""
        assert generate_id("BOOK", []) == "BOOK_0001"
        assert generate_id("BOOK", ["BOOK_0001", "BOOK_0002"]) == "BOOK_0003"

    def test_search_items(self):
        """Test search_items function"""
        items = [{"name": "A", "type": "x"}, {"name": "B", "type": "x"}, {"name": "C", "type": "y"}]
        assert len(search_items(items, type="x")) == 2
        assert len(search_items(items, name="A")) == 1


class TestBook:
    """Test suite for Book class"""

    def test_book_attributes(self):
        """Test Book constructor and attributes"""
        book = Book("B001", "Python 101", "Smith", "Technology")
        assert book.title == "Python 101"
        assert book.author == "Smith"
        assert book.genre == "Technology"
        assert book.available == True

    def test_book_to_dict(self):
        """Test Book to_dict method"""
        book = Book("B001", "Python 101", "Smith", "Technology")
        book_dict = book.to_dict()
        assert book_dict["author"] == "Smith"
        assert book_dict["title"] == "Python 101"

    def test_book_from_dict(self):
        """Test Book from_dict class method"""
        book = Book("B001", "Python 101", "Smith", "Technology")
        book_dict = book.to_dict()
        book2 = Book.from_dict(book_dict)
        assert book2.title == "Python 101"
        assert book2.author == "Smith"

    def test_book_invalid_genre(self):
        """Test Book raises ValueError for invalid genre"""
        with pytest.raises(ValueError):
            Book("B002", "Bad Book", "Author", "InvalidGenre")


class TestBorrower:
    """Test suite for Borrower class"""

    def test_borrower_attributes(self):
        """Test Borrower constructor and attributes"""
        borrower = Borrower("U001", "Alice", "alice@test.com")
        assert borrower.name == "Alice"
        assert borrower.email == "alice@test.com"
        assert borrower.borrowed_books == []

    def test_borrower_can_borrow(self):
        """Test Borrower can_borrow method"""
        borrower = Borrower("U001", "Alice", "alice@test.com")
        assert borrower.can_borrow() == True

    def test_borrower_borrow_book(self):
        """Test Borrower borrow_book method"""
        borrower = Borrower("U001", "Alice", "alice@test.com")
        assert borrower.borrow_book("B001") == True
        assert "B001" in borrower.borrowed_books

    def test_borrower_return_book(self):
        """Test Borrower return_book method"""
        borrower = Borrower("U001", "Alice", "alice@test.com")
        borrower.borrow_book("B001")
        assert borrower.return_book("B001") == True
        assert "B001" not in borrower.borrowed_books

    def test_borrower_return_book_not_borrowed(self):
        """Test Borrower return_book returns False for book not borrowed"""
        borrower = Borrower("U001", "Alice", "alice@test.com")
        assert borrower.return_book("B999") == False

    def test_borrower_to_dict_from_dict(self):
        """Test Borrower to_dict and from_dict methods"""
        borrower = Borrower("U001", "Alice", "alice@test.com")
        borrower_dict = borrower.to_dict()
        borrower2 = Borrower.from_dict(borrower_dict)
        assert borrower2.name == "Alice"
        assert borrower2.email == "alice@test.com"


class TestLibrary:
    """Test suite for Library class"""

    @pytest.fixture(autouse=True)
    def cleanup(self):
        """Cleanup test files before and after each test"""
        test_files = ["library_books.json", "library_borrowers.json"]
        for f in test_files:
            if os.path.exists(f):
                os.remove(f)

        yield

        for f in test_files:
            if os.path.exists(f):
                os.remove(f)

    def test_library_add_book(self):
        """Test Library add_book method"""
        lib = Library("Test Library")
        b1 = lib.add_book("Python 101", "Smith", "Technology")
        b2 = lib.add_book("History of Rome", "Jones", "History")
        b3 = lib.add_book("Science Today", "Brown", "Science")
        assert len(lib.books) == 3

    def test_library_add_borrower(self):
        """Test Library add_borrower method"""
        lib = Library("Test Library")
        alice = lib.add_borrower("Alice", "alice@test.com")
        bob = lib.add_borrower("Bob", "bob@test.com")
        assert len(lib.borrowers) == 2

    def test_library_checkout_book(self):
        """Test Library checkout_book method"""
        lib = Library("Test Library")
        b1 = lib.add_book("Python 101", "Smith", "Technology")
        alice = lib.add_borrower("Alice", "alice@test.com")

        assert lib.checkout_book(b1.book_id, alice.borrower_id) == True
        assert lib.books[b1.book_id].available == False
        assert b1.book_id in lib.borrowers[alice.borrower_id].borrowed_books

    def test_library_checkout_unavailable_book(self):
        """Test Library checkout_book fails for unavailable book"""
        lib = Library("Test Library")
        b1 = lib.add_book("Python 101", "Smith", "Technology")
        alice = lib.add_borrower("Alice", "alice@test.com")
        bob = lib.add_borrower("Bob", "bob@test.com")

        lib.checkout_book(b1.book_id, alice.borrower_id)
        assert lib.checkout_book(b1.book_id, bob.borrower_id) == False

    def test_library_return_book(self):
        """Test Library return_book method"""
        lib = Library("Test Library")
        b1 = lib.add_book("Python 101", "Smith", "Technology")
        alice = lib.add_borrower("Alice", "alice@test.com")

        lib.checkout_book(b1.book_id, alice.borrower_id)
        assert lib.return_book(b1.book_id, alice.borrower_id) == True
        assert lib.books[b1.book_id].available == True

    def test_library_search_books(self):
        """Test Library search_books method"""
        lib = Library("Test Library")
        lib.add_book("Python 101", "Smith", "Technology")
        lib.add_book("History of Rome", "Jones", "History")

        tech_books = lib.search_books(genre="Technology")
        assert len(tech_books) == 1

    def test_library_get_available_books(self):
        """Test Library get_available_books method"""
        lib = Library("Test Library")
        b1 = lib.add_book("Python 101", "Smith", "Technology")
        lib.add_book("History of Rome", "Jones", "History")
        lib.add_book("Science Today", "Brown", "Science")

        available = lib.get_available_books()
        assert len(available) == 3

    def test_library_get_statistics(self):
        """Test Library get_statistics method"""
        lib = Library("Test Library")
        lib.add_book("Python 101", "Smith", "Technology")
        lib.add_book("History of Rome", "Jones", "History")
        lib.add_borrower("Alice", "alice@test.com")
        lib.add_borrower("Bob", "bob@test.com")

        stats = lib.get_statistics()
        assert stats["total_books"] == 2
        assert stats["total_borrowers"] == 2

    def test_library_persistence(self):
        """Test Library persists data to files"""
        lib = Library("Test Library")
        lib.add_book("Python 101", "Smith", "Technology")
        lib.add_book("History of Rome", "Jones", "History")
        lib.add_borrower("Alice", "alice@test.com")

        # Create new instance from same files
        lib2 = Library("Test Library")
        assert len(lib2.books) == 2
        assert len(lib2.borrowers) == 1

