"""Technical expertise database for field technician assistant."""

# Technical repair procedures for common issues
TECHNICAL_PROCEDURES = {
    "broken pipe": {
        "diagnosis": "Broken or cracked pipe causing fluid leakage",
        "severity": "HIGH - May cause equipment damage or safety hazard",
        "tools_required": ["Pipe cutter", "Wrench set", "Gasket puller", "Sealant tape", "New pipe section"],
        "materials_needed": ["Replacement pipe", "Gaskets/O-rings", "Thread sealant", "Anti-corrosion coating"],
        "safety_precautions": [
            "Depressurize the system completely before work",
            "Drain all remaining fluid into containment",
            "Wear safety glasses and gloves",
            "Use proper respiratory protection if fumes present",
            "Ensure work area is well-ventilated"
        ],
        "steps": [
            "1. SAFETY: Shut down the system and lockout/tagout",
            "2. ASSESSMENT: Locate the exact break point and check surrounding components for damage",
            "3. DRAINAGE: Place containment vessel and drain system completely",
            "4. REMOVAL: Using pipe cutter, remove 2-3 inches of pipe on each side of the break to ensure clean edges",
            "5. INSPECTION: Examine pipe interior for scale, debris, or corrosion",
            "6. CLEANING: Clean pipe ends with wire brush to remove burrs and scale",
            "7. MEASUREMENT: Precisely measure the removed section and prepare replacement",
            "8. INSTALLATION: Install new pipe section using proper fittings - ensure thread sealant applied",
            "9. TIGHTENING: Use torque wrench for proper fastener tension per specifications",
            "10. TESTING: Pressure test at 150% of operating pressure for 30 minutes",
            "11. VERIFICATION: Inspect all connections for leaks using soap solution",
            "12. RESTORATION: Return system to operation gradually, monitoring pressure and temperature"
        ],
        "common_causes": ["Age-related corrosion", "Water hammer", "Thermal stress", "Material fatigue", "Improper installation"],
        "preventive_maintenance": "Inspect pipes quarterly, replace annually if over 5 years old, monitor system pressure"
    },
    
    "rusted component": {
        "diagnosis": "Surface or structural rust due to moisture exposure",
        "severity": "MEDIUM - May reduce structural integrity over time",
        "tools_required": ["Wire brush", "Sandpaper (80-120 grit)", "Angle grinder", "Rust converter", "Paint applicator"],
        "materials_needed": ["Rust converter", "Epoxy primer", "Protective paint", "Corrosion inhibitor"],
        "safety_precautions": [
            "Wear safety glasses and dust mask when grinding",
            "Ensure proper ventilation",
            "Disconnect power before any grinding work",
            "Allow rust converter to dry completely (check label)"
        ],
        "steps": [
            "1. ASSESSMENT: Measure rust depth using pit gauge - if > 3mm, component may need replacement",
            "2. CLEANING: Use wire brush to remove loose rust",
            "3. GRINDING: For heavy rust, use angle grinder with wire wheel to expose bare metal",
            "4. SURFACE PREP: Sand with 80-grit paper, then 120-grit for smooth finish",
            "5. RUST CONVERSION: Apply rust converter per manufacturer instructions - allows painting over remaining rust",
            "6. DRYING: Allow 24 hours for rust converter to cure completely",
            "7. PRIMING: Apply epoxy primer in 2 coats, minimum 6 hours between coats",
            "8. PAINTING: Apply protective paint in 2 coats",
            "9. CURING: Allow 7 days before returning to service",
            "10. COATING: For critical components, add corrosion inhibitor coating annually"
        ],
        "common_causes": ["Water exposure", "Poor drainage design", "Missing protective coating", "Salt environment"],
        "preventive_maintenance": "Annual inspection, protective coating every 2 years, ensure proper drainage"
    },

    "burn marks": {
        "diagnosis": "Thermal damage or electrical burn on component",
        "severity": "HIGH - Indicates potential electrical or thermal hazard",
        "tools_required": ["Multimeter", "Thermal camera", "Screwdrivers", "Component extractor"],
        "materials_needed": ["Replacement component", "Thermal paste", "Insulation tape"],
        "safety_precautions": [
            "CRITICAL: Verify all power is OFF and line is grounded",
            "Do NOT touch burned area - risk of burns and electrical hazard",
            "Allow component to cool for minimum 30 minutes",
            "Check for smoke or fume release"
        ],
        "steps": [
            "1. EMERGENCY: Immediately cut power to affected circuit",
            "2. COOLING: Allow minimum 30 minutes for complete cooling",
            "3. ASSESSMENT: Determine cause - electrical short, friction, or thermal runaway",
            "4. ELECTRICAL TEST: Using multimeter, test for continuity and ground faults",
            "5. ROOT CAUSE: Investigate why component overheated (bearing failure, electrical fault, alignment issue)",
            "6. DOCUMENTATION: Photograph damage for warranty/insurance claims",
            "7. REPLACEMENT: Remove damaged component and install new one (must be same specification)",
            "8. VERIFICATION: Re-test electrical connections and thermal monitoring",
            "9. OPERATION TEST: Run at reduced power for 15 minutes, monitor temperature",
            "10. FULL RESTART: Gradually return to normal operation"
        ],
        "common_causes": ["Electrical short circuit", "Bearing seizure", "Misalignment", "Inadequate cooling"],
        "preventive_maintenance": "Monthly thermal imaging, quarterly bearing inspection, annual electrical certification"
    },

    "pipe leak": {
        "diagnosis": "Fluid leakage from joint, crack, or hole",
        "severity": "MEDIUM to HIGH - Depends on leak rate and fluid type",
        "tools_required": ["Wrenches", "Pipe compound gauge", "Sealant applicator", "Leak stop clamp (temporary)"],
        "materials_needed": ["Pipe sealant tape", "Thread compound", "Gaskets", "Emergency repair clamp (if needed)"],
        "safety_precautions": [
            "Contain spilled fluid in proper containment",
            "Identify fluid type - may be toxic or flammable",
            "Wear chemical-resistant gloves and apron",
            "Ensure proper disposal of contaminated materials"
        ],
        "steps": [
            "1. LOCATION: Identify exact leak point - joint, crack, or seal failure",
            "2. SAFETY: Reduce system pressure if possible (verify safe to do so)",
            "3. CONTAINMENT: Place drain pan or absorbent material under leak",
            "4. TEMPORARY FIX (if needed): Apply emergency repair clamp to buy time",
            "5. INSPECTION: Check if leak is from fitting or pipe body",
            "6. IF JOINT LEAK: Try tightening fitting 1/2 turn clockwise with wrench",
            "7. IF STILL LEAKING: Shut down system and depressurize",
            "8. REMOVAL: Disconnect leaking fitting",
            "9. CLEANING: Remove old sealant and thread compound completely",
            "10. PREP: Wrap threads with sealant tape (minimum 3 layers, clockwise)",
            "11. COMPOUND: Apply new thread compound to male threads",
            "12. INSTALLATION: Hand-tighten, then use wrench for 1.5 turns additional",
            "13. TEST: Restart system and monitor for 30 minutes",
            "14. REPAIR LOG: Document repair date, fluid amount lost, parts replaced"
        ],
        "common_causes": ["Vibration loosening connections", "Thermal expansion", "Age-related seal failure", "Installation error"],
        "preventive_maintenance": "Monthly visual inspection, annual pressure test, quarterly fluid level check"
    },

    "damaged component": {
        "diagnosis": "Component showing physical deformation, dents, or failure",
        "severity": "MEDIUM - Depends on component function",
        "tools_required": ["Diagnostic tools specific to component", "Replacement parts kit", "Alignment tools"],
        "materials_needed": ["Replacement component", "Fasteners", "Sealing compound"],
        "safety_precautions": [
            "Wear appropriate PPE for component type",
            "Ensure system is properly de-energized",
            "Check for sharp edges or hazards"
        ],
        "steps": [
            "1. IDENTIFICATION: Document component model, serial number, and installation date",
            "2. FAILURE ANALYSIS: Determine root cause of damage",
            "3. ASSESSMENT: Determine if repair or replacement is cost-effective",
            "4. PROCUREMENT: Order replacement component with 48-hour delivery if critical",
            "5. REMOVAL: Carefully remove damaged component following proper procedure",
            "6. INSPECTION: Inspect mounting points for secondary damage",
            "7. CLEANING: Clean mounting surfaces to remove corrosion or debris",
            "8. INSTALLATION: Install replacement following manufacturer specifications",
            "9. ALIGNMENT: Verify proper alignment using precision tools",
            "10. FASTENING: Tighten all fasteners to specification torque values",
            "11. TESTING: Perform functional test at 50% capacity before full operation",
            "12. DOCUMENTATION: Update maintenance records with replacement details"
        ],
        "common_causes": ["Impact or collision", "Fatigue failure", "Design defect", "Improper maintenance"],
        "preventive_maintenance": "Quarterly visual inspection, annual condition assessment"
    }
}

