<!---
{
  "title": "Create.ai - AI-Powered Video Creation Platform",
  "badges": [],
  "content": "Create.ai is an AI-powered video creation platform that automates the process of generating scripts, converting them to audio, and creating videos with customizable subtitles. Whether you're a content creator, marketer, or simply looking to create videos easily, Create.ai can simplify your video production process.",
  "featured": {
    "link": "https://github.com/0aaryan/create-ai",
    "name": "Repository"
  },
  "image": "https://github.com/0aaryan/create.ai/assets/73797587/09656210-6baa-48da-bb77-9c311670ebaa",
  "links": [
    {
      "icon": "fab fa-github",
      "url": "https://github.com/0aaryan/create.ai"
    },
    {
      "icon": "fa fa-external-link-alt",
      "url": "https://createai.streamlit.app"
    }
  ]
}
--->

# Create.ai - AI-Powered Video Creation Platform

**Create.ai** is an AI-powered video creation platform that automates the process of generating scripts, converting them to audio, and creating videos with customizable subtitles. Whether you're a content creator, marketer, or simply looking to create videos easily, Create.ai can simplify your video production process.

![Create.ai](https://github.com/0aaryan/create.ai/assets/73797587/09656210-6baa-48da-bb77-9c311670ebaa)


## Table of Contents

- [Features](#features)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
  - [Step 1: Sample Scripts](#step-1-sample-scripts)
  - [Step 2: Generate Scripts](#step-2-generate-scripts)
  - [Step 3: Generate Audio](#step-3-generate-audio)
  - [Step 4: Background Video](#step-4-background-video)
  - [Step 5: Subtitle Options](#step-5-subtitle-options)
- [Contributing](#contributing)
- [Issues and Suggestions](#issues-and-suggestions)
- [License](#license)

## Features

- **Sample Scripts**: Easily input sample scripts or extract them from a YouTube channel's videos.

- **Generate Scripts**: Utilize the power of AI to generate scripts based on a given prompt and category.

- **Generate Audio**: Convert your generated scripts to audio, allowing you to use AI-generated content in your videos.

- **Background Video**: Upload a background video for your project to use as a visual backdrop.

- **Subtitle Options**: Customize subtitle settings, such as font, size, color, position, and more, to create engaging subtitles for your videos.

- **Video Generation**: Create videos by combining audio, scripts, and background video while applying customizable subtitles.

## Getting Started

### Prerequisites

Before you start, make sure you have the following:

- Python 3.7 or higher installed
- [Magick](https://imagemagick.org/index.php) binary installed (for video generation)
- [FFmpeg](https://www.ffmpeg.org/) installed (for audio generation)

### Installation

1. Clone the repository to your local machine:

   ```bash
   git clone https://github.com/your-username/create-ai.git
   ```

2. Navigate to the project directory:

   ```bash
   cd create-ai
   ```

3. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv venv
   ```

4. Activate the virtual environment:

   - On Windows:

     ```bash
     venv\Scripts\activate
     ```

   - On macOS and Linux:

     ```bash
     source venv/bin/activate
     ```

5. Install the project dependencies:

   ```bash
   pip install -r requirements.txt
   ```

6. Create a `.env` file in the project root and set your OpenAI API key:

   ```
   OPENAI_API_KEY=your-api-key
   ```

## Usage

The Create.ai platform consists of several steps for generating videos. Here's how to use each step:

### Step 1: Sample Scripts

- Input sample scripts manually in the text area.
- Alternatively, extract sample scripts from a YouTube channel by providing the channel ID and specifying the number of short videos to retrieve.

### Step 2: Generate Scripts

- Provide a prompt and a category.
- Specify the number of scripts you want to generate.
- Click "Generate Scripts" to use AI to create scripts based on your input.

### Step 3: Generate Audio

- View the generated script or manually input a script in the text area.
- Click "Generate Audio" to convert the script to audio.

### Step 4: Background Video

- Upload your background video to serve as the visual backdrop for your project.

### Step 5: Subtitle Options

- Customize subtitle settings, including font, size, color, position, and more.
- Choose whether to generate a sample video or a full video.
- Click the respective button to create the video.

## Contributing

We welcome contributions from the community. If you'd like to contribute to Create.ai, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix: `git checkout -b feature/your-feature-name`.
3. Make your changes and commit them.
4. Push your changes to your fork: `git push origin feature/your-feature-name`.
5. Create a pull request on the [Create.ai GitHub repository](https://github.com/your-username/create-ai) and describe your changes.

## Issues and Suggestions

If you encounter any issues or have suggestions for improving Create.ai, please visit the [Issues tab](https://github.com/your-username/create-ai/issues) on GitHub and create a new issue. We appreciate your feedback!

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
