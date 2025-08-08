import PyPDF2
import re
from typing import List, Dict
import os

class PDFExtractor:
    def __init__(self, pdf_path: str):
        self.pdf_path = pdf_path
        self.text_content = ""
        self.sections = []
        
    def extract_text(self) -> str:
        """Extract all text from the PDF"""
        try:
            with open(self.pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                num_pages = len(pdf_reader.pages)
                
                print(f"Extracting text from {num_pages} pages...")
                
                for page_num in range(num_pages):
                    page = pdf_reader.pages[page_num]
                    self.text_content += page.extract_text() + "\n"
                    
            return self.text_content
        except Exception as e:
            print(f"Error extracting PDF: {e}")
            return ""
    
    def parse_sections(self) -> List[Dict[str, str]]:
        """Parse the extracted text into logical sections"""
        lines = self.text_content.split('\n')
        current_section = {"title": "Introduction", "content": ""}
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Detect section headers (lines in all caps or with specific patterns)
            if self._is_section_header(line):
                if current_section["content"]:
                    self.sections.append(current_section)
                current_section = {"title": line, "content": ""}
            else:
                current_section["content"] += line + " "
        
        # Add the last section
        if current_section["content"]:
            self.sections.append(current_section)
            
        return self.sections
    
    def _is_section_header(self, line: str) -> bool:
        """Determine if a line is likely a section header"""
        # Check if line is all caps and reasonably short
        if line.isupper() and len(line) < 100:
            return True
        # Check for numbered sections
        if re.match(r'^\d+\.?\s+[A-Z]', line):
            return True
        # Check for common header keywords
        header_keywords = ['Introduction', 'Overview', 'Conclusion', 'Summary', 
                          'Properties', 'Applications', 'Technology', 'Performance']
        for keyword in header_keywords:
            if keyword.lower() in line.lower() and len(line) < 100:
                return True
        return False
    
    def get_summary(self, max_sections: int = 5) -> List[Dict[str, str]]:
        """Get a summary of the most important sections"""
        if not self.sections:
            self.extract_text()
            self.parse_sections()
            
        # Prioritize sections with substantial content
        sorted_sections = sorted(self.sections, 
                               key=lambda x: len(x["content"]), 
                               reverse=True)
        
        return sorted_sections[:max_sections]

if __name__ == "__main__":
    # Test the extractor
    extractor = PDFExtractor("/workspace/GaN Overview.pdf")
    text = extractor.extract_text()
    print(f"Extracted {len(text)} characters")
    
    sections = extractor.parse_sections()
    print(f"\nFound {len(sections)} sections:")
    for i, section in enumerate(sections[:5]):
        print(f"\n{i+1}. {section['title']}")
        print(f"   Content preview: {section['content'][:200]}...")