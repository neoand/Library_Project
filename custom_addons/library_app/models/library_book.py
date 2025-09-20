# -*- coding: utf-8 -*-
from datetime import date, timedelta

from odoo import models, fields, api
from odoo.exceptions import ValidationError

class LibraryBook(models.Model):
    _name = 'library.book'
    _description = 'Library Book'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name'

    # Campos principais
    name = fields.Char(string='Title', required=True, tracking=True)
    isbn = fields.Char(string='ISBN', index=True, tracking=True)
    pages = fields.Integer(string='Number of Pages', tracking=True)
    cover = fields.Binary(string='Cover Image', attachment=True)
    description = fields.Html(string='Description', tracking=True)

    # Relacionamentos
    author_id = fields.Many2one(
        comodel_name='res.partner',
        string='Author',
        domain=[('is_company', '=', False), ('is_author', '=', True)], # Adicionado filtro para is_author
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
        tracking=True,
        group_expand='_read_group_stage_ids', # Para visualização Kanban
    )
    user_id = fields.Many2one(
        comodel_name='res.users',
        string='Library Responsible',
        default=lambda self: self.env.user,
        index=True,
        tracking=True
    )

    # Publicação e status
    date_published = fields.Date(string='Published On', tracking=True)
    active = fields.Boolean(string='Active', default=True, tracking=True)
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
    
    # Novo campo computado para status do livro
    book_status = fields.Selection([
        ('available', 'Available'),
        ('borrowed', 'Borrowed'),
        ('lost', 'Lost'),
    ], string='Book Status', compute='_compute_book_status', store=True, tracking=True)

    # Novo campo computado para data de retorno esperada
    expected_return_date = fields.Date(
        string='Expected Return Date',
        compute='_compute_expected_return_date',
        store=False # Não armazenar, pois pode mudar frequentemente
    )
    
    # Status e disponibilidade (campos simples, não mais relacionados ao estoque)
    total_copies = fields.Integer(string='Total Copies', default=1, tracking=True)
    available_copies = fields.Integer(
        string='Available Copies',
        compute='_compute_availability',
        store=True,
        help="Number of copies available for lending"
    )
    
    copies_on_loan = fields.Integer(
        string='Copies on Loan',
        compute='_compute_availability',
        store=True,
        help="Number of copies currently loaned"
    )

    # Restrições de unicidade
    _sql_constraints = [
        ('isbn_unique', 'unique(isbn)', 'ISBN must be unique.'),
    ]

    # Métodos computados
    @api.depends('loan_ids')
    def _compute_loan_count(self):
        """Conta quantos empréstimos já foram feitos deste livro."""
        for rec in self:
            rec.loan_count = len(rec.loan_ids)

    @api.depends('loan_ids.state', 'loan_ids.quantity', 'total_copies')
    def _compute_book_status(self):
        """Determina o status atual do livro com base nos empréstimos."""
        for book in self:
            total_on_loan = sum(book.loan_ids.filtered(lambda l: l.state == 'ongoing').mapped('quantity'))
            lost_copies = sum(book.loan_ids.filtered(lambda l: l.state == 'lost').mapped('quantity'))
            available = book.total_copies - total_on_loan
            
            if lost_copies > 0 and available <= 0 and total_on_loan <= 0:
                book.book_status = 'lost'
            elif available <= 0:
                book.book_status = 'borrowed' 
            else:
                book.book_status = 'available'
    
    @api.depends('loan_ids.state', 'loan_ids.quantity', 'total_copies')
    def _compute_availability(self):
        """Calcula disponibilidade de cópias baseada em empréstimos e total de cópias."""
        for book in self:
            total_on_loan = sum(book.loan_ids.filtered(lambda l: l.state == 'ongoing').mapped('quantity'))
            book.copies_on_loan = total_on_loan
            book.available_copies = max(0, book.total_copies - total_on_loan)

    @api.depends('loan_ids.expected_return_date', 'loan_ids.state')
    def _compute_expected_return_date(self):
        """Calcula a data de retorno esperada do empréstimo ativo."""
        for book in self:
            active_loan = book.loan_ids.filtered(lambda l: l.state == 'ongoing')
            if active_loan:
                book.expected_return_date = active_loan[0].expected_return_date
            else:
                book.expected_return_date = False

    # Restrições e validações
    @api.constrains('isbn')
    def _check_isbn_format(self):
        """ISBN deve ter 10 ou 13 caracteres."""
        for rec in self:
            if rec.isbn and len(rec.isbn) not in (10, 13):
                raise ValidationError('ISBN must be either 10 or 13 characters long.')

    # Sobrescrevendo métodos padrão
    @api.model_create_multi
    def create(self, vals_list):
        """
        Define stage padrão para novos livros.
        """
        default_stage = self.env['library.book.stage'].search([('is_default', '=', True)], limit=1)
        
        for vals in vals_list:
            # Configurações de estágio (biblioteca)
            if not vals.get('stage_id') and default_stage:
                vals['stage_id'] = default_stage.id
        
        return super().create(vals_list)

    def write(self, vals):
        """Sobrescreve o método write para adicionar lógica customizada."""
        # Exemplo: Adicionar alguma lógica antes de salvar
        # if 'name' in vals:
        #     _logger.info(f"Book name changed from {self.name} to {vals['name']}")
        res = super().write(vals)
        return res

    def unlink(self):
        """Impede a exclusão de livros com empréstimos ativos."""
        books_with_active_loans = self.filtered(lambda b: b.loan_ids.filtered(lambda l: l.state == 'ongoing'))
        if books_with_active_loans:
            raise ValidationError(
                "You cannot delete books that are currently borrowed. "
                "Please return them first."
            )
        return super().unlink()

    @api.depends('name', 'isbn')
    def name_get(self):
        """Retorna uma representação amigável do livro (Título [ISBN])."""
        result = []
        for book in self:
            name = book.name
            if book.isbn:
                name = f"{name} ({book.isbn})"
            result.append((book.id, name))
        return result

    @api.model
    def _read_group_stage_ids(self, stages, domain):
        """Expande os estágios para visualização Kanban.
        
        Args:
            stages: recordset of stages already in the result
            domain: current domain for the read_group
        
        Returns:
            All available stages for kanban view display
        """
        # Return all stages ordered by sequence
        return self.env['library.book.stage'].search([], order='sequence, name')

    # Métodos de ação
    def action_open_loans(self):
        """Abrir a lista de empréstimos deste livro."""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': f'Loans for {self.name}',
            'res_model': 'library.book.loan',
            'view_mode': 'list,form',
            'domain': [('book_id', '=', self.id)],
            'context': {'default_book_id': self.id},
        }

    def action_mark_available(self):
        """Marcar o livro como disponível (finaliza empréstimos ativos)."""
        self.ensure_one()
        active_loans = self.loan_ids.filtered(lambda l: l.state == 'ongoing')
        if active_loans:
            active_loans.write({'state': 'done', 'return_date': fields.Date.today()})
        return True

    def action_borrow_book(self):
        """Ação rápida para emprestar o livro."""
        self.ensure_one()
        if self.available_copies <= 0:
            raise ValidationError(f"No copies available for borrowing. Available: {self.available_copies}, On loan: {self.copies_on_loan}")
        
        # Calcular data de retorno esperada (15 dias por padrão)
        expected_date = fields.Date.today() + timedelta(days=15)
        
        return {
            'type': 'ir.actions.act_window',
            'name': 'New Loan',
            'res_model': 'library.book.loan',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_book_id': self.id,
                'default_loan_date': fields.Date.today(),
                'default_expected_return_date': expected_date,
                'default_state': 'ongoing',
                'form_view_initial_mode': 'edit',
            },
        }