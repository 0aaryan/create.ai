import os
from google.cloud import speech
from google.cloud import texttospeech as tts
from google.oauth2 import service_account

class AudioGenerator:
    def __init__(self, credentials_json):
        """
        Initialize the SpeechProcessor with Google Cloud credentials.

        Args:
            gcp_credentials_path (str): Path to the Google Cloud credentials JSON file.
        """
        # os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = gcp_credentials_path  
        self.credentials = service_account.Credentials.from_service_account_info(credentials_json)

    def  generate_transcript(self, speech_file_path):
        """
        Transcribe an audio file using Google Cloud Speech-to-Text API.

        Args:
            speech_file_path (str): Path to the audio file.

        Returns:
            list: A list of dictionaries containing transcribed words with timestamps.
        """
        try:
            # Create a Google Cloud Speech-to-Text client
            client = speech.SpeechClient(credentials=self.credentials)

            # Read the audio file
            with open(speech_file_path, "rb") as audio_file:
                content = audio_file.read()

            audio = speech.RecognitionAudio(content=content)

            # Configure recognition settings
            config = speech.RecognitionConfig(
                encoding=speech.RecognitionConfig.AudioEncoding.ENCODING_UNSPECIFIED,
                language_code="en-US",
                # sample_rate_hertz=16000,
                enable_word_time_offsets=True,
                model="video",
            )

            # Perform audio transcription
            response = client.recognize(config=config, audio=audio)

            words = []

            # Extract transcribed words and their timestamps
            for result in response.results:
                for word_info in result.alternatives[0].words:
                    word = word_info.word
                    start_time = word_info.start_time
                    end_time = word_info.end_time
                    words.append(
                        {
                            "word": word,
                            "start_time": str(start_time.total_seconds()),
                            "end_time": str(end_time.total_seconds()),
                        }
                    )

            return words

        except Exception as e:
            print("Error: " + str(e))
            return None

    def generate_audio(self, text, output_file_path):
        """
        Convert text to speech using Google Cloud Text-to-Speech API.

        Args:
            text (str): The text to be converted to speech.
            output_file_path (str): Path to save the generated audio file.
        """
        try:

            text_input = tts.SynthesisInput(text=text)
            voice_params = tts.VoiceSelectionParams(
                language_code="en-US", name="en-US-News-M"
            )
            audio_config = tts.AudioConfig(
                audio_encoding=tts.AudioEncoding.LINEAR16, speaking_rate=0.9, pitch=-10.0
            )

            client = tts.TextToSpeechClient(credentials=self.credentials)
            response = client.synthesize_speech(
                input=text_input,
                voice=voice_params,
                audio_config=audio_config,
            )

            # Save the generated audio content to the specified output file
            with open(output_file_path, 'wb') as out:
                out.write(response.audio_content)
                print('Audio content written to file ' + output_file_path)

        except Exception as e:
            print("Error: " + str(e))


# # Example Usage:
# if __name__ == "__main__":
#     gcp_credentials_path = "./.credentials/gcp.json"
#     processor = SpeechProcessor(gcp_credentials_path)

#     # Transcribe Audio
#     transcribed_words = processor.transcribe_audio("audio.wav")
#     print(transcribed_words)

#     # Text to Speech
#     processor.text_to_speech("This is a test.", "output.mp3")


