# Contexto Essencial - Library Project

## 📁 Estrutura do Projeto
```
Library_Project/
├── odoo.conf                    # Porta 8073 para testes
├── start_odoo.sh               # Script interativo
├── custom_addons/
│   └── library_app/            # Módulo principal
│       ├── __manifest__.py     # Dependências: base, contacts, mail, web
│       ├── models/
│       │   └── library_book.py # Modelo principal (SEM herança de product)
│       └── data/
│           └── product_category_data.xml # ❌ CAUSA DO ERRO
```

## 🔧 Configuração
- **Database**: lib_neo (localhost:5432, user: odoo, pass: odoo)
- **Porta de teste**: 8073 (para evitar conflitos)
- **Odoo 18** com addon paths configurados

## 📋 Comando de Atualização
```bash
python3 source_odoo/odoo-bin -c odoo.conf -u library_app --http-port=8073
```

## 🎯 Objetivo
Ter um sistema de biblioteca simples SEM herança de produtos, apenas com:
- Livros (library.book) com chatter
- Empréstimos (library.book.loan) 
- Gerenciamento simples de disponibilidade