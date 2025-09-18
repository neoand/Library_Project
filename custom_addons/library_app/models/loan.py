# -*- coding: utf-8 -*-
from odoo import models, fields, api

class LibraryBookLoan(models.Model):
    _name = 'library.book.loan'
    _description = 'Book Loan'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'loan_date desc'

    book_id = fields.Many2one(
        comodel_name='library.book',
        string='Book',
        ondelete='cascade',
        index=True,
        required=True,
        tracking=True,
    )
    partner_id = fields.Many2one(
        comodel_name='res.partner',
        string='Borrower',
        domain=[('customer_rank', '>', 0)],
        ondelete='set null',
        tracking=True,
    )
    loan_date = fields.Date(
        string='Loan Date',
        default=fields.Date.context_today,
        required=True,
        tracking=True,
    )
    return_date = fields.Date(string='Return Date', tracking=True)
    state = fields.Selection([
        ('ongoing', 'Ongoing'),
        ('done', 'Returned'),
        ('lost', 'Lost'),
    ], string='Status', default='ongoing', tracking=True)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('return_date'):
                vals['state'] = 'ongoing'
        return super().create(vals_list)