# 🤖 Expert Field Technician Assistant

An AI-powered field assistant for detecting equipment issues and providing professional repair guidance.

## Features

- **Image Analysis**: Automatically detects and analyzes equipment issues from uploaded images
- **Expert Technician Knowledge**: Professional repair procedures with tools, materials, and safety warnings
- **Multi-model Support**: Works with LLaVA-1.5-7b-hf vision model with graceful fallbacks
- **AI Assistance**: Provides step-by-step repair guidance from a 15+ year expert technician perspective
- **Speech Output**: Converts responses to speech for hands-free operation
- **Memory System**: Maintains conversation history and context
- **Safety First**: Emphasizes critical safety precautions and hazard awareness

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Optional: For enhanced vision capabilities, set Hugging Face token:
```bash
set HF_API_TOKEN=your_hf_token_here
```

## Usage

### Run the App

```bash
streamlit run app.py
```

The app will start at `http://localhost:8501`

### Upload an Image

1. Click "Upload Image" and select equipment photo
2. The app automatically detects the issue
3. Ask specific questions about repair, safety, prevention, or next steps
4. Get professional expert technician guidance with:
   - Required tools and materials
   - Step-by-step repair procedures
   - Safety precautions (⚠️ warnings)
   - Root cause analysis
   - Preventive maintenance recommendations

## How Detection Works

The system uses a multi-tier detection pipeline:

1. **Filename Extraction**: Parses issue from filename (e.g., "broken_pip1.jpg" → "Broken pipe")
2. **LLaVA Vision Model**: Analyzes image content for detailed issue identification
3. **Color Analysis**: Detects rust (red>green+40), corrosion (orange), burn marks, wear patterns
4. **Fallback**: Basic image analysis when other methods unavailable

## Expert Response Types

The system intelligently routes user queries to appropriate expert responses:

- **Repair Steps**: "How do I fix this?" → Detailed step-by-step procedures
- **Safety Warnings**: "What are the precautions?" → Critical hazard identification
- **Prevention**: "How can I prevent this?" → Maintenance schedules and preventive care
- **Troubleshooting**: "Something went wrong" → Diagnostic guidance
- **Next Steps**: "What's next?" → Continuation of repair sequence

## Project Structure

```
├── app.py                 # Main Streamlit app
├── agent/
│   ├── agent_core.py     # Main agent orchestration
│   ├── memory.py         # Session memory management
│   └── parser.py         # LLM response parsing
├── vision/
│   └── vision.py         # Image detection with LLaVA support
├── technician/
│   └── expertise.py      # Professional repair procedures
├── llm/
│   └── llm_engine.py     # LLM integration with expert responses
├── rag/
│   ├── loader.py         # Document loading
│   ├── retriever.py      # Context retrieval
│   └── prompt_builder.py # System prompt generation
├── speech/
│   └── speech_engine.py  # Text-to-speech
├── data/
│   ├── images/           # Sample images
│   └── manuals/          # Technical reference manuals
└── requirements.txt      # Python dependencies
```

## Environment Variables (Optional)

- `HF_API_TOKEN`: Hugging Face token for LLaVA vision model
- `HUGGINGFACE_TOKEN`: Alternative Hugging Face token

## System Requirements

- Python 3.12+
- Virtual environment (recommended)
- 4GB RAM minimum
- Windows/Linux/Mac

## Troubleshooting

**Detection returns "unknown"?**
- Ensure image filename contains issue hint (e.g., "broken_pipe.jpg")
- Try image analysis with clear, well-lit photos
- Ensure LLaVA model can be downloaded from Hugging Face

**Responses taking too long?**
- System uses expert knowledge base for instant responses
- Should return in <1 second
- Check internet connection for model access

**Installation issues?**
- Use Python 3.12 or higher
- Create a fresh virtual environment
- Run `pip install -r requirements.txt`

## Credits

Built as Expert Field Technician Assistant - providing professional maintenance and repair guidance.

