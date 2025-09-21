# Development Patterns & Best Practices - Library Project

Este arquivo documenta padrões e boas práticas específicas do projeto para manter consistência e qualidade.

---

## 🏗️ **Padrões Arquiteturais**

### **Modelo de Dados**

#### ✅ **Padrão Preferido: Modelo Independente**
```python
class LibraryBook(models.Model):
    _name = 'library.book'
    _description = 'Library Book'
    _inherit = ['mail.thread', 'mail.activity.mixin']  # Apenas funcionalidades essenciais
    _order = 'name'
```

**Justificativa**: Simplicidade, performance e domínio específico (baseado em ADR-001)

#### ⚠️ **Quando Considerar Herança**
Apenas quando o domínio for **genuinamente compatível**:
- Sistema híbrido (biblioteca + livraria comercial)
- Necessidade real de campos comerciais (preços, impostos, etc.)

### **Estrutura de Campos**

#### **Campos Obrigatórios**
```python
# Identificação básica
name = fields.Char(string='Title', required=True, tracking=True)
description = fields.Html(string='Description', tracking=True)

# Rastreabilidade (sempre incluir)
_inherit = ['mail.thread', 'mail.activity.mixin']

# Ordenação padrão
_order = 'name'  # ou campo mais relevante
```

#### **Campos Específicos do Domínio**
```python
# Biblioteca - Controle de cópias
total_copies = fields.Integer(default=1)
available_copies = fields.Integer(compute='_compute_available_copies', store=True)
copies_on_loan = fields.Integer(compute='_compute_copies_on_loan', store=True)

# Relacionamentos
author_id = fields.Many2one('res.partner', string='Author', 
                           domain=[('is_company', '=', False), ('is_author', '=', True)])
loan_ids = fields.One2many('library.book.loan', 'book_id', string='Loans')
```

### **Computação de Campos**

#### **Padrão para Campos Computados**
```python
@api.depends('loan_ids.state')
def _compute_available_copies(self):
    """Padrão: compute + store=True para performance"""
    for book in self:
        active_loans = book.loan_ids.filtered(lambda l: l.state == 'ongoing')
        book.available_copies = book.total_copies - len(active_loans)
```

**Regras:**
- ✅ Use `store=True` quando o campo é usado em views/searches
- ✅ Inclua `@api.depends()` sempre
- ✅ Loop `for record in self:` para compatibilidade com múltiplos registros

---

## 📁 **Estrutura de Arquivos**

### **Organização Padrão**
```
custom_addons/library_app/
├── __manifest__.py          # Metadados e dependências
├── __init__.py             # Imports dos modelos
├── models/                 # Lógica de negócio
│   ├── __init__.py
│   ├── library_book.py     # Modelo principal
│   ├── loan.py            # Modelos relacionados
│   ├── partner.py         # Extensions de modelos existentes
│   └── category.py        # Modelos auxiliares
├── views/                 # Interface do usuário  
│   ├── book_view.xml      # Views (form, list, kanban)
│   ├── book_action.xml    # Actions (separado das views)
│   ├── book_search.xml    # Search views (separado)
│   └── library_menu.xml   # Menu structure
├── security/              # Controle de acesso
│   ├── security.xml       # Grupos e regras
│   └── ir.model.access.csv # Permissões de modelo
├── data/                  # Dados iniciais
│   └── library_book_stage_data.xml
└── static/                # Assets (CSS, JS, images)
    └── src/css/
        └── chatter_layout.css
```

### **Convenções de Nomenclatura**

#### **Arquivos**
- `model_name_view.xml` - Views principais
- `model_name_action.xml` - Actions (separado)  
- `model_name_search.xml` - Search views
- `module_menu.xml` - Estrutura de menus
- `model_data.xml` - Dados iniciais

#### **IDs XML**
```xml
<!-- Padrão: model_name_view_type -->
<record id="library_book_view_form" model="ir.ui.view">
<record id="library_book_action_window" model="ir.actions.act_window">
<record id="library_book_menu_main" model="ir.ui.menu">
```

---

## 🎨 **Padrões de Views**

### **Form View**
```xml
<form string="Book">
    <sheet>
        <!-- Header com botões de ação -->
        <div class="oe_button_box" name="button_box">
            <button name="action_borrow_book" type="object" 
                    class="oe_stat_button" icon="fa-book">
                <field name="copies_on_loan" widget="statinfo" 
                       string="On Loan"/>
            </button>
        </div>
        
        <!-- Campos principais -->
        <group>
            <group>
                <field name="name"/>
                <field name="author_id"/>
                <field name="isbn"/>
            </group>
            <group>
                <field name="pages"/>
                <field name="total_copies"/>
                <field name="available_copies"/>
            </group>
        </group>
        
        <!-- Chatter -->
        <chatter/>
    </sheet>
</form>
```

