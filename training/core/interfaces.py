from abc import ABC, abstractmethod
from typing import List, Dict, Tuple, Any

class BaseLanguageAnalyzer(ABC):
    """
    Protocol that any language extension must implement.
    """
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Name of the language (e.g., 'Python', 'JavaScript')"""
        pass
        
    @property
    @abstractmethod
    def file_extensions(self) -> List[str]:
        """List of file extensions this analyzer supports (e.g., ['.py', '.pyw'])"""
        pass

    @abstractmethod
    def validate_syntax(self, source_code: str) -> bool:
        """Returns True if the code has valid syntax for this language."""
        pass

    @abstractmethod
    def analyze(self, source_code: str) -> List[Dict[str, Any]]:
        """
        Parses the code and returns a list of symbols/nodes.
        Format: [{'name': 'Foo', 'type': 'Class', 'line': 10}, ...]
        """
        pass

    @abstractmethod
    def get_block_at_line(self, lines: List[str], line_number: int) -> Tuple[int, int, str, str]:
        """
        Returns (start_line, end_line, content, indent) for the block at the given line.
        """
        pass

    @abstractmethod
    def translate_node(self, node_info: Dict[str, Any], difficulty: str) -> str:
        """
        Translates a specific node/block into natural language.
        difficulty: 'beginner', 'technical', 'balanced'
        """
        pass
    
    @abstractmethod
    def get_explanation(self, node_info: Dict[str, Any]) -> str:
        """
        Returns a detailed explanation ("Why does this work?") for the node.
        """
        pass
