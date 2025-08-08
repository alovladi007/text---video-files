import json
import os
from typing import Dict, List
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import cv2
from moviepy.editor import VideoFileClip, AudioFileClip, CompositeVideoClip, ImageClip, concatenate_videoclips
from gtts import gTTS
import requests
from io import BytesIO
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from tqdm import tqdm

class VideoGenerator:
    def __init__(self, script_path: str, output_path: str = "gan_overview_video.mp4"):
        self.script_path = script_path
        self.output_path = output_path
        self.temp_dir = "temp_video_assets"
        self.width = 1920
        self.height = 1080
        self.fps = 30
        
        # Create temp directory
        os.makedirs(self.temp_dir, exist_ok=True)
        
        # Load script
        with open(script_path, 'r') as f:
            self.script_data = json.load(f)
            self.scenes = self.script_data['scenes']
    
    def create_ai_character(self, action: str = "explaining") -> np.ndarray:
        """Create a simple AI character avatar"""
        # Create a blank image
        img = Image.new('RGBA', (400, 400), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Draw character based on action
        if action == "greeting":
            # Waving character
            # Head
            draw.ellipse([150, 50, 250, 150], fill=(100, 150, 255), outline=(50, 100, 200), width=3)
            # Eyes
            draw.ellipse([170, 80, 190, 100], fill=(255, 255, 255))
            draw.ellipse([210, 80, 230, 100], fill=(255, 255, 255))
            draw.ellipse([175, 85, 185, 95], fill=(0, 0, 0))
            draw.ellipse([215, 85, 225, 95], fill=(0, 0, 0))
            # Smile
            draw.arc([170, 100, 230, 130], start=0, end=180, fill=(50, 100, 200), width=3)
            # Body
            draw.rectangle([170, 150, 230, 250], fill=(100, 150, 255), outline=(50, 100, 200), width=3)
            # Waving arm
            draw.line([230, 170, 280, 140], fill=(100, 150, 255), width=20)
            draw.ellipse([270, 130, 290, 150], fill=(255, 200, 150))
            # Other arm
            draw.line([170, 170, 120, 200], fill=(100, 150, 255), width=20)
            
        elif action == "explaining":
            # Presenting character
            # Head
            draw.ellipse([150, 50, 250, 150], fill=(100, 150, 255), outline=(50, 100, 200), width=3)
            # Eyes
            draw.ellipse([170, 80, 190, 100], fill=(255, 255, 255))
            draw.ellipse([210, 80, 230, 100], fill=(255, 255, 255))
            draw.ellipse([175, 85, 185, 95], fill=(0, 0, 0))
            draw.ellipse([215, 85, 225, 95], fill=(0, 0, 0))
            # Talking mouth
            draw.ellipse([180, 110, 220, 125], fill=(50, 100, 200))
            # Body
            draw.rectangle([170, 150, 230, 250], fill=(100, 150, 255), outline=(50, 100, 200), width=3)
            # Pointing arm
            draw.line([230, 170, 280, 170], fill=(100, 150, 255), width=20)
            draw.polygon([(280, 160), (300, 170), (280, 180)], fill=(255, 200, 150))
            # Other arm
            draw.line([170, 170, 120, 200], fill=(100, 150, 255), width=20)
            
        else:  # concluding
            # Confident stance
            # Head
            draw.ellipse([150, 50, 250, 150], fill=(100, 150, 255), outline=(50, 100, 200), width=3)
            # Eyes
            draw.ellipse([170, 80, 190, 100], fill=(255, 255, 255))
            draw.ellipse([210, 80, 230, 100], fill=(255, 255, 255))
            draw.ellipse([175, 85, 185, 95], fill=(0, 0, 0))
            draw.ellipse([215, 85, 225, 95], fill=(0, 0, 0))
            # Confident smile
            draw.arc([170, 100, 230, 130], start=0, end=180, fill=(50, 100, 200), width=3)
            # Body
            draw.rectangle([170, 150, 230, 250], fill=(100, 150, 255), outline=(50, 100, 200), width=3)
            # Arms crossed
            draw.line([170, 170, 230, 200], fill=(100, 150, 255), width=20)
            draw.line([230, 170, 170, 200], fill=(100, 150, 255), width=20)
        
        return np.array(img)
    
    def generate_scene_image(self, scene: Dict) -> str:
        """Generate or create an image for a scene"""
        image_path = os.path.join(self.temp_dir, f"scene_{scene['scene_id']}.png")
        
        # Create a scientific visualization based on the scene content
        fig, ax = plt.subplots(figsize=(16, 9), dpi=120)
        fig.patch.set_facecolor('#0a0a0a')
        ax.set_facecolor('#0a0a0a')
        
        title_text = scene['title']
        
        if "introduction" in title_text.lower():
            # Create a GaN crystal structure visualization
            self._create_crystal_structure(ax)
            
        elif "application" in title_text.lower():
            # Create applications diagram
            self._create_applications_diagram(ax)
            
        elif "structure" in title_text.lower() or "architecture" in title_text.lower():
            # Create HEMT structure diagram
            self._create_hemt_structure(ax)
            
        elif "performance" in title_text.lower():
            # Create performance comparison chart
            self._create_performance_chart(ax)
            
        else:
            # Default: create a tech-themed background
            self._create_tech_background(ax)
        
        # Add title
        ax.text(0.5, 0.95, title_text, transform=ax.transAxes, 
                fontsize=32, color='white', ha='center', va='top',
                fontweight='bold', bbox=dict(boxstyle="round,pad=0.5", 
                facecolor='#1a1a1a', edgecolor='#4a90e2', linewidth=2))
        
        plt.tight_layout()
        plt.savefig(image_path, facecolor='#0a0a0a', edgecolor='none')
        plt.close()
        
        return image_path
    
    def _create_crystal_structure(self, ax):
        """Create a GaN crystal structure visualization"""
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 10)
        ax.axis('off')
        
        # Draw hexagonal lattice
        positions = [(2, 5), (3, 6), (4, 5), (5, 6), (6, 5), (3, 4), (5, 4)]
        for i, (x, y) in enumerate(positions):
            color = '#4a90e2' if i % 2 == 0 else '#e24a90'
            circle = plt.Circle((x, y), 0.4, color=color, alpha=0.8)
            ax.add_patch(circle)
            
            # Add connections
            for j, (x2, y2) in enumerate(positions[i+1:], i+1):
                dist = np.sqrt((x2-x)**2 + (y2-y)**2)
                if dist < 2:
                    ax.plot([x, x2], [y, y2], 'w-', alpha=0.5, linewidth=2)
        
        # Add labels
        ax.text(2, 5.5, 'Ga', color='white', ha='center', fontsize=14, fontweight='bold')
        ax.text(3, 6.5, 'N', color='white', ha='center', fontsize=14, fontweight='bold')
        
        # Add description
        ax.text(5, 2, 'GaN Crystal Structure\nWide Bandgap Semiconductor', 
                ha='center', color='white', fontsize=18, alpha=0.8)
    
    def _create_applications_diagram(self, ax):
        """Create applications visualization"""
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 10)
        ax.axis('off')
        
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
    
    def _create_hemt_structure(self, ax):
        """Create HEMT layer structure"""
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 10)
        ax.axis('off')
        
        # Layer structure
        layers = [
            (2, "Substrate", '#333333'),
            (3, "Buffer Layer", '#555555'),
            (4, "GaN Channel", '#4a90e2'),
            (5, "AlGaN Barrier", '#e24a90'),
            (6, "Gate", '#ffd700'),
            (7, "Source/Drain", '#90e24a')
        ]
        
        for y, label, color in layers:
            rect = patches.Rectangle((2, y-0.4), 6, 0.8, 
                                   facecolor=color, alpha=0.8,
                                   edgecolor='white', linewidth=1)
            ax.add_patch(rect)
            ax.text(1.5, y, label, ha='right', va='center',
                   color='white', fontsize=12)
        
        # Add 2DEG indication
        ax.plot([2, 8], [4.5, 4.5], 'y--', linewidth=2, alpha=0.8)
        ax.text(5, 4.8, '2DEG', ha='center', color='yellow', fontsize=10)
    
    def _create_performance_chart(self, ax):
        """Create performance comparison chart"""
        materials = ['Si', 'GaAs', 'SiC', 'GaN']
        metrics = {
            'Breakdown Field': [0.3, 0.4, 3.0, 3.3],
            'Electron Mobility': [1.4, 8.5, 0.9, 2.0],
            'Thermal Conductivity': [1.5, 0.5, 4.9, 2.3]
        }
        
        x = np.arange(len(materials))
        width = 0.25
        
        colors = ['#4a90e2', '#e24a90', '#90e24a']
        
        for i, (metric, values) in enumerate(metrics.items()):
            normalized = [v/max(values) for v in values]
            ax.bar(x + i*width, normalized, width, label=metric, 
                  color=colors[i], alpha=0.8)
        
        ax.set_xlabel('Material', fontsize=14, color='white')
        ax.set_ylabel('Normalized Performance', fontsize=14, color='white')
        ax.set_xticks(x + width)
        ax.set_xticklabels(materials, color='white')
        ax.tick_params(colors='white')
        ax.legend(loc='upper left', facecolor='#1a1a1a', edgecolor='white')
        ax.grid(True, alpha=0.3)
        
        # Highlight GaN
        ax.axvspan(2.75, 3.75, alpha=0.2, color='yellow')
    
    def _create_tech_background(self, ax):
        """Create a generic tech background"""
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 10)
        ax.axis('off')
        
        # Circuit pattern
        np.random.seed(42)
        for _ in range(20):
            x = np.random.uniform(0, 10)
            y = np.random.uniform(0, 10)
            ax.plot([x, x + np.random.uniform(-1, 1)], 
                   [y, y + np.random.uniform(-1, 1)], 
                   'b-', alpha=0.3, linewidth=1)
            
        # Add some nodes
        for _ in range(10):
            x = np.random.uniform(1, 9)
            y = np.random.uniform(1, 9)
            circle = plt.Circle((x, y), 0.1, color='#4a90e2', alpha=0.6)
            ax.add_patch(circle)
    
    def generate_audio(self, scene: Dict) -> str:
        """Generate audio narration for a scene"""
        audio_path = os.path.join(self.temp_dir, f"audio_{scene['scene_id']}.mp3")
        
        # Generate speech using gTTS
        tts = gTTS(text=scene['narration'], lang='en', slow=False)
        tts.save(audio_path)
        
        return audio_path
    
    def create_scene_video(self, scene: Dict) -> str:
        """Create a video clip for a single scene"""
        print(f"Creating scene {scene['scene_id']}: {scene['title']}")
        
        # Generate assets
        image_path = self.generate_scene_image(scene)
        audio_path = self.generate_audio(scene)
        character_img = self.create_ai_character(scene['character_action'])
        
        # Create character image
        char_path = os.path.join(self.temp_dir, f"char_{scene['scene_id']}.png")
        Image.fromarray(character_img).save(char_path)
        
        # Load audio to get actual duration
        audio_clip = AudioFileClip(audio_path)
        duration = max(audio_clip.duration, scene['duration'])
        
        # Create video clips
        bg_clip = ImageClip(image_path).set_duration(duration)
        char_clip = (ImageClip(char_path)
                    .set_duration(duration)
                    .resize(0.3)
                    .set_position(('right', 'bottom'))
                    .set_margin(50))
        
        # Composite video
        video = CompositeVideoClip([bg_clip, char_clip])
        video = video.set_audio(audio_clip)
        
        # Save scene video
        scene_path = os.path.join(self.temp_dir, f"scene_{scene['scene_id']}.mp4")
        video.write_videofile(scene_path, fps=self.fps, codec='libx264', audio_codec='aac')
        
        return scene_path
    
    def generate_video(self):
        """Generate the complete video"""
        print("Starting video generation...")
        
        # Create all scene videos
        scene_videos = []
        for scene in tqdm(self.scenes, desc="Creating scenes"):
            scene_path = self.create_scene_video(scene)
            scene_videos.append(VideoFileClip(scene_path))
        
        # Concatenate all scenes
        print("Concatenating scenes...")
        final_video = concatenate_videoclips(scene_videos)
        
        # Write final video
        print(f"Writing final video to {self.output_path}...")
        final_video.write_videofile(self.output_path, fps=self.fps, 
                                  codec='libx264', audio_codec='aac')
        
        print(f"Video generation complete! Output: {self.output_path}")
        
        # Cleanup
        for video in scene_videos:
            video.close()
        
        return self.output_path
    
    def cleanup(self):
        """Remove temporary files"""
        import shutil
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
            print("Cleaned up temporary files")

if __name__ == "__main__":
    # Generate video from script
    generator = VideoGenerator("video_script.json")
    output_path = generator.generate_video()
    print(f"Video saved to: {output_path}")