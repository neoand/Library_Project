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
    
    @api.constrains('book_id', 'quantity', 'state')
    def _check_availability(self):
        """Valida se há cópias disponíveis para empréstimo."""
        for loan in self:
            if loan.state == 'ongoing' and loan.book_id:
                # Calcular quantas cópias já estão emprestadas (excluindo este empréstimo)
                other_loans = loan.book_id.loan_ids.filtered(
                    lambda l: l.state == 'ongoing' and l.id != loan.id
                )
                total_on_loan = sum(other_loans.mapped('quantity'))
                available = loan.book_id.qty_on_hand - total_on_loan
                
                if loan.quantity > available:
                    raise ValidationError(
                        f"Not enough copies available. Requested: {loan.quantity}, "
                        f"Available: {available}, Total copies: {loan.book_id.qty_on_hand}"
                    )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('return_date'):
                vals['state'] = 'ongoing'
        loans = super().create(vals_list)
        # Criar movimentação de estoque para empréstimos ativos
        for loan in loans:
            if loan.state == 'ongoing':
                loan._create_stock_move_out()
        return loans
    
    def write(self, vals):
        """Override write to handle stock movements on state changes."""
        old_states = {loan.id: loan.state for loan in self}
        result = super().write(vals)
        
        if 'state' in vals:
            for loan in self:
                old_state = old_states[loan.id]
                new_state = loan.state
                
                # Devolução: criar movimento de entrada
                if old_state == 'ongoing' and new_state == 'done':
                    loan._create_stock_move_in()
                
                # Perda: criar ajuste de inventário negativo
                elif old_state == 'ongoing' and new_state == 'lost':
                    loan._create_stock_move_loss()
                    
                # Reativação de empréstimo: criar movimento de saída
                elif old_state in ['done', 'lost'] and new_state == 'ongoing':
                    loan._create_stock_move_out()
        
        return result
    
    def _create_stock_move_out(self):
        """Cria movimento de saída do estoque para empréstimo."""
        if not self.book_id or self.quantity <= 0:
            return
            
        # Localização de origem (estoque) e destino (empréstimo)
        source_location = self.env.ref('stock.stock_location_stock')
        dest_location = self._get_loan_location()
        
        move_vals = {
            'name': f'Loan: {self.book_id.name}',
            'product_id': self.book_id.id,
            'product_uom': self.book_id.uom_id.id,
            'product_uom_qty': self.quantity,
            'location_id': source_location.id,
            'location_dest_id': dest_location.id,
            'origin': f'Loan/{self.id}',
        }
        
        move = self.env['stock.move'].create(move_vals)
        move._action_confirm()
        move._action_done()
    
    def _create_stock_move_in(self):
        """Cria movimento de entrada no estoque para devolução."""
        if not self.book_id or self.quantity <= 0:
            return
            
        # Localização de origem (empréstimo) e destino (estoque)
        source_location = self._get_loan_location()
        dest_location = self.env.ref('stock.stock_location_stock')
        
        move_vals = {
            'name': f'Return: {self.book_id.name}',
            'product_id': self.book_id.id,
            'product_uom': self.book_id.uom_id.id,
            'product_uom_qty': self.quantity,
            'location_id': source_location.id,
            'location_dest_id': dest_location.id,
            'origin': f'Return/{self.id}',
        }
        
        move = self.env['stock.move'].create(move_vals)
        move._action_confirm()
        move._action_done()
    
    def _create_stock_move_loss(self):
        """Cria ajuste de inventário negativo para perda."""
        if not self.book_id or self.quantity <= 0:
            return
            
        # Localização de origem (empréstimo) e destino (perda)
        source_location = self._get_loan_location()
        dest_location = self.env.ref('stock.stock_location_scrapped')
        
        move_vals = {
            'name': f'Loss: {self.book_id.name} ({self.loss_type or "Unknown"})',
            'product_id': self.book_id.id,
            'product_uom': self.book_id.uom_id.id,
            'product_uom_qty': self.quantity,
            'location_id': source_location.id,
            'location_dest_id': dest_location.id,
            'origin': f'Loss/{self.id}',
        }
        
        move = self.env['stock.move'].create(move_vals)
        move._action_confirm()
        move._action_done()
    
    def _get_loan_location(self):
        """Obtém ou cria a localização virtual para empréstimos."""
        # Tentar usar a localização criada por dados primeiro
        try:
            location = self.env.ref('library_app.stock_location_library_loans')
        except ValueError:
            # Se não encontrar, buscar por nome ou criar
            location = self.env['stock.location'].search([
                ('name', '=', 'Library Loans'),
                ('usage', '=', 'internal')
            ], limit=1)
            
            if not location:
                # Criar localização para empréstimos
                parent_location = self.env.ref('stock.stock_location_locations')
                location = self.env['stock.location'].create({
                    'name': 'Library Loans',
                    'usage': 'internal',
                    'location_id': parent_location.id,
                })
        
        return location