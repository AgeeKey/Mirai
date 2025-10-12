import ast

def validate_python_code(code):
    try:
        ast.parse(code)
        return True, "Синтаксис корректен"
    except SyntaxError as e:
        return False, f"Ошибка синтаксиса: {e}"