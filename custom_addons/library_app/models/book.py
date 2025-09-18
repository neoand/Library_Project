# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError

class LibraryBook(models.Model):
    _name = 'library.book'
    _description = 'Library Book'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name'

    # Identificação
    name = fields.Char(string='Title', required=True, tracking=True)
    isbn = fields.Char(string='ISBN', index=True, tracking=True)
    cover = fields.Binary(string='Cover Image')

    # Relacionamentos
    author_id = fields.Many2one(
        comodel_name='res.partner',
        string='Author',
        domain=[('is_company', '=', False)],
        ondelete='set null',
        index=True,
        tracking=True
    )
    category_ids = fields.Many2many(
        comodel_name='library.book.category',
        relation='library_book_category_rel',
        column1='book_id',
        column2='category_id',
        string='Categories'
    )
    stage_id = fields.Many2one(
        comodel_name='library.book.stage',
        string='Stage',
        ondelete='restrict',
        index=True,
        tracking=True
    )
    user_id = fields.Many2one(
        comodel_name='res.users',
        string='Responsible',
        default=lambda self: self.env.user,
        index=True
    )

    # Publicação e status
    date_published = fields.Date(string='Published On', tracking=True)
    active = fields.Boolean(string='Active', default=True)
    color = fields.Integer(string='Color Index', default=0)

    # Empréstimos
    loan_ids = fields.One2many(
        comodel_name='library.book.loan',
        inverse_name='book_id',
        string='Loans'
    )
    loan_count = fields.Integer(
        string='Loan Count',
        compute='_compute_loan_count',
        store=True
    )

    # Restrições de unicidade
    _sql_constraints = [
        ('isbn_unique', 'unique(isbn)', 'ISBN must be unique.'),
    ]

    @api.constrains('isbn')
    def _check_isbn_format(self):
        """ISBN deve ter 10 ou 13 caracteres."""
        for rec in self:
            if rec.isbn and len(rec.isbn) not in (10, 13):
                raise ValidationError('ISBN must be either 10 or 13 characters long.')

    @api.depends('loan_ids')
    def _compute_loan_count(self):
        """Conta quantos empréstimos já foram feitos deste livro."""
        for rec in self:
            rec.loan_count = len(rec.loan_ids)

    @api.model_create_multi
    def create(self, vals_list):
        """
        Batch-safe override: define stage padrão se não vier no vals.
        Compatível com Odoo 17/18.
        """
        default_stage = self.env['library.book.stage'].search([('is_default', '=', True)], limit=1)
        for vals in vals_list:
            if not vals.get('stage_id') and default_stage:
                vals['stage_id'] = default_stage.id
        return super().create(vals_list)