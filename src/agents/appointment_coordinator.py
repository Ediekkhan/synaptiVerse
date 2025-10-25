"""
Appointment Coordinator Agent
Manages patient appointment requests, schedules, and coordinates with Medical Advisor
"""

import os
import logging
from datetime import datetime
from uuid import uuid4
from typing import Dict, List, Optional

from uagents import Agent, Context, Protocol, Model
from uagents.setup import fund_agent_if_low

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Agent configuration
AGENT_NAME = "appointment-coordinator"
AGENT_SEED = os.getenv("COORDINATOR_SEED", "coordinator_demo_seed_phrase_12345")
AGENT_PORT = 8000
AGENT_ENDPOINT = [f"http://localhost:{AGENT_PORT}/submit"]

# Initialize agent
agent = Agent(
    name=AGENT_NAME,
    seed=AGENT_SEED,
    port=AGENT_PORT,
    endpoint=AGENT_ENDPOINT,
)

# Fund agent if low on balance
fund_agent_if_low(agent.wallet.address())

# In-memory storage for appointments and sessions
appointment_storage: Dict[str, Dict] = {}
active_sessions: Dict[str, Dict] = {}

logger.info(f"Appointment Coordinator Agent initialized")
logger.info(f"Agent name: {agent.name}")
logger.info(f"Agent address: {agent.address}")


# Chat Protocol Implementation
chat_proto = Protocol(name="chat", version="1.0.0")


# Define message models
class ChatRequest(Model):
    message: str

class ChatResponse(Model):
    response: str
    appointment_id: Optional[str] = None


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
    
    # Extract request type
    if any(word in text_lower for word in ["appointment", "schedule", "book", "see a doctor"]):
        request_data["type"] = "appointment_request"
    elif any(word in text_lower for word in ["cancel", "reschedule"]):
        request_data["type"] = "modification"
    elif any(word in text_lower for word in ["status", "check", "confirm"]):
        request_data["type"] = "status_inquiry"
    
    # Extract symptoms
    symptom_keywords = ["fever", "cough", "pain", "headache", "nausea", "dizzy", 
                       "chest pain", "shortness of breath", "fatigue"]
    for symptom in symptom_keywords:
        if symptom in text_lower:
            request_data["symptoms"].append(symptom)
    
    # Extract urgency
    if any(word in text_lower for word in ["urgent", "emergency", "severe", "immediately"]):
        request_data["urgency"] = "urgent"
    
    # Extract time preferences
    if "tomorrow" in text_lower:
        request_data["preferred_time"] = "tomorrow"
    elif "today" in text_lower:
        request_data["preferred_time"] = "today"
    elif "next week" in text_lower:
        request_data["preferred_time"] = "next_week"
    
    return request_data


@chat_proto.on_message(model=ChatRequest)
async def handle_chat_message(ctx: Context, sender: str, msg: ChatRequest):
    """Handle incoming chat messages"""
    logger.info(f"💬 Received from {sender}: {msg.message}")
    
    # Initialize session if needed
    if sender not in active_sessions:
        active_sessions[sender] = {
            "start_time": datetime.utcnow(),
            "state": "active",
            "context": {}
        }
        
        welcome_msg = (
            "Welcome to SynaptiVerse Healthcare! 🏥\n\n"
            "I'm your Appointment Coordinator. I can help you:\n"
            "• Schedule medical appointments\n"
            "• Analyze symptoms and recommend specialists\n"
            "• Check appointment status\n\n"
            "Please describe your symptoms or what you need help with."
        )
        await ctx.send(sender, ChatResponse(response=welcome_msg))
        return
    
    # Parse the request
    request_data = parse_appointment_request(msg.message)
    
    # Route based on request type
    if request_data["type"] == "appointment_request":
        await handle_appointment_request(ctx, sender, request_data)
    elif request_data["type"] == "status_inquiry":
        await handle_status_inquiry(ctx, sender)
    elif request_data["type"] == "modification":
        response_msg = (
            "I can help you modify your appointment. "
            "Please provide your appointment ID or patient name."
        )
        await ctx.send(sender, ChatResponse(response=response_msg))
    else:
        # General inquiry
        if request_data["symptoms"]:
            await handle_appointment_request(ctx, sender, request_data)
        else:
            response_msg = (
                "I'd be happy to help! Could you please describe:\n"
                "• Your symptoms (if scheduling an appointment)\n"
                "• What type of appointment you need\n"
                "• Any time preferences"
            )
            await ctx.send(sender, ChatResponse(response=response_msg))


