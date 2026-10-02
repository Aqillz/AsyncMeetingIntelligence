# frontend.py
import streamlit as st
import requests

st.set_page_config(page_title="Meeting Minutes AI", page_icon="📝", layout="centered")
st.title("📝 Automated Meeting Minutes Engine")

# Create tabs for the UI
tab1, tab2 = st.tabs(["✨ Generate New", "📚 History"])

with tab1:
    st.markdown("Paste your raw meeting transcript below to instantly extract key decisions and action items.")
    transcript_input = st.text_area("Meeting Transcript", height=250)

    if st.button("Generate Minutes", type="primary"):
        if not transcript_input.strip():
            st.warning("Please paste a transcript first.")
        else:
            with st.spinner("AI is analyzing the transcript..."):
                try:
                    response = requests.post("http://127.0.0.1:8000/api/generate", json={"transcript": transcript_input})
                    response.raise_for_status()
                    data = response.json()
                    
                    st.success("Analysis Complete & Saved to Database!")
                    st.subheader("Action Items & Summary")
                    
                    minutes_text = data.get("minutes", "No content returned.")
                    st.write(minutes_text)
                    
                    # --- NEW: Download Button for New Generation ---
                    st.download_button(
                        label="📥 Download Minutes (.txt)",
                        data=minutes_text,
                        file_name="meeting_minutes.txt",
                        mime="text/plain"
                    )
                    
                except requests.exceptions.ConnectionError:
                    st.error("Failed to connect to the backend. Is your FastAPI server running?")
                except Exception as e:
                    st.error(f"An error occurred: {e}")

with tab2:
    st.header("Recent Meetings")
    if st.button("Refresh History"):
        try:
            response = requests.get("http://127.0.0.1:8000/api/history")
            response.raise_for_status()
            history_data = response.json()
            
            if not history_data:
                st.info("No meetings saved yet.")
            else:
                for meeting in history_data:
                    with st.expander(f"Meeting {meeting['id']} - {meeting['created_at'][:10]}"):
                        st.markdown("**Action Items:**")
                        st.write(meeting['minutes'])
                        
                        # --- NEW: Download Button for History ---
                        # Note: 'key' must be unique for every button in a loop
                        st.download_button(
                            label="📥 Download this record",
                            data=meeting['minutes'],
                            file_name=f"meeting_{meeting['id']}_minutes.txt",
                            mime="text/plain",
                            key=f"download_{meeting['id']}"
                        )
                        
                        st.markdown("**Original Transcript:**")
                        st.caption(meeting['transcript'])
        except Exception as e:
            st.error("Could not load history. Is the backend running?")