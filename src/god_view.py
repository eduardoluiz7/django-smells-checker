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

# Exemplo de uso
code_example = """
def complex_user_view(request):
    if request.method == 'GET':
        users = User.objects.all()
        user_data = []
        for user in users:
            profile = UserProfile.objects.get(user=user)
            user_data.append({
                'username': user.username,
                'email': user.email,
                'profile_pic': profile.profile_picture_url,
                'bio': profile.bio
            })
        return HttpResponse(str(user_data))

    elif request.method == 'POST':
        # Simulando processamento complexo de dados de entrada
        data = request.POST
        new_user = User(username=data['username'], email=data['email'])
        new_user.save()
        new_profile = UserProfile(user=new_user, bio=data['bio'], profile_picture_url=data['profile_pic'])
        new_profile.save()

        return HttpResponse("User created successfully!")

    elif request.method == 'PUT':
        # Simulando outra operação complexa
        return HttpResponse("User updated successfully!")

    else:
        return HttpResponse("Unsupported HTTP method", status=405)
"""

detect_god_view_smell(code_example)