### **List View (Odoo 18)**
```xml
<!-- Use 'list' ao invés de 'tree' no Odoo 18 -->
<list string="Books">
    <field name="name"/>
    <field name="author_id"/>
    <field name="book_status" widget="badge"/>
    <field name="available_copies"/>
</list>
```

### **Kanban View**
```xml
<kanban default_group_by="stage_id" class="o_kanban_small_column">
    <templates>
        <!-- Use 'card' ao invés de 'kanban-box' -->
        <t t-name="card">
            <div class="oe_kanban_global_click">
                <div class="oe_kanban_content">
                    <h4><field name="name"/></h4>
                    <div>Author: <field name="author_id"/></div>
                </div>
            </div>
        </t>
    </templates>
</kanban>
```

---

## 🔐 **Segurança**

### **Padrão Simples (Biblioteca)**
```csv
id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink
access_library_book_user,library.book.user,model_library_book,base.group_user,1,1,1,1
access_library_book_loan_user,library.book.loan.user,model_library_book_loan,base.group_user,1,1,1,1
```

**Princípio**: Para bibliotecas acadêmicas, simplicidade > complexidade na segurança

---

## 🚀 **Performance**

### **Boas Práticas**

#### **Campos Computados**
```python
# ✅ BOM: compute com store=True para campos usados em views
available_copies = fields.Integer(compute='_compute_available_copies', store=True)

# ❌ RUIM: compute sem store para campos em list views
available_copies = fields.Integer(compute='_compute_available_copies')
```

#### **Domínios Eficientes**
```python
# ✅ BOM: Domain específico
author_id = fields.Many2one('res.partner', 
                           domain=[('is_company', '=', False), ('is_author', '=', True)])

# ❌ RUIM: Domain muito amplo
author_id = fields.Many2one('res.partner')  # Todos os contatos
```

#### **Consultas de Banco**
```python
# ✅ BOM: Usar filtered() para lógica em memória
active_loans = book.loan_ids.filtered(lambda l: l.state == 'ongoing')

# ❌ RUIM: Múltiplas queries para dados já carregados
active_loans = self.env['library.book.loan'].search([('book_id', '=', book.id), ('state', '=', 'ongoing')])
```

---

## 🧪 **Testing**

### **Padrão de Teste**
```python
# Future: Estrutura para testes automatizados
tests/
├── __init__.py
├── test_library_book.py
├── test_loan.py
└── common.py  # Setup comum para testes
```

---

## 📦 **Deployment**

### **Manifest Padrão**
```python
{
    'name': 'Library App',
    'version': '18.0.1.0.0',
    'category': 'Productivity',
    'summary': 'Library Management System',
    'depends': ['base', 'contacts', 'mail', 'web'],  # Mínimo necessário
    'data': [
        # Ordem importante!
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/library_book_stage_data.xml',
        'views/book_view.xml',
        'views/book_action.xml', 
        'views/library_menu.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'library_app/static/src/css/chatter_layout.css',
        ],
    },
    'installable': True,
    'auto_install': False,
    'application': True,
}
```

---

## 🔄 **Migration Guide**

### **De product.product para Modelo Independente**

**Checklist de migração:**
- [ ] Remover `_inherit = ['product.product']`
- [ ] Implementar campos básicos (name, description)
- [ ] Substituir campos de produto por específicos do domínio
- [ ] Limpar views de campos de produto
- [ ] Atualizar dependências no manifest
- [ ] Testar todas as funcionalidades

---

## 📝 **Template para Novos Módulos**

### **Estrutura Básica**
```python
# models/new_model.py
from odoo import models, fields, api

class NewModel(models.Model):
    _name = 'library.new_model'
    _description = 'New Model Description'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name'
    
    # Campos básicos
    name = fields.Char(string='Name', required=True, tracking=True)
    description = fields.Html(string='Description', tracking=True)
    active = fields.Boolean(default=True, tracking=True)
    
    # Relacionamentos
    # ...
    
    # Campos computados  
    # ...
    
    # Constraints
    @api.constrains('field_name')
    def _check_field_name(self):
        # Validação
        pass
        
    # Métodos de negócio
    def action_do_something(self):
        # Ação específica
        pass
```

---

## 🎨 **Padrões de Interface (UI/UX)**

