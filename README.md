# GaN Overview Video Generator

This project creates an AI character video with images that explains the content of the "GaN Overview.pdf" file. The video features:
- An animated AI character narrator
- Scientific visualizations and diagrams
- Text-to-speech narration
- Automatic scene generation based on PDF content

## Features

- **PDF Content Extraction**: Automatically extracts and analyzes content from the GaN Overview PDF
- **Intelligent Script Generation**: Creates a video script with appropriate scenes based on the content
- **Visual Generation**: Creates scientific visualizations including:
  - GaN crystal structure diagrams
  - Application overview charts
  - HEMT layer structure visualizations
  - Performance comparison graphs
- **AI Character**: Animated character with different poses (greeting, explaining, concluding)
- **Text-to-Speech**: Converts script to natural-sounding narration using Google TTS

## Quick Start

### Option 1: Automated Generation (Recommended)
```bash
python3 generate_video_auto.py
```
This will automatically install dependencies and generate a preview video with the first 3 scenes.

### Option 2: Interactive Generation
```bash
# First install dependencies
pip3 install --break-system-packages -r requirements.txt

# Then run the main script
python3 create_gan_video.py
```

### Option 3: Step-by-Step
```bash
# 1. Extract PDF content
python3 pdf_extractor.py

# 2. Generate video script
python3 script_generator.py

# 3. Create the video
python3 video_generator.py
```

## Project Structure

```
/workspace/
├── GaN Overview.pdf          # Source PDF file
├── pdf_extractor.py         # Extracts content from PDF
├── script_generator.py      # Generates video script from content
├── video_generator.py       # Creates the actual video
├── create_gan_video.py      # Main orchestration script
├── generate_video_auto.py   # Automated version
├── requirements.txt         # Python dependencies
├── video_script.json        # Generated script (created automatically)
└── gan_overview_video.mp4   # Final output video
```

## Dependencies

- Python 3.8+
- FFmpeg (for video processing)
- Python packages (see requirements.txt):
  - PyPDF2: PDF text extraction
  - Pillow: Image processing
  - matplotlib: Scientific visualizations
  - moviepy: Video editing
  - gTTS: Text-to-speech
  - opencv-python: Video processing
  - numpy: Numerical operations
  - tqdm: Progress bars

## How It Works

1. **PDF Extraction**: The system reads the GaN Overview PDF and extracts all text content
2. **Content Analysis**: Identifies key sections and topics (introduction, applications, performance, etc.)
3. **Script Generation**: Creates a narration script with:
   - Scene titles and durations
   - Narration text (cleaned and simplified for speech)
   - Image prompts for each scene
   - Character actions
4. **Visual Creation**: Generates appropriate visualizations:
   - Crystal structure for introduction
   - Application diagrams for use cases
   - Layer diagrams for technical sections
   - Performance charts for comparisons
5. **Video Assembly**: Combines visuals, AI character, and narration into final video

## Output

The system generates a video (gan_overview_video.mp4) that includes:
- Professional scientific visualizations
- AI character narrator in the bottom-right corner
- Synchronized narration
- Scene transitions
- Typical duration: 30-60 seconds (depending on content)

## Customization

You can customize various aspects:

### Video Settings (in video_generator.py):
```python
self.width = 1920      # Video width
self.height = 1080     # Video height  
self.fps = 30          # Frames per second
```

### Scene Selection (in script_generator.py):
```python
for section in sections[:10]:  # Change number of sections
```

### AI Character Appearance:
Modify the `create_ai_character()` method in video_generator.py

### Visual Themes:
Adjust colors and styles in the `_create_*` methods

## Troubleshooting

1. **FFmpeg not found**: Install with `sudo apt-get install ffmpeg`
2. **Import errors**: Run `pip3 install --break-system-packages -r requirements.txt`
3. **Memory issues**: Reduce video resolution or number of scenes
4. **Audio issues**: Ensure internet connection for gTTS

## Notes

- The automated script creates a preview with 3 scenes for faster generation
- Full video generation may take several minutes depending on content length
- Temporary files are created in `temp_video_assets/` and can be cleaned up
- The system respects the structure and content of the source PDF

## Future Enhancements

- Support for multiple PDF files
- More AI character animations
- Additional visualization types
- Custom voice options
- Real-time preview during generation