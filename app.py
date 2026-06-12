import streamlit as st

from vision.vision import detect_issue
from agent.agent_core import run_agent
from agent.memory import init_memory
from speech.speech_engine import speak

# ✅ init memory
if "session" not in st.session_state:
    st.session_state.session = init_memory()

st.title("🤖 Intelligent Technician Assistant")

# ✅ image upload
image = st.file_uploader("Upload Image", type=["jpg", "png"])

if image:
    with open("temp.jpg", "wb") as f:
        f.write(image.getbuffer())

    issue = detect_issue("temp.jpg")
    st.session_state.session["issue"] = issue

    st.success(f"Detected Issue: {issue}")

# ✅ user input
query = st.text_input("🎤 Ask something")

if query and st.session_state.session["issue"]:

    action, response, raw = run_agent(
        st.session_state.session,
        query
    )

    st.subheader("🤖 Assistant")
    st.write(response)

    speak(response)

    # ✅ execute based on LLM decision

    if action == "generate_steps":
        steps = [s.strip() for s in response.split(",") if s.strip()]

        st.session_state.session["steps"] = steps
        st.session_state.session["current"] = 0

        if steps:
            st.write(f"👉 {steps[0]}")
            speak(steps[0])

    elif action == "next_step":
        i = st.session_state.session["current"] + 1

        if i < len(st.session_state.session["steps"]):
            st.session_state.session["current"] = i

            step = st.session_state.session["steps"][i]
            st.write(f"👉 {step}")
            speak(step)

    elif action == "repeat_step":
        i = st.session_state.session["current"]

        if i < len(st.session_state.session["steps"]):
            step = st.session_state.session["steps"][i]
            st.write(f"👉 {step}")
            speak(step)

    elif action == "stop":
        st.session_state.session["steps"] = []
        st.session_state.session["current"] = 0
        st.write("Stopped")
        speak("Stopping guidance")