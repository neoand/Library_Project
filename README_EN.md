# Library Project - Library Management System

## 📚 Overview

This is a comprehensive library management system developed as a custom addon for Odoo 18. The project allows you to manage book catalogs, authors, loans, and much more.

## 🚀 Key Features

- **Book Catalog**: Complete book management with ISBN, categories, and stages
- **Author Management**: Extension of partner model (res.partner) to include biographical data
- **Loan System**: Loan control with status tracking
- **Categories**: Book organization by categories (Fiction, Non-fiction, etc.)
- **Workflow Stages**: Book lifecycle control (Draft, Available, Borrowed, Lost)
- **Chatter Integration**: Integrated messaging system for tracking

## 📋 Project Structure

```
custom_addons/library_app/
├── __manifest__.py          # Module configuration
├── models/                  # Data models
│   ├── book.py             # Main book model
│   ├── author.py           # Partner extension for authors
│   ├── partner.py          # Additional fields in res.partner
│   ├── category.py         # Book categories
│   ├── stage.py            # Workflow stages
│   └── loan.py             # Loan system
├── views/                   # User interfaces
│   ├── book_view.xml       # Book forms and lists
│   ├── book_kanban.xml     # Kanban view
│   ├── author_view.xml     # Author views
│   ├── library_menu.xml    # Main menu
│   └── ...                 # Other views
├── data/                    # Initial data
│   └── library_book_stage_data.xml  # Default stages
├── security/                # Permissions and security
│   ├── security.xml        # Security groups
│   └── ir.model.access.csv # Access control
└── static/                  # Static resources
    └── description/
        └── icon.png        # Module icon
```

## 🛠️ How to Work with the Project

### 1. Installation and Setup

#### Prerequisites
- Odoo 18 installed
- Python 3.8+
- PostgreSQL

#### Installation Steps

1. **Clone the repository**:
```bash
git clone https://github.com/neoand/Library_Project.git
cd Library_Project
```

2. **Configure the addon in Odoo**:
```bash
# Copy the addon to Odoo's addons directory
cp -r custom_addons/library_app /path/to/odoo/addons/
```

3. **Configure odoo.conf file**:
```ini
[options]
addons_path = /path/to/odoo/addons,/path/to/custom_addons
```

4. **Install the module**:
   - Access Odoo via web browser
   - Go to Apps → Update Apps List
   - Search for "Library App"
   - Click "Install"

### 2. Using the System

#### 2.1 Book Management

**Creating a new book**:
1. Navigate to Library → Books → Books
2. Click "Create"
3. Fill in the required fields:
   - Book name
   - ISBN (10 or 13 digits)
   - Author (select a partner marked as author)
   - Publication date

**Available fields**:
- `name`: Book title
- `isbn`: Unique ISBN code
- `author_id`: Book author (res.partner)
- `category_ids`: Categories (Many2many)
- `stage_id`: Current stage (Draft, Available, Borrowed, Lost)
- `date_published`: Publication date
- `user_id`: Book responsible

#### 2.2 Author Management

**Converting a partner to author**:
1. Go to Library → Authors → Authors
2. Select an existing partner or create a new one
3. Check the "Is Author" field
4. Fill in biographical data:
   - Birth/death date
   - Birth place
   - Biography
   - Awards

**Special features**:
- Automatic age calculation
- Published books counter
- First and last publication dates
- Action to view author's books

#### 2.3 Loan System

**Creating a loan**:
1. Access Library → Loans → Book Loans
2. Click "Create"
3. Select:
   - Book to be borrowed
   - Borrower
   - Loan date

**Loan status**:
- `ongoing`: Ongoing
- `done`: Returned
- `lost`: Lost

#### 2.4 Categories and Stages

**Categories** (e.g., Fiction, Non-fiction, Biography):
- Organize your books by themes
- Each category has a unique code
- Automatic book counter

