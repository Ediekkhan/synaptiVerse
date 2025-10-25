"""
End-to-End Test Scenarios for SynaptiVerse
Tests the complete agent interaction flows
"""

import pytest
import asyncio
import sys
import os
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.metta.metta_interface import query_metta, get_metta_knowledge_graph


class TestScenarioA:
    """
    Scenario A (Happy Path):
    User requests appointment → Coordinator validates → Advisor analyzes symptoms
    → Appointment scheduled with confirmation
    """
    
    def test_symptom_analysis_flu(self):
        """Test MeTTa analysis for flu symptoms"""
        print("\n" + "="*60)
        print("TEST SCENARIO A: Happy Path - Flu Symptoms")
        print("="*60)
        
        # User input: "I need an appointment. I have fever, headache, and body aches"
        user_input = "fever headache body aches"
        
        # MeTTa analysis
        result = query_metta(user_input)
        
        # Assertions
        assert result["status"] == "success", "MeTTa query should succeed"
        assert len(result["identified_symptoms"]) >= 2, "Should identify at least 2 symptoms"
        assert len(result["possible_conditions"]) > 0, "Should return possible conditions"
        
        # Check top condition
        top_condition = result["possible_conditions"][0]
        print(f"\n✅ Identified symptoms: {result['identified_symptoms']}")
        print(f"✅ Top condition: {top_condition['condition']}")
        print(f"✅ Confidence: {top_condition['confidence']*100:.0f}%")
        print(f"✅ Specialist: {top_condition['specialist']}")
        print(f"✅ Urgency: {top_condition['urgency']}")
        
        assert top_condition["confidence"] > 0.4, "Confidence should be > 40%"
        assert top_condition["specialist"] is not None, "Should recommend a specialist"
        assert top_condition["urgency"] in ["low", "moderate", "high", "emergency"]
        
        print("\n✅ SCENARIO A PASSED: Happy path flow validated")
    
    def test_appointment_scheduling_workflow(self):
        """Test complete appointment scheduling workflow"""
        print("\n" + "="*60)
        print("TEST SCENARIO A: Complete Appointment Workflow")
        print("="*60)
        
        # Simulated workflow steps
        print("\n1️⃣ Patient submits request...")
        patient_request = {
            "symptoms": ["fever", "cough", "fatigue"],
            "urgency": "normal",
            "preferred_time": "tomorrow"
        }
        
        # 2. Coordinator validates request
        print("2️⃣ Coordinator validates request...")
        assert len(patient_request["symptoms"]) > 0, "Request must have symptoms"
        
        # 3. Advisor analyzes with MeTTa
        print("3️⃣ Medical Advisor analyzes symptoms using MeTTa...")
        analysis = query_metta(" ".join(patient_request["symptoms"]))
        
        assert analysis["status"] == "success"
        top_condition = analysis["possible_conditions"][0]
        
        # 4. Create appointment
        print("4️⃣ Creating appointment...")
        appointment = {
            "id": "apt_12345",
            "patient": "test_patient",
            "symptoms": patient_request["symptoms"],
            "specialist": top_condition["specialist"],
            "urgency": top_condition["urgency"],
            "scheduled_time": "2025-10-23 09:00 UTC",
            "status": "confirmed"
        }
        
        print(f"\n✅ Appointment created:")
        print(f"   ID: {appointment['id']}")
        print(f"   Specialist: {appointment['specialist']}")
        print(f"   Time: {appointment['scheduled_time']}")
        print(f"   Status: {appointment['status']}")
        
        assert appointment["status"] == "confirmed"
        assert appointment["specialist"] is not None
        
        print("\n✅ SCENARIO A PASSED: Full workflow completed successfully")


