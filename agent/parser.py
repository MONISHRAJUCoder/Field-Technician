def parse_output(output):
    """Parse expert technician response with proper action extraction."""
    try:
        lines = output.split("\n")

        action = None
        response = None
        
        # Look for Action: and Response: lines
        for i, line in enumerate(lines):
            if line.startswith("Action:"):
                action = line.split(":", 1)[1].strip().lower()
            elif line.startswith("Response:"):
                # Take everything after "Response:" as the response
                response_text = line.split(":", 1)[1].strip()
                # Include remaining lines as part of the response
                remaining = "\n".join(lines[i+1:])
                response = (response_text + "\n" + remaining).strip() if remaining else response_text
                break
        
        # Validate action
        valid_actions = ["generate_steps", "next_step", "repeat_step", "stop", "clarify", 
                        "safety_warning", "maintenance_tip", "clarify_issue"]
        
        if action and action in valid_actions and response:
            return action, response
        
        # Fallback parsing
        if len(lines) >= 2:
            try:
                action = lines[0].split(":")[1].strip().lower()
                response = lines[1].split(":")[1].strip()
                if action in valid_actions:
                    return action, response
            except:
                pass
        
        # Default fallback
        return "clarify", "I understand. Let me help with your repair. Please describe what step you're on or what specific guidance you need."
        
    except Exception as e:
        print(f"Parser error: {e}")
        return "clarify", "Let me assist you with the repair. What would you like help with?"