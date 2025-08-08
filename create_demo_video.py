#!/usr/bin/env python3
"""
Simplified Demo Video Creator
Creates a demo video showing GaN technology overview
"""

import json
import os
import subprocess
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def create_demo_frames():
    """Create demo frames for the video"""
    print("Creating demo frames...")
    
    # Create output directory
    os.makedirs("demo_frames", exist_ok=True)
    
    # Load the script
    with open("video_script.json", "r") as f:
        script_data = json.load(f)
    
    scenes = script_data["scenes"][:3]  # First 3 scenes
    
    for i, scene in enumerate(scenes):
        print(f"Creating frame for scene {i+1}: {scene['title']}")
        
        # Create visualization
        fig, ax = plt.subplots(figsize=(16, 9), dpi=120)
        fig.patch.set_facecolor('#0a0a0a')
        ax.set_facecolor('#0a0a0a')
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 10)
        ax.axis('off')
        
        if i == 0:  # Introduction - Crystal structure
            # Draw hexagonal lattice
            positions = [(2, 5), (3, 6), (4, 5), (5, 6), (6, 5), (3, 4), (5, 4)]
            for j, (x, y) in enumerate(positions):
                color = '#4a90e2' if j % 2 == 0 else '#e24a90'
                circle = plt.Circle((x, y), 0.4, color=color, alpha=0.8)
                ax.add_patch(circle)
                
                # Add connections
                for k, (x2, y2) in enumerate(positions[j+1:], j+1):
                    dist = np.sqrt((x2-x)**2 + (y2-y)**2)
                    if dist < 2:
                        ax.plot([x, x2], [y, y2], 'w-', alpha=0.5, linewidth=2)
            
            # Add labels
            ax.text(2, 5.5, 'Ga', color='white', ha='center', fontsize=14, fontweight='bold')
            ax.text(3, 6.5, 'N', color='white', ha='center', fontsize=14, fontweight='bold')
            
            # Add description
            ax.text(5, 2, 'GaN Crystal Structure\nWide Bandgap Semiconductor', 
                    ha='center', color='white', fontsize=18, alpha=0.8)
                    
        elif i == 1:  # Applications
            # Application boxes
            apps = [
                (2, 7, "5G\nCommunications", '#4a90e2'),
                (5, 7, "Electric\nVehicles", '#e24a90'),
                (8, 7, "Power\nElectronics", '#90e24a'),
                (2, 4, "RF\nAmplifiers", '#e2904a'),
                (5, 4, "Solar\nInverters", '#904ae2'),
                (8, 4, "Radar\nSystems", '#4ae290')
            ]
            
            for x, y, label, color in apps:
                rect = patches.FancyBboxPatch((x-0.8, y-0.5), 1.6, 1, 
                                            boxstyle="round,pad=0.1",
                                            facecolor=color, alpha=0.7,
                                            edgecolor='white', linewidth=2)
                ax.add_patch(rect)
                ax.text(x, y, label, ha='center', va='center', 
                       color='white', fontsize=12, fontweight='bold')
            
            # Central GaN node
            center = patches.Circle((5, 5.5), 1, facecolor='#1a1a1a', 
                                   edgecolor='#4a90e2', linewidth=3)
            ax.add_patch(center)
            ax.text(5, 5.5, 'GaN\nTechnology', ha='center', va='center',
                   color='white', fontsize=14, fontweight='bold')
                   
        else:  # Performance
            # Performance comparison chart
            materials = ['Si', 'GaAs', 'SiC', 'GaN']
            metrics = {
                'Breakdown Field': [0.3, 0.4, 3.0, 3.3],
                'Electron Mobility': [1.4, 8.5, 0.9, 2.0],
                'Thermal Conductivity': [1.5, 0.5, 4.9, 2.3]
            }
            
            x = np.arange(len(materials))
            width = 0.25
            
            colors = ['#4a90e2', '#e24a90', '#90e24a']
            
            for j, (metric, values) in enumerate(metrics.items()):
                normalized = [v/max(values) for v in values]
                ax.bar(x + j*width, normalized, width, label=metric, 
                      color=colors[j], alpha=0.8)
            
            ax.set_xlabel('Material', fontsize=14, color='white')
            ax.set_ylabel('Normalized Performance', fontsize=14, color='white')
            ax.set_xticks(x + width)
            ax.set_xticklabels(materials, color='white')
            ax.tick_params(colors='white')
            ax.legend(loc='upper left', facecolor='#1a1a1a', edgecolor='white')
            ax.grid(True, alpha=0.3)
            
            # Highlight GaN
            ax.axvspan(2.75, 3.75, alpha=0.2, color='yellow')
        
        # Add title
        ax.text(0.5, 0.95, scene['title'], transform=ax.transAxes, 
                fontsize=32, color='white', ha='center', va='top',
                fontweight='bold', bbox=dict(boxstyle="round,pad=0.5", 
                facecolor='#1a1a1a', edgecolor='#4a90e2', linewidth=2))
        
        # Add narration preview
        narration_preview = scene['narration'][:100] + "..."
        ax.text(0.5, 0.05, narration_preview, transform=ax.transAxes, 
                fontsize=12, color='white', ha='center', va='bottom',
                alpha=0.7, style='italic')
        
        plt.tight_layout()
        plt.savefig(f"demo_frames/frame_{i:03d}.png", facecolor='#0a0a0a', edgecolor='none')
        plt.close()
    
    print(f"Created {len(scenes)} frames in demo_frames/")
    return len(scenes)

def create_video_from_frames(num_frames):
    """Create a video from the frames using ffmpeg"""
    print("\nCreating video from frames...")
    
    # Create a simple video using ffmpeg
    # Each frame will be shown for 5 seconds
    cmd = [
        "ffmpeg",
        "-framerate", "1/5",  # 1 frame per 5 seconds
        "-i", "demo_frames/frame_%03d.png",
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-y",  # Overwrite output
        "gan_demo_video.mp4"
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            print("✓ Video created successfully: gan_demo_video.mp4")
            return True
        else:
            print(f"Error creating video: {result.stderr}")
            return False
    except FileNotFoundError:
        print("Error: ffmpeg not found. Please install ffmpeg.")
        return False

def create_animated_gif():
    """Create an animated GIF as an alternative"""
    print("\nCreating animated GIF...")
    
    images = []
    for i in range(3):
        img = Image.open(f"demo_frames/frame_{i:03d}.png")
        # Resize for smaller file size
        img = img.resize((960, 540), Image.Resampling.LANCZOS)
        images.append(img)
    
    # Save as animated GIF
    images[0].save(
        "gan_demo.gif",
        save_all=True,
        append_images=images[1:],
        duration=5000,  # 5 seconds per frame
        loop=0
    )
    print("✓ Animated GIF created: gan_demo.gif")

def main():
    print("=== GaN Demo Video Creator ===\n")
    
    # Create frames
    num_frames = create_demo_frames()
    
    # Try to create video
    video_created = create_video_from_frames(num_frames)
    
    # Also create GIF as backup
    create_animated_gif()
    
    # List created files
    print("\n=== Created Files ===")
    files = ["gan_demo_video.mp4", "gan_demo.gif"]
    for file in files:
        if os.path.exists(file):
            size = os.path.getsize(file) / (1024 * 1024)  # MB
            print(f"✓ {file} ({size:.2f} MB)")
    
    print("\nYou can view these files by downloading them from the workspace.")

if __name__ == "__main__":
    main()