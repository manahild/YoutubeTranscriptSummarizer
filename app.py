import streamlit as st
import google.generativeai as genai
api_key = "your api key"
genai.configure(api_key=api_key)

# Now you can use the GenerativeAI functionality
model = genai.GenerativeModel('gemini-1.0-pro-latest')

# Check if API key is provided
if api_key is None:
    st.error("Please provide the Google API key in the environment variable GOOGLE_API_KEY.")
    st.stop()  # Stop execution if API key is not provided


from youtube_transcript_api import YouTubeTranscriptApi

prompt = """You are a YouTube video summarizer. You will be taking the transcript text
and summarizing the entire video and providing the important summary in points
within 250 words. Please provide the summary of the text given here:  """

# Function to extract transcript details from YouTube videos
def extract_transcript_details(youtube_video_url):
    try:
        video_id = youtube_video_url.split("=")[1]
        transcript_text = YouTubeTranscriptApi.get_transcript(video_id)

        transcript = ""
        for i in transcript_text:
            transcript += " " + i["text"]

        return transcript

    except Exception as e:
        raise e

# Function to generate summary using Google Generative AI
def generate_gemini_content(transcript_text, prompt):
    model = genai.GenerativeModel('gemini-1.0-pro-latest')
    response = model.generate_content(prompt + transcript_text)
    return response.text

st.title("YouTube Transcript to Detailed Notes Converter")
youtube_link = st.text_input("Enter YouTube Video Link:")

if youtube_link:
    video_id = youtube_link.split("=")[1]
    st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_column_width=True)

if st.button("Get Detailed Notes"):
    transcript_text = extract_transcript_details(youtube_link)

    if transcript_text:
        summary = generate_gemini_content(transcript_text, prompt)
        st.markdown("## Detailed Notes:")
        st.write(summary)
