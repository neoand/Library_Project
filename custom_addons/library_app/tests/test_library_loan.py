# -*- coding: utf-8 -*-
"""
Tests for Library Book Loan Model

This module contains unit tests for the library.book.loan model,
testing the complete loan workflow.
"""

from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError
from datetime import date, timedelta


class TestLibraryLoan(TransactionCase):
    """Test cases for library.book.loan model"""

    def setUp(self):
        """Set up test data"""
        super().setUp()
        self.Loan = self.env['library.book.loan']
        self.Book = self.env['library.book']
        self.Partner = self.env['res.partner']
        self.Category = self.env['library.book.category']

        # Create test data
        self.test_author = self.Partner.create({
            'name': 'Test Author',
            'is_author': True,
        })

        self.test_borrower = self.Partner.create({
            'name': 'Test Borrower',
            'is_company': False,
        })

        self.test_category = self.Category.create({
            'name': 'Test Category',
            'code': 'TEST001',
        })

        self.test_book = self.Book.create({
            'name': 'Test Book',
            'isbn': '1234567890123',
            'author_id': self.test_author.id,
            'category_ids': [(6, 0, [self.test_category.id])],
        })

    def test_loan_creation(self):
        """Test basic loan creation"""
        loan = self.Loan.create({
            'book_id': self.test_book.id,
            'partner_id': self.test_borrower.id,
            'loan_date': date.today(),
            'expected_return_date': date.today() + timedelta(days=14),
        })
        
        self.assertEqual(loan.book_id, self.test_book)
        self.assertEqual(loan.partner_id, self.test_borrower)
        self.assertEqual(loan.state, 'ongoing')

    def test_loan_workflow(self):
        """Test complete loan workflow"""
        loan = self.Loan.create({
            'book_id': self.test_book.id,
            'partner_id': self.test_borrower.id,
            'loan_date': date.today(),
            'expected_return_date': date.today() + timedelta(days=14),
        })
        
        # Initially ongoing
        self.assertEqual(loan.state, 'ongoing')
        
        # Return the book
        loan.action_return_book()
        self.assertEqual(loan.state, 'done')
        self.assertIsNotNone(loan.return_date)

    def test_overdue_loans(self):
        """Test overdue loan detection"""
        # Create overdue loan
        overdue_loan = self.Loan.create({
            'book_id': self.test_book.id,
            'partner_id': self.test_borrower.id,
            'loan_date': date.today() - timedelta(days=30),
            'expected_return_date': date.today() - timedelta(days=15),
            'state': 'ongoing',
        })
        
        # Should be marked as overdue
        self.assertTrue(overdue_loan.is_overdue)

    def test_book_availability_after_loan(self):
        """Test that book status changes when loaned"""
        # Initially available
        self.assertEqual(self.test_book.book_status, 'available')
        
        # Create loan
        loan = self.Loan.create({
            'book_id': self.test_book.id,
            'partner_id': self.test_borrower.id,
            'loan_date': date.today(),
        })
        
        # Should now be borrowed
        self.assertEqual(self.test_book.book_status, 'borrowed')
        
        # Return book
        loan.action_return_book()
        
        # Should be available again
        self.assertEqual(self.test_book.book_status, 'available')

    def test_multiple_loans_same_book(self):
        """Test that a book can only have one active loan"""
        # Create first loan
        loan1 = self.Loan.create({
            'book_id': self.test_book.id,
            'partner_id': self.test_borrower.id,
            'loan_date': date.today(),
        })
        
        # Try to create second loan for same book
        with self.assertRaises(ValidationError):
            self.Loan.create({
                'book_id': self.test_book.id,
                'partner_id': self.test_borrower.id,
                'loan_date': date.today(),
            })

    def test_loan_duration_calculation(self):
        """Test loan duration calculation"""
        loan_date = date.today() - timedelta(days=10)
        loan = self.Loan.create({
            'book_id': self.test_book.id,
            'partner_id': self.test_borrower.id,
            'loan_date': loan_date,
            'state': 'ongoing',
        })
        
        # Should calculate correct duration
        expected_duration = (date.today() - loan_date).days
        self.assertEqual(loan.loan_duration, expected_duration)