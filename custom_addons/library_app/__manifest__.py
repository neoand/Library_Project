# -*- coding: utf-8 -*-
{
    'name': "Library App",
    'summary': "Manage library catalog and book lending system",
    'description': """
Comprehensive library management system for Odoo 18.
Features include:
- Book catalog
- Author management (extends res.partner)
- Categories and workflow stages
- Loan tracking
- Integrated messaging and chatter
    """,
    'author': "Anderson Oliveira & Mentor",
    'website': "https://www.linkedin.com/in/anderson-oliveira-dev/",
    'category': "Services/Library",
    'version': "18.0.1.0.0",
    'license': "LGPL-3",
    'depends': [
        'base',
        'contacts',
        'mail',
        'web',
    ],
    'data': [
        # Segurança
        'security/security.xml',
        'security/ir.model.access.csv',

        # Dados
        # 'data/product_category_data.xml',  # Removido - não usa mais produtos
        'data/library_book_stage_data.xml',

        # Views (carregadas antes das ações e menus)
        'views/book_view.xml',
        'views/author_view.xml',
        'views/partner_view.xml',
        'views/category_view.xml',
        'views/stage_view.xml',
        'views/loan_view.xml',
        'views/author_tree_view.xml',
        'views/author_search_view.xml',
        'views/book_search.xml',
        'views/book_kanban.xml',
        'views/loan_search.xml',

        # Ações
        'views/book_action.xml',
        'views/author_action.xml',
        'views/category_action.xml',
        'views/stage_action.xml',
        'views/loan_action.xml',

        # Menus
        'views/library_menu.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'library_app/static/src/css/chatter_layout.css',
        ],
    },
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
    'icon': "/library_app/static/description/icon.png",
}