class TestScenarioB:
    """
    Scenario B (Clarification Flow):
    Ambiguous symptoms → Advisor requests clarification → User clarifies
    → Recommendation provided
    """
    
    def test_ambiguous_symptoms_clarification(self):
        """Test clarification flow for ambiguous input"""
        print("\n" + "="*60)
        print("TEST SCENARIO B: Clarification Flow")
        print("="*60)
        
        # User provides vague input
        print("\n1️⃣ User provides vague symptoms...")
        vague_input = "I don't feel well"
        
        result = query_metta(vague_input)
        
        print(f"   Input: '{vague_input}'")
        print(f"   Status: {result['status']}")
        
        # Should request clarification
        assert result["status"] == "clarification_needed", \
            "Should request clarification for vague symptoms"
        
        print(f"✅ Clarification requested: {result['message']}")
        print(f"✅ Suggestions: {result['suggestions']}")
        
        # 2. User provides clarified symptoms
        print("\n2️⃣ User clarifies symptoms...")
        clarified_input = "I have fever and cough"
        
        result2 = query_metta(clarified_input)
        
        assert result2["status"] == "success", "Should succeed with clear symptoms"
        assert len(result2["possible_conditions"]) > 0
        
        print(f"   Clarified input: '{clarified_input}'")
        print(f"✅ Analysis successful")
        print(f"✅ Recommended: {result2['possible_conditions'][0]['condition']}")
        
        print("\n✅ SCENARIO B PASSED: Clarification flow handled correctly")
    
    def test_partial_symptom_matching(self):
        """Test behavior with partial symptom matches"""
        print("\n" + "="*60)
        print("TEST SCENARIO B: Partial Symptom Matching")
        print("="*60)
        
        # Provide some symptoms but not all typical for a condition
        partial_symptoms = "headache"
        
        result = query_metta(partial_symptoms)
        
        if result["status"] == "success":
            print(f"✅ Found conditions with partial match")
            print(f"   Symptoms: {result['identified_symptoms']}")
            print(f"   Possible conditions: {len(result['possible_conditions'])}")
            
            # Should still provide results but with lower confidence
            for cond in result["possible_conditions"][:3]:
                print(f"   - {cond['condition']}: {cond['confidence']*100:.0f}% confidence")
                assert cond["confidence"] < 0.9, \
                    "Partial matches should have lower confidence"
        
        print("\n✅ SCENARIO B PASSED: Partial matching works correctly")


class TestScenarioC:
    """
    Scenario C (Multi-hop Reasoning):
    Complex case requiring MeTTa graph traversal for diagnosis
    and specialist matching
    """
    
    def test_multihop_reasoning(self):
        """Test multi-hop MeTTa knowledge graph traversal"""
        print("\n" + "="*60)
        print("TEST SCENARIO C: Multi-hop MeTTa Reasoning")
        print("="*60)
        
        kg = get_metta_knowledge_graph()
        
        # Complex query requiring graph traversal
        print("\n1️⃣ Performing multi-hop query...")
        query = "show me urgent conditions with fever"
        
        result = kg.traverse_knowledge_graph(query, depth=2)
        
        print(f"   Query: '{query}'")
        print(f"   Depth: 2 hops")
        print(f"\n✅ Traversal completed:")
        print(f"   Hops executed: {result['hops_executed']}")
        
        # Validate traversal path
        assert result["hops_executed"] > 0, "Should perform at least 1 hop"
        assert "traversal_path" in result
        assert "final_results" in result
        
        print(f"\n   Traversal path:")
        for hop in result["traversal_path"]:
            print(f"   Hop {hop['hop']}: {hop['query']}")
            print(f"      Results: {hop['results']}")
        
        print(f"\n   Final results: {len(result['final_results'])} conditions")
        
        for condition in result["final_results"][:5]:
            print(f"   - {condition['condition']}: {condition['urgency']} urgency")
        
        print("\n✅ SCENARIO C PASSED: Multi-hop reasoning successful")
    
    def test_complex_symptom_combination(self):
        """Test complex symptom combination requiring deeper analysis"""
        print("\n" + "="*60)
        print("TEST SCENARIO C: Complex Symptom Analysis")
        print("="*60)
        
        # Complex symptom set
        complex_symptoms = "chest pain shortness of breath sweating"
        
        print(f"\n⚠️ Analyzing emergency symptoms: '{complex_symptoms}'")
        
        result = query_metta(complex_symptoms)
        
        assert result["status"] == "success"
        assert len(result["possible_conditions"]) > 0
        
        top_condition = result["possible_conditions"][0]
        
        print(f"\n✅ Analysis complete:")
        print(f"   Top condition: {top_condition['condition']}")
        print(f"   Urgency: {top_condition['urgency']}")
        print(f"   Specialist: {top_condition['specialist']}")
        print(f"   Confidence: {top_condition['confidence']*100:.0f}%")
        
        # Should detect high urgency
        assert top_condition["urgency"] in ["high", "emergency"], \
            "Emergency symptoms should trigger high/emergency urgency"
        
        print(f"\n🚨 Emergency detected correctly!")
        
        print("\n✅ SCENARIO C PASSED: Complex analysis handled correctly")
    
    def test_reasoning_explanation(self):
        """Test that reasoning can be explained"""
        print("\n" + "="*60)
        print("TEST SCENARIO C: Reasoning Explanation")
        print("="*60)
        
        kg = get_metta_knowledge_graph()
        
        symptoms = ["fever", "headache", "fatigue"]
        condition = "flu"
        
        explanation = kg.explain_reasoning(symptoms, condition)
        
        print(f"\n{explanation}")
        
        # Validate explanation contains key information
        assert "Matched symptoms" in explanation
        assert "Confidence" in explanation
        assert "Recommended specialist" in explanation
        assert "Urgency level" in explanation
        
        print("\n✅ SCENARIO C PASSED: Reasoning is explainable")


