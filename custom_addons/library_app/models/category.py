# -*- coding: utf-8 -*-
from odoo import models, fields, api

class LibraryBookCategory(models.Model):
    _name = 'library.book.category'
    _description = 'Library Book Category'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name'

    # Identificação
    name = fields.Char(string='Category Name', required=True, index=True, tracking=True)
    code = fields.Char(
        string='Technical Code',
        required=True,
        index=True,
        copy=False,
        tracking=True,
        help="Short unique code for this category (e.g., FIC, NF, BIO)."
    )

    # Relacionamento com livros (espelha a definição em library.book)
    book_ids = fields.Many2many(
        comodel_name='library.book',
        relation='library_book_category_rel',
        column1='category_id',
        column2='book_id',
        string='Books'
    )

    # Métrica
    book_count = fields.Integer(
        string='Book Count',
        compute='_compute_book_count',
        store=True
    )

    _sql_constraints = [
        ('category_code_unique', 'unique(code)', 'Category code must be unique.'),
        ('category_name_unique', 'unique(name)', 'Category name must be unique.'),
    ]

    @api.depends('book_ids')
    def _compute_book_count(self):
        """Conta quantos livros estão associados a esta categoria."""
        for categ in self:
            categ.book_count = len(categ.book_ids)