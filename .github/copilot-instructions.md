# Copilot Instructions - Library Project (Odoo 18)

## Architecture Overview

This is an **Odoo 18 development environment** with a complete library management system built on product inheritance patterns. The project follows Odoo's standard module architecture with three key addon paths:

- `source_odoo/addons/` - Official Odoo core modules  
- `custom_addons/` - Your custom business modules (main: `library_app`)
- `others_addons/web/` - Community web enhancement modules

**Core Innovation**: Books inherit from `product.product`, combining inventory management with library-specific functionality. This enables stock tracking, categorization, and standard product features while adding library workflows.

## Development Workflow

### Starting the Environment
Always use the interactive script: `./start_odoo.sh` 
- Menu-driven interface for common tasks
- Auto-checks PostgreSQL service status
- Handles module updates and installations
- Color-coded output for clear status indication

### Key Development Commands
```bash
# List all available modules with metadata
python3 list_modules.py

# Standard development start (with dev mode enabled in odoo.conf)
python3 source_odoo/odoo-bin -c odoo.conf

# Install/update specific modules
python3 source_odoo/odoo-bin -c odoo.conf -i module_name
python3 source_odoo/odoo-bin -c odoo.conf -u module_name
```

### Module Discovery Pattern
The `list_modules.py` script uses `eval()` to safely parse `__manifest__.py` files across all addon paths, extracting metadata like dependencies, categories, and installability status.

## Custom Module Patterns (`library_app`)

### Hybrid Model Architecture
**Books as Products**: Core pattern is `_inherit = ['product.product', 'mail.thread', 'mail.activity.mixin']`
- Leverages existing product features (categorization, variants, inventory)
- Adds library-specific fields: `isbn`, `pages`, `cover`, `author_id`
- Override inherited fields with tracking: `name = fields.Char(tracking=True)`
- Uses `description = fields.Html(tracking=True)` instead of Text for rich formatting

### Key Inheritance Patterns
- **Extend core models**: `res.partner` extended with `is_author` boolean for filtering
- **Domain filters**: `[('is_company', '=', False), ('is_author', '=', True)]` for author selection
- **Product integration**: Books inherit stock management, categories, and pricing from `product.product`
- **Loan system**: Full tracking with `library.book.loan` model linking books to borrowers
- **Status management**: Computed fields like `book_status` based on active loans (`available`/`borrowed`/`lost`)

### File Structure Convention
```
custom_addons/library_app/
├── __manifest__.py          # Dependencies: base, contacts, mail, web, stock
├── models/                  # Business logic
│   ├── library_book.py     # Main entity (inherits product.product)
│   ├── loan.py             # Loan tracking system
│   ├── partner.py          # Extends res.partner for authors
│   ├── stage.py            # Workflow stages
│   └── category.py         # Supporting models
├── views/                   # UI definitions (separate from actions)
│   ├── library_menu.xml    # Menu structure
│   ├── book_view.xml       # Form/tree views
│   ├── book_action.xml     # Window actions (separate file)
│   ├── loan_view.xml       # Loan management forms
│   └── book_kanban.xml     # Kanban view with stages
├── security/
│   ├── security.xml        # Groups and rules  
│   └── ir.model.access.csv # Model permissions
├── static/src/css/         # Custom styling
│   └── chatter_layout.css  # Chatter UI optimizations
└── data/
    ├── product_category_data.xml    # Product categories for books
    └── library_book_stage_data.xml  # Default workflow stages
```

### View Patterns
- **Kanban views** require `group_expand='_read_group_stage_ids'` in stage field
- **Group expand methods** in Odoo 18 use signature: `_read_group_stage_ids(self, stages, domain)` (no order parameter)
- **Dynamic field attributes** use direct syntax: `required="condition"` instead of `attrs="{'required': [('condition')]}`
- **View modes** use `list` instead of deprecated `tree` in Odoo 18 (`view_mode='list,form'`)
- **Chatter integration** use simplified `<chatter/>` tag instead of verbose div structure
- **Search views** should include filters for common workflows
- **Menu sequences** start at 10 for root, increment by 1 for children
- **Actions defined separately** from views in `*_action.xml` files

