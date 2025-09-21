# Library Project - Odoo 18

Este projeto contém uma configuração completa do Odoo 18 com módulos personalizados para gerenciamento d## 📚 Documentação

### Arquivos de Referência
- `README.md` - Esta documentação geral do projeto
- `ARCHITECTURE_DECISIONS.md` - Decisões arquiteturais e suas justificativas  
- `DEVELOPMENT_PATTERNS.md` - Padrões de código e boas práticas
- `CHANGELOG.md` - Histórico detalhado de mudanças e versões
- `PERFORMANCE.md` - Monitoramento e otimizações de performance
- `TESTING_STRATEGY.md` - Estratégia e implementação de testes
- `PROJECT_CONTEXT.md` - Contexto detalhado do projeto
- `CURRENT_ISSUE_STATUS.md` - Status atual de problemas/resoluções
- `.github/copilot-instructions.md` - Instruções para IA/Copilot

### Decisões Arquiteturais Importantes
Consulte `ARCHITECTURE_DECISIONS.md` para entender:
- ✅ **ADR-001**: Mudança de herança product.product para modelo independente
- 🎯 **Critérios de decisão**: Quando usar herança vs modelo independente
- 📊 **Métricas de sucesso**: Performance e manutenibilidade
- 📝 **Lições aprendidas**: Simplicidade vs reutilização de código

### Histórico de Mudanças
Consulte `CHANGELOG.md` para versões detalhadas:
- **v1.0.0** (2024-09-20): Refatoração completa - remoção de herança product.product
- **Performance**: 77% melhoria no tempo de carregamento (2s → 0.45s)
- **Dependencies**: Redução de 7 para 4 módulos essenciais

## �️ Ferramentas de Desenvolvimento

### Script de Utilidades
```bash
# Executar ferramentas de desenvolvimento
./dev_tools.sh
```

**Funcionalidades disponíveis:**
- 🔄 **Backup/Restore** de banco de dados
- 🧪 **Testes automatizados** (framework preparado)
- 📊 **Verificação de performance** e métricas
- 🔍 **Análise de qualidade** de código
- 🧹 **Limpeza de ambiente** (cache, logs, temporários)
- 🚀 **Verificação de deploy** (readiness check)

### Performance Monitoring
```bash
# Ver métricas atuais
./dev_tools.sh → opção 8

# Verificar performance completa  
./dev_tools.sh → opção 4
```

### Backup Strategy
```bash
# Criar backup automático
./dev_tools.sh → opção 1

# Restaurar backup específico
./dev_tools.sh → opção 2
```

## 🧪 Testing

### Estratégia de Testes
Consulte `TESTING_STRATEGY.md` para detalhes completos sobre:
- **Pirâmide de testes**: Unit → Integration → E2E
- **Padrões de teste**: Nomenclatura e estrutura
- **Performance testing**: Benchmarks e targets
- **CI/CD integration**: Automação de testes

### Executar Testes
```bash
# Testes via dev tools (recomendado)
./dev_tools.sh → opção 3

# Testes manuais com Odoo
python3 source_odoo/odoo-bin -c odoo.conf -i library_app --test-enable --stop-after-init
``` Estrutura do Projeto

```
Library_Project/
├── odoo.conf                    # Configuração principal do Odoo
├── start_odoo.sh               # Script de inicialização interativo
├── list_modules.py             # Script para listar módulos disponíveis
├── source_odoo/                # Código fonte do Odoo 18
├── custom_addons/              # Seus módulos personalizados
│   └── library_app/            # Módulo da biblioteca
└── others_addons/              # Módulos adicionais
    └── web/                    # Módulos web da comunidade
```

## 🚀 Como Iniciar o Ambiente

### Opção 1: Script Interativo (Recomendado)
```bash
./start_odoo.sh
```

Este script oferece um menu com várias opções:
- Listar todos os módulos disponíveis
- Iniciar Odoo normalmente
- Iniciar Odoo atualizando a lista de módulos
- Iniciar Odoo com modo de desenvolvimento
- Instalar módulo específico

### Opção 2: Comandos Diretos

**Iniciar Odoo normalmente:**
```bash
python3 source_odoo/odoo-bin -c odoo.conf
```

**Iniciar com atualização da lista de módulos:**
```bash
python3 source_odoo/odoo-bin -c odoo.conf -u base
```

**Instalar um módulo específico:**
```bash
python3 source_odoo/odoo-bin -c odoo.conf -i nome_do_modulo
```

## 📋 Visualizar Módulos Disponíveis

Para ver todos os módulos que podem ser instalados:
```bash
python3 list_modules.py
```

Este comando mostrará:
- ✅ Módulos instaláveis
- 🔄 Módulos com instalação automática
- 📂 Organização por categoria
- 🔗 Dependências de cada módulo

## 🎯 Módulos Personalizados

### library_app
Módulo principal para gerenciamento de biblioteca com funcionalidades completas:

**📚 Gerenciamento de Livros:**
- Cadastro de livros como entidades independentes (não herda product.product)
- Controle de categorias e estágios personalizados
- Sistema de autores integrado com res.partner

