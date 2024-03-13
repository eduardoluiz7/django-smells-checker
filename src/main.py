import ast
import os
from bulk_create import BulkCreateVisitor
from god_view import ComplexityVisitor


def bulk_create_checker(code):
    tree = ast.parse(code)
    bulk_create_visitor = BulkCreateVisitor()
    bulk_create_visitor.visit(tree)
    for smell in bulk_create_visitor.found_smells:
        print(f"Linha {smell[0]}: {smell[1]}")

def god_view_checker(code):
    tree = ast.parse(code)
    visitor = ComplexityVisitor(code)
    visitor.visit(tree)


def processar_diretorio(diretorio):
    for raiz, diretorios, arquivos in os.walk(diretorio):
        for nome_arquivo in arquivos:
            if nome_arquivo.endswith('.py'):
                caminho_completo = os.path.join(raiz, nome_arquivo)
                with open(caminho_completo, 'r', encoding='utf-8') as arquivo:
                    conteudo = arquivo.read()
                    bulk_create_checker(conteudo)
                    god_view_checker(conteudo)

processar_diretorio("repositorio")
