# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError

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
        domain=[('is_company', '=', False)],  # Apenas pessoas físicas
        ondelete='restrict',  # Impede deletar contatos com empréstimos
        required=True,  # Campo obrigatório
        tracking=True,
        help="Select the person who is borrowing this book"
    )
    loan_date = fields.Date(
        string='Loan Date',
        default=fields.Date.context_today,
        required=True,
        tracking=True,
    )
    return_date = fields.Date(string='Return Date', tracking=True)
    expected_return_date = fields.Date(string='Expected Return Date', tracking=True)
    state = fields.Selection([
        ('ongoing', 'Ongoing'),
        ('done', 'Returned'),
        ('lost', 'Lost'),
    ], string='Status', default='ongoing', tracking=True)
    
    # Controle de quantidade
    quantity = fields.Integer(
        string='Quantity',
        default=1,
        required=True,
        tracking=True,
        help="Number of copies being loaned"
    )
    
    # Controle de perdas
    loss_type = fields.Selection([
        ('not_returned', 'Not Returned by Borrower'),
        ('damaged', 'Damaged/Unusable Condition'),
        ('missing', 'Missing from Library'),
    ], string='Loss Type', tracking=True)
    
    loss_description = fields.Text(
        string='Loss Description',
        help="Detailed description of the loss or damage"
    )

    @api.constrains('partner_id')
    def _check_borrower(self):
        """Valida que o mutuário foi selecionado."""
        for loan in self:
            if not loan.partner_id:
                raise ValidationError("A borrower must be selected for the loan.")
    
    @api.constrains('quantity')
    def _check_quantity(self):
        """Valida a quantidade solicitada."""
        for loan in self:
            if loan.quantity <= 0:
                raise ValidationError("Quantity must be greater than zero.")
    
    @api.constrains('book_id', 'state', 'quantity')
    def _check_availability(self):
        """Garante que não se empreste mais cópias do que disponível."""
        for loan in self:
            if loan.state == 'ongoing' and loan.book_id and loan.quantity:
                # Calcular total de cópias já emprestadas (excluindo este empréstimo)
                other_loans = self.search([
                    ('book_id', '=', loan.book_id.id),
                    ('state', '=', 'ongoing'),
                    ('id', '!=', loan.id)
                ])
                total_borrowed = sum(other_loans.mapped('quantity'))
                
                # Verificar se a quantidade solicitada excede a disponível
                available_copies = loan.book_id.total_copies - total_borrowed
                if loan.quantity > available_copies:
                    raise ValidationError(
                        f"Não é possível emprestar {loan.quantity} cópia(s) do livro '{loan.book_id.name}'. "
                        f"Total de cópias: {loan.book_id.total_copies}, "
                        f"Já emprestadas: {total_borrowed}, "
                        f"Disponíveis: {available_copies}"
                    )

    @api.model_create_multi
    def create(self, vals_list):
        """Sobrescreve o método create para adicionar lógica de negócio."""
        loans = super().create(vals_list)
        return loans

    def write(self, vals):
        """Sobrescreve o método write para adicionar lógica de negócio."""
        result = super().write(vals)
        return result

    def unlink(self):
        """Override unlink to handle stock movements on state changes."""
        for loan in self:
            if loan.state == 'ongoing':
                raise ValidationError("Cannot delete an ongoing loan.")
        return super().unlink()

    def action_return_book(self):
        """Ação para marcar um livro como devolvido."""
        self.ensure_one()
        self.write({
            'state': 'done',
            'return_date': fields.Date.today()
        })
        
    def action_lost_book(self):
        """Ação para marcar um livro como perdido."""
        self.ensure_one()
        self.write({'state': 'lost'})

    # Funções de Cômputo
    
    @api.depends('loan_date', 'return_date', 'state')
    def _compute_loan_duration(self):
        """Computes loan duration in days.

        - If `return_date` is set: duration = return_date - loan_date
        - If loan is ongoing: duration = today - loan_date
        - Otherwise: 0
        """
        for record in self:
            if record.loan_date:
                end_date = record.return_date or fields.Date.today()
                delta = end_date - record.loan_date
                record.loan_duration = max(0, delta.days)
            else:
                record.loan_duration = 0

    loan_duration = fields.Integer(
        string='Loan Duration (days)',
        compute='_compute_loan_duration',
        store=True,
    )
    
    @api.depends('state', 'expected_return_date')
    def _compute_is_overdue(self):
        """Flags loan as overdue when ongoing and today > expected_return_date."""
        today = fields.Date.today()
        for record in self:
            record.is_overdue = bool(
                record.state == 'ongoing'
                and record.expected_return_date
                and today > record.expected_return_date
            )

    is_overdue = fields.Boolean(
        string='Is Overdue?',
        compute='_compute_is_overdue',
        store=True,
    )