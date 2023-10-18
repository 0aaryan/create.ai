from youtubesearchpython import Playlist, Transcript, playlist_from_channel_id
import json

class YouTubeTranscriptExtractor:
    def __init__(self):
        pass

    @staticmethod
    def get_short_videos_from_channel(channel_id):
        try:
            # Create a Playlist object using the provided channel_id
            playlist = Playlist(playlist_from_channel_id(channel_id))

            # Initialize a list to store the short videos
            short_videos = []

            # Retrieve videos from the playlist
            while playlist.hasMoreVideos:
                playlist.getNextVideos()

            # Iterate through the videos in the playlist
            for video in playlist.videos:
                duration = video['duration']
                if duration is None:
                    continue
                try:
                    duration = duration.split(':')
                    # Check if the video duration is less than 1 minute (60 seconds)
                    if int(duration[0]) == 0 and int(duration[1]) < 60:
                        short_videos.append(video['link'])
                except (ValueError, IndexError):
                    # Handle parsing errors or missing duration information
                    print(f"Error parsing duration for video: {video['title']}")

            print(f'Found {len(short_videos)} short videos.')
            return short_videos

        except Exception as e:
            print(f"Error retrieving playlist: {str(e)}")
            return []

    @staticmethod
    def get_transcripts_from_videos(video_links):
        try:
            # Initialize a list to store the transcripts
            transcripts = []

            # Iterate through the video links
            for link in video_links:
                # Create a Transcript object using the provided video link
                print(f'Getting transcript for {link}...')
                transcript = Transcript.get(link)
                if transcript is None:
                    continue
                transcripts.append({
                    'link': link,
                    'transcript': transcript
                })

            print(f'Found transcripts for {len(transcripts)} videos.')
            return transcripts
        except Exception as e:
            print(f"Error retrieving transcripts: {str(e)}")
            return []

    @staticmethod
    def extract_text_from_transcripts(transcripts):
        text_transcripts = []

        try:
            for link in transcripts:
                # Initialize a list to store the text
                text = []
                transcript = link['transcript']

                for segment in transcript['segments']:
                    # Append the text to the list
                    text.append(segment['text'])

                # Join the text into a single string
                text = ' '.join(text)
                text_transcripts.append({
                    'link': link['link'],
                    'text': text
                })

            return text_transcripts

        except Exception as e:
            print(f"Error extracting text from transcripts: {str(e)}")
            return []

    @staticmethod
    def save_to_json(data, filename):
        try:
            with open(filename, 'w') as outfile:
                json.dump(data, outfile)
            print(f'Saved data to {filename}')
        except Exception as e:
            print(f"Error saving data to {filename}: {str(e)}")


# Example usage:
# if __name__ == "__main__":
#     channel_id = "UCgkKA7xEOoBQNpC5TJxPLiw"
#     extractor = YouTubeTranscriptExtractor()

#     short_videos = extractor.get_short_videos_from_channel(channel_id)
#     short_videos = short_videos[:10]
#     transcripts = extractor.get_transcripts(short_videos)

#     # Save transcripts to JSON
#     extractor.save_to_json(transcripts, 'transcripts.json')

#     # Extract text from transcripts
#     text_transcripts = extractor.extract_text_from_transcripts(transcripts)

#     # Save text transcripts to JSON
#     extractor.save_to_json(text_transcripts, 'text_transcripts.json')
