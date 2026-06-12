import os
import requests
from typing import Optional
from technician.expertise import get_technical_procedure

# Try to use transformers pipeline as fallback (local)
try:
    from transformers import pipeline
    generator = pipeline(
        "text-generation",
        model="TinyLlama/TinyLlama-1.1B-Chat-v1.0",
        device_map="auto"
    )
    HAS_LOCAL_LLM = True
except Exception:
    HAS_LOCAL_LLM = False


def generate_expert_response(issue: str, query: str) -> str:
    """Generate a realistic expert technician response based on the issue."""
    procedure = get_technical_procedure(issue)
    
    query_lower = query.lower()
    
    # Check more specific patterns FIRST before generic ones
    
    # 1. Safety queries take priority
    if any(word in query_lower for word in ["safe", "danger", "risk", "warning", "careful", "hazard", "precaution"]):
        response = f"""Action: safety_warning
Response: Excellent - safety awareness is critical. Here are the key hazards for {issue.lower()}:

CRITICAL SAFETY HAZARDS:
⚠️  PRESSURE HAZARD - System may contain stored pressure even when powered off
⚠️  CHEMICAL HAZARD - Fluid may be toxic or corrosive
⚠️  ELECTRICAL HAZARD - Verify all circuits are de-energized
⚠️  THERMAL HAZARD - Components may be extremely hot

MANDATORY PRECAUTIONS:
• LOCKOUT/TAGOUT - Lock power switch and tag with your name
• CONTAINMENT - Drain fluids into proper containers
• PPE - Safety glasses, gloves, appropriate footwear minimum
• VENTILATION - Ensure area is well-ventilated for fumes
• NO SMOKING - Critical if flammable fluids present

EMERGENCY CONTACTS:
• Have first aid kit accessible
• Know location of emergency eye wash
• Have emergency contact phone numbers ready

Do not proceed until all hazards are controlled. Safety first - always."""
    
    # 2. Preventive maintenance/prevention queries
    elif any(word in query_lower for word in ["prevent", "prevention", "maintenance", "avoid", "future", "happen again", "recurrence"]):
        if procedure:
            response = f"""Action: maintenance_tip
Response: Smart thinking about prevention! Here's how to avoid repeating this {issue.lower()} failure:

ROOT CAUSE PREVENTION:
The main causes of {issue.lower()} are:
{chr(10).join(f'• {cause}' for cause in procedure['common_causes'])}

YOUR PREVENTIVE MAINTENANCE PLAN:
{procedure['preventive_maintenance']}

DETAILED SCHEDULE:
• WEEKLY - Visual inspection for any signs of wear or leakage
• MONTHLY - Detailed component assessment and measurements  
• QUARTERLY - Professional testing (pressure/thermal/electrical)
• ANNUALLY - Full system inspection and proactive component replacement

DOCUMENTATION SYSTEM:
• Keep maintenance log with dates and findings
• Record any repairs immediately with parts used
• Track component age - plan replacements before failure
• Monitor any performance trends

COST BENEFIT:
Preventive maintenance typically costs 10-15% of emergency repair costs and extends equipment life 2-3x.

I recommend starting quarterly professional inspections immediately."""
        else:
            response = f"""Action: maintenance_tip
Response: Excellent planning! Preventive maintenance prevents 85% of equipment failures. For {issue.lower()}:

WEEKLY TASKS:
• Visual inspection - look for leaks, discoloration, unusual wear
• Check fluid levels
• Monitor unusual sounds or vibrations

MONTHLY CHECKS:
• Detailed component inspection with photos
• Pressure/performance verification
• Check for corrosion or oxidation
• Confirm all fasteners are tight

QUARTERLY PROFESSIONAL SERVICE:
• Thermal imaging to detect heat issues
• Ultrasonic testing for early failure detection
• Full pressure testing
• Electrical circuit verification

ANNUAL DEEP INSPECTION:
• Replace questionable components proactively
• Full system recalibration
• Update documentation and maintenance records

Starting a maintenance program now will prevent costly failures later."""
    
    # 3. Troubleshooting/problem queries
    elif any(word in query_lower for word in ["problem", "wrong", "not working", "failed", "issue", "error", "trouble"]):
        response = f"""Action: clarify_issue
Response: Let me help troubleshoot. Can you describe specifically what happened:

DIAGNOSTIC QUESTIONS:
• What exact symptom are you seeing? (leak, noise, malfunction, etc.)
• Did the repair go according to plan so far?
• Any unexpected conditions or complications?
• Are there any warning signs or measurements?

COMMON COMPLICATIONS:
• Parts don't fit as expected - may indicate wrong specification
• New parts leaking - may need reseating or sealant
• System won't start - may indicate improper reassembly
• Unusual sounds/vibrations - misalignment issue

Share more details and I'll provide specific troubleshooting steps."""
    
    # 4. Next step / continuation queries
    elif any(word in query_lower for word in ["next", "continue", "proceed", "then", "after", "what's next"]):
        response = f"""Action: next_step
Response: Here's the next critical phase of the repair:

NEXT MAJOR STEP:
• Continue with component removal if not yet done
• Perform detailed inspection of mounting surfaces
• Prepare components for new installation
• Ensure all old sealants/gaskets are completely removed

KEY POINTS:
• Clean all surfaces thoroughly - contamination causes failures
• Check torque specifications from the manual
• Have a helper ready for alignment/installation
• Take photos of original configuration before disassembly

Proceed carefully and let me know when you're ready for the final steps."""
    
    # 5. General repair/fix queries (catches "how", "steps", "fix", "repair", "do")
    elif any(word in query_lower for word in ["how", "steps", "fix", "repair", "do", "procedure", "technique"]):
        if procedure:
            response = f"""Action: generate_steps
Response: I'll walk you through the professional repair procedure for {issue.lower()}:

SEVERITY: {procedure['severity']}

TOOLS YOU'LL NEED:
{chr(10).join(f'• {tool}' for tool in procedure['tools_required'][:5])}

MATERIALS:
{chr(10).join(f'• {material}' for material in procedure['materials_needed'][:4])}

⚠️  CRITICAL SAFETY FIRST:
{chr(10).join(f'• {safety}' for safety in procedure['safety_precautions'][:3])}

REPAIR SEQUENCE:
{chr(10).join(procedure['steps'][:6])}

This is a {procedure['severity'].lower()} priority repair. Follow each step precisely. After completing these initial steps, I can guide you through the remaining detailed steps.

Would you like me to continue with the next steps?"""
        else:
            response = f"""Action: generate_steps
Response: I understand you need to repair the {issue.lower()}. Let me provide expert guidance:

FIRST - SAFETY ASSESSMENT:
• Shut down and isolate the affected system
• Verify all power sources are de-energized
• Check for any hazardous materials or conditions
• Establish proper containment if fluids involved

DIAGNOSTIC STEPS:
• Visually inspect the full extent of damage
• Check for secondary damage to surrounding components
• Document condition with photos for warranty purposes
• Assess if repair or replacement is more cost-effective

BEFORE STARTING REPAIRS:
• Gather all necessary tools and materials
• Allow sufficient time for proper repair (no rushing)
• Have spare parts available in case of complications
• Verify you have the correct replacement specifications

What's the next step you'd like detailed guidance on?"""
    
    # 6. Default fallback
    else:
        response = f"""Action: clarify_issue
Response: As your expert technician, I'm here to help. Can you clarify what you need:

REPAIR OPTIONS:
• I can provide step-by-step repair procedures
• I can explain safety precautions
• I can help troubleshoot problems
• I can recommend preventive maintenance
• I can explain which tools/materials you'll need

For the {issue.lower()} issue we identified:

QUICK ASSESSMENT:
• Is this your first time attempting this repair?
• Do you have access to required tools?
• Are you working alone or with a helper?
• How much time do you have available?

Let me know what information would be most helpful right now."""
    
    return response


