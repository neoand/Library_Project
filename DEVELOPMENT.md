# 🔧 Guia de Desenvolvimento - Library Project

## 📋 Fluxo de Trabalho para Desenvolvedores

Este guia explica como trabalhar eficientemente com o projeto Library, fazer modificações e contribuições.

## 🚀 Configuração do Ambiente de Desenvolvimento

### 1. Preparação Inicial

```bash
# Clone o repositório
git clone https://github.com/neoand/Library_Project.git
cd Library_Project

# Crie uma branch para sua feature
git checkout -b feature/minha-nova-funcionalidade

# Configure o ambiente virtual (opcional, mas recomendado)
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows
```

### 2. Configuração do Odoo para Desenvolvimento

```bash
# Inicie o Odoo em modo de desenvolvimento
./odoo-bin -d biblioteca_dev \
    --addons-path=/caminho/para/odoo/addons,/caminho/para/Library_Project/custom_addons \
    --dev=reload,qweb,werkzeug,xml \
    --log-level=debug
```

**Parâmetros importantes**:
- `--dev=reload`: Recarrega automaticamente quando arquivos Python mudam
- `--dev=qweb`: Recompila templates QWeb automaticamente
- `--dev=xml`: Recarrega dados XML automaticamente
- `--log-level=debug`: Mostra logs detalhados

## 📁 Estrutura de Desenvolvimento

### Organização dos Arquivos

```
custom_addons/library_app/
├── models/                 # 🐍 Lógica de negócio
│   ├── __init__.py
│   ├── book.py            # ← Modelo principal
│   ├── author.py          # ← Extensão de res.partner
│   ├── category.py        # ← Categorias
│   ├── stage.py           # ← Estágios de workflow
│   └── loan.py            # ← Sistema de empréstimos
├── views/                 # 🎨 Interface do usuário
│   ├── book_view.xml      # ← Forms e listas
│   ├── book_kanban.xml    # ← Visualização kanban
│   ├── library_menu.xml   # ← Menu principal
│   └── *_action.xml       # ← Ações dos menus
├── data/                  # 📊 Dados iniciais
├── security/              # 🔒 Permissões
└── static/               # 🖼️ Recursos estáticos
```

## 🔨 Padrões de Desenvolvimento

### 1. Criando um Novo Modelo

```python
# models/novo_modelo.py
from odoo import models, fields, api
from odoo.exceptions import ValidationError

class LibraryNovoModelo(models.Model):
    _name = 'library.novo.modelo'
    _description = 'Descrição do Novo Modelo'
    _inherit = ['mail.thread', 'mail.activity.mixin']  # Para chatter
    _order = 'name'
    
    # Campos básicos
    name = fields.Char(string='Nome', required=True, tracking=True)
    active = fields.Boolean(string='Ativo', default=True)
    
    # Relacionamentos
    book_ids = fields.One2many('library.book', 'novo_modelo_id', string='Livros')
    
    # Campos computados
    book_count = fields.Integer(string='Total de Livros', compute='_compute_book_count')
    
    # Métodos computados
    @api.depends('book_ids')
    def _compute_book_count(self):
        for record in self:
            record.book_count = len(record.book_ids)
    
    # Validações
    @api.constrains('name')
    def _check_name(self):
        for record in self:
            if not record.name or len(record.name) < 3:
                raise ValidationError("Nome deve ter pelo menos 3 caracteres")
```

**Não esqueça de**:
1. Adicionar ao `models/__init__.py`
2. Criar as views XML
3. Adicionar permissões em `security/`

### 2. Criando Views

```xml
<!-- views/novo_modelo_view.xml -->
<odoo>
    <data>
        <!-- Form View -->
        <record id="view_library_novo_modelo_form" model="ir.ui.view">
            <field name="name">library.novo.modelo.form</field>
            <field name="model">library.novo.modelo</field>
            <field name="arch" type="xml">
                <form string="Novo Modelo">
                    <header>
                        <!-- Botões de ação aqui -->
                    </header>
                    <sheet>
                        <group>
                            <group>
                                <field name="name"/>
                                <field name="active"/>
                            </group>
                            <group>
                                <field name="book_count"/>
                            </group>
                        </group>
                        <notebook>
                            <page string="Livros">
                                <field name="book_ids"/>
                            </page>
                        </notebook>
                    </sheet>
                    <div class="oe_chatter">
                        <field name="message_follower_ids"/>
                        <field name="activity_ids"/>
                        <field name="message_ids"/>
                    </div>
                </form>
            </field>
        </record>
        
        <!-- Tree View -->
        <record id="view_library_novo_modelo_tree" model="ir.ui.view">
            <field name="name">library.novo.modelo.tree</field>
            <field name="model">library.novo.modelo</field>
            <field name="arch" type="xml">
                <tree string="Novos Modelos">
                    <field name="name"/>
                    <field name="book_count"/>
                    <field name="active"/>
                </tree>
            </field>
        </record>
    </data>
</odoo>
```

