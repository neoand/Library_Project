# -*- coding: utf-8 -*-
"""
Tests for Partner Loan Filtering

This module contains tests for the res.partner loan filtering functionality,
including computed fields and search filters.
"""

from datetime import datetime, timedelta
from odoo.tests.common import TransactionCase


class TestPartnerLoanFiltering(TransactionCase):
    """Test cases for partner loan filtering functionality"""

    def setUp(self):
        """Set up test data"""
        super().setUp()
        self.Partner = self.env['res.partner']
        self.Book = self.env['library.book']
        self.Loan = self.env['library.book.loan']
        
        # Create test books
        self.test_book1 = self.Book.create({
            'name': 'Test Book 1',
            'isbn': '1111111111111',
        })
        
        self.test_book2 = self.Book.create({
            'name': 'Test Book 2',
            'isbn': '2222222222222',
        })
        
        # Create borrowers
        self.borrower1 = self.Partner.create({
            'name': 'Borrower With On-Time Loans',
            'is_company': False,
        })
        
        self.borrower2 = self.Partner.create({
            'name': 'Borrower With Overdue Loans',
            'is_company': False,
        })
        
        self.borrower3 = self.Partner.create({
            'name': 'Borrower With No Loans',
            'is_company': False,
        })
        
        # Create loans
        today = datetime.now().date()
        future_date = today + timedelta(days=10)
        past_date = today - timedelta(days=10)
        
        # On-time loan for borrower1
        self.on_time_loan = self.Loan.create({
            'book_id': self.test_book1.id,
            'partner_id': self.borrower1.id,
            'loan_date': today.strftime('%Y-%m-%d'),
            'expected_return_date': future_date.strftime('%Y-%m-%d'),
            'state': 'ongoing',
        })
        
        # Overdue loan for borrower2
        self.overdue_loan = self.Loan.create({
            'book_id': self.test_book2.id,
            'partner_id': self.borrower2.id,
            'loan_date': past_date.strftime('%Y-%m-%d'),
            'expected_return_date': past_date.strftime('%Y-%m-%d'),
            'state': 'ongoing',
        })

    def test_loan_counts(self):
        """Test computed loan count fields"""
        # Check borrower with on-time loan
        self.assertEqual(self.borrower1.active_loans_count, 1)
        self.assertEqual(self.borrower1.on_time_loans_count, 1)
        self.assertEqual(self.borrower1.overdue_loans_count, 0)
        
        # Check borrower with overdue loan
        self.assertEqual(self.borrower2.active_loans_count, 1)
        self.assertEqual(self.borrower2.on_time_loans_count, 0)
        self.assertEqual(self.borrower2.overdue_loans_count, 1)
        
        # Check borrower with no loans
        self.assertEqual(self.borrower3.active_loans_count, 0)
        self.assertEqual(self.borrower3.on_time_loans_count, 0)
        self.assertEqual(self.borrower3.overdue_loans_count, 0)
    
    def test_search_filters(self):
        """Test search filters for borrowers"""
        # Test filter for partners with active loans
        partners_with_loans = self.Partner.search([
            ('active_loans_count', '>', 0)
        ])
        self.assertIn(self.borrower1, partners_with_loans)
        self.assertIn(self.borrower2, partners_with_loans)
        self.assertNotIn(self.borrower3, partners_with_loans)
        
        # Test filter for partners with overdue loans
        partners_with_overdue = self.Partner.search([
            ('overdue_loans_count', '>', 0)
        ])
        self.assertNotIn(self.borrower1, partners_with_overdue)
        self.assertIn(self.borrower2, partners_with_overdue)
        self.assertNotIn(self.borrower3, partners_with_overdue)
        
        # Test filter for partners with on-time loans only
        partners_on_time = self.Partner.search([
            ('active_loans_count', '>', 0),
            ('overdue_loans_count', '=', 0)
        ])
        self.assertIn(self.borrower1, partners_on_time)
        self.assertNotIn(self.borrower2, partners_on_time)
        self.assertNotIn(self.borrower3, partners_on_time)
    
    def test_loan_state_changes(self):
        """Test loan counts update when loan states change"""
        # Return the overdue loan
        self.overdue_loan.write({
            'return_date': datetime.now().date().strftime('%Y-%m-%d'),
            'state': 'returned',
        })
        
        # Check borrower loan counts after return
        self.assertEqual(self.borrower2.active_loans_count, 0)
        self.assertEqual(self.borrower2.overdue_loans_count, 0)
        
        # Make the on-time loan overdue by changing expected return date
        past_date = (datetime.now().date() - timedelta(days=5)).strftime('%Y-%m-%d')
        self.on_time_loan.write({
            'expected_return_date': past_date,
        })
        
        # Check that the loan is now counted as overdue
        self.assertEqual(self.borrower1.active_loans_count, 1)
        self.assertEqual(self.borrower1.on_time_loans_count, 0)
        self.assertEqual(self.borrower1.overdue_loans_count, 1)