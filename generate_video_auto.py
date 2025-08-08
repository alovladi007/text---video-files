#!/usr/bin/env python3
"""
Automated GaN Video Generator
Generates the video without user interaction
"""

import os
import subprocess
import sys

def install_dependencies():
    """Install required dependencies"""
    print("Installing dependencies...")
    deps = [
        "pillow",
        "matplotlib", 
        "gtts",
        "moviepy",
        "opencv-python",
        "numpy",
        "tqdm"
    ]
    
    for dep in deps:
        print(f"Installing {dep}...")
        subprocess.run([sys.executable, "-m", "pip", "install", "--break-system-packages", dep], 
                      capture_output=True)
    
    print("✓ Dependencies installed")

def main():
    print("=== Automated GaN Video Generation ===")
    
    # Install dependencies first
    install_dependencies()
    
    # Import after installation
    from pdf_extractor import PDFExtractor
    from script_generator import ScriptGenerator
    from video_generator import VideoGenerator
    
    pdf_path = "/workspace/GaN Overview.pdf"
    
    # Step 1: Extract PDF content
    print("\n1. Extracting PDF content...")
    extractor = PDFExtractor(pdf_path)
    text = extractor.extract_text()
    print(f"   ✓ Extracted {len(text)} characters")
    
    # Step 2: Generate script
    print("\n2. Generating video script...")
    script_gen = ScriptGenerator(pdf_path)
    script = script_gen.generate_script()
    script_gen.save_script("video_script.json")
    print(f"   ✓ Generated {len(script)} scenes")
    
    # Step 3: Generate video
    print("\n3. Creating video (this may take a few minutes)...")
    try:
        video_gen = VideoGenerator("video_script.json")
        
        # For automated version, let's create a shorter preview
        # Limit to first 3 scenes for faster generation
        video_gen.scenes = video_gen.scenes[:3]
        
        output_path = video_gen.generate_video()
        print(f"\n✓ Video created successfully!")
        print(f"  Output: {os.path.abspath(output_path)}")
        print(f"  Duration: ~{sum(s['duration'] for s in video_gen.scenes)} seconds")
        
        # Auto cleanup
        video_gen.cleanup()
        
    except Exception as e:
        print(f"\nError: {e}")
        print("Note: Video generation requires ffmpeg. Install with: sudo apt-get install ffmpeg")
        return 1
    
    print("\n=== Generation Complete! ===")
    return 0

if __name__ == "__main__":
    sys.exit(main())