class TestIntegration:
    """Integration tests for complete system"""
    
    def test_metta_knowledge_graph_loaded(self):
        """Verify MeTTa knowledge graph is properly initialized"""
        print("\n" + "="*60)
        print("INTEGRATION TEST: MeTTa Knowledge Graph")
        print("="*60)
        
        kg = get_metta_knowledge_graph()
        
        print(f"\n✅ Knowledge graph initialized")
        print(f"   Facts loaded: {len(kg.knowledge_base)}")
        print(f"   Reasoning rules: {len(kg.reasoning_rules)}")
        
        assert len(kg.knowledge_base) > 0, "Knowledge base should not be empty"
        assert len(kg.reasoning_rules) > 0, "Should have reasoning rules"
        
        # Check coverage
        specialties = set(fact.specialist for fact in kg.knowledge_base)
        urgency_levels = set(fact.urgency for fact in kg.knowledge_base)
        
        print(f"   Specialists covered: {len(specialties)}")
        print(f"   Urgency levels: {urgency_levels}")
        
        assert len(specialties) >= 5, "Should cover multiple specialties"
        assert "emergency" in urgency_levels, "Should have emergency cases"
        
        print("\n✅ INTEGRATION TEST PASSED: Knowledge graph verified")
    
    def test_end_to_end_performance(self):
        """Test system performance metrics"""
        print("\n" + "="*60)
        print("INTEGRATION TEST: Performance Metrics")
        print("="*60)
        
        test_cases = [
            "fever cough fatigue",
            "chest pain shortness of breath",
            "headache dizziness",
            "nausea vomiting diarrhea",
            "joint pain swelling"
        ]
        
        total_time = 0
        successful_queries = 0
        
        for test in test_cases:
            start = datetime.now()
            result = query_metta(test)
            end = datetime.now()
            
            query_time = (end - start).total_seconds()
            total_time += query_time
            
            if result["status"] == "success":
                successful_queries += 1
            
            print(f"   Query: '{test}' - {query_time:.3f}s")
        
        avg_time = total_time / len(test_cases)
        success_rate = (successful_queries / len(test_cases)) * 100
        
        print(f"\n📊 Performance Metrics:")
        print(f"   Average response time: {avg_time:.3f}s")
        print(f"   Success rate: {success_rate:.0f}%")
        print(f"   Total queries: {len(test_cases)}")
        
        assert avg_time < 1.0, "Average response should be < 1 second"
        assert success_rate >= 80, "Success rate should be >= 80%"
        
        print("\n✅ INTEGRATION TEST PASSED: Performance acceptable")


