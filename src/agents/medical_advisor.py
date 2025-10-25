"""
Medical Advisor Agent
Provides medical triage, symptom analysis using MeTTa knowledge graphs,
and specialist recommendations
"""

import os
import logging
from datetime import datetime
from uuid import uuid4
from typing import Dict, List, Optional

from uagents.setup import fund_agent_if_low
from uagents_core.core import Agent, Context, Protocol
from uagents_core.contrib.protocols.chat import (
    ChatAcknowledgement,
    ChatMessage,
    StartSessionContent,
    TextContent,
    EndSessionContent,
    chat_protocol_spec,
)

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Import MeTTa interface
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from metta.metta_interface import query_metta, get_metta_knowledge_graph

# Agent configuration
AGENT_NAME = "medical-advisor"
AGENT_SEED = os.getenv("ADVISOR_SEED", "advisor_demo_seed_phrase_67890")
AGENT_PORT = 8001
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

# In-memory storage for consultations
consultation_history: Dict[str, List[Dict]] = {}

logger.info(f"Medical Advisor Agent initialized")
logger.info(f"Agent name: {agent.name}")
logger.info(f"Agent address: {agent.address}")

# Initialize MeTTa knowledge graph
metta_kg = get_metta_knowledge_graph()


# Chat Protocol Implementation
chat_proto = Protocol(spec=chat_protocol_spec)


def create_text_chat(text: str, end_session: bool = False) -> ChatMessage:
    """Helper to create ChatMessage with text content"""
    content = [TextContent(type="text", text=text)]
    if end_session:
        content.append(EndSessionContent(type="end_session"))
    return ChatMessage(
        timestamp=datetime.utcnow(),
        msg_id=uuid4(),
        content=content
    )


@chat_proto.on_message(ChatMessage)
async def handle_chat_message(ctx: Context, sender: str, msg: ChatMessage):
    """Handle incoming chat messages"""
    
    # Send acknowledgement
    await ctx.send(
        sender,
        ChatAcknowledgement(
            timestamp=datetime.utcnow(),
            acknowledged_msg_id=msg.msg_id
        )
    )
    
    # Process message content
    for item in msg.content:
        if isinstance(item, StartSessionContent):
            logger.info(f"🔬 Medical consultation session started with {sender}")
            
            if sender not in consultation_history:
                consultation_history[sender] = []
            
            welcome_msg = (
                "Hello! I'm the Medical Advisor Agent 🩺\n\n"
                "I use advanced MeTTa knowledge graphs to analyze symptoms "
                "and provide evidence-based medical triage.\n\n"
                "Please describe your symptoms in detail, and I'll help you "
                "understand possible conditions and recommend appropriate specialists.\n\n"
                "⚠️ Note: I provide guidance only. For emergencies, call emergency services immediately."
            )
            await ctx.send(sender, create_text_chat(welcome_msg))
        
        elif isinstance(item, TextContent):
            user_text = item.text
            logger.info(f"🩺 Medical inquiry from {sender}: {user_text}")
            
            # Analyze symptoms using MeTTa
            await analyze_symptoms(ctx, sender, user_text)
        
        elif isinstance(item, EndSessionContent):
            logger.info(f"👋 Medical consultation ended with {sender}")
            
            # Provide summary
            if sender in consultation_history and consultation_history[sender]:
                summary = create_consultation_summary(sender)
                await ctx.send(sender, create_text_chat(summary, end_session=True))
        
        else:
            logger.warning(f"Unknown content type from {sender}")


