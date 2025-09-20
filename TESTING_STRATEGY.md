# Testing Strategy - Library Project

This document outlines the testing approach and standards for the library management system.

## 🧪 Testing Philosophy

> **"Test early, test often, test with purpose"**

Our testing strategy focuses on:
- **Quality assurance** through automated testing
- **Regression prevention** during refactoring 
- **Performance validation** for critical operations
- **User workflow verification** for business processes

## 📋 Testing Pyramid

```
    🔺 E2E Tests (Few)
      - Complete user workflows
      - Integration across modules
      
   🔺🔺 Integration Tests (Some)  
     - Model interactions
     - Database operations
     - Business logic flows
     
  🔺🔺🔺 Unit Tests (Many)
    - Individual methods
    - Field validations  
    - Computed field logic
```

## 🎯 Test Categories

### 1. **Unit Tests** 🧪
Test individual components in isolation.

```python
# tests/test_library_book.py
from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError

class TestLibraryBook(TransactionCase):
    
    def setUp(self):
        super().setUp()
        self.Book = self.env['library.book']
        self.author = self.env['res.partner'].create({
            'name': 'Test Author',
            'is_author': True,
        })
    
    def test_book_creation(self):
        """Test basic book creation"""
        book = self.Book.create({
            'name': 'Test Book',
            'isbn': '1234567890',
            'author_id': self.author.id,
            'total_copies': 3,
        })
        self.assertEqual(book.name, 'Test Book')
        self.assertEqual(book.available_copies, 3)
        self.assertEqual(book.book_status, 'available')
    
    def test_isbn_validation(self):
        """Test ISBN format validation"""
        with self.assertRaises(ValidationError):
            self.Book.create({
                'name': 'Invalid ISBN Book',
                'isbn': '12345',  # Too short
                'author_id': self.author.id,
            })
    
    def test_available_copies_computation(self):
        """Test available copies calculation"""
        book = self.Book.create({
            'name': 'Multi-copy Book',
            'total_copies': 5,
        })
        # Initially all available
        self.assertEqual(book.available_copies, 5)
        
        # Create a loan
        loan = self.env['library.book.loan'].create({
            'book_id': book.id,
            'borrower_id': self.env.user.partner_id.id,
            'quantity': 2,
            'state': 'ongoing',
        })
        # Should reduce available copies
        self.assertEqual(book.available_copies, 3)
```

### 2. **Integration Tests** 🔗
Test interaction between components.

```python
# tests/test_loan_workflow.py
class TestLoanWorkflow(TransactionCase):
    
    def test_complete_loan_cycle(self):
        """Test complete borrow -> return -> lost workflow"""
        # Setup
        book = self.env['library.book'].create({
            'name': 'Workflow Test Book',
            'total_copies': 1,
        })
        borrower = self.env['res.partner'].create({
            'name': 'Test Borrower'
        })
        
        # Test borrow
        loan = self.env['library.book.loan'].create({
            'book_id': book.id,
            'borrower_id': borrower.id,
        })
        loan.action_start_loan()
        
        self.assertEqual(book.book_status, 'borrowed')
        self.assertEqual(book.available_copies, 0)
        
        # Test return
        loan.action_return_book()
        self.assertEqual(book.book_status, 'available')
        self.assertEqual(book.available_copies, 1)
```

### 3. **Performance Tests** 📊
Validate system performance under load.

```python
# tests/test_performance.py
import time
from odoo.tests.common import TransactionCase

class TestPerformance(TransactionCase):
    
    def test_book_list_performance(self):
        """Test book list loading with many records"""
        # Create 1000 test books
        books_data = []
        for i in range(1000):
            books_data.append({
                'name': f'Performance Test Book {i}',
                'isbn': f'123456789{i:04d}',
            })
        
        start_time = time.time()
        books = self.env['library.book'].create(books_data)
        creation_time = time.time() - start_time
        
        # Assert reasonable creation time
        self.assertLess(creation_time, 5.0, "Book creation took too long")
        
        # Test search performance
        start_time = time.time()
        found_books = self.env['library.book'].search([('name', 'ilike', 'Performance')])
        search_time = time.time() - start_time
        
        self.assertLess(search_time, 0.5, "Search took too long")
        self.assertEqual(len(found_books), 1000)
```

## 🚀 Running Tests

