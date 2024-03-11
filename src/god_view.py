import ast

class ComplexityVisitor(ast.NodeVisitor):
    def __init__(self, code):
        self.code = code
        self.max_depth = 0
        self.current_depth = 0
        self.line_count = 0

    def generic_visit(self, node):
        if hasattr(node, 'body'):
            self.current_depth += 1
            if self.current_depth > self.max_depth:
                self.max_depth = self.current_depth
            super().generic_visit(node)
            self.current_depth -= 1
        else:
            super().generic_visit(node)

    def visit_FunctionDef(self, node):
        self.line_count = len(ast.get_source_segment(self.code, node).splitlines())
        self.max_depth = 0
        self.current_depth = 0
        self.generic_visit(node)
        if self.line_count > 50 or self.max_depth > 3: 
            print(f"Potential God View detected in {node.name}: {self.line_count} lines, depth of {self.max_depth}")
        self.line_count = 0

def detect_god_view_smell(code):
    tree = ast.parse(code)
    visitor = ComplexityVisitor(code)
    visitor.visit(tree)
