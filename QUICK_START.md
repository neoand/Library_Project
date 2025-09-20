# 🚀 Guia de Início Rápido - Library Project

## Como começar a trabalhar com seus projetos aqui

### 📋 Lista de Verificação Rápida

**✅ Primeiro uso:**
1. [ ] Instalar o módulo Library App no Odoo
2. [ ] Criar algumas categorias básicas (Ficção, Não-ficção, etc.)
3. [ ] Cadastrar autores (marcar parceiros como "Is Author")
4. [ ] Adicionar seus primeiros livros
5. [ ] Testar o sistema de empréstimos

**✅ Para desenvolvimento:**
1. [ ] Clonar o repositório localmente
2. [ ] Configurar ambiente Odoo de desenvolvimento
3. [ ] Ativar modo de desenvolvimento (`--dev=reload`)
4. [ ] Fazer suas modificações
5. [ ] Testar as mudanças
6. [ ] Fazer commit das alterações

## 🏃‍♂️ Início Imediato

### Opção 1: Usuário Final (apenas usar o sistema)

1. **Acesse o Odoo** onde o módulo está instalado
2. **Vá para o menu Library** (deve aparecer na barra de navegação principal)
3. **Comece cadastrando:**
   - Categorias em Library → Configuration → Categories
   - Autores em Library → Authors → Authors
   - Livros em Library → Books → Books

### Opção 2: Desenvolvedor (modificar o sistema)

```bash
# 1. Clone o repositório
git clone https://github.com/neoand/Library_Project.git
cd Library_Project

# 2. Copie para o diretório de addons do Odoo
cp -r custom_addons/library_app /path/to/your/odoo/addons/

# 3. Inicie o Odoo em modo de desenvolvimento
./odoo-bin -d your_database -i library_app --dev=reload,qweb,werkzeug,xml
```

## 📚 Funcionalidades Prontas para Usar

### 1. Gerenciamento de Livros
- ➕ **Criar livro**: Library → Books → Books → Create
- 🔍 **Buscar livros**: Use a barra de pesquisa avançada
- 📊 **Visualização Kanban**: Organize por estágios (Draft, Available, Borrowed, Lost)

### 2. Gestão de Autores
- 👤 **Cadastrar autor**: Library → Authors → Authors → Create
- ✏️ **Dados biográficos**: Data nascimento/morte, biografia, prêmios
- 📖 **Ver livros do autor**: Botão "View Books" no formulário do autor

### 3. Sistema de Empréstimos
- 📋 **Novo empréstimo**: Library → Loans → Book Loans → Create
- ✅ **Controlar status**: ongoing, done, lost
- 📅 **Acompanhar datas**: Data do empréstimo e devolução

### 4. Organização
- 🏷️ **Categorias**: Fiction, Non-fiction, Biography, etc.
- 📈 **Estágios**: Draft → Available → Borrowed → Lost
- 🔢 **Contadores automáticos**: Livros por autor, por categoria

## 🛠️ Personalizações Comuns

### Adicionar Campo Simples (ex: Editora)

1. **Edite o modelo** (`models/book.py`):
```python
publisher = fields.Char(string='Publisher')
```

2. **Atualize a view** (`views/book_view.xml`):
```xml
<field name="publisher"/>
```

3. **Atualize o módulo**: Apps → Library App → Upgrade

### Criar Nova Categoria

1. **Vá para**: Library → Configuration → Categories
2. **Clique**: Create
3. **Preencha**:
   - Name: "Science Fiction"
   - Code: "SCI_FI"

### Configurar Novo Estágio

1. **Vá para**: Library → Configuration → Stages
2. **Clique**: Create
3. **Configure**:
   - Name: "Under Review"
   - Code: "review"
   - Sequence: 15 (entre Draft e Available)

## 🔧 Resolução Rápida de Problemas

### ❌ "Não consigo ver o menu Library"
**Solução**: Verificar se o usuário tem permissões. Vá em Settings → Users & Companies → Users e adicione o grupo "Library User".

### ❌ "Erro ao criar livro"
**Verificar**:
- ISBN tem 10 ou 13 dígitos
- Autor está marcado como "Is Author"
- Campos obrigatórios preenchidos

### ❌ "Views não aparecem depois de modificar"
**Soluções**:
1. Atualizar módulo: Apps → Library App → Upgrade
2. Limpar cache: F5 ou Ctrl+F5
3. Reiniciar Odoo em modo desenvolvimento

### ❌ "Erro de permissão"
**Verificar**:
- Arquivo `security/ir.model.access.csv`
- Grupos de usuário em `security/security.xml`

## 📞 Onde Buscar Ajuda

1. **Documentação completa**: Veja README.md principal
2. **Documentação Odoo**: [odoo.com/documentation](https://www.odoo.com/documentation/18.0/)
3. **Issues no GitHub**: [Abrir issue](https://github.com/neoand/Library_Project/issues)
4. **Contato direto**: [LinkedIn do Anderson](https://www.linkedin.com/in/anderson-oliveira-dev/)

## 🎯 Próximos Passos Sugeridos

1. **Para usuários**:
   - [ ] Cadastrar 5-10 livros de teste
   - [ ] Criar empréstimos de exemplo
   - [ ] Explorar diferentes visualizações (List, Kanban, Form)
   - [ ] Usar filtros de pesquisa

2. **Para desenvolvedores**:
   - [ ] Explorar código dos models
   - [ ] Modificar uma view simples
   - [ ] Adicionar um campo novo
   - [ ] Criar relatório customizado
   - [ ] Implementar validação personalizada

---
**💡 Dica**: Comece pequeno! Cadastre alguns dados de teste e explore as funcionalidades básicas antes de fazer modificações complexas.