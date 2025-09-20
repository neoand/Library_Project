# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError

class LibraryBookCategory(models.Model):
    _name = 'library.book.category'
    _description = 'Library Book Category'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name'

    # Identificação
    name = fields.Char(
        string='Category Name', 
        required=True, 
        index=True, 
        tracking=True,
        help="Full name of the category (e.g., Fiction, Non-Fiction, Biography)"
    )
    code = fields.Char(
        string='Technical Code',
        required=True,
        index=True,
        copy=False,
        tracking=True,
        help="Short unique code for this category (e.g., FIC, NF, BIO)."
    )
    description = fields.Html(
        string='Description',
        tracking=True,
        help="Detailed description of this category"
    )
    
    # Configurações da categoria
    active = fields.Boolean(
        string='Active', 
        default=True, 
        tracking=True,
        help="Uncheck to archive this category"
    )
    color = fields.Integer(
        string='Color Index', 
        default=0,
        tracking=True,
        help="Color for kanban view visualization"
    )
    sequence = fields.Integer(
        string='Sequence', 
        default=10,
        tracking=True,
        help="Order of categories in lists"
    )
    
    # Categoria pai (hierarquia)
    parent_id = fields.Many2one(
        comodel_name='library.book.category',
        string='Parent Category',
        ondelete='cascade',
        tracking=True,
        help="Parent category for hierarchical organization"
    )
    child_ids = fields.One2many(
        comodel_name='library.book.category',
        inverse_name='parent_id',
        string='Child Categories'
    )
    
    # Responsável pela categoria
    user_id = fields.Many2one(
        comodel_name='res.users',
        string='Responsible',
        default=lambda self: self.env.user,
        tracking=True,
        help="User responsible for managing this category"
    )

    # Relacionamento com livros (espelha a definição em library.book)
    book_ids = fields.Many2many(
        comodel_name='library.book',
        relation='library_book_category_rel',
        column1='category_id',
        column2='book_id',
        string='Books'
    )

    # Métricas computadas (com tracking quando mudarem significativamente)
    book_count = fields.Integer(
        string='Book Count',
        compute='_compute_book_count',
        store=True,
        help="Total number of books in this category"
    )
    active_book_count = fields.Integer(
        string='Active Books',
        compute='_compute_active_book_count',
        store=True,
        help="Number of active books in this category"
    )
    
    # Restrições de unicidade
    _sql_constraints = [
        ('category_code_unique', 'unique(code)', 'Category code must be unique.'),
        ('category_name_unique', 'unique(name)', 'Category name must be unique.'),
    ]

    @api.depends('book_ids')
    def _compute_book_count(self):
        """Conta quantos livros estão associados a esta categoria."""
        for categ in self:
            categ.book_count = len(categ.book_ids)
    
    @api.depends('book_ids.active')
    def _compute_active_book_count(self):
        """Conta quantos livros ativos estão associados a esta categoria."""
        for categ in self:
            categ.active_book_count = len(categ.book_ids.filtered('active'))

    @api.constrains('parent_id')
    def _check_parent_recursion(self):
        """Impede recursão infinita na hierarquia."""
        if not self._check_recursion():
            raise ValidationError("You cannot create recursive category hierarchies.")

    def name_get(self):
        """Retorna nome com hierarquia se houver categoria pai."""
        result = []
        for category in self:
            name = category.name
            if category.parent_id:
                name = f"{category.parent_id.name} / {name}"
            result.append((category.id, name))
        return result
    
    def action_open_books(self):
        """Abre a lista de livros desta categoria."""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': f'Books in {self.name}',
            'res_model': 'library.book',
            'view_mode': 'kanban,list,form',
            'domain': [('category_ids', 'in', [self.id])],
            'context': {
                'default_category_ids': [(6, 0, [self.id])],
                'search_default_group_by_stage': 1,
            },
        }
    
    def action_archive_with_audit(self):
        """Arquiva categoria com registro de auditoria."""
        self.ensure_one()
        if self.book_count > 0:
            # Cria uma mensagem de auditoria antes de arquivar
            self.message_post(
                body=f"Category '{self.name}' archived with {self.book_count} books assigned.",
                message_type='comment',
                subtype_xmlid='mail.mt_note'
            )
        self.active = False
        return True