def get_technical_procedure(issue):
    """Get detailed technical procedure for an issue."""
    issue_key = issue.lower().replace("detected issue: ", "").strip()
    
    for key in TECHNICAL_PROCEDURES:
        if key in issue_key.lower() or issue_key in key:
            return TECHNICAL_PROCEDURES[key]
    
    return None

def format_procedure_for_technician(procedure):
    """Format procedure into technician-friendly output."""
    if not procedure:
        return None
    
    output = f"""
TECHNICAL REPAIR PROCEDURE
{'='*60}

ISSUE DIAGNOSIS:
{procedure['diagnosis']}

SEVERITY LEVEL: {procedure['severity']}

REQUIRED TOOLS:
{chr(10).join(f'  • {tool}' for tool in procedure['tools_required'])}

MATERIALS NEEDED:
{chr(10).join(f'  • {material}' for material in procedure['materials_needed'])}

⚠️  SAFETY PRECAUTIONS:
{chr(10).join(f'  • {safety}' for safety in procedure['safety_precautions'])}

STEP-BY-STEP REPAIR PROCEDURE:
{chr(10).join(f'  {step}' for step in procedure['steps'])}

ROOT CAUSES (To prevent future issues):
{chr(10).join(f'  • {cause}' for cause in procedure['common_causes'])}

PREVENTIVE MAINTENANCE:
{procedure['preventive_maintenance']}
"""
    return output