async def analyze_symptoms(ctx: Context, sender: str, symptom_text: str):
    """
    Analyze symptoms using MeTTa knowledge graph
    This is the core medical reasoning function
    """
    
    # Step 1: Query MeTTa knowledge graph
    logger.info(f"🧠 Querying MeTTa knowledge graph for: {symptom_text}")
    metta_result = query_metta(symptom_text)
    
    # Record consultation
    consultation_record = {
        "timestamp": datetime.utcnow().isoformat(),
        "symptoms_text": symptom_text,
        "metta_result": metta_result
    }
    
    if sender not in consultation_history:
        consultation_history[sender] = []
    consultation_history[sender].append(consultation_record)
    
    # Step 2: Process MeTTa results and respond
    if metta_result["status"] == "clarification_needed":
        # Need more information
        response_text = (
            f"🤔 {metta_result['message']}\n\n"
            f"To provide accurate analysis, please mention specific symptoms like:\n"
            f"{', '.join(metta_result['suggestions'])}\n\n"
            f"Example: 'I have fever, cough, and fatigue'"
        )
        await ctx.send(sender, create_text_chat(response_text))
        return
    
    # Step 3: Analyze conditions and provide recommendations
    possible_conditions = metta_result.get("possible_conditions", [])
    identified_symptoms = metta_result.get("identified_symptoms", [])
    
    if not possible_conditions:
        response_text = (
            "I've analyzed your symptoms, but couldn't identify specific conditions. "
            "I recommend scheduling an appointment with a general practitioner "
            "for a comprehensive evaluation."
        )
        await ctx.send(sender, create_text_chat(response_text))
        return
    
    # Step 4: Format detailed medical analysis
    response_text = format_medical_analysis(identified_symptoms, possible_conditions, metta_result)
    
    await ctx.send(sender, create_text_chat(response_text))
    
    # Step 5: Check if multi-hop reasoning needed
    top_condition = possible_conditions[0]
    if top_condition["urgency"] in ["high", "emergency"]:
        # Perform multi-hop MeTTa traversal for urgent cases
        logger.info("🔍 Performing multi-hop MeTTa analysis for urgent case")
        
        traversal_query = f"show me urgent conditions with {' '.join(identified_symptoms[:2])}"
        traversal_result = metta_kg.traverse_knowledge_graph(traversal_query, depth=2)
        
        # Send additional insights
        additional_msg = (
            f"\n🔍 Deep Analysis (Multi-hop MeTTa Reasoning):\n"
            f"Performed {traversal_result['hops_executed']} reasoning hops.\n\n"
            f"⚠️ Given the urgency, I recommend immediate medical attention."
        )
        
        await ctx.send(sender, create_text_chat(additional_msg))


def format_medical_analysis(symptoms: List[str], conditions: List[Dict], metta_result: Dict) -> str:
    """Format comprehensive medical analysis response"""
    
    msg = "📊 Medical Analysis Results\n"
    msg += "=" * 40 + "\n\n"
    
    # Identified symptoms
    msg += f"🔍 Identified Symptoms: {', '.join(symptoms)}\n"
    msg += f"🧠 MeTTa Query: {metta_result.get('metta_query', 'N/A')}\n\n"
    
    # Top condition (most likely)
    top_condition = conditions[0]
    msg += "📌 Most Likely Condition:\n"
    msg += f"• {top_condition['condition'].replace('_', ' ').title()}\n"
    msg += f"• Confidence: {top_condition['confidence']*100:.0f}%\n"
    msg += f"• Urgency: {top_condition['urgency'].upper()}\n"
    msg += f"• Recommended Specialist: {top_condition['specialist'].replace('_', ' ').title()}\n"
    msg += f"• Matched Symptoms: {', '.join(top_condition.get('matching_symptoms', []))}\n\n"
    
    # Urgency-specific advice
    if top_condition['urgency'] == 'emergency':
        msg += "🚨 EMERGENCY ALERT 🚨\n"
        msg += "This appears to be a medical emergency!\n"
        msg += "Please call emergency services (911) or go to the nearest ER immediately.\n\n"
    elif top_condition['urgency'] == 'high':
        msg += "⚠️ HIGH PRIORITY\n"
        msg += "Please seek medical attention within the next few hours.\n\n"
    elif top_condition['urgency'] == 'moderate':
        msg += "⚡ MODERATE PRIORITY\n"
        msg += "Schedule an appointment with the recommended specialist soon.\n\n"
    else:
        msg += "ℹ️ ROUTINE CARE\n"
        msg += "Schedule an appointment at your convenience.\n\n"
    
    # Alternative conditions
    if len(conditions) > 1:
        msg += "🔄 Alternative Possibilities:\n"
        for i, cond in enumerate(conditions[1:4], 2):  # Show up to 3 alternatives
            msg += f"{i}. {cond['condition'].replace('_', ' ').title()} "
            msg += f"({cond['confidence']*100:.0f}% confidence)\n"
        msg += "\n"
    
    # Reasoning explanation
    if conditions:
        msg += "💡 Reasoning:\n"
        msg += f"{top_condition.get('reasoning', 'Based on symptom matching')}\n\n"
    
    # Next steps
    msg += "📋 Recommended Next Steps:\n"
    msg += f"1. Schedule appointment with: {top_condition['specialist'].replace('_', ' ').title()}\n"
    msg += "2. Monitor your symptoms\n"
    msg += "3. Note any changes or new symptoms\n"
    
    if top_condition['urgency'] not in ['emergency', 'high']:
        msg += "4. Rest and stay hydrated\n"
    
    msg += "\n" + "=" * 40 + "\n"
    msg += "🤖 Analysis powered by MeTTa Knowledge Graph AI"
    
    return msg


