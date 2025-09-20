# 💡 Exemplos Práticos - Library Project

## Como usar o sistema na prática - Exemplos reais

### 📚 Exemplo 1: Cadastrando uma Biblioteca Completa

#### Cenário: Biblioteca Escolar
Você precisa cadastrar 100 livros de uma biblioteca escolar.

**Passo a passo:**

1. **Criar Categorias Básicas**
```
Biblioteca → Configuração → Categorias → Criar

Categoria 1: Ficção
- Nome: "Ficção"
- Código: "FIC"

Categoria 2: Didáticos
- Nome: "Livros Didáticos"
- Código: "DID"

Categoria 3: Referência
- Nome: "Livros de Referência"
- Código: "REF"
```

2. **Cadastrar Autores Principais**
```
Biblioteca → Autores → Autores → Criar

Autor 1: Machado de Assis
- Nome: "Machado de Assis"
- É Autor: ✓ Sim
- Data Nascimento: 21/06/1839
- Data Falecimento: 29/09/1908
- Local Nascimento: "Rio de Janeiro, RJ"
- Biografia: "Joaquim Maria Machado de Assis foi um escritor brasileiro..."

Autor 2: Clarice Lispector
- Nome: "Clarice Lispector"
- É Autor: ✓ Sim
- Data Nascimento: 10/12/1920
- Data Falecimento: 09/12/1977
- Biografia: "Escritora e jornalista brasileira..."
```

3. **Adicionar Livros**
```
Biblioteca → Livros → Livros → Criar

Livro 1:
- Nome: "Dom Casmurro"
- ISBN: "9788525406583"
- Autor: Machado de Assis
- Categorias: Ficção
- Data Publicação: 1899-01-01
- Estágio: Disponível

Livro 2:
- Nome: "A Hora da Estrela"
- ISBN: "9788520925515"
- Autor: Clarice Lispector
- Categorias: Ficção
- Data Publicação: 1977-01-01
- Estágio: Disponível
```

### 👥 Exemplo 2: Sistema de Empréstimos

#### Cenário: Controle de Empréstimos para Estudantes

**Situação**: João Silva quer pegar "Dom Casmurro" emprestado.

**Passo a passo:**

1. **Verificar se João existe como contato**
```
Biblioteca → Autores → Parceiros (ou Contatos → Contatos)
- Se não existe, criar novo contato:
  - Nome: "João Silva"
  - É Autor: ✗ Não (ele é estudante, não autor)
  - Email: "joao.silva@escola.com"
```

2. **Criar o empréstimo**
```
Biblioteca → Empréstimos → Empréstimos de Livros → Criar

Novo Empréstimo:
- Livro: Dom Casmurro
- Pessoa: João Silva
- Data Empréstimo: Hoje
- Status: Em andamento (automático)
```

3. **Quando João devolver o livro**
```
Abrir o registro do empréstimo:
- Data Devolução: Preencher com a data atual
- Status: Devolvido

O sistema automaticamente mudará o status para "done"
```

### 📊 Exemplo 3: Relatórios e Análises

#### Cenário: Diretor quer relatórios mensais

**Relatórios disponíveis via interface:**

1. **Livros mais emprestados**
```
Biblioteca → Livros → Livros
- Usar a visualização em lista
- Ordenar por "Loan Count" (Contador de Empréstimos)
```

2. **Autores com mais livros**
```
Biblioteca → Autores → Autores
- Visualização em lista
- Ordenar por "Book Count"
```

3. **Status dos empréstimos**
```
Biblioteca → Empréstimos → Empréstimos de Livros
- Filtrar por Status = "Em andamento" para ver empréstimos ativos
- Filtrar por Status = "Devolvido" para histórico
```

### 🔧 Exemplo 4: Personalizações Simples

#### Cenário: Escola quer campo "Número da Sala" nos livros

**Modificação necessária:**

1. **Editar o modelo Book** (`models/book.py`):
```python
# Adicionar após os outros campos
room_number = fields.Char(string='Room Number', help="Room where the book is located")
```

