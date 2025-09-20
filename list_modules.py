#!/usr/bin/env python3
"""
Script para listar todos os módulos Odoo disponíveis no projeto
"""

import os
import json
from pathlib import Path

def find_odoo_modules(base_path):
    """Encontra todos os módulos Odoo em um diretório"""
    modules = []
    
    if not os.path.exists(base_path):
        return modules
    
    for item in os.listdir(base_path):
        item_path = os.path.join(base_path, item)
        
        # Verifica se é um diretório
        if os.path.isdir(item_path):
            # Procura por __manifest__.py ou __openerp__.py
            manifest_files = ['__manifest__.py', '__openerp__.py']
            
            for manifest_file in manifest_files:
                manifest_path = os.path.join(item_path, manifest_file)
                if os.path.exists(manifest_path):
                    try:
                        # Lê o arquivo manifest
                        with open(manifest_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                            # Avalia o conteúdo do manifest de forma segura
                            manifest_dict = eval(content)
                            
                            modules.append({
                                'name': item,
                                'path': item_path,
                                'display_name': manifest_dict.get('name', item),
                                'summary': manifest_dict.get('summary', ''),
                                'description': manifest_dict.get('description', '').split('\n')[0][:100],
                                'version': manifest_dict.get('version', ''),
                                'depends': manifest_dict.get('depends', []),
                                'category': manifest_dict.get('category', 'Uncategorized'),
                                'installable': manifest_dict.get('installable', True),
                                'auto_install': manifest_dict.get('auto_install', False)
                            })
                    except Exception as e:
                        print(f"Erro ao ler manifest de {item}: {e}")
                    break
    
    return modules

def main():
    print("=" * 80)
    print("MÓDULOS ODOO DISPONÍVEIS NO PROJETO")
    print("=" * 80)
    
    # Caminhos dos módulos
    addon_paths = [
        "/Users/andersongoliveira/Devops/Library_Project/source_odoo/addons",
        "/Users/andersongoliveira/Devops/Library_Project/custom_addons", 
        "/Users/andersongoliveira/Devops/Library_Project/others_addons/web"
    ]
    
    all_modules = []
    
    for path in addon_paths:
        print(f"\n📁 Buscando módulos em: {path}")
        modules = find_odoo_modules(path)
        
        if modules:
            print(f"   Encontrados {len(modules)} módulos")
            all_modules.extend(modules)
        else:
            print("   Nenhum módulo encontrado")
    
    if not all_modules:
        print("\n❌ Nenhum módulo encontrado em nenhum dos caminhos!")
        return
    
    # Organiza por categoria
    by_category = {}
    for module in all_modules:
        category = module['category']
        if category not in by_category:
            by_category[category] = []
        by_category[category].append(module)
    
    print(f"\n📊 RESUMO: {len(all_modules)} módulos encontrados")
    print("=" * 80)
    
    for category, modules in sorted(by_category.items()):
        print(f"\n📂 {category.upper()} ({len(modules)} módulos)")
        print("-" * 50)
        
        for module in sorted(modules, key=lambda x: x['name']):
            status = "✅" if module['installable'] else "❌"
            auto = "🔄" if module['auto_install'] else "  "
            
            print(f"  {status}{auto} {module['name']:<30} - {module['display_name']}")
            
            if module['summary']:
                print(f"      📝 {module['summary']}")
            
            if module['depends']:
                deps = ', '.join(module['depends'][:5])
                if len(module['depends']) > 5:
                    deps += f" ... (+{len(module['depends'])-5} mais)"
                print(f"      🔗 Depende de: {deps}")
    
    print(f"\n" + "=" * 80)
    print("LEGENDA:")
    print("✅ = Módulo instalável")
    print("❌ = Módulo não instalável") 
    print("🔄 = Instalação automática")
    print("🔗 = Dependências")
    print("=" * 80)
    
    # Módulos personalizados
    custom_modules = [m for m in all_modules if 'custom_addons' in m['path']]
    web_modules = [m for m in all_modules if 'others_addons/web' in m['path']]
    
    print(f"\n🎯 MÓDULOS PERSONALIZADOS: {len(custom_modules)}")
    for module in custom_modules:
        print(f"   • {module['name']} - {module['display_name']}")
    
    print(f"\n🌐 MÓDULOS WEB: {len(web_modules)}")
    for module in sorted(web_modules, key=lambda x: x['name'])[:10]:  # Mostra só os primeiros 10
        print(f"   • {module['name']} - {module['display_name']}")
    
    if len(web_modules) > 10:
        print(f"   ... e mais {len(web_modules)-10} módulos web")

if __name__ == "__main__":
    main()