from moviepy.editor import *
from moviepy.config import change_settings
import json
from traceback import print_exc

class VideoGenerator:
    def __init__(self, magick_binary="./magick"):
        """
        Initialize the VideoTranscriber.

        Args:
            magick_binary (str, optional): Path to the IMAGEMAGICK_BINARY if needed. Default is "./magick".
        """
        change_settings({"IMAGEMAGICK_BINARY": magick_binary})

    def generate_subtitle(
            self ,
            transcript_json,
            screen_size,
            font_size = 35 ,
            font_color = "#FFFFFF",
            stroke_color = "#000000",
            stroke_width = 1,
            font = "Liberation-Mono-Bold",
            position_x = "center",
            position_y = "center",
            words_per_line = 4):

        """
        Create subtitle clips from a transcript json format.

        Args:
            transcript_json (list): A list of dictionaries containing transcribed words with timestamps.
            font_size (int): Font size for subtitles.
            font_color (str): Font color in hexadecimal format (e.g., "#000000").
            stroke_color (str): Stroke color in hexadecimal format (e.g., "#FFFFFF").
            stroke_width (int): Stroke width for subtitles.
            font (str): Font style for subtitles.
            position_x (str): Horizontal position of subtitles ("center", "left", "right").
            position_y (str): Vertical position of subtitles ("center", "top", "bottom").
            screen_size (tuple): Screen size for subtitles (width, height).
            words_per_line (int): Maximum number of words per line in subtitles.

        Returns:
            CompositeVideoClip: A composite video clip containing the subtitle clips.
        """




        try:
            # Initialize variables for subtitle generation
            text_clips = []
            sentences = []

            # Initialize variables for the current sentence
            current_sentence = []
            start_time = None
            end_time = None

            # Iterate through the transcribed words and group them into sentences
            for word_info in transcript_json:
                word = word_info['word']
                if start_time is None:
                    start_time = word_info['start_time']

                current_sentence.append(word)
                end_time = word_info['end_time']

                # Check if the current sentence exceeds the specified word limit
                if len(current_sentence) >= words_per_line:
                    sentences.append((current_sentence, start_time, end_time))
                    current_sentence = []
                    start_time = None

            # Reduce screen size x for margin
            screen_size = (screen_size[0] - 100, font_size * words_per_line * 1.1)

            # Generate subtitle clips for each sentence
            for sentence, start_time, end_time in sentences:
                sentence_text = ' '.join(sentence)
                text_clip = TextClip(sentence_text, fontsize=font_size, color=font_color, font=font,size=screen_size, stroke_color=stroke_color, stroke_width=stroke_width, method="caption", align="center")
                text_clip = text_clip.set_start(float(start_time)).set_end(float(end_time))
                text_clips.append(text_clip)

            # Concatenate subtitle clips and set their position
            return concatenate_videoclips(text_clips).set_position((position_x, position_y))

        except Exception as e:
            print("Error in creating subtitle clips: " + str(e))
            print_exc()
            return None





    def generate_video(self, subtitles, video_file, audio_file, output_file,fps):
        """
        generate a transcript with optional audio and subtitles to a video.

        Args:
            subtitles (CompositeVideoClip): A composite video clip containing the subtitle clips.
            video_file (str): Path to the background video file.
            audio_file (str): Path to the input audio file (None if no audio).
            output_file (str): Path to the output video file.
        """
        try:
            # Load the background video
            bg_video = VideoFileClip(video_file)
            print(bg_video.size)

            # Resize the video to 720p and aspect ratio 9:16
            bg_video = bg_video.resize(height=720)
            print(bg_video.size)
            
            #center
            centerX = bg_video.size[0]/2
            centerY = bg_video.size[1]/2

            width = bg_video.size[1] / 16 * 9
            height = bg_video.size[1]
            
            width = min(width, bg_video.size[0])

            x1 = centerX - width/2
            y1 = centerY - height/2

            x2 = centerX + width/2
            y2 = centerY + height/2
            # bg_video.write_videofile("temp_video.mp4", fps=24, threads=8,codec = "h264")

            bg_video = bg_video.crop(x1=x1, y1=y1, x2=x2, y2=y2)
            print(bg_video.size)
            #save bg video as temp_video.mp4
            # Ensure the background video duration matches or exceeds the subtitles
            if bg_video.duration < subtitles.duration:
                bg_video = bg_video.fx(vfx.loop, duration=subtitles.duration)
            else:
                bg_video = bg_video.set_duration(subtitles.duration)

            # Load and set the audio (if specified)
            if audio_file:
                audio = AudioFileClip(audio_file)
                audio = audio.set_duration(bg_video.duration)
                bg_video = bg_video.set_audio(audio)

            # Composite the video with subtitles
            video = CompositeVideoClip([bg_video, subtitles])
            ffmpeg_options = "-c:v libx264 -pix_fmt yuv420p"
            # Write the final video
            video.write_videofile(output_file, fps=fps, threads=8)
            print("Video creation successful")

        except Exception as e:
            print("Error in converting transcript to video: " + str(e))
            print_exc()