2. **Editar a view** (`views/book_view.xml`):
```xml
<!-- Adicionar no formulário, por exemplo: -->
<field name="room_number"/>
```

3. **Atualizar o módulo**:
```
Apps → Library App → Upgrade
```

#### Cenário: Adicionar campo "Observações" nos empréstimos

1. **Editar modelo Loan** (`models/loan.py`):
```python
notes = fields.Text(string='Notes')
```

2. **Editar view de empréstimo** (`views/loan_view.xml`):
```xml
<field name="notes"/>
```

### 🎯 Exemplo 5: Workflow Avançado

#### Cenário: Biblioteca com processo de revisão

**Configuração de novos estágios:**

1. **Criar estágio personalizado**
```
Biblioteca → Configuração → Estágios → Criar

Novo Estágio:
- Nome: "Em Revisão"
- Código: "review"
- Sequência: 15 (entre Draft e Available)
- Dobrado no Kanban: ✗ Não
- Cor: Amarelo
```

2. **Workflow sugerido:**
```
Rascunho → Em Revisão → Disponível → Emprestado → Disponível
                ↓
               Perdido (se necessário)
```

### 📱 Exemplo 6: Uso via Interface Kanban

#### Cenário: Visualização por estágios

**Como usar:**

1. **Acessar visualização Kanban**
```
Biblioteca → Livros → Livros
- Clicar no ícone de Kanban (quatro quadrados)
```

2. **Mover livros entre estágios**
```
- Arrastar cartões entre colunas
- Útil para mudanças rápidas de status
```

3. **Criar livro direto no estágio**
```
- Clicar "+" na coluna desejada
- O livro já será criado no estágio correto
```

### 🔍 Exemplo 7: Buscas Avançadas

#### Cenário: Encontrar livros específicos rapidamente

**Filtros úteis:**

1. **Livros disponíveis para empréstimo**
```
Biblioteca → Livros → Livros
- Filtrar: Estágio = "Disponível"
```

2. **Livros de um autor específico**
```
- Filtrar: Autor = "Machado de Assis"
```

3. **Livros por categoria**
```
- Filtrar: Categorias → contém → "Ficção"
```

4. **Combinações múltiplas**
```
- Categoria = "Ficção" E Estágio = "Disponível"
- Resultado: Todos os livros de ficção disponíveis
```

### 📈 Exemplo 8: Métricas e KPIs

#### Cenário: Acompanhar performance da biblioteca

**Métricas automáticas disponíveis:**

1. **Por Autor:**
```
- Número de livros publicados
- Data da primeira publicação
- Data da última publicação
- Idade (se ainda vivo) ou idade ao falecer
```

2. **Por Categoria:**
```
- Número total de livros na categoria
- Acessível via lista de categorias
```

3. **Por Livro:**
```
- Número total de empréstimos
- Histórico de empréstimos
```

### 🚨 Exemplo 9: Cenários de Problema e Soluções

#### Problema 1: "Livro foi perdido"

**Solução:**
```
1. Encontrar o empréstimo ativo
2. Marcar Status = "Perdido"
3. Livro automaticamente muda para estágio "Perdido"
```

#### Problema 2: "Autor tem nome duplicado"

**Solução:**
```
1. Escolher qual registro manter
2. Editar os livros para apontar para o registro correto
3. Excluir o registro duplicado
```

#### Problema 3: "ISBN digitado errado"

**Solução:**
```
1. Editar o livro
2. Corrigir o ISBN (sistema valida 10 ou 13 dígitos)
3. Salvar
```

## 🎓 Casos de Uso Educacionais

### Para Professores de Literatura
- Acompanhar quais livros os alunos mais emprestam
- Organizar leituras por período letivo
- Controlar empréstimos por turma

### Para Bibliotecários
- Inventário completo automatizado
- Relatórios de livros em atraso
- Estatísticas de uso da biblioteca

### Para Administradores
- Métricas de ROI dos livros
- Planejamento de novas aquisições
- Controle orçamentário

---

**💡 Dica Final**: Comece com um conjunto pequeno de dados (5-10 livros) para se familiarizar com o sistema antes de fazer a migração completa de sua biblioteca!