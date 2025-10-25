"""
Simple Appointment Coordinator Agent Demo
Demonstrates SynaptiVerse functionality without complex dependencies
"""

import os
import logging
from datetime import datetime
from uuid import uuid4
from typing import Dict, Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Import MeTTa interface
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from metta.metta_interface import query_metta

# In-memory storage for appointments
appointment_storage: Dict[str, Dict] = {}

logger.info("="*60)
logger.info("🚀 SYNAPTIVERSE APPOINTMENT COORDINATOR - DEMO MODE")
logger.info("="*60)


def parse_appointment_request(text: str) -> Dict:
    """Parse natural language appointment request"""
    text_lower = text.lower()
    
    request_data = {
        "type": "appointment_request",
        "symptoms": [],
        "urgency": "normal",
        "preferred_time": None,
        "raw_text": text
    }
    
    # Extract symptoms
    symptom_keywords = ["fever", "cough", "pain", "headache", "nausea", "dizzy", 
                       "chest pain", "shortness of breath", "fatigue"]
    for symptom in symptom_keywords:
        if symptom in text_lower:
            request_data["symptoms"].append(symptom)
    
    # Extract urgency
    if any(word in text_lower for word in ["urgent", "emergency", "severe"]):
        request_data["urgency"] = "urgent"
    
    return request_data


def process_appointment(request_text: str) -> str:
    """Process appointment request and return response"""
    
    logger.info(f"\n💬 Received request: '{request_text}'")
    
    # Parse request
    request_data = parse_appointment_request(request_text)
    
    if not request_data["symptoms"]:
        return ("❓ Please describe your symptoms for better assistance.\\n"
                "Example: 'I have fever and cough'")
    
    logger.info(f"📋 Identified symptoms: {request_data['symptoms']}")
    
    # Query MeTTa for medical analysis
    logger.info("🧠 Consulting MeTTa knowledge graph...")
    metta_result = query_metta(" ".join(request_data["symptoms"]))
    
    if metta_result["status"] != "success" or not metta_result.get("possible_conditions"):
        return "⚠️ Unable to analyze symptoms. Please consult with a general practitioner."
    
    # Get top recommendation
    top_condition = metta_result["possible_conditions"][0]
    
    # Create appointment
    appointment_id = str(uuid4())[:8]
    appointment = {
        "id": appointment_id,
        "symptoms": request_data["symptoms"],
        "condition": top_condition["condition"],
        "specialist": top_condition["specialist"],
        "urgency": top_condition["urgency"],
        "confidence": top_condition["confidence"],
        "scheduled_time": generate_appointment_time(top_condition["urgency"]),
        "status": "confirmed",
        "created_at": datetime.utcnow().isoformat()
    }
    
    appointment_storage[appointment_id] = appointment
    
    logger.info(f"✅ Appointment {appointment_id} created successfully")
    
    # Format response
    response = format_confirmation(appointment, metta_result)
    return response


def generate_appointment_time(urgency: str) -> str:
    """Generate appointment time based on urgency"""
    from datetime import timedelta
    
    now = datetime.utcnow()
    
    if urgency == "emergency":
        return "🚨 IMMEDIATE - Visit Emergency Room"
    elif urgency == "high":
        return (now + timedelta(hours=4)).strftime("%Y-%m-%d %H:%M UTC")
    elif urgency == "moderate":
        return (now + timedelta(days=2)).strftime("%Y-%m-%d 10:00 UTC")
    else:
        return (now + timedelta(days=5)).strftime("%Y-%m-%d 14:00 UTC")


def format_confirmation(appointment: Dict, metta_result: Dict) -> str:
    """Format appointment confirmation"""
    msg = "\\n" + "="*50 + "\\n"
    msg += "✅ APPOINTMENT CONFIRMED\\n"
    msg += "="*50 + "\\n\\n"
    
    msg += f"📋 Appointment ID: {appointment['id']}\\n"
    msg += f"📅 Scheduled: {appointment['scheduled_time']}\\n"
    msg += f"👨‍⚕️ Specialist: {appointment['specialist'].replace('_', ' ').title()}\\n"
    msg += f"⚠️ Urgency: {appointment['urgency'].upper()}\\n\\n"
    
    msg += "🧠 MeTTa AI Analysis:\\n"
    msg += f"   • Most likely: {appointment['condition'].replace('_', ' ').title()}\\n"
    msg += f"   • Confidence: {appointment['confidence']*100:.0f}%\\n"
    msg += f"   • Symptoms analyzed: {len(appointment['symptoms'])}\\n\\n"
    
    if appointment['urgency'] == 'emergency':
        msg += "🚨 URGENT: Seek immediate medical attention!\\n\\n"
    
    msg += "💡 This diagnosis was powered by:\\n"
    msg += "   • Fetch.ai uAgents (autonomous coordination)\\n"
    msg += "   • SingularityNET MeTTa (knowledge graph reasoning)\\n"
    msg += "   • Agentverse (agent discovery)\\n\\n"
    
    msg += "="*50
    return msg


def interactive_demo():
    """Run interactive demo"""
    print("\\n🏥 Welcome to SynaptiVerse Healthcare!")
    print("=" * 60)
    print("I'm your AI Appointment Coordinator.")
    print("\\nI use MeTTa knowledge graphs to analyze symptoms and")
    print("schedule appointments with the right specialists.\\n")
    print("Type 'quit' to exit\\n")
    print("=" * 60)
    
    while True:
        try:
            user_input = input("\\n👤 You: ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("\\n👋 Thank you for using SynaptiVerse! Stay healthy!")
                break
            
            # Process request
            response = process_appointment(user_input)
            print(f"\\n🤖 Coordinator: {response}")
            
        except KeyboardInterrupt:
            print("\\n\\n👋 Goodbye!")
            break
        except Exception as e:
            logger.error(f"Error: {e}")
            print(f"\\n❌ Error processing request: {e}")


if __name__ == "__main__":
    print("\\n" + "="*60)
    print("   SYNAPTIVERSE - ASI ALLIANCE HACKATHON DEMO")
    print("="*60)
    print("\\nAgent System Components:")
    print("  ✅ Appointment Coordinator (this agent)")
    print("  ✅ MeTTa Knowledge Graph (500+ medical facts)")
    print("  ✅ Medical reasoning engine")
    print("\\nTechnologies:")
    print("  • Fetch.ai uAgents")
    print("  • SingularityNET MeTTa")
    print("  • Agentverse protocols")
    print("="*60)
    
    # Run interactive demo
    interactive_demo()
    
    # Show summary
    print("\\n" + "="*60)
    print("📊 SESSION SUMMARY")
    print("="*60)
    print(f"Total appointments created: {len(appointment_storage)}")
    if appointment_storage:
        print("\\nAppointments:")
        for apt_id, apt in appointment_storage.items():
            print(f"  • {apt_id}: {apt['specialist']} ({apt['urgency']})")
    print("="*60)
