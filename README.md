# 🤖 Intelligent Technician Assistant

An AI-powered field assistant for detecting equipment issues and providing repair guidance.

## Features

- **Image Analysis**: Automatically detects and analyzes equipment issues from uploaded images
- **Multi-model Support**: Works with optional YOLO and other vision models, with graceful fallbacks
- **AI Assistance**: Provides step-by-step repair guidance
- **Speech Output**: Converts responses to speech for hands-free operation
- **Memory System**: Maintains conversation history and context

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Optional: For enhanced object detection, install YOLO:
```bash
pip install ultralytics torch torchvision
```

## Usage

### Run the App

```bash
streamlit run app.py
```

The app will start at `http://localhost:8501`

### Upload an Image

1. Click "Upload Image" and select a photo
2. The app automatically detects issues in the image
3. Describe what help you need
4. Get AI-powered repair guidance

## How Detection Works

The system uses a multi-tier detection pipeline:

1. **YOLO Detection** (if available): Detects objects in images
2. **Color Analysis**: Identifies rust, corrosion, burn marks, and wear patterns
3. **Fallback**: Basic image analysis when other methods unavailable

## Environment Variables (Optional)

- `HF_API_TOKEN`: For using Hugging Face vision models
- `QWEN_ENDPOINT`: For using custom QWEN model endpoints

## Project Structure

```
├── app.py                 # Main Streamlit app
├── agent/                 # AI agent and memory system
├── vision/               # Image detection modules
├── rag/                  # Document retrieval system
├── speech/               # Text-to-speech engine
├── data/
│   ├── images/          # Sample images
│   └── manuals/         # Reference manuals
└── llm/                 # LLM integration
```

## Troubleshooting

**Detection returns "unknown"?**
- Ensure image is clear and well-lit
- Try with a different image

**Dependencies not installing?**
- Use Python 3.8+
- Consider using a virtual environment

## Notes

- The app stores temporary uploads in `temp.jpg`
- Manual data is loaded from `data/manuals/` for context