def create_consultation_summary(patient_id: str) -> str:
    """Create summary of consultation session"""
    
    if patient_id not in consultation_history or not consultation_history[patient_id]:
        return "No consultation history available."
    
    consultations = consultation_history[patient_id]
    
    msg = "📋 Consultation Summary\n"
    msg += "=" * 40 + "\n\n"
    msg += f"Total consultations: {len(consultations)}\n\n"
    
    for i, consult in enumerate(consultations, 1):
        msg += f"Consultation {i}:\n"
        msg += f"Time: {consult['timestamp']}\n"
        msg += f"Symptoms: {consult['symptoms_text'][:100]}...\n"
        
        if consult['metta_result'].get('possible_conditions'):
            top = consult['metta_result']['possible_conditions'][0]
            msg += f"Diagnosis: {top['condition']}\n"
            msg += f"Specialist: {top['specialist']}\n"
        
        msg += "\n"
    
    msg += "Thank you for using Medical Advisor Agent!\n"
    msg += "Take care and get well soon! 💙"
    
    return msg


@chat_proto.on_message(ChatAcknowledgement)
async def handle_ack(ctx: Context, sender: str, msg: ChatAcknowledgement):
    """Handle chat acknowledgements"""
    logger.debug(f"✓ Ack received from {sender} for message {msg.acknowledged_msg_id}")


# Inter-agent protocol for coordination with Appointment Coordinator
inter_agent_proto = Protocol(name="medical_consultation")


@inter_agent_proto.on_message(model=dict)
async def handle_consultation_request(ctx: Context, sender: str, msg: dict):
    """
    Handle consultation requests from Appointment Coordinator agent
    This enables inter-agent coordination
    """
    logger.info(f"🤝 Received consultation request from {sender}")
    logger.info(f"Request: {msg}")
    
    # Extract symptoms from request
    symptoms = msg.get("symptoms", [])
    patient_id = msg.get("patient_id", "unknown")
    urgency = msg.get("urgency", "normal")
    
    # Analyze using MeTTa
    symptom_text = " ".join(symptoms)
    metta_result = query_metta(symptom_text)
    
    # Prepare response
    if metta_result["status"] == "success" and metta_result["possible_conditions"]:
        top_condition = metta_result["possible_conditions"][0]
        
        response = {
            "status": "success",
            "patient_id": patient_id,
            "specialist": top_condition["specialist"],
            "urgency": top_condition["urgency"],
            "conditions": [c["condition"] for c in metta_result["possible_conditions"][:3]],
            "confidence": top_condition["confidence"],
            "analysis": format_medical_analysis(
                metta_result["identified_symptoms"],
                metta_result["possible_conditions"],
                metta_result
            )
        }
    else:
        response = {
            "status": "clarification_needed",
            "patient_id": patient_id,
            "message": "Unable to provide specific diagnosis. Recommend general practitioner.",
            "specialist": "general_practitioner",
            "urgency": urgency
        }
    
    # Send response back to coordinator
    await ctx.send(sender, response)
    logger.info(f"✅ Sent consultation response to {sender}")


# Include protocols
agent.include(chat_proto, publish_manifest=True)
agent.include(inter_agent_proto, publish_manifest=True)


@agent.on_event("startup")
async def startup(ctx: Context):
    """Agent startup event"""
    logger.info("=" * 60)
    logger.info("🚀 MEDICAL ADVISOR AGENT STARTED")
    logger.info("=" * 60)
    logger.info(f"Agent Name: {ctx.name}")
    logger.info(f"Agent Address: {ctx.agent.address}")
    logger.info(f"Agent Port: {AGENT_PORT}")
    logger.info(f"Chat Protocol: ENABLED")
    logger.info(f"Inter-Agent Protocol: ENABLED")
    logger.info(f"Manifest Publishing: ENABLED")
    logger.info(f"MeTTa Knowledge Graph: LOADED")
    logger.info("=" * 60)


@agent.on_event("shutdown")
async def shutdown(ctx: Context):
    """Agent shutdown event"""
    logger.info("👋 Medical Advisor Agent shutting down...")


if __name__ == "__main__":
    logger.info("Starting Medical Advisor Agent...")
    agent.run()
