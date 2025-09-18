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
        # Segurança e permissões
        'security/security.xml',
        'security/ir.model.access.csv',

        # Dados iniciais de estágios de livro
        'data/library_book_stage_data.xml',

        # Ações (sempre antes dos menus)
        'views/book_action.xml',
        'views/author_action.xml',
        'views/category_action.xml',
        'views/stage_action.xml',       # ← nova action para Stages
        'views/loan_action.xml',

        # Menu principal e submenus
        'views/library_menu.xml',

        # Views de Book
        'views/book_view.xml',
        'views/book_search.xml',
        'views/book_kanban.xml',

        # Views de Author (res.partner)
        'views/author_tree_view.xml',
        'views/author_search_view.xml',
        'views/author_view.xml',
        'views/partner_view.xml',

        # Views de Category e Stage
        'views/category_view.xml',
        'views/stage_view.xml',

        # Views de Loan
        'views/loan_view.xml',
        'views/loan_search.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
    'icon': "static/description/icon.png",
}