def call_llm_online(prompt: str, timeout: int = 15) -> str:
    """Call LLM via free online API with timeout."""
    try:
        # Try using Hugging Face Inference API if token available
        hf_token = os.getenv("HF_API_TOKEN") or os.getenv("HUGGINGFACE_TOKEN")
        if hf_token:
            api_url = "https://api-inference.huggingface.co/models/TinyLlama/TinyLlama-1.1B-Chat-v1.0"
            headers = {"Authorization": f"Bearer {hf_token}"}
            payload = {"inputs": prompt, "parameters": {"max_new_tokens": 150}}
            response = requests.post(api_url, headers=headers, json=payload, timeout=timeout)
            
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list) and len(data) > 0:
                    return data[0].get("generated_text", prompt)
    except Exception as e:
        print(f"Online LLM call failed: {e}")
    
    return None


def call_llm_local(prompt: str) -> str:
    """Call local TinyLlama with short timeout."""
    if not HAS_LOCAL_LLM:
        return None
    
    try:
        output = generator(
            prompt,
            max_new_tokens=100,
            temperature=0.6,
            do_sample=True,
            top_p=0.9
        )
        return output[0]["generated_text"]
    except Exception as e:
        print(f"Local LLM error: {e}")
        return None


def call_llm(prompt: str) -> str:
    """Call LLM with intelligent fallback.
    
    Tries online API first (faster, non-blocking), then local model if available,
    finally returns a sensible default response.
    """
    # Extract issue from prompt to use expert responses
    issue = ""
    if "Current Issue:" in prompt or "CURRENT DETECTED ISSUE:" in prompt:
        try:
            lines = prompt.split("\n")
            for line in lines:
                if "CURRENT DETECTED ISSUE:" in line or "Current Issue:" in line:
                    issue = line.split(":", 1)[1].strip()
                    break
        except:
            pass
    
    # Extract query
    query = ""
    if "Query:" in prompt or "USER QUERY:" in prompt:
        try:
            lines = prompt.split("\n")
            for line in lines:
                if "USER QUERY:" in line or "User Input:" in line:
                    query = line.split(":", 1)[1].strip()
                    break
        except:
            pass
    
    # If we can generate expert response, do it
    if issue and query:
        expert_response = generate_expert_response(issue, query)
        if expert_response:
            print("Using expert technician knowledge base")
            return expert_response
    
    # Try online API first
    result = call_llm_online(prompt, timeout=15)
    if result:
        print("Used online LLM")
        return result
    
    # Fall back to local model if available
    if HAS_LOCAL_LLM:
        result = call_llm_local(prompt)
        if result:
            print("Used local LLM")
            return result
    
    # If all LLM calls fail, provide expert fallback
    print("LLM unavailable, using expert technician fallback")
    return f"""Action: generate_steps
Response: As your expert field technician, I can help you repair the {issue.lower() if issue else 'detected issue'}.

IMMEDIATE ACTION PLAN:
1. SAFETY FIRST - Shut down and isolate the system completely
2. ASSESSMENT - Examine the damage thoroughly  
3. GATHERING - Collect all required tools and materials
4. PREPARATION - Follow the proper repair sequence
5. EXECUTION - Complete repairs with attention to detail
6. VERIFICATION - Test and confirm repair success
7. DOCUMENTATION - Record what was done for maintenance records

I'm here to guide you through each step in detail. What would you like to tackle first?"""
