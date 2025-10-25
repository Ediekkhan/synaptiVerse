"""
MeTTa integration module for SynaptiVerse
"""

from .metta_interface import (
    query_metta,
    get_metta_knowledge_graph,
    MeTTaKnowledgeGraph,
    MedicalFact
)

__all__ = [
    'query_metta',
    'get_metta_knowledge_graph',
    'MeTTaKnowledgeGraph',
    'MedicalFact'
]