**Stages** (Workflow):
- `draft`: Draft (default)
- `available`: Available
- `borrowed`: Borrowed
- `lost`: Lost

### 3. Development and Customization

#### 3.1 Adding New Fields

**Example: Adding "Publisher" field to Book model**:

```python
# In models/book.py
publisher = fields.Char(string='Publisher')
```

**Updating the view**:
```xml
<!-- In views/book_view.xml -->
<field name="publisher"/>
```

#### 3.2 Creating New Reports

**Example: Books by author report**:

```python
# New file models/report.py
from odoo import models, fields

class LibraryBookReport(models.Model):
    _name = 'library.book.report'
    _description = 'Library Book Report'
    _auto = False
    
    author_id = fields.Many2one('res.partner', string='Author')
    book_count = fields.Integer(string='Book Count')
    
    def init(self):
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute("""
            CREATE OR REPLACE VIEW %s AS (
                SELECT 
                    row_number() OVER () AS id,
                    author_id,
                    COUNT(*) as book_count
                FROM library_book 
                WHERE author_id IS NOT NULL
                GROUP BY author_id
            )
        """ % self._table)
```

#### 3.3 Custom Workflow

**Adding custom validations**:

```python
# In models/book.py
@api.constrains('date_published')
def _check_publication_date(self):
    for book in self:
        if book.date_published and book.date_published > fields.Date.today():
            raise ValidationError("Publication date cannot be in the future")
```

### 4. Testing and Development

#### 4.1 Running the Project

```bash
# Start Odoo in development mode
./odoo-bin -d your_database -i library_app --dev=reload,qweb,werkzeug,xml
```

#### 4.2 Testing Features

**Basic book creation test**:
1. Create an author
2. Create a category
3. Create a book associating author and category
4. Check if counters were updated
5. Test the loan system

#### 4.3 Debug and Logs

**Activating detailed logs**:
```ini
# In odoo.conf
log_level = debug
log_handler = odoo.addons.library_app:DEBUG
```

### 5. Data Structure

#### 5.1 Main Models

| Model | Description | Main Fields |
|--------|-----------|-------------------|
| `library.book` | Books | name, isbn, author_id, category_ids, stage_id |
| `res.partner` | Authors (extension) | is_author, birth_date, biography, book_ids |
| `library.book.category` | Categories | name, code, book_ids |
| `library.book.stage` | Stages | name, code, sequence, is_default |
| `library.book.loan` | Loans | book_id, partner_id, loan_date, return_date, state |

#### 5.2 Relationships

```
res.partner (Author) ──→ library.book (One2many)
                    ↓
library.book.category ←──→ library.book (Many2many)
                    ↓
library.book.stage ←── library.book (Many2one)
                    ↓
library.book ──→ library.book.loan (One2many)
```

## 🔧 Troubleshooting

### Common Issues

**1. Permission error when accessing models**:
- Check the `security/ir.model.access.csv` file
- Make sure the user has the correct group

**2. Views don't appear**:
- Check if actions are defined before menus
- Confirm the order in `__manifest__.py` file

**3. Data is not created**:
- Check constraints in models
- Confirm required fields are filled

## 📝 Next Steps

### Planned Features

- [ ] Reservation system
- [ ] Advanced reports
- [ ] Barcode integration
- [ ] Automatic expiration notifications
- [ ] Library metrics dashboard

### How to Contribute

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the LGPL-3 License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Anderson Oliveira**
- LinkedIn: [anderson-oliveira-dev](https://www.linkedin.com/in/anderson-oliveira-dev/)
- GitHub: [neoand](https://github.com/neoand)

## 🆘 Support

If you have questions or need help:

1. Consult the [Odoo documentation](https://www.odoo.com/documentation/18.0/)
2. Open an [issue](https://github.com/neoand/Library_Project/issues) on GitHub
3. Contact via LinkedIn

---
**Developed with ❤️ for the Odoo community**