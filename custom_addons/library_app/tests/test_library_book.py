# -*- coding: utf-8 -*-
"""
Tests for Library Book Model

This module contains unit tests for the library.book model,
following the testing strategy outlined in TESTING_STRATEGY.md.
"""

from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError


class TestLibraryBook(TransactionCase):
    """Test cases for library.book model"""

    def setUp(self):
        """Set up test data"""
        super().setUp()
        self.Book = self.env['library.book']
        self.Partner = self.env['res.partner']
        self.Category = self.env['library.book.category']
        self.Loan = self.env['library.book.loan']

        # Clean up existing data safely
        # First, return all active loans to allow book deletion
        active_loans = self.Loan.search([('state', '=', 'ongoing')])
        active_loans.write({'state': 'done'})
        
        # Then delete test data
        self.Book.search([('name', 'like', 'Test')]).unlink()
        self.Partner.search([('name', 'like', 'Test')]).unlink()
        self.Category.search([('name', 'like', 'Test')]).unlink()

        # Create test author
        self.test_author = self.Partner.create({
            'name': 'Test Author',
            'is_author': True,
        })

        # Create test category
        self.test_category = self.Category.create({
            'name': 'Test Category',
            'code': 'TEST001',
        })

    def test_book_creation(self):
        """Test basic book creation"""
        book = self.Book.create({
            'name': 'Test Book',
            'isbn': '1234567890123',
            'pages': 200,
            'author_id': self.test_author.id,
            'category_ids': [(6, 0, [self.test_category.id])],
        })
        
        self.assertEqual(book.name, 'Test Book')
        self.assertEqual(book.isbn, '1234567890123')
        self.assertEqual(book.pages, 200)
        self.assertEqual(book.author_id, self.test_author)
        self.assertIn(self.test_category, book.category_ids)

    def test_isbn_validation(self):
        """Test ISBN format validation"""
        with self.assertRaises(ValidationError):
            self.Book.create({
                'name': 'Test Book',
                'isbn': '12345', # Invalid ISBN
                'author_id': self.test_author.id,
            })

        # Valid 10-digit ISBN
        book_10 = self.Book.create({
            'name': 'Test Book 10',
            'isbn': '1234567890',
            'author_id': self.test_author.id,
            'category_ids': [(6, 0, [self.test_category.id])],
        })
        self.assertEqual(book_10.isbn, '1234567890')

        # Valid 13-digit ISBN
        book_13 = self.Book.create({
            'name': 'Test Book 13',
            'isbn': '1234567890123',
            'author_id': self.test_author.id,
            'category_ids': [(6, 0, [self.test_category.id])],
        })
        self.assertEqual(book_13.isbn, '1234567890123')

    def test_positive_pages_validation(self):
        """Test that pages must be a positive number"""
        with self.assertRaises(ValidationError):
            self.Book.create({
                'name': 'Test Book',
                'pages': -5, # Invalid pages
                'author_id': self.test_author.id,
            })

    def test_book_status_computation(self):
        """Test book status computation based on loans"""
        book = self.Book.create({
            'name': 'Test Book',
            'isbn': '1234567890123',
            'author_id': self.test_author.id,
            'category_ids': [(6, 0, [self.test_category.id])],
        })
        
        # Initially available
        self.assertEqual(book.book_status, 'available')
        
        # Create active loan
        loan = self.env['library.book.loan'].create({
            'book_id': book.id,
            'partner_id': self.test_author.id,
            'loan_date': '2025-09-20',
            'state': 'ongoing',
        })
        
        # Should now be borrowed
        self.assertEqual(book.book_status, 'borrowed')

    def test_book_tracking(self):
        """Test chatter integration and field tracking"""
        # Create a book and track changes
        book = self.Book.create({
            'name': 'Initial Name',
            'isbn': '9876543210',
            'author_id': self.test_author.id,
        })
        
        # Check initial message
        self.assertEqual(len(book.message_ids), 1)
        
        # Update tracked fields
        book.write({
            'name': 'Updated Name',
            'description': '<p>New description</p>',
        })
        
        # Check if a new message was posted
        self.assertEqual(len(book.message_ids), 2)
        self.assertIn("Book updated", book.message_ids[0].body)

    def test_book_search_functionality(self):
        """Test book search functionality"""
        book1 = self.Book.create({
            'name': 'Test Python Programming Unique',
            'isbn': '1111111111111',
            'author_id': self.test_author.id,
            'category_ids': [(6, 0, [self.test_category.id])],
        })
        
        book2 = self.Book.create({
            'name': 'Test Java Development Unique',
            'isbn': '2222222222222',
            'author_id': self.test_author.id,
            'category_ids': [(6, 0, [self.test_category.id])],
        })
        
        # Search by name with unique identifier
        python_books = self.Book.search([('name', 'ilike', 'Test Python Programming Unique')])
        self.assertEqual(len(python_books), 1)
        self.assertEqual(python_books[0], book1)
        
        # Search by ISBN
        isbn_books = self.Book.search([('isbn', '=', '2222222222222')])
        self.assertEqual(len(isbn_books), 1)
        self.assertEqual(isbn_books[0], book2)

    def test_book_action_borrow(self):
        """Test the borrow book action"""
        book = self.Book.create({
            'name': 'Test Book',
            'isbn': '1234567890123',
            'author_id': self.test_author.id,
            'category_ids': [(6, 0, [self.test_category.id])],
        })
        
        # Test the action returns proper context
        action = book.action_borrow_book()
        
        self.assertEqual(action['type'], 'ir.actions.act_window')
        self.assertEqual(action['res_model'], 'library.book.loan')
        self.assertEqual(action['view_mode'], 'form')
        self.assertEqual(action['target'], 'new')
        self.assertEqual(action['context']['default_book_id'], book.id)