async def handle_appointment_request(ctx: Context, sender: str, request_data: Dict):
    """Process appointment request and coordinate with Medical Advisor"""
    
    if not request_data["symptoms"]:
        # Ask for more information
        response_msg = (
            "To schedule the right appointment, please describe your symptoms. "
            "For example: 'I have fever and cough' or 'I have chest pain and shortness of breath'."
        )
        await ctx.send(sender, ChatResponse(response=response_msg))
        return
    
    # Step 1: Acknowledge request
    initial_msg = (
        f"📋 Processing your appointment request...\n"
        f"Identified symptoms: {', '.join(request_data['symptoms'])}\n"
        f"Urgency: {request_data['urgency']}\n\n"
        f"Consulting with our Medical Advisor agent..."
    )
    await ctx.send(sender, ChatResponse(response=initial_msg))
    
    # Step 2: Request medical analysis from Medical Advisor agent
    # In a real deployment, this would be an inter-agent message
    # For demo, we'll simulate the coordination
    
    advisor_address = os.getenv("ADVISOR_ADDRESS", "advisor_agent_simulated")
    
    # Create inter-agent consultation request
    consultation_request = {
        "patient_id": sender,
        "symptoms": request_data["symptoms"],
        "urgency": request_data["urgency"],
        "request_time": datetime.utcnow().isoformat()
    }
    
    logger.info(f"🤝 Coordinating with Medical Advisor: {consultation_request}")
    
    # Simulate advisor response (in production, this is an actual agent message)
    # The Medical Advisor agent would analyze using MeTTa and respond
    advisor_response = await simulate_advisor_consultation(consultation_request)
    
    # Step 3: Create appointment based on advisor recommendation
    appointment_id = str(uuid4())[:8]
    appointment = {
        "id": appointment_id,
        "patient": sender,
        "symptoms": request_data["symptoms"],
        "recommended_specialist": advisor_response["specialist"],
        "urgency": advisor_response["urgency"],
        "conditions": advisor_response["conditions"],
        "scheduled_time": generate_appointment_time(request_data["preferred_time"], 
                                                     advisor_response["urgency"]),
        "status": "confirmed",
        "created_at": datetime.utcnow().isoformat()
    }
    
    appointment_storage[appointment_id] = appointment
    
    # Step 4: Send confirmation to patient
    confirmation_msg = format_appointment_confirmation(appointment, advisor_response)
    await ctx.send(sender, ChatResponse(response=confirmation_msg, appointment_id=appointment_id))
    
    logger.info(f"✅ Appointment {appointment_id} created for {sender}")


async def simulate_advisor_consultation(request: Dict) -> Dict:
    """
    Simulate Medical Advisor agent response
    In production, this is an actual inter-agent Chat Protocol message
    """
    # Import MeTTa interface
    import sys
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
    from metta.metta_interface import query_metta
    
    # Use MeTTa to analyze symptoms
    metta_result = query_metta(" ".join(request["symptoms"]))
    
    if metta_result["status"] == "success" and metta_result["possible_conditions"]:
        top_condition = metta_result["possible_conditions"][0]
        
        return {
            "specialist": top_condition["specialist"],
            "urgency": top_condition["urgency"],
            "conditions": [c["condition"] for c in metta_result["possible_conditions"][:3]],
            "confidence": top_condition["confidence"],
            "metta_analysis": metta_result
        }
    else:
        return {
            "specialist": "general_practitioner",
            "urgency": "moderate",
            "conditions": ["general_consultation"],
            "confidence": 0.5,
            "metta_analysis": metta_result
        }


