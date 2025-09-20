# -*- coding: utf-8 -*-
"""
Tests for Partner Integration

This module contains tests for the res.partner model extensions
and author functionality.
"""

from odoo.tests.common import TransactionCase


class TestPartnerIntegration(TransactionCase):
    """Test cases for partner integration with library system"""

    def setUp(self):
        """Set up test data"""
        super().setUp()
        self.Partner = self.env['res.partner']
        self.Book = self.env['library.book']
        self.Category = self.env['library.book.category']

        # Create test category
        self.test_category = self.Category.create({
            'name': 'Test Category',
            'code': 'TEST001',
        })

    def test_author_creation(self):
        """Test creating author with is_author flag"""
        author = self.Partner.create({
            'name': 'Test Author',
            'is_author': True,
            'is_company': False,
        })
        
        self.assertTrue(author.is_author)
        self.assertFalse(author.is_company)
        self.assertEqual(author.name, 'Test Author')

    def test_author_book_relationship(self):
        """Test one2many relationship between author and books"""
        author = self.Partner.create({
            'name': 'Prolific Author',
            'is_author': True,
        })
        
        # Create multiple books for this author
        book1 = self.Book.create({
            'name': 'First Book',
            'isbn': '1111111111111',
            'author_id': author.id,
            'category_ids': [(6, 0, [self.test_category.id])],
        })
        
        book2 = self.Book.create({
            'name': 'Second Book',
            'isbn': '2222222222222',
            'author_id': author.id,
            'category_ids': [(6, 0, [self.test_category.id])],
        })
        
        # Check book count
        self.assertEqual(author.book_count, 2)
        self.assertEqual(len(author.book_ids), 2)
        self.assertIn(book1, author.book_ids)
        self.assertIn(book2, author.book_ids)

    def test_author_search_domain(self):
        """Test author search domain filters"""
        # Create regular partner
        regular_partner = self.Partner.create({
            'name': 'Regular Partner',
            'is_company': True,
        })
        
        # Create author
        author = self.Partner.create({
            'name': 'Author Partner',
            'is_author': True,
            'is_company': False,
        })
        
        # Search for authors only
        authors = self.Partner.search([
            ('is_company', '=', False),
            ('is_author', '=', True)
        ])
        
        self.assertIn(author, authors)
        self.assertNotIn(regular_partner, authors)

    def test_borrower_functionality(self):
        """Test that partners can be borrowers"""
        borrower = self.Partner.create({
            'name': 'Book Borrower',
            'is_company': False,
        })
        
        author = self.Partner.create({
            'name': 'Book Author',
            'is_author': True,
        })
        
        book = self.Book.create({
            'name': 'Test Book',
            'isbn': '1234567890123',
            'author_id': author.id,
            'category_ids': [(6, 0, [self.test_category.id])],
        })
        
        # Create loan
        loan = self.env['library.book.loan'].create({
            'book_id': book.id,
            'partner_id': borrower.id,
            'loan_date': '2025-09-20',
        })
        
        self.assertEqual(loan.partner_id, borrower)

    def test_partner_display_name(self):
        """Test partner display name functionality"""
        author = self.Partner.create({
            'name': 'Jane Doe',
            'is_author': True,
        })
        
        # Display name should include the name
        self.assertIn('Jane Doe', author.display_name)