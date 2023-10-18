import streamlit as st
from social_media.youtube import YouTubeTranscriptExtractor

# Define the Streamlit app
#this is sample server

def main():
    st.set_page_config(
        page_title="Social Media Transcript Extractor",
        page_icon="🔍"
    )
    st.title("Social Media Transcript Extractor")

    # User input: Choose a social media platform
    social_media_platform = st.selectbox("Choose a Social Media Platform", ["YouTube","Instagram"])

    if social_media_platform == "YouTube":
        st.header("YouTube Data Collection")

        # User input: Fetch data from channel ID or video link
        data_source = st.radio("Select data source:", ["Channel ID", "Video Link"])

        if data_source == "Channel ID":
            channel_id = st.text_input("Enter YouTube Channel ID:")
            limit = st.number_input("Enter the number of videos to fetch:", min_value=0, step=10, value=0)
            st.info("Enter 0 to fetch all videos.")
        else:
            video_link = st.text_input("Enter YouTube Video Link:")

        # Button to trigger data collection
        if st.button("Fetch Data"):
            if social_media_platform == "YouTube":
                if data_source == "Channel ID":
                    if not channel_id:
                        st.warning("Please enter a YouTube Channel ID.")
                    else:
                        extractor = YouTubeTranscriptExtractor()

                        with st.spinner(f"Fetching videos for channel: {channel_id}..."):
                            short_videos = extractor.get_short_videos_from_channel(channel_id)

                        st.info(f"Found {len(short_videos)} short videos.")
                        if not short_videos:
                            st.error("No short videos found.")
                        else:
                            if limit > 0:
                                short_videos = short_videos[:limit]

                            with st.spinner(f"Fetching transcripts for {len(short_videos)} videos..."):
                                transcripts = extractor.get_transcripts(short_videos)
                                text_transcripts = extractor.extract_text_from_transcripts(transcripts)

                                transcript_text = []
                                for i, transcript in enumerate(text_transcripts):
                                    text = f"Video {i + 1}: {transcript['text']}."
                                    transcript_text.append(text)

                                transcript_text = '\n'.join(transcript_text)
                                st.subheader("Transcripts")
                                st.code(transcript_text, "plaintext")

                elif data_source == "Video Link":
                    if not video_link:
                        st.warning("Please enter a YouTube Video Link.")
                    else:
                        extractor = YouTubeTranscriptExtractor()

                        with st.spinner(f"Fetching transcript for video: {video_link}..."):
                            transcript = extractor.get_transcripts([video_link])

                        if not transcript:
                            st.error("No transcript found.")
                        else:
                            transcript_text = extractor.extract_text_from_transcripts(transcript)

                            st.subheader("Transcript")
                            st.code(transcript_text[0]['text'], "plaintext")

    elif social_media_platform == "Instagram":
        st.header("Instagram Data Collection")
        st.warning("Coming soon!")


# Run the Streamlit app
if __name__ == "__main__":
    main()
