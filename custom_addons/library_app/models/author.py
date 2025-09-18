# -*- coding: utf-8 -*-
# library_app/models/author.py

from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import date


class ResPartner(models.Model):
    _inherit = 'res.partner'

    # Campo para identificar autores
    is_author = fields.Boolean(
        string='Is Author',
        default=False,
        help="Check this box if this contact is an author"
    )

    # Campos biográficos do autor
    birth_date = fields.Date(
        string='Birth Date',
        help="Author's date of birth"
    )

    death_date = fields.Date(
        string='Death Date',
        help="Author's date of death (if applicable)"
    )

    birth_place = fields.Char(
        string='Birth Place',
        help="Author's place of birth"
    )

    biography = fields.Html(
        string='Biography',
        help="Detailed biography of the author",
        sanitize=True,
        strip_style=False
    )

    awards = fields.Text(
        string='Awards',
        help="Literary awards and recognitions received by the author"
    )

    website = fields.Char(
        string='Author Website',
        help="Official website of the author"
    )

    # Campos relacionados aos livros
    book_ids = fields.One2many(
        comodel_name='library.book',
        inverse_name='author_id',
        string='Authored Books',
        help="Books written by this author"
    )

    book_count = fields.Integer(
        string='Book Count',
        compute='_compute_book_count',
        store=True,
        help="Number of books written by this author"
    )

    # Campos computados para estatísticas
    age = fields.Integer(
        string='Age',
        compute='_compute_age',
        store=False,
        help="Current age of the author (if living) or age at death"
    )

    is_alive = fields.Boolean(
        string='Is Alive',
        compute='_compute_is_alive',
        store=False,
        help="Indicates if the author is still alive"
    )

    first_publication = fields.Date(
        string='First Publication',
        compute='_compute_publication_dates',
        store=True,
        help="Date of the author's first publication"
    )

    last_publication = fields.Date(
        string='Latest Publication',
        compute='_compute_publication_dates',
        store=True,
        help="Date of the author's most recent publication"
    )

    # Restrições de banco de dados
    _sql_constraints = [
        ('birth_before_death',
         'CHECK (death_date IS NULL OR birth_date IS NULL OR death_date >= birth_date)',
         'Death date must be after birth date if both are provided.'),
    ]

    # Métodos computados
    @api.depends('book_ids')
    def _compute_book_count(self):
        """Calcula o número de livros escritos pelo autor"""
        for author in self:
            author.book_count = len(author.book_ids)

    @api.depends('birth_date', 'death_date')
    def _compute_age(self):
        """Calcula a idade do autor (se vivo) ou idade ao falecer"""
        today = date.today()
        for author in self:
            if author.birth_date:
                if author.death_date:
                    # Autor falecido: calcular idade na morte
                    delta = author.death_date - author.birth_date
                    author.age = delta.days // 365
                else:
                    # Autor vivo: calcular idade atual
                    delta = today - author.birth_date
                    author.age = delta.days // 365
            else:
                author.age = 0

    @api.depends('death_date')
    def _compute_is_alive(self):
        """Determina se o autor está vivo"""
        for author in self:
            author.is_alive = not bool(author.death_date)

    @api.depends('book_ids.date_published')
    def _compute_publication_dates(self):
        """Calcula a primeira e última publicação do autor"""
        for author in self:
            if author.book_ids:
                dates = author.book_ids.mapped('date_published')
                valid_dates = [d for d in dates if d]
                if valid_dates:
                    author.first_publication = min(valid_dates)
                    author.last_publication = max(valid_dates)
                else:
                    author.first_publication = False
                    author.last_publication = False
            else:
                author.first_publication = False
                author.last_publication = False

    # Métodos de ação
    def action_view_books(self):
        """Abre a vista de livros do autor"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': f'Books by {self.name}',
            'res_model': 'library.book',
            'view_mode': 'tree,form,kanban',
            'domain': [('author_id', '=', self.id)],
            'context': {'default_author_id': self.id}
        }

    def toggle_author_status(self):
        """Alterna o status de autor do contato"""
        for author in self:
            author.is_author = not author.is_author
            # Se estiver marcando como autor, garantir que tem pelo menos um livro
            if author.is_author and not author.book_ids:
                # Criar um livro vazio se não houver livros
                self.env['library.book'].create({
                    'name': f'Untitled work by {author.name}',
                    'author_id': author.id
                })

    # Restrições e validações
    @api.constrains('birth_date', 'death_date')
    def _check_dates(self):
        """Valida que as datas de nascimento e morte são consistentes"""
        for author in self:
            if author.birth_date and author.death_date:
                if author.death_date < author.birth_date:
                    raise ValidationError("Death date cannot be before birth date.")

    @api.constrains('birth_date')
    def _check_birth_date(self):
        """Valida que a data de nascimento não é futura"""
        for author in self:
            if author.birth_date and author.birth_date > date.today():
                raise ValidationError("Birth date cannot be in the future.")

    # Sobrescrevendo métodos padrão
    def copy(self, default=None):
        """Sobrescreve o método de cópia para evitar copiar livros"""
        default = default or {}
        default['book_ids'] = False
        return super().copy(default)

    def unlink(self):
        """Impede a exclusão de autores que possuem livros"""
        authors_with_books = self.filtered(lambda a: a.book_count > 0)
        if authors_with_books:
            raise ValidationError(
                "You cannot delete authors who have books. "
                "Please reassign or delete their books first."
            )
        return super().unlink()