### Model Relationships
- **Many2one with domains**: Filter related records (`domain=[('field', '=', value)]`)
- **Computed fields with store=True**: For performance on metrics like `book_count`
- **One2many inverse relationships**: Link parent to children (`book_ids = One2many('library.book', 'author_id')`)
- **Status tracking**: Use computed fields based on related model states (`book_status` from `loan_ids.state`)
- **Cascade relationships**: `loan_id` uses `ondelete='cascade'` with books, `ondelete='restrict'` with partners

## Business Logic Patterns

### Computed Field Architecture
Follow this pattern for dependent calculations:
```python
book_status = fields.Selection([...], compute='_compute_book_status', store=True)

@api.depends('loan_ids.state')
def _compute_book_status(self):
    for book in self:
        active_loans = book.loan_ids.filtered(lambda l: l.state == 'ongoing')
        book.book_status = 'borrowed' if active_loans else 'available'
```

### Action Methods
Implement smart actions for business workflows:
```python
def action_borrow_book(self):
    """Context-aware action with pre-filled form data."""
    return {
        'type': 'ir.actions.act_window',
        'name': 'New Loan', 
        'res_model': 'library.book.loan',
        'view_mode': 'form',
        'target': 'new',
        'context': {'default_book_id': self.id, 'form_view_initial_mode': 'edit'},
    }
```

### Validation Patterns
Use `@api.constrains` for business rules:
```python
@api.constrains('isbn')
def _check_isbn_format(self):
    for rec in self:
        if rec.isbn and len(rec.isbn) not in (10, 13):
            raise ValidationError('ISBN must be either 10 or 13 characters long.')
```

## Configuration Specifics

### Database Setup (`odoo.conf`)
- **Database**: `lib_neo` on localhost:5432
- **Development mode**: `dev = all` enables auto-reload
- **Single worker**: `workers = 0` for development debugging
- **HTTP port**: 8071 (avoid conflicts with default 8069)
- **Locale**: Brazilian Portuguese (`load_language = pt_BR`) - forms and interface may be in Portuguese
- **GeEvent port**: 8072 for real-time features

### Security Model
- **Simple permissions**: All custom models grant full CRUD to `base.group_user`
- **No custom groups**: Leverages Odoo's built-in user management
- **Tracking enabled**: Automatic change logging via `mail.thread`

## Critical Development Notes

### Module Dependencies
- Always include `mail` dependency for chatter functionality
- Add `web` dependency for enhanced UI components
- Include `stock` dependency when inheriting from `product.product`
- Base dependencies: `base`, `contacts` for partner extensions

### Custom Assets Integration
Include CSS/JS assets in `__manifest__.py`:
```python
'assets': {
    'web.assets_backend': [
        'library_app/static/src/css/chatter_layout.css',
    ],
}
```

### Data Loading Order (in `__manifest__.py`)
1. Security files first (`security/*.xml`, `security/*.csv`)
2. Data files (`data/*.xml`) 
3. Views (`views/*.xml`)
4. Actions and menus last

### Common Pitfalls
- **Model inheritance**: Use `_inherit = 'existing.model'` for extensions, `_name` for new models
- **Field tracking**: Add `tracking=True` to fields you want in chatter history
- **Kanban stages**: Require `group_expand` method with signature `(self, stages, domain)` in Odoo 18
- **View attributes**: Use direct syntax `readonly="condition"` instead of deprecated `attrs` in Odoo 18
- **View modes**: Use `list` instead of deprecated `tree` in view_mode definitions
- **Chatter integration**: Use `<chatter/>` tag instead of manual message field definitions
- **Required field constraints**: Use `ondelete='restrict'` with `required=True`, not `ondelete='set null'`
- **PostgreSQL dependency**: Always verify service is running before Odoo start

## Module Installation
- Use `./start_odoo.sh` option 5 for interactive module installation
- Core custom module: `library_app` (library management system)
- Recommended web modules: `web_responsive`, `web_environment_ribbon`

## Testing and Debugging
- **Development mode**: Already enabled in `odoo.conf` with `dev = all`
- **Log level**: Set to `debug` for detailed error information  
- **Access via**: http://localhost:8071 (admin/admin)
- **Database listing**: Enabled for easy database switching