### **Estrutura de Menus**

Para garantir uma experiência de usuário consistente e intuitiva, todos os novos módulos devem seguir uma estrutura de menu hierárquica, separando operações diárias de configurações.

**✅ Padrão de Estrutura de Menu:**
```xml
<!-- Menu Raiz -->
<menuitem id="menu_library_root" name="Library" sequence="10"/>

<!-- 1. Operações (Ações do dia a dia) -->
<menuitem id="menu_library_operations" name="Operations" parent="menu_library_root" sequence="1"/>
<menuitem id="menu_library_books" name="Books" parent="menu_library_operations" action="action_library_book" sequence="1"/>
<menuitem id="menu_library_loans" name="Loans" parent="menu_library_operations" action="action_library_book_loan" sequence="2"/>

<!-- 2. Catálogos (Dados mestres) -->
<menuitem id="menu_library_catalogs" name="Catalogs" parent="menu_library_root" sequence="2"/>
<menuitem id="menu_library_authors" name="Authors" parent="menu_library_catalogs" action="action_library_author" sequence="1"/>

<!-- 3. Configuração (Itens raramente modificados) -->
<menuitem id="menu_library_configuration" name="Configuration" parent="menu_library_root" sequence="3"/>
<menuitem id="menu_library_stages" name="Book Stages" parent="menu_library_configuration" action="action_library_book_stage" sequence="1"/>
```

**Justificativa (baseada em ADR-002):**
- **Intuitividade**: Alinha-se com os padrões nativos do Odoo.
- **Escalabilidade**: Facilita a adição de novos itens sem poluir a interface.
- **Organização**: Separa claramente as responsabilidades de cada menu.

### **Remoção de Elementos de UI Indesejados**

Quando um módulo dependente (transitivo) adiciona elementos de UI que são irrelevantes para o contexto do módulo atual, a remoção deve ser feita de forma robusta.

**⚠️ Problema Comum:**
- Tentar remover botões/campos com `xpath` pode falhar se eles forem adicionados dinamicamente com base em grupos de segurança.

**✅ Solução Preferida: Ocultar com CSS**
É a abordagem mais estável e garantida.

1.  **Identifique o Seletor do Elemento**: Use as ferramentas de desenvolvedor do navegador para encontrar um seletor CSS estável para o elemento (ex: `[name="action_view_stock_lots"]`).
2.  **Adicione a Regra CSS**: Inclua a regra no arquivo CSS do seu módulo.

```css
/* Exemplo em static/src/css/chatter_layout.css */
.o_form_view .oe_button_box .oe_stat_button[name="action_view_stock_lots"] {
    display: none !important;
}
```

**Justificativa (baseada em ADR-003):**
- **Robustez**: Funciona independentemente de grupos ou renderização dinâmica.
- **Manutenção**: Centraliza as customizações de estilo.

---

## 🐍 **Padrões de Código Python**

### **Estrutura e Organização**

#### **Imports**
```python
# Imports padrão
from odoo import models, fields, api

# Imports de bibliotecas externas
import logging
import datetime

# Imports internos do módulo
from . import partner
from . import loan
```

#### **Classes**
```python
class LibraryBook(models.Model):
    _name = 'library.book'
    _description = 'Library Book'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name'
    
    # Campos
    name = fields.Char(string='Title', required=True, tracking=True)
    description = fields.Html(string='Description', tracking=True)
    
    # Métodos
    @api.model
    def create(self, vals):
        # Lógica personalizada na criação
        return super(LibraryBook, self).create(vals)
```

#### **Métodos**
```python
# Métodos padrão do Odoo
@api.model
def create(self, vals):
    """Sobrescreve o método create para lógica personalizada"""
    return super(LibraryBook, self).create(vals)

@api.multi
def write(self, vals):
    """Sobrescreve o método write para lógica personalizada"""
    return super(LibraryBook, self).write(vals)

@api.multi
def unlink(self):
    """Sobrescreve o método unlink para lógica personalizada"""
    return super(LibraryBook, self).unlink()

# Métodos específicos do domínio
def action_borrow_book(self):
    """Ação para emprestar um livro"""
    # Lógica da ação
    pass
```

### **Boas Práticas**

#### **Uso de Decorators**
```python
@api.model
def create(self, vals):
    # Sempre use @api.model para métodos que criam registros
    pass

@api.depends('loan_ids.state')
def _compute_available_copies(self):
    # Sempre use @api.depends para campos computados
    pass
```

