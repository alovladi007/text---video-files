from pdf_extractor import PDFExtractor
from typing import List, Dict
import re
import json

class ScriptGenerator:
    def __init__(self, pdf_path: str):
        self.extractor = PDFExtractor(pdf_path)
        self.scenes = []
        
    def generate_script(self) -> List[Dict]:
        """Generate a video script with scenes based on PDF content"""
        # Extract and parse PDF content
        self.extractor.extract_text()
        sections = self.extractor.parse_sections()
        
        # Create introduction scene
        self.scenes.append({
            "scene_id": 1,
            "title": "Introduction to GaN Technology",
            "narration": "Welcome to our comprehensive overview of Gallium Nitride, or GaN technology. Today, we'll explore how GaN High Electron Mobility Transistors, or HEMTs, are revolutionizing high-frequency and high-power electronics.",
            "duration": 8,
            "image_prompt": "A futuristic semiconductor chip with glowing blue circuits, representing GaN technology, modern tech aesthetic",
            "character_action": "greeting"
        })
        
        # Process main content sections
        scene_id = 2
        for section in sections[:10]:  # Limit to top 10 sections
            if len(section["content"]) < 100:  # Skip very short sections
                continue
                
            # Clean and summarize content
            summary = self._summarize_content(section["content"])
            if not summary:
                continue
                
            # Determine image prompt based on content
            image_prompt = self._generate_image_prompt(section["title"], summary)
            
            self.scenes.append({
                "scene_id": scene_id,
                "title": self._clean_title(section["title"]),
                "narration": summary,
                "duration": max(5, len(summary.split()) // 20),  # ~20 words per second
                "image_prompt": image_prompt,
                "character_action": "explaining"
            })
            scene_id += 1
        
        # Add conclusion scene
        self.scenes.append({
            "scene_id": scene_id,
            "title": "Conclusion",
            "narration": "GaN technology represents a significant advancement in semiconductor technology, enabling faster, more efficient, and more powerful electronic devices. From 5G communications to electric vehicles, GaN HEMTs are shaping the future of electronics.",
            "duration": 8,
            "image_prompt": "A montage of modern applications: 5G towers, electric vehicles, renewable energy systems, all powered by GaN technology",
            "character_action": "concluding"
        })
        
        return self.scenes
    
    def _summarize_content(self, content: str) -> str:
        """Create a concise, narration-friendly summary of the content"""
        # Remove references, citations, and technical notation
        content = re.sub(r'\[\d+\]', '', content)
        content = re.sub(r'\([^)]*\d{4}[^)]*\)', '', content)
        content = re.sub(r'et al\.?', 'and colleagues', content)
        
        # Split into sentences
        sentences = re.split(r'[.!?]+', content)
        
        # Filter and clean sentences
        clean_sentences = []
        for sentence in sentences[:5]:  # Take first 5 sentences
            sentence = sentence.strip()
            if len(sentence) > 20 and not any(skip in sentence.lower() for skip in ['figure', 'table', 'equation']):
                clean_sentences.append(sentence)
        
        # Join and ensure proper ending
        summary = '. '.join(clean_sentences)
        if summary and not summary.endswith('.'):
            summary += '.'
            
        return summary[:300]  # Limit length
    
    def _generate_image_prompt(self, title: str, content: str) -> str:
        """Generate an appropriate image prompt based on the section content"""
        title_lower = title.lower()
        content_lower = content.lower()
        
        # Map keywords to image concepts
        if any(word in title_lower for word in ['introduction', 'overview']):
            return "Modern semiconductor wafer with GaN crystals, blue and purple color scheme, high-tech laboratory setting"
        elif 'application' in title_lower:
            return "Collage of modern electronics: smartphones, 5G towers, electric vehicles, solar panels, all highlighting GaN components"
        elif 'structure' in title_lower or 'architecture' in title_lower:
            return "3D visualization of GaN HEMT structure showing layers: substrate, buffer, channel, barrier, with electron flow animation"
        elif 'performance' in title_lower or 'efficiency' in title_lower:
            return "Performance graphs and charts showing GaN advantages, with glowing efficiency metrics, modern data visualization"
        elif 'reliability' in title_lower:
            return "Robust electronic component undergoing stress tests, showing durability and longevity, industrial testing environment"
        elif 'biosensor' in content_lower:
            return "Medical biosensor device with GaN chip, showing biological molecule detection, clean medical tech aesthetic"
        elif 'power' in content_lower:
            return "High-power electronic systems with GaN components, showing energy flow, industrial power electronics"
        else:
            return "Advanced GaN semiconductor chip with intricate circuit patterns, blue LED illumination, futuristic technology"
    
    def _clean_title(self, title: str) -> str:
        """Clean up section titles for video presentation"""
        # Remove numbering
        title = re.sub(r'^\d+\.?\s*', '', title)
        # Capitalize properly
        words = title.split()
        cleaned = []
        for word in words:
            if word.isupper() and len(word) > 3:
                word = word.capitalize()
            cleaned.append(word)
        return ' '.join(cleaned)
    
    def save_script(self, output_path: str = "video_script.json"):
        """Save the generated script to a JSON file"""
        if not self.scenes:
            self.generate_script()
            
        script_data = {
            "title": "GaN Technology: A Comprehensive Overview",
            "total_duration": sum(scene["duration"] for scene in self.scenes),
            "scene_count": len(self.scenes),
            "scenes": self.scenes
        }
        
        with open(output_path, 'w') as f:
            json.dump(script_data, f, indent=2)
            
        print(f"Script saved to {output_path}")
        print(f"Total scenes: {len(self.scenes)}")
        print(f"Total duration: {script_data['total_duration']} seconds")
        
        return script_data

if __name__ == "__main__":
    generator = ScriptGenerator("/workspace/GaN Overview.pdf")
    script = generator.generate_script()
    generator.save_script()
    
    # Preview first few scenes
    print("\nScript Preview:")
    for scene in script[:3]:
        print(f"\nScene {scene['scene_id']}: {scene['title']}")
        print(f"Duration: {scene['duration']}s")
        print(f"Narration: {scene['narration'][:100]}...")
        print(f"Image: {scene['image_prompt'][:80]}...")