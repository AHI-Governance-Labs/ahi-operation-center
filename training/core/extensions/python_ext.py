import ast
from .interfaces import BaseLanguageAnalyzer
from typing import List, Dict, Tuple, Any

class PythonAnalyzer(BaseLanguageAnalyzer):
    @property
    def name(self) -> str:
        return "Python"

    @property
    def file_extensions(self) -> List[str]:
        return ['.py', '.pyw']

    def validate_syntax(self, source_code: str) -> bool:
        try:
            ast.parse(source_code)
            return True
        except SyntaxError:
            return False

    def analyze(self, source_code: str) -> List[Dict[str, Any]]:
        try:
            tree = ast.parse(source_code)
            nodes = []
            
            for node in ast.walk(tree):
                if isinstance(node, (ast.ClassDef, ast.FunctionDef)):
                    # Determine type
                    node_type = "Class" if isinstance(node, ast.ClassDef) else "Method"
                    if isinstance(node, ast.FunctionDef):
                        # Simple check: if it's top level or nested in function, it's a Function.
                        # If nested in Class, it's a Method. (Approximation for now)
                        # The original code relied on parent_is_class which ast.walk doesn't set by default
                        # We will stick to the simplified logic from the extensive original file or improve it.
                        node_type = "Function" # Default to function, will be refined if we traverse differently
                        
                        # Note: To correctly distinguish Method vs Function with ast.walk, we usually 
                        # need to track context. For this migration, I'll keep it simple:
                        # If the original code had specific logic, we replicate it.
                        # The original used `getattr(node, 'parent_is_class', False)`. 
                        # Standard AST doesn't have parent links. We can re-implement the parent setter text.
                        pass

                    # Re-implementing a smarter traversal to catch Methods correctly
                    pass

            # Let's use a NodeVisitor to correctly identify methods vs functions
            visitor = SymbolVisitor()
            visitor.visit(tree)
            return visitor.symbols
            
        except Exception as e:
            # print(f"Analysis error: {e}")
            return []

    def get_block_at_line(self, lines: List[str], line_number: int) -> Tuple[int, int, str, str]:
        if line_number > len(lines):
            return 0, 0, "", ""
            
        source = "".join([l + "\n" if not l.endswith('\n') else l for l in lines])
        try:
            tree = ast.parse(source)
            
            candidates = []
            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
                    if hasattr(node, 'lineno') and hasattr(node, 'end_lineno'):
                         if node.lineno <= line_number <= node.end_lineno:
                             candidates.append(node)
            
            # Sort by linenumber descending (innermost first)
            candidates.sort(key=lambda n: n.lineno, reverse=True)
            
            if candidates:
                target = candidates[0]
                start = target.lineno
                end = target.end_lineno
                
                block_lines = lines[start-1:end]
                content = "".join([l + ("\n" if not l.endswith('\n') else "") for l in block_lines])
                
                first_line = block_lines[0]
                indent_base = first_line[:len(first_line) - len(first_line.lstrip())]
                
                return start, end, content, indent_base

        except Exception:
            pass
            
        return 0, 0, "", ""

class SymbolVisitor(ast.NodeVisitor):
    def __init__(self):
        self.symbols = []
        self._in_class = False

    def visit_ClassDef(self, node):
        self.symbols.append({
            "name": node.name,
            "type": "Class",
            "line": node.lineno
        })
        prev_in_class = self._in_class
        self._in_class = True
        self.generic_visit(node)
        self._in_class = prev_in_class

    def visit_FunctionDef(self, node):
        node_type = "Method" if self._in_class else "Function"
        self.symbols.append({
            "name": node.name,
            "type": node_type,
            "line": node.lineno
        })
        # We don't set in_class to True for nested functions inside functions
        # But if a class is defined inside a function, visit_ClassDef will handle it.
        prev_in_class = self._in_class
        self._in_class = False # Reset for nested functions
        self.generic_visit(node)
        self._in_class = prev_in_class

    def translate_node(self, node_info: Dict[str, Any], difficulty: str) -> str:
        node_type = node_info.get('type')
        name = node_info.get('name')
        
        if difficulty == 'beginner':
            if node_type == 'Class':
                return f"PLANTILLA (Clase) llamada '{name}' para crear objetos."
            elif node_type == 'Function':
                return f"ACCIÓN (Función) llamada '{name}' que realiza una tarea específica."
            elif node_type == 'Method':
                return f"HABILIDAD (Método) '{name}' que pertenece a una Plantilla."
                
        elif difficulty == 'technical':
            if node_type == 'Class':
                return f"Definición de Clase '{name}'."
            elif node_type == 'Function':
                return f"Definición de Función '{name}'."
            elif node_type == 'Method':
                return f"Definición de Método '{name}'."
        
        # Balanced / Default
        translation_map = {
            'Class': 'Clase',
            'Function': 'Función',
            'Method': 'Método'
        }
        type_str = translation_map.get(node_type, node_type)
        return f"Define una {type_str} llamada '{name}'."

    def get_explanation(self, node_info: Dict[str, Any]) -> str:
        node_type = node_info.get('type')
        if node_type == 'Class':
            return "Una clase actúa como un plano o molde. Define las características y comportamientos que tendrán los objetos creados a partir de ella."
        elif node_type == 'Function':
            return "Una función es un bloque de código reutilizable que realiza una tarea específica. Ayuda a organizar el código y evitar repeticiones."
        elif node_type == 'Method':
            return "Un método es similar a una función, pero vive dentro de una clase. Define lo que los objetos de esa clase pueden 'hacer'."
        return "Sin explicación adicional."
