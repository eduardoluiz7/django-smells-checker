import ast

class QueryInLoopVisitor(ast.NodeVisitor):
    def visit_For(self, node):
        self.inside_loop = True
        self.generic_visit(node) 
        self.inside_loop = False

    def visit_Call(self, node):
        if self.inside_loop:
            if isinstance(node.func, ast.Attribute) and node.func.attr in ['filter', 'get', 'all', 'exclude']:
                print(f"Query method '{node.func.attr}' potentially used inside a loop at line {node.lineno}.")
        self.generic_visit(node)

def detect_queries_in_loops(code):
    tree = ast.parse(code)
    visitor = QueryInLoopVisitor()
    visitor.inside_loop = False
    visitor.visit(tree)

