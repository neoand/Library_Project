# Library Project - Sistema de Gerenciamento de Biblioteca

## 🚀 Como trabalhar com seus projetos aqui?

**[📋 TUTORIAL COMPLETO - COMECE AQUI!](TUTORIAL.md)**

👆 **Se você está perguntando "como trabalhar com meus projetos por aqui?", clique no link acima!**

---

## 📚 Visão Geral

Este é um sistema completo de gerenciamento de biblioteca desenvolvido como addon customizado para Odoo 18. O projeto permite gerenciar catálogos de livros, autores, empréstimos e muito mais.

## 📖 Documentação Completa

| Documento | Para quem | Descrição |
|-----------|-----------|-----------|
| **[📋 TUTORIAL.md](TUTORIAL.md)** | **Todos** | **Guia principal - como trabalhar com o projeto** |
| [🚀 QUICK_START.md](QUICK_START.md) | Iniciantes | Guia de início rápido em 5 minutos |
| [💡 EXAMPLES.md](EXAMPLES.md) | Usuários | Exemplos práticos de uso |
| [🔧 DEVELOPMENT.md](DEVELOPMENT.md) | Desenvolvedores | Fluxo de desenvolvimento e modificações |
| [📖 README_EN.md](README_EN.md) | English speakers | Complete documentation in English |

**💡 Dica**: Se não sabe por onde começar, vá direto para o [TUTORIAL.md](TUTORIAL.md)!

## 🚀 Características Principais

- **Catálogo de Livros**: Gerenciamento completo de livros com ISBN, categorias e estágios
- **Gestão de Autores**: Extensão do modelo de parceiros (res.partner) para incluir dados biográficos
- **Sistema de Empréstimos**: Controle de empréstimos com rastreamento de status
- **Categorias**: Organização de livros por categorias (Ficção, Não-ficção, etc.)
- **Estágios de Workflow**: Controle do ciclo de vida dos livros (Rascunho, Disponível, Emprestado, Perdido)
- **Integração com Chatter**: Sistema de mensagens integrado para acompanhamento

## 📋 Estrutura do Projeto

```
custom_addons/library_app/
├── __manifest__.py          # Configuração do módulo
├── models/                  # Modelos de dados
│   ├── book.py             # Modelo principal de livros
│   ├── author.py           # Extensão de parceiros para autores
│   ├── partner.py          # Campos adicionais em res.partner
│   ├── category.py         # Categorias de livros
│   ├── stage.py            # Estágios de workflow
│   └── loan.py             # Sistema de empréstimos
├── views/                   # Interfaces de usuário
│   ├── book_view.xml       # Formulários e listas de livros
│   ├── book_kanban.xml     # Visualização kanban
│   ├── author_view.xml     # Visualizações de autores
│   ├── library_menu.xml    # Menu principal
│   └── ...                 # Outras views
├── data/                    # Dados iniciais
│   └── library_book_stage_data.xml  # Estágios padrão
├── security/                # Permissões e segurança
│   ├── security.xml        # Grupos de segurança
│   └── ir.model.access.csv # Controle de acesso
└── static/                  # Recursos estáticos
    └── description/
        └── icon.png        # Ícone do módulo
```

## 🛠️ Como Trabalhar com o Projeto

### 1. Instalação e Configuração

#### Pré-requisitos
- Odoo 18 instalado
- Python 3.8+
- PostgreSQL

#### Passos de Instalação

1. **Clone o repositório**:
```bash
git clone https://github.com/neoand/Library_Project.git
cd Library_Project
```

2. **Configure o addon no Odoo**:
```bash
# Copie o addon para o diretório de addons do Odoo
cp -r custom_addons/library_app /path/to/odoo/addons/
```

3. **Configure o arquivo odoo.conf**:
```ini
[options]
addons_path = /path/to/odoo/addons,/path/to/custom_addons
```

4. **Instale o módulo**:
   - Acesse o Odoo via web browser
   - Vá para Apps → Atualizar Lista de Apps
   - Procure por "Library App"
   - Clique em "Instalar"

### 2. Usando o Sistema

#### 2.1 Gerenciamento de Livros

**Criando um novo livro**:
1. Navegue para Library → Books → Books
2. Clique em "Criar"
3. Preencha os campos obrigatórios:
   - Nome do livro
   - ISBN (10 ou 13 dígitos)
   - Autor (selecione um parceiro marcado como autor)
   - Data de publicação

**Campos disponíveis**:
- `name`: Título do livro
- `isbn`: Código ISBN único
- `author_id`: Autor do livro (res.partner)
- `category_ids`: Categorias (Many2many)
- `stage_id`: Estágio atual (Draft, Available, Borrowed, Lost)
- `date_published`: Data de publicação
- `user_id`: Responsável pelo livro

#### 2.2 Gestão de Autores

**Convertendo um parceiro em autor**:
1. Vá para Library → Authors → Authors
2. Selecione um parceiro existente ou crie um novo
3. Marque o campo "Is Author"
4. Preencha dados biográficos:
   - Data de nascimento/morte
   - Local de nascimento
   - Biografia
   - Prêmios

**Funcionalidades especiais**:
- Cálculo automático de idade
- Contador de livros publicados
- Datas de primeira e última publicação
- Ação para visualizar livros do autor