#### **Evitar Código Duplicado**
```python
# ❌ RUIM: Código duplicado em vários métodos
def action_approve_loan(self):
    # Lógica de aprovação
    ...

def action_reject_loan(self):
    # Lógica de rejeição (código duplicado)
    ...

# ✅ BOM: Extrair lógica comum para um método separado
def _common_loan_logic(self):
    # Lógica comum
    ...

def action_approve_loan(self):
    self._common_loan_logic()
    # Lógica adicional de aprovação

def action_reject_loan(self):
    self._common_loan_logic()
    # Lógica adicional de rejeição
```

#### **Tratamento de Exceções**
```python
try:
    # Código que pode gerar exceção
    ...
except Exception as e:
    # Log da exceção
    _logger.error('Erro ao processar: %s', e)
    raise  # Re-raise da exceção para o Odoo tratar
```

---

## 📜 **Documentação e Comentários**

### **Docstrings**
```python
class LibraryBook(models.Model):
    _name = 'library.book'
    _description = 'Library Book'
    
    def action_borrow_book(self):
        """
        Ação para emprestar um livro.

        Este método verifica a disponibilidade do livro e cria um registro de empréstimo
        se o livro estiver disponível.

        :return: True se o empréstimo foi bem-sucedido, False caso contrário.
        """
        ...
```

### **Comentários em Código**
```python
# Cálculo da disponibilidade de cópias
@api.depends('loan_ids.state')
def _compute_available_copies(self):
    """Padrão: compute + store=True para performance"""
    for book in self:
        active_loans = book.loan_ids.filtered(lambda l: l.state == 'ongoing')
        book.available_copies = book.total_copies - len(active_loans)
```

---

## 🧪 **Testes Automatizados**

### **Estrutura de Testes**
```python
# tests/test_library_book.py
from odoo.tests import TransactionCase

class TestLibraryBook(TransactionCase):

    def setUp(self):
        super(TestLibraryBook, self).setUp()
        # Criação de registros de teste
        self.book = self.env['library.book'].create({
            'name': 'Test Book',
            'author_id': self.env.ref('base.res_partner_1').id,
            'total_copies': 5,
        })

    def test_available_copies_computation(self):
        """Teste da computação de cópias disponíveis"""
        self.assertEqual(self.book.available_copies, 5)
        
        # Criação de um empréstimo em andamento
        self.env['library.book.loan'].create({
            'book_id': self.book.id,
            'state': 'ongoing',
        })
        
        # Reavaliação da disponibilidade
        self.assertEqual(self.book.available_copies, 4)
```

### **Execução de Testes**
```bash
# Executar todos os testes do módulo
$ pytest --odoo-bin=/caminho/para/odoo-bin --addons-path=/caminho/para/addons --log-level=test
```

---

## 📦 **Deployment**

### **Manifest Padrão**
```python
{
    'name': 'Library App',
    'version': '18.0.1.0.0',
    'category': 'Productivity',
    'summary': 'Library Management System',
    'depends': ['base', 'contacts', 'mail', 'web'],  # Mínimo necessário
    'data': [
        # Ordem importante!
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/library_book_stage_data.xml',
        'views/book_view.xml',
        'views/book_action.xml', 
        'views/library_menu.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'library_app/static/src/css/chatter_layout.css',
        ],
    },
    'installable': True,
    'auto_install': False,
    'application': True,
}
```

---

## 🔄 **Migration Guide**

### **De product.product para Modelo Independente**

**Checklist de migração:**
- [ ] Remover `_inherit = ['product.product']`
- [ ] Implementar campos básicos (name, description)
- [ ] Substituir campos de produto por específicos do domínio
- [ ] Limpar views de campos de produto
- [ ] Atualizar dependências no manifest
- [ ] Testar todas as funcionalidades

---

## 📝 **Template para Novos Módulos**

### **Estrutura Básica**
```python
# models/new_model.py
from odoo import models, fields, api

class NewModel(models.Model):
    _name = 'library.new_model'
    _description = 'New Model Description'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name'
    
    # Campos básicos
    name = fields.Char(string='Name', required=True, tracking=True)
    description = fields.Html(string='Description', tracking=True)
    active = fields.Boolean(default=True, tracking=True)
    
    # Relacionamentos
    # ...
    
    # Campos computados  
    # ...
    
    # Constraints
    @api.constrains('field_name')
    def _check_field_name(self):
        # Validação
        pass
        
    # Métodos de negócio
    def action_do_something(self):
        # Ação específica
        pass
```

---

**Última atualização**: 2024-09-20  
**Responsável**: Equipe de Desenvolvimento