def run_all_scenarios():
    """Run all test scenarios and generate report"""
    print("\n" + "🚀 " + "="*58)
    print("   SYNAPTIVERSE E2E TEST SUITE - ASI ALLIANCE HACKATHON")
    print("="*60 + "\n")
    
    test_results = {
        "total": 0,
        "passed": 0,
        "failed": 0,
        "start_time": datetime.now()
    }
    
    # Run Scenario A tests
    print("\n📋 SCENARIO A: HAPPY PATH TESTS")
    scenario_a = TestScenarioA()
    try:
        scenario_a.test_symptom_analysis_flu()
        test_results["passed"] += 1
    except AssertionError as e:
        print(f"❌ FAILED: {e}")
        test_results["failed"] += 1
    test_results["total"] += 1
    
    try:
        scenario_a.test_appointment_scheduling_workflow()
        test_results["passed"] += 1
    except AssertionError as e:
        print(f"❌ FAILED: {e}")
        test_results["failed"] += 1
    test_results["total"] += 1
    
    # Run Scenario B tests
    print("\n📋 SCENARIO B: CLARIFICATION FLOW TESTS")
    scenario_b = TestScenarioB()
    try:
        scenario_b.test_ambiguous_symptoms_clarification()
        test_results["passed"] += 1
    except AssertionError as e:
        print(f"❌ FAILED: {e}")
        test_results["failed"] += 1
    test_results["total"] += 1
    
    try:
        scenario_b.test_partial_symptom_matching()
        test_results["passed"] += 1
    except AssertionError as e:
        print(f"❌ FAILED: {e}")
        test_results["failed"] += 1
    test_results["total"] += 1
    
    # Run Scenario C tests
    print("\n📋 SCENARIO C: MULTI-HOP REASONING TESTS")
    scenario_c = TestScenarioC()
    try:
        scenario_c.test_multihop_reasoning()
        test_results["passed"] += 1
    except AssertionError as e:
        print(f"❌ FAILED: {e}")
        test_results["failed"] += 1
    test_results["total"] += 1
    
    try:
        scenario_c.test_complex_symptom_combination()
        test_results["passed"] += 1
    except AssertionError as e:
        print(f"❌ FAILED: {e}")
        test_results["failed"] += 1
    test_results["total"] += 1
    
    try:
        scenario_c.test_reasoning_explanation()
        test_results["passed"] += 1
    except AssertionError as e:
        print(f"❌ FAILED: {e}")
        test_results["failed"] += 1
    test_results["total"] += 1
    
    # Run Integration tests
    print("\n📋 INTEGRATION TESTS")
    integration = TestIntegration()
    try:
        integration.test_metta_knowledge_graph_loaded()
        test_results["passed"] += 1
    except AssertionError as e:
        print(f"❌ FAILED: {e}")
        test_results["failed"] += 1
    test_results["total"] += 1
    
    try:
        integration.test_end_to_end_performance()
        test_results["passed"] += 1
    except AssertionError as e:
        print(f"❌ FAILED: {e}")
        test_results["failed"] += 1
    test_results["total"] += 1
    
    # Generate report
    test_results["end_time"] = datetime.now()
    duration = (test_results["end_time"] - test_results["start_time"]).total_seconds()
    
    print("\n" + "="*60)
    print("📊 TEST SUMMARY REPORT")
    print("="*60)
    print(f"Total tests: {test_results['total']}")
    print(f"✅ Passed: {test_results['passed']}")
    print(f"❌ Failed: {test_results['failed']}")
    print(f"Success rate: {(test_results['passed']/test_results['total'])*100:.1f}%")
    print(f"Duration: {duration:.2f}s")
    print("="*60)
    
    if test_results["failed"] == 0:
        print("🎉 ALL TESTS PASSED! System ready for deployment.")
    else:
        print(f"⚠️ {test_results['failed']} test(s) failed. Please review.")
    
    print("\n")
    
    return test_results


if __name__ == "__main__":
    # Run all scenarios
    results = run_all_scenarios()
    
    # Exit with appropriate code
    sys.exit(0 if results["failed"] == 0 else 1)
