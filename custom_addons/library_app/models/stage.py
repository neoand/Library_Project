# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError

class LibraryBookStage(models.Model):
    _name = 'library.book.stage'
    _description = 'Book Stage'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'sequence, name'

    # Identificação
    name = fields.Char(string='Stage Name', required=True, tracking=True)
    code = fields.Char(
        string='Technical Code',
        required=True,
        index=True,
        copy=False,
        help="Technical code for this stage (e.g., 'draft', 'in_progress', 'done').",
        tracking=True,
    )
    description = fields.Text(string='Description', help='Describe the purpose and rules of this stage.')
    sequence = fields.Integer(string='Sequence', default=1)

    # Comportamento visual/kanban
    fold = fields.Boolean(string='Folded in Kanban', tracking=True)
    color = fields.Integer(string='Color Index', default=0)

    # Regras de negócio
    is_default = fields.Boolean(string='Default Stage', tracking=True)

    # Relacionamentos e métricas
    book_ids = fields.One2many(
        comodel_name='library.book',
        inverse_name='stage_id',
        string='Books'
    )
    book_count = fields.Integer(
        string='Book Count',
        compute='_compute_book_count',
        store=True
    )

    _sql_constraints = [
        ('stage_code_unique', 'unique(code)', 'Stage code must be unique.'),
    ]

    @api.depends('book_ids')
    def _compute_book_count(self):
        for stage in self:
            stage.book_count = len(stage.book_ids)

    @api.constrains('is_default')
    def _check_only_one_default(self):
        for stage in self:
            if stage.is_default:
                others = self.search([('is_default', '=', True), ('id', '!=', stage.id)])
                if others:
                    raise ValidationError("Only one stage can be the default.")

    @api.model_create_multi
    def create(self, vals_list):
        if any(vals.get('is_default') for vals in vals_list):
            self.search([('is_default', '=', True)]).write({'is_default': False})
        return super().create(vals_list)

    def write(self, vals):
        if vals.get('is_default'):
            self.search([('is_default', '=', True)]).write({'is_default': False})
        return super().write(vals)