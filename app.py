import streamlit as st
from utils.features import generate_script_from_transcript, get_transcript_from_channel , generate_audio_from_script, generate_short_video,get_font_list
from traceback import print_exc
import tempfile
import os




st.set_page_config(
    page_title="CREATE.AI",
    page_icon="🎥",
)



# Define constants
STEPS = {
    1: "Sample Scripts",
    2: "Generate Scripts",
    3: "Generate Audio",
    4: "Background Video",
}

FONT_LIST = get_font_list()

SESSION_STATE_VARS = ['sample_scripts', 'generated_scripts','transcript','audio','bg_video','subtitle_options','prompt']
OUTPUT_DIR = './output/'
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)
st.markdown(
    f"""
    <style>
    .stVideo {{
        height: {360}px;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)



def init_session_state():
    for var in SESSION_STATE_VARS:
        if var not in st.session_state:
            st.session_state[var] = ""

def sample_scripts_section():
    st.title("Step 1: Sample Scripts")

    # Define a two-column layout
    col1, col2 = st.columns(2)

    # Option 1: Enter Video Transcript
    with col1:
        st.header("Option 1: Enter sample scripts")
        st.text_area("Enter sample scripts", key="sample_scripts_textbox")
        st.session_state["sample_scripts"] = st.session_state["sample_scripts_textbox"]

    # Option 2: Generate Transcripts from YouTube
    with col2:
        st.header("Option 2: Extract sample scripts from YouTube")
        channel_id = st.text_input("Enter the YouTube Channel ID")
        limit = st.number_input("Enter the Limit for Short Videos", min_value=1, value=5, step=1)

        if st.button("Extract Transcripts"):
            with st.spinner("Retrieving transcripts from YouTube..."):
                if channel_id:
                    try:
                        sample_transcripts = get_transcript_from_channel(channel_id, limit)
                        st.text_area("Sample Scripts textbox", value=sample_transcripts)
                        st.session_state["sample_scripts"] = sample_transcripts
                        st.session_state["prompt"] = sample_transcripts
                        st.success("Transcripts retrieved successfully!")
                    except:
                        st.error("Error in retrieving transcripts")
                else:
                    st.error("Invalid Channel ID")
    

def generate_scripts_section():
    st.title("Step 2: Generate Scripts")
    # Define a two-column layout
    col1, col2 = st.columns(2)

    with col1:
        st.header("Prompt:")
        st.text(st.session_state["prompt"])

    with col2:
        st.header("Category:")
        category = st.text_input("Enter the category of the script")
        st.header("Number of Scripts:")
        num_of_scripts = st.number_input("Enter the number of scripts to generate", min_value=1, value=1, step=1)
    
    if st.button("Generate Scripts"):
        with st.spinner("Generating scripts..."):
            try:
                generated_scripts = generate_script_from_transcript(category, st.session_state["prompt"], num_of_scripts)
                st.session_state["generated_scripts"] = generated_scripts
                st.success("Scripts generated successfully!")
            except:
                print_exc()
                st.error("Error in generating scripts")
        


def generate_audio_section():
    st.title("Step 3: Generate Audio")
    script = st.text_area("Script", value=st.session_state["generated_scripts"])
    if st.button("Generate Audio"):
        with st.spinner("Generating audio..."):
            try:
                # audio_path = OUTPUT_DIR + "audio.mp3"
                audio_path = tempfile.NamedTemporaryFile(delete=False).name
                transcript = generate_audio_from_script(script,output_path=audio_path)
                st.session_state["transcript"] = transcript
                st.session_state["audio"] = audio_path
                st.success("Audio generated successfully!")
            except:
                print_exc()
                st.error("Error in generating audio")

        if st.session_state["audio"] != "":
            st.audio(st.session_state["audio"])


def background_video_section():
    st.title("Step 4: Background Video")
    #video upload
    st.subheader("Upload your background video")
    if 'bg_video' not in st.session_state:
        st.session_state['bg_video'] = ""
    col1, col2 = st.columns(2)
    with col1:
        uploaded_file = st.file_uploader("Choose a file", type=["mp4"])
        if uploaded_file is not None:
            video = tempfile.NamedTemporaryFile(delete=False)
            video.write(uploaded_file.read())
            st.session_state["bg_video"] = video.name
            st.success("Video uploaded successfully!")
        else:
            st.error("Please upload a video")
    
    with col2:
        if st.session_state["bg_video"] != "":
            st.video(st.session_state["bg_video"])




# def subtitle_options_section():
#     st.title("Step 6: Subtitle Options")
#     st.subheader("Customize Subtitle Settings")
#     st.video(st.session_state["bg_video"])
#     col1, col2 = st.columns(2)
#     with col1:
#         st.subheader("Font Settings")
#         font_size = st.number_input("Font Size", min_value=1, value=35, step=1)
#         font_color = st.color_picker("Font Color", "#FFFFFF")
#         st.text("Selected Font Color Hex Code: " + font_color)
#         stroke_color = st.color_picker("Stroke Color", "#000000")
#         st.text("Selected Stroke Color Hex Code: " + stroke_color)
#         stroke_width = st.number_input("Stroke Width", min_value=0, value=0, step=1)
#         font = st.text_input("Font (e.g., Liberation-Mono-Bold)", "Liberation-Mono-Bold")


#     with col2:
#         st.subheader("Position Settings")
#         position_x = st.selectbox("Horizontal Position", ["left", "center", "right"], index=1)
#         position_y = st.selectbox("Vertical Position", ["top", "center", "bottom"], index=1)
#         words_per_line = st.number_input("Words Per Line", min_value=1, value=3, step=1)

#     # Save the selected subtitle options to the session state
#     st.session_state["subtitle_options"] = {
#         "font_size": font_size,
#         "font_color": font_color,
#         "stroke_color": stroke_color,
#         "stroke_width": stroke_width,
#         "font": font,
#         "position_x": position_x,
#         "position_y": position_y,
#         "words_per_line": words_per_line,
#     }

def subtitle_options_section():
    st.title("Step 5: Subtitle Options")
    st.subheader("Customize Subtitle Settings")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Font Settings")

        # font = st.text_input("Font", "Liberation-Mono-Bold")

        font = st.selectbox("Font", FONT_LIST, index=0)


        font_size = st.slider("Font Size", min_value=1, max_value=100, value=35, step=1)
        stroke_width = st.slider("Stroke Width", min_value=0, max_value=10, value=0, step=1)

        subcol1, subcol2 = st.columns(2)
        with subcol1:
            font_color = st.color_picker("Font Color", "#FFFFFF")
        with subcol2:
            st.text("Hex Code: " + font_color)

        subcol1, subcol2 = st.columns(2)
        with subcol1:
            stroke_color = st.color_picker("Stroke Color", "#000000")
        with subcol2:
            st.text("Hex Code: " + stroke_color)




        # font = st.text_input("Font (e.g., Liberation-Mono-Bold)", "Liberation-Mono-Bold")

    with col2:
        st.subheader("Position Settings")
        position_x = st.selectbox("Horizontal Position", ["left", "center", "right"], index=1)
        position_y = st.selectbox("Vertical Position", ["top", "center", "bottom"], index=1)
        words_per_line = st.slider("Words Per Line", min_value=1, max_value=10, value=3, step=1)
    
    #apply filter checkbox , filter color and transparency
    st.markdown("---")
    st.subheader("Apply Filter")
    apply_filter = st.checkbox("Apply Filter")
    if apply_filter:
        filter_color = st.color_picker("Filter Color", "#000000")
        transparency = st.slider("Transparency", min_value=0.0, max_value=1.0, value=0.25, step=0.01)
        st.session_state["filter_color"] = filter_color
        st.session_state["transparency"] = transparency
    else:
        st.session_state["filter_color"] = ""
        st.session_state["transparency"] = 0.0





    # Save the selected subtitle options to the session state
    st.session_state["subtitle_options"] = {
        "transcript_json": st.session_state["transcript"],
        "font_size": font_size,
        "font_color": font_color,
        "stroke_color": stroke_color,
        "stroke_width": stroke_width,
        "font": font,
        "position_x": position_x,
        "position_y": position_y,
        "words_per_line": words_per_line,
        "filter_color": st.session_state["filter_color"],
        "filter_transparency": st.session_state["transparency"],
    }
    st.markdown("---")
    # Add a button to generate a sample video
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Generate Sample Video"):
            with st.spinner("Generating sample video..."):
                try:
                    # video_path = OUTPUT_DIR + "video.mp4"
                    video_path = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4').name
                    subtitle_options = st.session_state["subtitle_options"]
                    generate_short_video(
                        audio_path=st.session_state["audio"],
                        video_path=st.session_state["bg_video"],
                        output_path=video_path,
                        subtitle_options=subtitle_options,
                        sample_video=True,
                    )
                    st.video(video_path)
                    st.success("Sample video generated successfully!")
                except:
                    print_exc()
                    st.error("Error in generating sample video")

    with col2:
        if st.button("Generate Full Video"):
            with st.spinner("Generating video..."):
                try:
                    # video_path = OUTPUT_DIR + "video.mp4"
                    # video_path = tempfile.NamedTemporaryFile(delete=False).name
                    video_path = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4').name
                    subtitle_options = st.session_state["subtitle_options"]
                    generate_short_video(
                        audio_path=st.session_state["audio"],
                        video_path=st.session_state["bg_video"],
                        output_path=video_path,
                        subtitle_options=subtitle_options,
                    )
                    st.video(video_path)
                    st.success("Video generated successfully!")
                except:
                    print_exc()
                    st.error("Error in generating video")


def main():

    st.title("🎥 CREATE.AI 📜")
    st.subheader("AI Powered Video Creation Platform")

    st.markdown("---")
    sample_scripts_section()

    st.markdown("---")
    generate_scripts_section()

    st.markdown("---")
    generate_audio_section()

    st.markdown("---")
    background_video_section()

    st.markdown("---")
    subtitle_options_section()

if __name__ == "__main__":
    init_session_state()
    main()
