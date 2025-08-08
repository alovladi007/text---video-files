#!/usr/bin/env python3
"""
GaN Overview Video Creator
Creates an AI character video with images explaining the content of the GaN Overview PDF
"""

import os
import sys
from pdf_extractor import PDFExtractor
from script_generator import ScriptGenerator
from video_generator import VideoGenerator

def main():
    print("=== GaN Overview Video Creator ===")
    print("This script will create an AI character video explaining GaN technology")
    print()
    
    # Check if PDF exists
    pdf_path = "/workspace/GaN Overview.pdf"
    if not os.path.exists(pdf_path):
        print(f"Error: PDF file not found at {pdf_path}")
        sys.exit(1)
    
    print("Step 1: Extracting content from PDF...")
    extractor = PDFExtractor(pdf_path)
    text = extractor.extract_text()
    print(f"✓ Extracted {len(text)} characters from PDF")
    
    print("\nStep 2: Generating video script...")
    script_gen = ScriptGenerator(pdf_path)
    script = script_gen.generate_script()
    script_gen.save_script("video_script.json")
    print(f"✓ Generated script with {len(script)} scenes")
    
    print("\nStep 3: Installing required dependencies...")
    print("Please run: pip3 install --break-system-packages -r requirements.txt")
    print("Note: Some packages like matplotlib, pillow, and gtts are needed for video generation")
    
    # Check if user wants to continue
    response = input("\nHave you installed the dependencies? (y/n): ")
    if response.lower() != 'y':
        print("Please install dependencies and run again.")
        sys.exit(0)
    
    print("\nStep 4: Generating video...")
    print("This may take several minutes depending on the number of scenes.")
    
    try:
        video_gen = VideoGenerator("video_script.json")
        output_path = video_gen.generate_video()
        
        print(f"\n✓ Video successfully created: {output_path}")
        print(f"Video duration: {video_gen.script_data['total_duration']} seconds")
        print(f"Number of scenes: {video_gen.script_data['scene_count']}")
        
        # Cleanup option
        cleanup = input("\nDo you want to remove temporary files? (y/n): ")
        if cleanup.lower() == 'y':
            video_gen.cleanup()
            
    except Exception as e:
        print(f"\nError during video generation: {e}")
        print("Make sure all dependencies are installed correctly.")
        sys.exit(1)
    
    print("\n=== Video Creation Complete! ===")
    print(f"Your video is ready at: {os.path.abspath(output_path)}")

if __name__ == "__main__":
    main()