from utils.dataCollection.social_media.youtube import YouTubeTranscriptExtractor
from utils.audioGenerator import AudioGenerator
from utils.videoGenerator import VideoGenerator
from utils.scriptGenerator import ScriptGenerator
from traceback import print_exc
from utils.videoGenerator import VideoGenerator
from dotenv import load_dotenv
import os
import json
import tempfile




load_dotenv()


def get_transcript_from_channel(channel_id , limit = 10):
    extractor = YouTubeTranscriptExtractor()
    short_videos = extractor.get_short_videos_from_channel(channel_id)
    short_videos = short_videos[:limit]
    transcripts = extractor.get_transcripts_from_videos(short_videos)
    transcript_texts = extractor.extract_text_from_transcripts(transcripts)
    transcript_str = ""
    for i,transcript in enumerate(transcript_texts):
        transcript_str += f"video {i+1}: {transcript['text']} \n"
    return transcript_str


def generate_script_from_transcript(category,sample_transcripts,num_of_scripts = 1):
    script_generator = ScriptGenerator(api_key = os.getenv("OPENAI_API_KEY"))
    script = script_generator.generate_scripts(category,sample_transcripts,num_of_scripts)
    return script


def generate_audio_from_script(script,output_path):
    gcp_credentials = {
        "type": os.environ.get("GCP_TYPE"),
        "project_id": os.environ.get("GCP_PROJECT_ID"),
        "private_key_id": os.environ.get("GCP_PRIVATE_KEY_ID"),
        "private_key": os.environ.get("GCP_PRIVATE_KEY"),
        "client_email": os.environ.get("GCP_CLIENT_EMAIL"),
        "client_id": os.environ.get("GCP_CLIENT_ID"),
        "auth_uri": os.environ.get("GCP_AUTH_URI"),
        "token_uri": os.environ.get("GCP_TOKEN_URI"),
        "auth_provider_x509_cert_url": os.environ.get("GCP_AUTH_PROVIDER_X509_CERT_URL"),
        "client_x509_cert_url": os.environ.get("GCP_CLIENT_X509_CERT_URL"),
        "universe_domain": os.environ.get("GCP_UNIVERSE_DOMAIN")
    }

    audio_generator = AudioGenerator(credentials_json=gcp_credentials)
    audio_generator.generate_audio(script,output_file_path=output_path)
    transcript = audio_generator.generate_transcript(output_path)
    return transcript






def generate_short_video(
        audio_path,
        video_path,
        output_path,
        subtitle_options,
        magick_binary="./utils/magick",
        add_audio=True,
        add_subtitles=True,
        sample_video = False,
    ):
        # Generate the video
        magick_binary = os.path.abspath(magick_binary)
        transcript_json = subtitle_options.get("transcript_json", None)
        screen_size = subtitle_options.get("screen_size", (720 /16 * 9 , 720))
        font_size = subtitle_options.get("font_size", 35)
        font_color = subtitle_options.get("font_color", "#FFFFFF")
        stroke_color = subtitle_options.get("stroke_color", "#000000")
        stroke_width = subtitle_options.get("stroke_width", 0)
        font = subtitle_options.get("font", "Liberation-Mono-Bold")
        position_x = subtitle_options.get("position_x", "center")
        position_y = subtitle_options.get("position_y", "center")
        words_per_line = subtitle_options.get("words_per_line", 3)
        filter_color = subtitle_options.get("filter_color", "#000000")
        filter_transparency = subtitle_options.get("filter_transparency",0)

        fps = 24
        if sample_video:
            #transcript = only words_per_line words for sample video
            transcript_json = transcript_json[:words_per_line]
            fps = 1

        video_generator = VideoGenerator(magick_binary=magick_binary)
        subtitles = video_generator.generate_subtitle(
            transcript_json=transcript_json,
            screen_size=screen_size,
            font_size=font_size,
            font_color=font_color,
            stroke_color=stroke_color,
            stroke_width=stroke_width,
            font=font,
            position_x=position_x,
            position_y=position_y,
            words_per_line=words_per_line,
            
        )



        video_generator.generate_video(
            audio_file=audio_path,
            video_file=video_path,
            output_file=output_path,
            subtitles=subtitles,
            fps = fps,
            filter_color = filter_color,
            filter_transparency = filter_transparency,
        )


def apply_filter_to_video(
          video_path,
            output_path,
            color = "(0,0,0)",
            transparency = 0.25,
            magick_binary="./utils/magick",
        ):
        magick_binary = os.path.abspath(magick_binary)
        video_generator = VideoGenerator(magick_binary=magick_binary)
        video_generator.apply_filter(
            video_file=video_path,
            color=color,
            transparency=transparency,
            output_file=output_path,
        )


def get_font_list(magick_binary="./utils/magick"):
    video_generator = VideoGenerator(magick_binary=magick_binary)
    return video_generator.get_font_list()


if __name__ == "__main__":
    try:
        channel_id = 'UCRjReqWC57lY-LMwPQuzI3A'
        category = "motivation and success"
        limit = 5

        # 1. Get the transcript from YouTube
        transcript = get_transcript_from_channel(channel_id,limit)

        # 2. generate the script using the sample transcripts
        sample_transcripts = transcript
        num_of_scripts = 1

        print("Generating script...")
        script = generate_script_from_transcript(category,sample_transcripts,num_of_scripts)
        print(script)
        print("-"*100)
        # 3. convert the script to audio

        print("Generating audio...")
        audio_path = "./output/audio.mp3"
        transcript = generate_audio_from_script(script,audio_path)
        print(transcript)
        print("-"*100)

        # #save transcript to json
        with open('./output/transcript.json', 'w') as outfile:
            json.dump(transcript, outfile)


        # with open('./output/transcript.json') as json_file:
        #     transcript = json.load(json_file)
        #     audio_path = "./output/audio.mp3"

        # 4. create the video
        video_path = "./output/test.mp4"
        output_path = "./output/video.mp4"
        font_size = 35
        font_color = "#FFFFFF"
        stroke_color = "#000000"
        stroke_width = 0
        font = "Liberation-Mono-Bold"
        words_per_line = 3
        position_x = "center"
        position_y = "center"
        add_audio = True
        add_subtitles = True
        height = 720
        width = 720 /16 * 9
        print("Generating video...")

        video_generator = VideoGenerator(magick_binary="./utils/magick")
        subtitles = video_generator.generate_subtitle(
            transcript_json=transcript,
            screen_size=(width, height),
            font_size=font_size,
            font_color=font_color,
            stroke_color=stroke_color,
            stroke_width=stroke_width,
            font=font,
            position_x=position_x,
            position_y=position_y,
            words_per_line=words_per_line,
        )

        # 5. generate the video

    # def generate_video(self, subtitles, video_file, audio_file, output_file, **kwargs):


        video_generator.generate_video(
            audio_file = audio_path,
            video_file = video_path,
            output_file = output_path,
            subtitles = subtitles,
        )


    except Exception as e:
        print_exc()
        print(e)
