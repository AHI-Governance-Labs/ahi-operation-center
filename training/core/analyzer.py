from typing import List, Dict, Tuple, Any
from .interfaces import BaseLanguageAnalyzer
from .extensions.python_ext import PythonAnalyzer

class CodeAnalyzer:
    def __init__(self):
        self.extensions: List[BaseLanguageAnalyzer] = [
            PythonAnalyzer()
        ]
        self.active_extension: BaseLanguageAnalyzer = self.extensions[0] # Default to Python
    
    def set_language_by_filename(self, filename: str):
        for ext in self.extensions:
            for file_ext in ext.file_extensions:
                if filename.endswith(file_ext):
                    self.active_extension = ext
                    return
        # If no match, default to Python or a "GenericText" analyzer (fallback)
        self.active_extension = self.extensions[0]

    def validate_syntax(self, source: str) -> bool:
        return self.active_extension.validate_syntax(source)

    def analyze(self, source_code: str) -> List[Dict[str, Any]]:
        return self.active_extension.analyze(source_code)

    def get_block_at_line(self, lines: List[str], line_number: int) -> Tuple[int, int, str, str]:
        return self.active_extension.get_block_at_line(lines, line_number)
    
    def translate_node(self, node_info: Dict[str, Any], difficulty: str = 'balanced') -> str:
        if not node_info:
            return ""
        return self.active_extension.translate_node(node_info, difficulty)

    def get_explanation(self, node_info: Dict[str, Any]) -> str:
        if not node_info:
            return ""
        return self.active_extension.get_explanation(node_info)
        
    def find_node_at_line(self, line_number):
        return None, "Bloque seleccionado"