def generate_appointment_time(preferred: Optional[str], urgency: str) -> str:
    """Generate appointment time based on preferences and urgency"""
    from datetime import timedelta
    
    now = datetime.utcnow()
    
    if urgency == "emergency":
        return "IMMEDIATE - Please visit Emergency Room"
    elif urgency == "high":
        return (now + timedelta(hours=4)).strftime("%Y-%m-%d %H:%M UTC")
    elif urgency == "moderate":
        if preferred == "today":
            return (now + timedelta(hours=8)).strftime("%Y-%m-%d %H:%M UTC")
        elif preferred == "tomorrow":
            return (now + timedelta(days=1)).strftime("%Y-%m-%d 09:00 UTC")
        else:
            return (now + timedelta(days=2)).strftime("%Y-%m-%d 10:00 UTC")
    else:  # low urgency
        if preferred == "next_week":
            return (now + timedelta(days=7)).strftime("%Y-%m-%d 10:00 UTC")
        else:
            return (now + timedelta(days=3)).strftime("%Y-%m-%d 14:00 UTC")


def format_appointment_confirmation(appointment: Dict, advisor_response: Dict) -> str:
    """Format appointment confirmation message"""
    msg = "✅ Appointment Confirmed!\n\n"
    msg += f"Appointment ID: {appointment['id']}\n"
    msg += f"Scheduled: {appointment['scheduled_time']}\n"
    msg += f"Specialist: {appointment['recommended_specialist'].replace('_', ' ').title()}\n"
    msg += f"Urgency: {appointment['urgency'].upper()}\n\n"
    
    msg += "📊 Medical Analysis (via MeTTa AI):\n"
    if advisor_response['conditions']:
        msg += f"Possible conditions: {', '.join(advisor_response['conditions'])}\n"
    msg += f"Confidence: {advisor_response['confidence']*100:.0f}%\n\n"
    
    if appointment['urgency'] == 'emergency':
        msg += "⚠️ URGENT: Please seek immediate medical attention!\n\n"
    
    msg += "📞 You will receive a confirmation call/email shortly.\n"
    msg += "Reply 'status' anytime to check your appointment."
    
    return msg


async def handle_status_inquiry(ctx: Context, sender: str):
    """Handle appointment status inquiry"""
    # Find appointments for this sender
    user_appointments = [apt for apt in appointment_storage.values() 
                        if apt["patient"] == sender]
    
    if not user_appointments:
        response_msg = (
            "You don't have any appointments scheduled. "
            "Would you like to schedule one?"
        )
    else:
        response_msg = f"📋 Your Appointments ({len(user_appointments)}):\n\n"
        for apt in user_appointments:
            response_msg += f"ID: {apt['id']}\n"
            response_msg += f"Time: {apt['scheduled_time']}\n"
            response_msg += f"Specialist: {apt['recommended_specialist']}\n"
            response_msg += f"Status: {apt['status']}\n\n"
    
    await ctx.send(sender, ChatResponse(response=response_msg))


# Simple message handler for testing
@agent.on_message(model=ChatRequest)
async def message_handler(ctx: Context, sender: str, msg: ChatRequest):
    """Simple message handler for direct messages"""
    await handle_chat_message(ctx, sender, msg)


# Include chat protocol
agent.include(chat_proto)


@agent.on_event("startup")
async def startup(ctx: Context):
    """Agent startup event"""
    logger.info("=" * 60)
    logger.info("🚀 APPOINTMENT COORDINATOR AGENT STARTED")
    logger.info("=" * 60)
    logger.info(f"Agent Name: {ctx.name}")
    logger.info(f"Agent Address: {ctx.agent.address}")
    logger.info(f"Agent Port: {AGENT_PORT}")
    logger.info(f"Chat Protocol: ENABLED")
    logger.info(f"Manifest Publishing: ENABLED")
    logger.info("=" * 60)


@agent.on_event("shutdown")
async def shutdown(ctx: Context):
    """Agent shutdown event"""
    logger.info("👋 Appointment Coordinator Agent shutting down...")


if __name__ == "__main__":
    logger.info("Starting Appointment Coordinator Agent...")
    agent.run()