**🔄 Sistema de Empréstimos:**
- Controle completo de empréstimos com datas de devolução
- Tracking de quantidade de cópias disponíveis
- Status automático: disponível/emprestado/perdido
- Cálculo automático de duração e atraso de empréstimos

**👥 Gestão de Mutuários (Novo!):**
- **Filtros rápidos** para identificar pessoas com livros ativos
- **Contadores automáticos**: empréstimos ativos, em atraso e em dia
- **Visualização dedicada**: menu "Borrowers" para acesso direto aos mutuários
- **Botões estatísticos** nos contatos com navegação direta para empréstimos
- **Aba de detalhes** com informações completas dos empréstimos ativos

**🔍 Recursos de Busca:**
- Filtros: "Com Empréstimos Ativos", "Com Empréstimos em Atraso", "Apenas Em Dia"
- Busca avançada por status de empréstimo
- Visibilidade dinâmica (elementos aparecem apenas quando relevantes)

**⚡ Performance:**
- 77% melhoria no tempo de carregamento após refatoração
- Campos computados otimizados com store=True
- Dependências reduzidas de 7 para 4 módulos essenciais

### Módulos Web Adicionais
- `web_responsive`: Interface responsiva
- `web_environment_ribbon`: Faixa indicadora de ambiente
- `web_theme_classic`: Tema clássico
- E muitos outros módulos web úteis...

## ⚙️ Configuração

### Banco de Dados
- **Host:** localhost
- **Porta:** 5432
- **Usuário:** odoo
- **Senha:** odoo
- **Database:** lib_neo

### Servidor Web
- **Porta HTTP:** 8071
- **Interface:** 0.0.0.0 (todas as interfaces)
- **Porta GeEvent:** 8072

### Desenvolvimento
- **Modo Dev:** Ativado (dev=all)
- **Log Level:** Debug
- **Workers:** 0 (modo single-thread para desenvolvimento)

## 🔧 Pré-requisitos

1. **Python 3.8+**
2. **PostgreSQL 12+**
3. **Dependências Python:**
   ```bash
   pip install -r source_odoo/requirements.txt
   ```

## 📝 Uso no VS Code

1. Abra o terminal integrado (`Ctrl+` ` `)
2. Execute o script interativo: `./start_odoo.sh`
3. Escolha a opção desejada do menu
4. Acesse o Odoo em: http://localhost:8071

## 🎨 Interface Web

Após iniciar o Odoo, você pode:

1. **Acessar:** http://localhost:8071
2. **Login:** admin
3. **Senha:** admin (ou a definida no primeiro acesso)
4. **Instalar Módulos:** Apps → Procurar por módulos personalizados

## 🔍 Localizar Módulos

Todos os módulos estão configurados nos seguintes caminhos:
- `/source_odoo/addons` - Módulos oficiais do Odoo
- `/custom_addons` - Seus módulos personalizados  
- `/others_addons/web` - Módulos web da comunidade

## 📊 Monitoramento

- **Logs:** Configurado para nível debug
- **Lista de DBs:** Habilitada
- **Demo Data:** Desabilitado por padrão

## 📚 Documentação

### Arquivos de Referência
- `README.md` - Esta documentação geral do projeto
- `ARCHITECTURE_DECISIONS.md` - Decisões arquiteturais e suas justificativas  
- `PROJECT_CONTEXT.md` - Contexto detalhado do projeto
- `CURRENT_ISSUE_STATUS.md` - Status atual de problemas/resoluções
- `.github/copilot-instructions.md` - Instruções para IA/Copilot

### Decisões Arquiteturais Importantes
Consulte `ARCHITECTURE_DECISIONS.md` para entender:
- ✅ **ADR-001**: Mudança de herança product.product para modelo independente
- � **Critérios de decisão**: Quando usar herança vs modelo independente
- 📊 **Métricas de sucesso**: Performance e manutenibilidade
- 📝 **Lições aprendidas**: Simplicidade vs reutilização de código

### Histórico de Mudanças
- **2024-09-20**: Refatoração completa - remoção de herança product.product
- **2024-09-20**: Implementação de controle próprio de inventário
- **2024-09-20**: Melhoria no sistema de empréstimos com quantity/loss tracking

## �🆘 Solução de Problemas

### PostgreSQL não conecta
```bash
brew services start postgresql@14
# ou
brew services start postgresql
```

### Módulos não aparecem
1. Reinicie o Odoo com: `./start_odoo.sh` → opção 3
2. Ou force atualização: `-u base`

### Porta em uso
Altere a porta no `odoo.conf`:
```ini
http_port = 8072  # ou outra porta disponível
```

### Consultar Decisões Passadas
Para entender o histórico de decisões arquiteturais:
```bash
# Visualizar decisões importantes
cat ARCHITECTURE_DECISIONS.md

# Verificar status atual de issues
cat CURRENT_ISSUE_STATUS.md
```

---

**Desenvolvido para facilitar o desenvolvimento e gerenciamento de módulos Odoo 18** 🚀