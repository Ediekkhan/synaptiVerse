"""
MeTTa Knowledge Graph Interface for SynaptiVerse
Provides medical knowledge reasoning and inference capabilities
"""

import json
import logging
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass

# Note: In production, this would interface with actual Hyperon MeTTa runtime
# For hackathon demo, we implement a MeTTa-inspired reasoning engine

logger = logging.getLogger(__name__)


@dataclass
class MedicalFact:
    """Represents a medical fact in the knowledge graph"""
    condition: str
    symptoms: List[str]
    urgency: str  # low, moderate, high, emergency
    specialist: str
    confidence: float


class MeTTaKnowledgeGraph:
    """
    MeTTa-backed medical knowledge graph for symptom analysis and reasoning
    
    In production, this interfaces with Hyperon MeTTa runtime.
    For the hackathon, we implement MeTTa-style symbolic reasoning.
    """
    
    def __init__(self):
        self.knowledge_base = self._initialize_knowledge_base()
        self.reasoning_rules = self._initialize_reasoning_rules()
        logger.info("MeTTa Knowledge Graph initialized with %d medical facts", 
                   len(self.knowledge_base))
    
    def _initialize_knowledge_base(self) -> List[MedicalFact]:
        """Initialize medical knowledge base (MeTTa facts)"""
        return [
            # Respiratory conditions
            MedicalFact("common_cold", ["runny_nose", "sore_throat", "cough", "sneezing"], 
                       "low", "general_practitioner", 0.85),
            MedicalFact("flu", ["fever", "headache", "fatigue", "body_aches", "cough"], 
                       "moderate", "general_practitioner", 0.80),
            MedicalFact("pneumonia", ["high_fever", "chest_pain", "shortness_of_breath", "cough"], 
                       "high", "pulmonologist", 0.75),
            MedicalFact("covid19", ["fever", "dry_cough", "fatigue", "loss_of_taste", "shortness_of_breath"], 
                       "high", "infectious_disease", 0.78),
            
            # Cardiovascular
            MedicalFact("heart_attack", ["chest_pain", "shortness_of_breath", "nausea", "sweating"], 
                       "emergency", "cardiologist", 0.90),
            MedicalFact("hypertension", ["headache", "dizziness", "blurred_vision"], 
                       "moderate", "cardiologist", 0.70),
            
            # Neurological
            MedicalFact("migraine", ["severe_headache", "nausea", "light_sensitivity", "visual_disturbance"], 
                       "moderate", "neurologist", 0.82),
            MedicalFact("stroke", ["sudden_numbness", "confusion", "severe_headache", "vision_problems"], 
                       "emergency", "neurologist", 0.95),
            
            # Gastrointestinal
            MedicalFact("gastritis", ["stomach_pain", "nausea", "bloating", "indigestion"], 
                       "moderate", "gastroenterologist", 0.75),
            MedicalFact("food_poisoning", ["nausea", "vomiting", "diarrhea", "stomach_cramps"], 
                       "moderate", "general_practitioner", 0.80),
            MedicalFact("appendicitis", ["severe_abdominal_pain", "nausea", "fever", "vomiting"], 
                       "emergency", "surgeon", 0.85),
            
            # Musculoskeletal
            MedicalFact("arthritis", ["joint_pain", "stiffness", "swelling"], 
                       "moderate", "rheumatologist", 0.78),
            MedicalFact("muscle_strain", ["muscle_pain", "swelling", "limited_mobility"], 
                       "low", "physical_therapist", 0.82),
            
            # Dermatological
            MedicalFact("allergic_reaction", ["rash", "itching", "swelling", "hives"], 
                       "moderate", "allergist", 0.80),
            MedicalFact("eczema", ["itching", "red_patches", "dry_skin"], 
                       "low", "dermatologist", 0.75),
            
            # Endocrine
            MedicalFact("diabetes", ["excessive_thirst", "frequent_urination", "fatigue", "blurred_vision"], 
                       "high", "endocrinologist", 0.85),
            MedicalFact("thyroid_disorder", ["fatigue", "weight_changes", "mood_swings"], 
                       "moderate", "endocrinologist", 0.72),
            
            # Mental Health
            MedicalFact("anxiety", ["restlessness", "rapid_heartbeat", "sweating", "difficulty_concentrating"], 
                       "moderate", "psychiatrist", 0.75),
            MedicalFact("depression", ["persistent_sadness", "fatigue", "loss_of_interest", "sleep_changes"], 
                       "moderate", "psychiatrist", 0.78),
        ]
    
    def _initialize_reasoning_rules(self) -> Dict[str, Any]:
        """Initialize MeTTa-style reasoning rules"""
        return {
            "urgency_escalation": {
                "chest_pain + shortness_of_breath": "emergency",
                "severe_headache + sudden_numbness": "emergency",
                "high_fever + chest_pain": "high",
            },
            "symptom_clusters": {
                "respiratory": ["cough", "shortness_of_breath", "chest_pain"],
                "cardiovascular": ["chest_pain", "palpitations", "dizziness"],
                "neurological": ["headache", "dizziness", "numbness"],
                "gastrointestinal": ["nausea", "vomiting", "abdominal_pain"],
            },
            "multi_hop_inference": {
                "fever + cough + fatigue": ["flu", "covid19", "pneumonia"],
                "chest_pain + shortness_of_breath": ["heart_attack", "pneumonia"],
            }
        }
    
    def query_symptoms(self, symptoms: List[str]) -> List[Dict[str, Any]]:
        """
        Query MeTTa knowledge graph for symptom analysis
        
        MeTTa-style query: (query-symptoms (symptom1 symptom2 symptom3))
        Returns: [(condition confidence urgency specialist)]
        """
        logger.info("MeTTa query: analyzing symptoms %s", symptoms)
        
        # Normalize symptoms
        normalized_symptoms = [s.lower().replace(" ", "_") for s in symptoms]
        
        results = []
        
        # Single-hop: Direct symptom matching
        for fact in self.knowledge_base:
            matching_symptoms = set(normalized_symptoms) & set(fact.symptoms)
            if matching_symptoms:
                match_ratio = len(matching_symptoms) / len(fact.symptoms)
                confidence = fact.confidence * match_ratio
                
                # Boost confidence if critical symptoms match
                if match_ratio > 0.6:
                    confidence = min(0.95, confidence * 1.2)
                
                results.append({
                    "condition": fact.condition,
                    "confidence": round(confidence, 2),
                    "urgency": fact.urgency,
                    "specialist": fact.specialist,
                    "matching_symptoms": list(matching_symptoms),
                    "reasoning": f"Matched {len(matching_symptoms)}/{len(fact.symptoms)} symptoms"
                })
        
        # Multi-hop: Apply reasoning rules
        results = self._apply_reasoning_rules(results, normalized_symptoms)
        
        # Sort by confidence
        results.sort(key=lambda x: x["confidence"], reverse=True)
        
        logger.info("MeTTa query returned %d possible conditions", len(results))
        return results[:5]  # Return top 5
    
    def _apply_reasoning_rules(self, results: List[Dict], symptoms: List[str]) -> List[Dict]:
        """Apply MeTTa-style reasoning rules for inference"""
        
        # Check urgency escalation rules
        for pattern, urgency in self.reasoning_rules["urgency_escalation"].items():
            pattern_symptoms = pattern.replace(" ", "").split("+")
            if all(s in symptoms for s in pattern_symptoms):
                for result in results:
                    if any(s in result.get("matching_symptoms", []) for s in pattern_symptoms):
                        result["urgency"] = urgency
                        result["reasoning"] += " | Urgency escalated by rule"
        
        return results
    
    def traverse_knowledge_graph(self, query: str, depth: int = 2) -> Dict[str, Any]:
        """
        Multi-hop MeTTa graph traversal for complex reasoning
        
        Example: Patient has fever -> what conditions? -> which need urgent care?
        """
        logger.info("Multi-hop traversal: query='%s', depth=%d", query, depth)
        
        traversal_path = []
        
        # Parse query (simplified for demo)
        if "fever" in query.lower():
            # Hop 1: Find conditions with fever
            hop1 = [f for f in self.knowledge_base if "fever" in f.symptoms]
            traversal_path.append({
                "hop": 1,
                "query": "conditions with fever",
                "results": [f.condition for f in hop1]
            })
            
            # Hop 2: Filter by urgency if in query
            if "urgent" in query.lower() or "emergency" in query.lower():
                hop2 = [f for f in hop1 if f.urgency in ["high", "emergency"]]
                traversal_path.append({
                    "hop": 2,
                    "query": "urgent cases only",
                    "results": [f.condition for f in hop2]
                })
                final_results = hop2
            else:
                final_results = hop1
        else:
            final_results = []
        
        return {
            "traversal_path": traversal_path,
            "final_results": [
                {
                    "condition": f.condition,
                    "urgency": f.urgency,
                    "specialist": f.specialist
                } for f in final_results
            ],
            "hops_executed": len(traversal_path)
        }
    
    def get_specialist_recommendation(self, condition: str) -> Optional[str]:
        """Get specialist recommendation for a specific condition"""
        for fact in self.knowledge_base:
            if fact.condition == condition:
                return fact.specialist
        return None
    
    def explain_reasoning(self, symptoms: List[str], condition: str) -> str:
        """
        Generate human-readable explanation of MeTTa reasoning
        """
        normalized_symptoms = [s.lower().replace(" ", "_") for s in symptoms]
        
        for fact in self.knowledge_base:
            if fact.condition == condition:
                matching = set(normalized_symptoms) & set(fact.symptoms)
                missing = set(fact.symptoms) - set(normalized_symptoms)
                
                explanation = f"MeTTa Reasoning for {condition}:\n"
                explanation += f"- Matched symptoms: {', '.join(matching)}\n"
                if missing:
                    explanation += f"- Typical symptoms not reported: {', '.join(missing)}\n"
                explanation += f"- Confidence: {fact.confidence}\n"
                explanation += f"- Recommended specialist: {fact.specialist}\n"
                explanation += f"- Urgency level: {fact.urgency}"
                
                return explanation
        
        return f"No reasoning path found for condition: {condition}"


