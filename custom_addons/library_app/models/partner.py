# -*- coding: utf-8 -*-
from odoo import models, fields, api

class ResPartner(models.Model):
    _inherit = 'res.partner'

    # Sinalizador de autor
    is_author = fields.Boolean(string="Is Author", default=False, index=True)

    # Dados biográficos
    birth_date = fields.Date(string="Birth Date")
    death_date = fields.Date(string="Death Date")
    birth_place = fields.Char(string="Place of Birth")
    biography = fields.Html(string="Biography")
    website = fields.Char(string="Website")
    awards = fields.Text(string="Awards")

    # Relação com livros
    book_ids = fields.One2many(
        comodel_name='library.book',
        inverse_name='author_id',
        string='Books'
    )

    # Relação com empréstimos
    loan_ids = fields.One2many(
        comodel_name='library.book.loan',
        inverse_name='partner_id',
        string='Loans'
    )

    # Métricas de empréstimos
    active_loans_count = fields.Integer(
        string="Active Loans",
        compute='_compute_loan_metrics',
        store=True,
        help="Number of ongoing book loans"
    )
    
    overdue_loans_count = fields.Integer(
        string="Overdue Loans",
        compute='_compute_loan_metrics',
        store=True,
        help="Number of overdue book loans"
    )
    
    on_time_loans_count = fields.Integer(
        string="On Time Loans",
        compute='_compute_loan_metrics',
        store=True,
        help="Number of ongoing loans that are still on time"
    )

    # Métricas e publicações
    book_count = fields.Integer(
        string="Book Count",
        compute='_compute_author_metrics',
        store=True
    )
    first_publication = fields.Char(string="First Publication")
    last_publication = fields.Char(string="Last Publication")

    @api.depends('book_ids.date_published')
    def _compute_author_metrics(self):
        for partner in self:
            books = partner.book_ids
            partner.book_count = len(books)
            dates = sorted(d for d in books.mapped('date_published') if d)
            if dates:
                partner.first_publication = dates[0].strftime('%Y-%m-%d')
                partner.last_publication = dates[-1].strftime('%Y-%m-%d')
            else:
                partner.first_publication = False
                partner.last_publication = False

    @api.depends('loan_ids.state', 'loan_ids.is_overdue')
    def _compute_loan_metrics(self):
        """Computes loan metrics for borrowers."""
        for partner in self:
            # Filtrar empréstimos ativos
            active_loans = partner.loan_ids.filtered(lambda l: l.state == 'ongoing')
            partner.active_loans_count = len(active_loans)
            
            # Filtrar empréstimos em atraso
            overdue_loans = active_loans.filtered(lambda l: l.is_overdue)
            partner.overdue_loans_count = len(overdue_loans)
            
            # Empréstimos em dia (ativos mas não em atraso)
            partner.on_time_loans_count = partner.active_loans_count - partner.overdue_loans_count

    def toggle_author_status(self):
        """Marca/desmarca como autor."""
        for partner in self:
            partner.is_author = not partner.is_author

    def action_view_active_loans(self):
        """Abre uma visualização com todos os empréstimos ativos do usuário."""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Active Loans - %s' % self.name,
            'view_mode': 'list,form',
            'res_model': 'library.book.loan',
            'domain': [('partner_id', '=', self.id), ('state', '=', 'ongoing')],
            'context': {'default_partner_id': self.id},
        }

    def action_view_overdue_loans(self):
        """Abre uma visualização com todos os empréstimos em atraso do usuário."""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Overdue Loans - %s' % self.name,
            'view_mode': 'list,form',
            'res_model': 'library.book.loan',
            'domain': [
                ('partner_id', '=', self.id), 
                ('state', '=', 'ongoing'),
                ('is_overdue', '=', True)
            ],
            'context': {'default_partner_id': self.id},
        }

    def action_view_books(self):
        """Abre uma visualização com todos os livros do autor."""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Books by %s' % self.name,
            'view_mode': 'list,form',
            'res_model': 'library.book',
            'domain': [('author_id', '=', self.id)],
            'context': {'default_author_id': self.id},
        }

    def action_open_author_books(self):
        """Abre os livros deste autor em kanban/list/form."""
        self.ensure_one()
        action = self.env.ref(
            'library_app.action_library_author_books',
            raise_if_not_found=False
        )
        if not action:
            return {
                'name': 'Books',
                'type': 'ir.actions.act_window',
                'res_model': 'library.book',
                'view_mode': 'kanban,list,form',
                'domain': [('author_id', '=', self.id)],
                'context': {'default_author_id': self.id},
            }
        result = action.read()[0]
        result.update({
            'domain': [('author_id', '=', self.id)],
            'context': {'default_author_id': self.id},
        })
        return result