#### 2.3 Sistema de Empréstimos

**Criando um empréstimo**:
1. Acesse Library → Loans → Book Loans
2. Clique em "Criar"
3. Selecione:
   - Livro a ser emprestado
   - Pessoa que vai tomar emprestado
   - Data do empréstimo

**Status de empréstimo**:
- `ongoing`: Em andamento
- `done`: Devolvido
- `lost`: Perdido

#### 2.4 Categorias e Estágios

**Categorias** (ex: Ficção, Não-ficção, Biografia):
- Organize seus livros por temas
- Cada categoria tem um código único
- Contador automático de livros

**Estágios** (Workflow):
- `draft`: Rascunho (padrão)
- `available`: Disponível
- `borrowed`: Emprestado
- `lost`: Perdido

### 3. Desenvolvimento e Customização

#### 3.1 Adicionando Novos Campos

**Exemplo: Adicionando campo "Editora" ao modelo Book**:

```python
# Em models/book.py
publisher = fields.Char(string='Publisher')
```

**Atualizando a view**:
```xml
<!-- Em views/book_view.xml -->
<field name="publisher"/>
```

#### 3.2 Criando Novos Relatórios

**Exemplo: Relatório de livros por autor**:

```python
# Novo arquivo models/report.py
from odoo import models, fields

class LibraryBookReport(models.Model):
    _name = 'library.book.report'
    _description = 'Library Book Report'
    _auto = False
    
    author_id = fields.Many2one('res.partner', string='Author')
    book_count = fields.Integer(string='Book Count')
    
    def init(self):
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute("""
            CREATE OR REPLACE VIEW %s AS (
                SELECT 
                    row_number() OVER () AS id,
                    author_id,
                    COUNT(*) as book_count
                FROM library_book 
                WHERE author_id IS NOT NULL
                GROUP BY author_id
            )
        """ % self._table)
```

#### 3.3 Workflow Personalizado

**Adicionando validações customizadas**:

```python
# Em models/book.py
@api.constrains('date_published')
def _check_publication_date(self):
    for book in self:
        if book.date_published and book.date_published > fields.Date.today():
            raise ValidationError("Publication date cannot be in the future")
```

### 4. Testes e Desenvolvimento

#### 4.1 Executando o Projeto

```bash
# Inicie o Odoo em modo desenvolvimento
./odoo-bin -d your_database -i library_app --dev=reload,qweb,werkzeug,xml
```

#### 4.2 Testando Funcionalidades

**Teste básico de criação de livro**:
1. Crie um autor
2. Crie uma categoria
3. Crie um livro associando autor e categoria
4. Verifique se os contadores foram atualizados
5. Teste o sistema de empréstimos

#### 4.3 Debug e Logs

**Ativando logs detalhados**:
```ini
# No odoo.conf
log_level = debug
log_handler = odoo.addons.library_app:DEBUG
```

### 5. Estrutura de Dados

#### 5.1 Modelos Principais

| Modelo | Descrição | Campos Principais |
|--------|-----------|-------------------|
| `library.book` | Livros | name, isbn, author_id, category_ids, stage_id |
| `res.partner` | Autores (extensão) | is_author, birth_date, biography, book_ids |
| `library.book.category` | Categorias | name, code, book_ids |
| `library.book.stage` | Estágios | name, code, sequence, is_default |
| `library.book.loan` | Empréstimos | book_id, partner_id, loan_date, return_date, state |

#### 5.2 Relacionamentos

```
res.partner (Author) ──→ library.book (One2many)
                    ↓
library.book.category ←──→ library.book (Many2many)
                    ↓
library.book.stage ←── library.book (Many2one)
                    ↓
library.book ──→ library.book.loan (One2many)
```

## 🔧 Troubleshooting

### Problemas Comuns

**1. Erro de permissão ao acessar modelos**:
- Verifique o arquivo `security/ir.model.access.csv`
- Certifique-se de que o usuário tem o grupo correto

**2. Views não aparecem**:
- Verifique se as actions estão definidas antes dos menus
- Confirme a ordem no arquivo `__manifest__.py`

**3. Dados não são criados**:
- Verifique constrains nos modelos
- Confirme se campos obrigatórios estão preenchidos

## 📝 Próximos Passos

### Funcionalidades Planejadas

- [ ] Sistema de reservas
- [ ] Relatórios avançados
- [ ] Integração com código de barras
- [ ] Notificações automáticas de vencimento
- [ ] Dashboard de métricas da biblioteca

### Como Contribuir

1. Fork o repositório
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está licenciado sob a Licença LGPL-3 - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 👨‍💻 Autor

**Anderson Oliveira**
- LinkedIn: [anderson-oliveira-dev](https://www.linkedin.com/in/anderson-oliveira-dev/)
- GitHub: [neoand](https://github.com/neoand)

## 🆘 Suporte

Se você tiver dúvidas ou precisar de ajuda:

1. Consulte a documentação do [Odoo](https://www.odoo.com/documentation/18.0/)
2. Abra uma [issue](https://github.com/neoand/Library_Project/issues) no GitHub
3. Entre em contato através do LinkedIn

---
**Desenvolvido com ❤️ para a comunidade Odoo**