# Singleton instance
_metta_kg_instance = None


def get_metta_knowledge_graph() -> MeTTaKnowledgeGraph:
    """Get singleton instance of MeTTa knowledge graph"""
    global _metta_kg_instance
    if _metta_kg_instance is None:
        _metta_kg_instance = MeTTaKnowledgeGraph()
    return _metta_kg_instance


def query_metta(natural_text: str) -> Dict[str, Any]:
    """
    Main interface for MeTTa queries from natural language
    Converts natural language to MeTTa query and returns results
    """
    kg = get_metta_knowledge_graph()
    
    # Simple NL parsing (in production, use proper NLP)
    symptoms = []
    
    # Extract symptoms from natural language
    symptom_keywords = {
        "fever": "fever", "cough": "cough", "headache": "headache",
        "nausea": "nausea", "pain": "pain", "fatigue": "fatigue",
        "dizzy": "dizziness", "chest pain": "chest_pain",
        "shortness of breath": "shortness_of_breath", "vomit": "vomiting",
        "sore throat": "sore_throat", "runny nose": "runny_nose",
        "body aches": "body_aches", "sweating": "sweating"
    }
    
    text_lower = natural_text.lower()
    for keyword, symptom in symptom_keywords.items():
        if keyword in text_lower:
            symptoms.append(symptom)
    
    if not symptoms:
        return {
            "status": "clarification_needed",
            "message": "Could not identify clear symptoms. Please describe your symptoms more specifically.",
            "suggestions": ["fever", "cough", "headache", "nausea", "pain"]
        }
    
    # Query MeTTa knowledge graph
    results = kg.query_symptoms(symptoms)
    
    return {
        "status": "success",
        "identified_symptoms": symptoms,
        "possible_conditions": results,
        "metta_query": f"(query-symptoms ({' '.join(symptoms)}))"
    }


# For testing
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    # Test queries
    print("=== Test 1: Flu symptoms ===")
    result = query_metta("I have fever, headache, and body aches")
    print(json.dumps(result, indent=2))
    
    print("\n=== Test 2: Multi-hop traversal ===")
    kg = get_metta_knowledge_graph()
    traversal = kg.traverse_knowledge_graph("show me urgent conditions with fever", depth=2)
    print(json.dumps(traversal, indent=2))
    
    print("\n=== Test 3: Reasoning explanation ===")
    explanation = kg.explain_reasoning(["fever", "headache", "fatigue"], "flu")
    print(explanation)
