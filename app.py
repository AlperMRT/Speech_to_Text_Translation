import streamlit as st
from backend import transcribe_audio_file
import tempfile
import os
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Accessible Speech-to-Text",
    page_icon="🦻",
    layout="centered",
    initial_sidebar_state="auto",
)

st.title("Accessible Speech-to-Text Application")
st.markdown(
    """
    This application helps people with communication impairments to easily convert speech to text.
    You can upload an audio file or record your voice and get instant transcription results.
    """
)

# --- AUDIO FILE UPLOAD ---
st.header("1️⃣ Transcribe from Audio File")
uploaded_file = st.file_uploader(
    "Upload your audio file (wav, mp3, mp4, etc.)",
    type=["wav", "mp3", "mp4", "m4a"]
)

if "file_transcription" not in st.session_state:
    st.session_state.file_transcription = ""

if uploaded_file is not None:
    with st.spinner("Transcribing..."):
        temp_dir = "temp_files"
        os.makedirs(temp_dir, exist_ok=True)
        temp_audio_path = os.path.join(temp_dir, "input.mp3")
        with open(temp_audio_path, "wb") as temp_audio:
            temp_audio.write(uploaded_file.read())
        abs_audio_path = os.path.abspath(temp_audio_path).replace("\\", "/")
        try:
            transcription = transcribe_audio_file(abs_audio_path)
            st.session_state.file_transcription = transcription
            st.success("Transcription complete!")
        except Exception as e:
            st.session_state.file_transcription = ""
            st.error(f"Error during transcription: {e}")
        finally:
            if os.path.exists(abs_audio_path):
                os.remove(abs_audio_path)

if st.session_state.file_transcription:
    st.text_area("Transcribed Text:", st.session_state.file_transcription, height=200)

# --- MICROPHONE (HTML5 Recorder) ---
st.header("2️⃣ Record Audio via Microphone (Web Recorder)")
st.markdown("""
Use the recorder below to record your voice in the browser.  
After recording, download the audio file and **drag & drop or select it above** to get your transcription automatically.
""")

html_string = """
<div style="margin-bottom: 15px;">
  <audio id="audioPlayback" controls style="width:100%;"></audio><br>
  <button id="startBtn">Start Recording</button>
  <button id="stopBtn" disabled>Stop Recording</button>
  <a id="downloadLink" style="display: none;">Download Recording</a>
</div>
<script>
let mediaRecorder;
let audioChunks = [];

const startBtn = document.getElementById('startBtn');
const stopBtn = document.getElementById('stopBtn');
const audioPlayback = document.getElementById('audioPlayback');
const downloadLink = document.getElementById('downloadLink');

startBtn.onclick = async function() {
    audioChunks = [];
    startBtn.disabled = true;
    stopBtn.disabled = false;
    let stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    mediaRecorder = new MediaRecorder(stream);
    mediaRecorder.start();
    mediaRecorder.ondataavailable = e => audioChunks.push(e.data);
};

stopBtn.onclick = function() {
    mediaRecorder.stop();
    startBtn.disabled = false;
    stopBtn.disabled = true;
    mediaRecorder.onstop = function() {
        let blob = new Blob(audioChunks, { type: 'audio/wav' });
        let url = URL.createObjectURL(blob);
        audioPlayback.src = url;
        downloadLink.href = url;
        downloadLink.download = "recording.wav";
        downloadLink.style.display = 'inline';
        downloadLink.textContent = 'Download Recording';
    };
};
</script>
"""

components.html(html_string, height=220)
