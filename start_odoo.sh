#!/bin/bash

# Script de inicialização do Odoo - Library Project
# Este script facilita o start do ambiente Odoo com os módulos personalizados

echo "🚀 Iniciando Ambiente Odoo - Library Project"
echo "=============================================="

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Função para verificar se o PostgreSQL está rodando
check_postgresql() {
    echo -e "${BLUE}🔍 Verificando PostgreSQL...${NC}"
    if pgrep -x "postgres" > /dev/null; then
        echo -e "${GREEN}✅ PostgreSQL está rodando${NC}"
        return 0
    else
        echo -e "${RED}❌ PostgreSQL não está rodando${NC}"
        echo -e "${YELLOW}💡 Iniciando PostgreSQL...${NC}"
        brew services start postgresql@14 2>/dev/null || brew services start postgresql 2>/dev/null
        sleep 3
        
        if pgrep -x "postgres" > /dev/null; then
            echo -e "${GREEN}✅ PostgreSQL iniciado com sucesso${NC}"
            return 0
        else
            echo -e "${RED}❌ Falha ao iniciar PostgreSQL${NC}"
            return 1
        fi
    fi
}

# Função para listar módulos disponíveis
list_modules() {
    echo -e "${BLUE}📋 Listando módulos disponíveis...${NC}"
    python3 list_modules.py
}

# Função principal
main() {
    # Verifica se está na pasta correta
    if [ ! -f "odoo.conf" ]; then
        echo -e "${RED}❌ Arquivo odoo.conf não encontrado!${NC}"
        echo -e "${YELLOW}💡 Execute este script na pasta do projeto Library_Project${NC}"
        exit 1
    fi
    
    # Verifica PostgreSQL
    if ! check_postgresql; then
        echo -e "${RED}❌ PostgreSQL é necessário para executar o Odoo${NC}"
        exit 1
    fi
    
    echo
    echo -e "${BLUE}📁 Caminhos de módulos configurados:${NC}"
    echo "   • source_odoo/addons (módulos oficiais)"
    echo "   • custom_addons (seus módulos personalizados)"
    echo "   • others_addons/web (módulos web adicionais)"
    echo
    
    # Menu de opções
    echo -e "${YELLOW}🎯 O que você gostaria de fazer?${NC}"
    echo "1) Listar todos os módulos disponíveis"
    echo "2) Iniciar Odoo normalmente"
    echo "3) Iniciar Odoo atualizando a lista de módulos"
    echo "4) Iniciar Odoo com modo de desenvolvimento"
    echo "5) Iniciar Odoo e instalar módulo específico"
    echo "6) Sair"
    echo
    
    read -p "Escolha uma opção (1-6): " choice
    
    case $choice in
        1)
            list_modules
            echo
            read -p "Pressione Enter para voltar ao menu..."
            main
            ;;
        2)
            echo -e "${GREEN}🚀 Iniciando Odoo...${NC}"
            python3 source_odoo/odoo-bin -c odoo.conf
            ;;
        3)
            echo -e "${GREEN}🔄 Iniciando Odoo com atualização da lista de módulos...${NC}"
            python3 source_odoo/odoo-bin -c odoo.conf -u base
            ;;
        4)
            echo -e "${GREEN}🛠️  Iniciando Odoo em modo de desenvolvimento...${NC}"
            python3 source_odoo/odoo-bin -c odoo.conf --dev=all
            ;;
        5)
            echo
            echo -e "${BLUE}📋 Alguns módulos personalizados disponíveis:${NC}"
            echo "   • library_app (seu módulo de biblioteca)"
            echo "   • web_responsive (interface responsiva)"
            echo "   • web_environment_ribbon (faixa de ambiente)"
            echo
            read -p "Digite o nome do módulo para instalar: " module_name
            if [ ! -z "$module_name" ]; then
                echo -e "${GREEN}📦 Instalando módulo: $module_name${NC}"
                python3 source_odoo/odoo-bin -c odoo.conf -i $module_name
            else
                echo -e "${RED}❌ Nome do módulo não pode estar vazio${NC}"
            fi
            ;;
        6)
            echo -e "${BLUE}👋 Até logo!${NC}"
            exit 0
            ;;
        *)
            echo -e "${RED}❌ Opção inválida!${NC}"
            echo
            main
            ;;
    esac
}

# Executa a função principal
main