### Local Testing
```bash
# Run all tests
python3 source_odoo/odoo-bin -c odoo.conf -i library_app --test-enable --stop-after-init

# Run specific test file
python3 source_odoo/odoo-bin -c odoo.conf -i library_app --test-enable --test-file=tests/test_library_book.py

# Run with coverage
coverage run source_odoo/odoo-bin -c odoo.conf -i library_app --test-enable --stop-after-init
coverage report --show-missing
```

### Test Database
```bash
# Use separate test database
python3 source_odoo/odoo-bin -c odoo.conf -d lib_neo_test --test-enable --stop-after-init
```

## 📊 Test Data Management

### Fixtures
```python
# tests/fixtures/sample_data.py
def create_sample_books(env, count=10):
    """Create sample books for testing"""
    books = []
    for i in range(count):
        books.append({
            'name': f'Sample Book {i+1}',
            'isbn': f'978123456{i:03d}',
            'pages': 200 + i * 10,
            'total_copies': (i % 3) + 1,
        })
    return env['library.book'].create(books)

def create_sample_authors(env, count=5):
    """Create sample authors for testing"""
    authors = []
    for i in range(count):
        authors.append({
            'name': f'Author {i+1}',
            'is_author': True,
            'email': f'author{i+1}@example.com',
        })
    return env['res.partner'].create(authors)
```

## 🔍 Code Coverage Goals

| Component | Target Coverage | Current |
|-----------|----------------|---------|
| Models | 90% | TBD |
| Business Logic | 95% | TBD |
| Computed Fields | 100% | TBD |
| Validations | 100% | TBD |

## 🚨 Critical Test Cases

### Must-Have Tests
- ✅ Book creation and validation
- ✅ ISBN format validation  
- ✅ Available copies computation
- ✅ Loan workflow (borrow/return/lost)
- ✅ Author assignment
- ✅ Performance benchmarks

### Edge Cases
- Multiple copies of same book
- Concurrent loan operations
- Data migration scenarios
- Large dataset performance
- Invalid data handling

## 🔄 CI/CD Integration

### GitHub Actions Workflow
```yaml
# .github/workflows/tests.yml
name: Tests
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:13
        env:
          POSTGRES_PASSWORD: postgres
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.8'
    
    - name: Install dependencies
      run: |
        pip install -r source_odoo/requirements.txt
        pip install coverage
    
    - name: Run tests
      run: |
        coverage run source_odoo/odoo-bin -c odoo.conf -i library_app --test-enable --stop-after-init
        coverage xml
    
    - name: Upload coverage
      uses: codecov/codecov-action@v1
```

## 📈 Performance Benchmarks

### Baseline Metrics
```python
# Performance targets (to be measured)
PERFORMANCE_TARGETS = {
    'book_creation': 0.1,  # seconds
    'book_search': 0.3,    # seconds  
    'loan_creation': 0.15, # seconds
    'bulk_operations': 2.0 # seconds for 100 records
}
```

### Load Testing
```bash
# Future: Load testing with artillery.io or similar
# Test concurrent users, stress testing, etc.
```

## 🎯 Testing Checklist

### Before Each Release
- [ ] All unit tests pass
- [ ] Integration tests pass  
- [ ] Performance benchmarks met
- [ ] Code coverage above targets
- [ ] No regression in critical workflows

### Before Major Changes
- [ ] Backup test data
- [ ] Run full test suite
- [ ] Performance comparison
- [ ] Migration tests (if applicable)

## 📝 Test Documentation

### Writing Good Tests
```python
def test_descriptive_name(self):
    """
    Clear description of what this test validates
    
    Given: Initial conditions
    When: Action being tested
    Then: Expected outcome
    """
    # Arrange
    setup_code()
    
    # Act  
    result = method_under_test()
    
    # Assert
    self.assertEqual(expected, result)
```

### Test Naming Convention
- `test_[feature]_[scenario]_[expected_outcome]()`
- Examples:
  - `test_book_creation_with_valid_data_succeeds()`
  - `test_isbn_validation_with_invalid_format_raises_error()`

---

**Next Steps:**
1. Implement basic unit tests for core models
2. Set up CI/CD pipeline with automated testing
3. Establish performance baseline measurements
4. Create comprehensive test data fixtures

**Last Updated**: 2024-09-20  
**Review Schedule**: Monthly