### 3. Adicionando ao Menu

```xml
<!-- views/novo_modelo_action.xml -->
<odoo>
    <data>
        <record id="action_library_novo_modelo" model="ir.actions.act_window">
            <field name="name">Novos Modelos</field>
            <field name="res_model">library.novo.modelo</field>
            <field name="view_mode">tree,form</field>
            <field name="context">{}</field>
            <field name="help" type="html">
                <p class="o_view_nocontent_smiling_face">
                    Crie seu primeiro novo modelo!
                </p>
            </field>
        </record>
        
        <menuitem id="menu_library_novo_modelo"
                  name="Novos Modelos"
                  parent="menu_library_configuration"
                  action="action_library_novo_modelo"
                  sequence="10"/>
    </data>
</odoo>
```

## 🧪 Testando Modificações

### 1. Testes Manuais

```bash
# 1. Atualize o módulo após mudanças
# Via interface: Apps → Library App → Upgrade
# Ou via linha de comando:
./odoo-bin -d biblioteca_dev -u library_app

# 2. Teste funcionalidades básicas:
# - Criar registro
# - Editar registro
# - Excluir registro
# - Testar validações
# - Verificar relacionamentos
```

### 2. Teste de Dados

```python
# Crie dados de teste para validar
# Via interface web ou shell do Odoo:

# Iniciar shell do Odoo
./odoo-bin shell -d biblioteca_dev

# No shell:
env['library.novo.modelo'].create({
    'name': 'Teste'
})
```

## 🐛 Debug e Resolução de Problemas

### 1. Logs Úteis

```python
# Adicione logs em seus métodos para debug
import logging
_logger = logging.getLogger(__name__)

def meu_metodo(self):
    _logger.debug("Iniciando método")
    _logger.info("Processando %s registros", len(self))
    _logger.warning("Algo pode estar errado")
    _logger.error("Erro encontrado: %s", str(e))
```

### 2. Debug com PDB

```python
# Adicione breakpoints para debug interativo
def meu_metodo(self):
    import pdb; pdb.set_trace()
    # Seu código aqui
```

### 3. Problemas Comuns

**Erro: "KeyError: 'library.novo.modelo'"**
- Verifique se o modelo está em `models/__init__.py`
- Confirme se o módulo foi atualizado

**Views não aparecem**
- Verifique sintaxe XML
- Confirme se as actions estão definidas antes dos menus no `__manifest__.py`

**Erro de permissão**
- Adicione linhas no `ir.model.access.csv`
- Verifique grupos de segurança

## 📋 Checklist de Desenvolvimento

### ✅ Antes de começar
- [ ] Branch criada a partir da main
- [ ] Ambiente de desenvolvimento configurado
- [ ] Odoo rodando em modo `--dev`

### ✅ Durante o desenvolvimento
- [ ] Código seguindo padrões do Odoo
- [ ] Comentários em português/inglês
- [ ] Logs de debug removidos
- [ ] Testado manualmente

### ✅ Antes do commit
- [ ] Módulo atualizado e funcionando
- [ ] Sem erros no log
- [ ] Views carregando corretamente
- [ ] Permissões configuradas
- [ ] Dados de teste criados

### ✅ Preparando o Pull Request
- [ ] Commit com mensagem descritiva
- [ ] Push para sua branch
- [ ] Pull Request com descrição clara
- [ ] Screenshots se houver mudanças visuais

## 🔄 Workflow de Contribuição

```bash
# 1. Sua feature pronta?
git add .
git commit -m "feat: adiciona novo modelo para controle de estoque"
git push origin feature/controle-estoque

# 2. Abra Pull Request no GitHub

# 3. Após aprovação e merge:
git checkout main
git pull origin main
git branch -d feature/controle-estoque
```

## 📚 Recursos Úteis

- [Documentação Odoo Development](https://www.odoo.com/documentation/18.0/developer.html)
- [Guia de Views](https://www.odoo.com/documentation/18.0/developer/reference/backend/views.html)
- [ORM do Odoo](https://www.odoo.com/documentation/18.0/developer/reference/backend/orm.html)
- [Segurança](https://www.odoo.com/documentation/18.0/developer/reference/backend/security.html)

---
**💡 Dica**: Use o modo `--dev=reload` para que suas mudanças em Python sejam automaticamente recarregadas!