import ast

class BulkCreateVisitor(ast.NodeVisitor):
    def __init__(self):
        self.found_smells = []

    def visit_For(self, node):
        # Verifica se o corpo do loop contém chamadas a métodos que parecem criar objetos de modelo
        for child in ast.iter_child_nodes(node):
            if isinstance(child, ast.Expr):
                if hasattr(child, 'value') and isinstance(child.value, ast.Call):
                    call = child.value
                    if hasattr(call.func, 'attr') and call.func.attr == 'save':
                        self.found_smells.append((node.lineno, "Possível uso ineficiente de criação de modelo dentro de um loop. Considere usar 'bulk_create'."))
        self.generic_visit(node)

def detect_bulk_create_smell(code):
    print("code")
    tree = ast.parse(code)
    print(tree)
    visitor = BulkCreateVisitor()
    visitor.visit(tree)
    return visitor.found_smells
