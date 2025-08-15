#!/usr/bin/env python3
"""
Documentation Processing Script for Voither Landing Page

This script processes documentation from the docs repository and organizes it
into the 4 invariant axes: ontologies, parsings, vectors, graphs.
"""

import argparse
import json
import os
import re
import shutil
import yaml
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional

import markdown
from bs4 import BeautifulSoup


class DocumentProcessor:
    """Processes and organizes documentation content."""
    
    def __init__(self, source_dir: str, target_dir: str, timestamp: str):
        self.source_dir = Path(source_dir)
        self.target_dir = Path(target_dir)
        self.timestamp = timestamp
        self.processed_files = []
        self.metadata = {
            "sync_timestamp": timestamp,
            "processed_files": [],
            "statistics": {
                "total_files": 0,
                "ontologies_count": 0,
                "parsings_count": 0,
                "content_size": 0
            }
        }
    
    def process_all(self):
        """Main processing function."""
        print(f"🔄 Starting documentation processing...")
        print(f"📂 Source: {self.source_dir}")
        print(f"🎯 Target: {self.target_dir}")
        
        # Ensure target directories exist
        self.ensure_target_structure()
        
        # Process different file types
        self.process_markdown_files()
        self.process_yaml_config_files()
        self.process_text_files()
        self.extract_ontologies()
        
        # Generate index files
        self.generate_indexes()
        
        # Save metadata
        self.save_metadata()
        
        print(f"✅ Processing complete. Processed {len(self.processed_files)} files.")
    
    def ensure_target_structure(self):
        """Ensure all required directories exist."""
        directories = [
            self.target_dir / "ontologies" / "concepts",
            self.target_dir / "ontologies" / "taxonomies", 
            self.target_dir / "ontologies" / "frameworks",
            self.target_dir / "parsings" / "markdown",
            self.target_dir / "parsings" / "structured",
            self.target_dir / "parsings" / "extracted",
            self.target_dir / "vectors" / "embeddings",
            self.target_dir / "vectors" / "indices",
            self.target_dir / "graphs" / "knowledge",
            self.target_dir / "graphs" / "relationships"
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
    
    def process_markdown_files(self):
        """Process all markdown files from the source."""
        if not self.source_dir.exists():
            print(f"⚠️  Source directory {self.source_dir} does not exist. Creating sample structure.")
            self.create_sample_structure()
            return
            
        markdown_files = list(self.source_dir.rglob("*.md"))
        
        for md_file in markdown_files:
            try:
                content = md_file.read_text(encoding='utf-8')
                
                # Parse markdown to HTML for better structure extraction
                html = markdown.markdown(content, extensions=['meta', 'toc'])
                soup = BeautifulSoup(html, 'html.parser')
                
                # Extract structured content
                parsed_content = {
                    "original_path": str(md_file.relative_to(self.source_dir)),
                    "title": self.extract_title(content),
                    "headings": self.extract_headings(soup),
                    "concepts": self.extract_concepts(content),
                    "content": content,
                    "html": html,
                    "processed_at": self.timestamp
                }
                
                # Save to parsings directory
                output_file = self.target_dir / "parsings" / "markdown" / f"{md_file.stem}.json"
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(parsed_content, f, indent=2, ensure_ascii=False)
                
                self.processed_files.append(str(md_file))
                self.metadata["statistics"]["total_files"] += 1
                
                print(f"📄 Processed: {md_file.name}")
                
            except Exception as e:
                print(f"❌ Error processing {md_file}: {e}")
    
    def process_yaml_config_files(self):
        """Process YAML configuration files."""
        if not self.source_dir.exists():
            return
            
        yaml_files = list(self.source_dir.rglob("*.yml")) + list(self.source_dir.rglob("*.yaml"))
        
        for yaml_file in yaml_files:
            try:
                with open(yaml_file, 'r', encoding='utf-8') as f:
                    data = yaml.safe_load(f)
                
                # Structure the YAML data
                structured_content = {
                    "original_path": str(yaml_file.relative_to(self.source_dir)),
                    "data": data,
                    "processed_at": self.timestamp
                }
                
                # Save to parsings/structured
                output_file = self.target_dir / "parsings" / "structured" / f"{yaml_file.stem}.json"
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(structured_content, f, indent=2, ensure_ascii=False)
                
                self.processed_files.append(str(yaml_file))
                print(f"⚙️  Processed config: {yaml_file.name}")
                
            except Exception as e:
                print(f"❌ Error processing {yaml_file}: {e}")
    
    def process_text_files(self):
        """Process plain text files."""
        if not self.source_dir.exists():
            return
            
        text_files = list(self.source_dir.rglob("*.txt"))
        
        for txt_file in text_files:
            try:
                content = txt_file.read_text(encoding='utf-8')
                
                # Structure the text content
                structured_content = {
                    "original_path": str(txt_file.relative_to(self.source_dir)),
                    "content": content,
                    "line_count": len(content.splitlines()),
                    "word_count": len(content.split()),
                    "processed_at": self.timestamp
                }
                
                # Save to parsings directory
                output_file = self.target_dir / "parsings" / "extracted" / f"{txt_file.stem}.json"
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(structured_content, f, indent=2, ensure_ascii=False)
                
                self.processed_files.append(str(txt_file))
                print(f"📝 Processed text: {txt_file.name}")
                
            except Exception as e:
                print(f"❌ Error processing {txt_file}: {e}")
    
    def extract_ontologies(self):
        """Extract and organize ontological concepts."""
        concepts = []
        taxonomies = []
        frameworks = []
        
        # Extract from all processed content
        for processed_file in self.processed_files:
            if processed_file.endswith('.md'):
                md_path = Path(processed_file)
                if md_path.exists():
                    content = md_path.read_text(encoding='utf-8')
                    
                    # Extract concepts based on patterns
                    concepts.extend(self.extract_domain_concepts(content))
                    taxonomies.extend(self.extract_taxonomies(content))
                    frameworks.extend(self.extract_frameworks(content))
        
        # Save ontologies
        self.save_ontology_data("concepts", concepts)
        self.save_ontology_data("taxonomies", taxonomies)
        self.save_ontology_data("frameworks", frameworks)
        
        self.metadata["statistics"]["ontologies_count"] = len(concepts) + len(taxonomies) + len(frameworks)
    
    def extract_title(self, content: str) -> str:
        """Extract title from markdown content."""
        lines = content.split('\n')
        for line in lines:
            if line.startswith('# '):
                return line[2:].strip()
        return "Untitled"
    
    def extract_headings(self, soup: BeautifulSoup) -> List[Dict]:
        """Extract all headings from HTML soup."""
        headings = []
        for i in range(1, 7):
            for heading in soup.find_all(f'h{i}'):
                headings.append({
                    "level": i,
                    "text": heading.get_text().strip(),
                    "id": heading.get('id', '')
                })
        return headings
    
    def extract_concepts(self, content: str) -> List[str]:
        """Extract key concepts from content."""
        # Simple concept extraction based on patterns
        concepts = []
        
        # Look for capitalized terms and technical terms
        pattern = r'\b[A-Z][A-Z0-9]*\b|\b[A-Z][a-z]+(?:[A-Z][a-z]+)*\b'
        matches = re.findall(pattern, content)
        
        # Filter and clean concepts
        for match in matches:
            if len(match) > 2 and match not in ['THE', 'AND', 'FOR', 'WITH']:
                concepts.append(match)
        
        return list(set(concepts))
    
    def extract_domain_concepts(self, content: str) -> List[Dict]:
        """Extract domain-specific concepts."""
        concepts = []
        
        # Voither-specific terms
        voither_terms = [
            'BRRE', 'AUTOAGENCY', 'HOLOFRACTOR', 'MEDSCRIBE', 'PEER-AI',
            'kairos', 'lived time', 'clinical time', 'compliance that compiles',
            'rhizomatic memory', 'signal layers', 'E2E Pipeline'
        ]
        
        for term in voither_terms:
            if term.lower() in content.lower():
                concepts.append({
                    "term": term,
                    "category": "voither_concept",
                    "found_at": self.timestamp
                })
        
        return concepts
    
    def extract_taxonomies(self, content: str) -> List[Dict]:
        """Extract taxonomical structures."""
        taxonomies = []
        
        # Look for list structures that indicate taxonomies
        lines = content.split('\n')
        current_taxonomy = None
        
        for line in lines:
            if line.strip().startswith('##') and any(word in line.lower() for word in ['types', 'categories', 'classification']):
                current_taxonomy = {
                    "name": line.strip('#').strip(),
                    "items": [],
                    "extracted_at": self.timestamp
                }
            elif current_taxonomy and line.strip().startswith('-'):
                current_taxonomy["items"].append(line.strip('- ').strip())
            elif current_taxonomy and line.strip() == '':
                if current_taxonomy["items"]:
                    taxonomies.append(current_taxonomy)
                current_taxonomy = None
        
        return taxonomies
    
    def extract_frameworks(self, content: str) -> List[Dict]:
        """Extract framework definitions."""
        frameworks = []
        
        # Look for framework patterns
        framework_indicators = ['framework', 'architecture', 'system', 'engine', 'pipeline']
        
        for indicator in framework_indicators:
            pattern = rf'{indicator}[:\s]+(.*?)(?:\n\n|\n#|$)'
            matches = re.findall(pattern, content, re.IGNORECASE | re.DOTALL)
            
            for match in matches:
                if len(match.strip()) > 20:  # Only substantial content
                    frameworks.append({
                        "type": indicator,
                        "description": match.strip(),
                        "extracted_at": self.timestamp
                    })
        
        return frameworks
    
    def save_ontology_data(self, category: str, data: List[Dict]):
        """Save ontology data to appropriate files."""
        if not data:
            return
            
        output_file = self.target_dir / "ontologies" / category / f"{category}.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump({
                "category": category,
                "items": data,
                "count": len(data),
                "generated_at": self.timestamp
            }, f, indent=2, ensure_ascii=False)
    
    def generate_indexes(self):
        """Generate index files for easy navigation."""
        # Generate parsings index
        parsings_index = {
            "generated_at": self.timestamp,
            "markdown_files": [],
            "structured_files": [],
            "extracted_files": []
        }
        
        # Scan parsings directory
        for subdir in ["markdown", "structured", "extracted"]:
            dir_path = self.target_dir / "parsings" / subdir
            if dir_path.exists():
                files = list(dir_path.glob("*.json"))
                parsings_index[f"{subdir}_files"] = [f.name for f in files]
        
        with open(self.target_dir / "parsings" / "index.json", 'w') as f:
            json.dump(parsings_index, f, indent=2)
        
        # Generate ontologies index
        ontologies_index = {
            "generated_at": self.timestamp,
            "categories": ["concepts", "taxonomies", "frameworks"],
            "files": []
        }
        
        ontologies_dir = self.target_dir / "ontologies"
        for category in ontologies_index["categories"]:
            cat_dir = ontologies_dir / category
            if cat_dir.exists():
                files = list(cat_dir.glob("*.json"))
                ontologies_index["files"].extend([f"{category}/{f.name}" for f in files])
        
        with open(self.target_dir / "ontologies" / "index.json", 'w') as f:
            json.dump(ontologies_index, f, indent=2)
    
    def create_sample_structure(self):
        """Create sample structure when docs repository doesn't exist."""
        print("📁 Creating sample documentation structure...")
        
        sample_dir = self.source_dir
        sample_dir.mkdir(parents=True, exist_ok=True)
        
        # Create sample markdown file
        sample_md = sample_dir / "voither-overview.md"
        sample_content = """# Voither Medical Platform

## Overview
Voither is a revolutionary medical AI platform that transforms clinical workflows through intelligent automation.

## Core Technologies

### BRRE Engine
A reasoning engine that operates in lived time (kairos), not just clock time. It detects *when* to act, not just *what* to do.

### E2E Pipeline
A pipeline that connects speech to signal, decision, and paperwork in seconds, with measurable ROI.

### AUTOAGENCY
Executes documentation, orders, scheduling, and billing with auditing and measured time savings.

## Key Features
- Clinical Time as a 1st Class Citizen (kairos)
- Compliance that Compiles (.ee)
- Rhizomatic Memory + Signal Layers
- Native Clinical Automation (ReEngine)

## Products
- MEDSCRIBE: Clinical documentation assistant
- HOLOFRACTOR: Patient data analysis
- PEER-AI: Collaborative intelligence system
"""
        
        sample_md.write_text(sample_content, encoding='utf-8')
        
        # Create sample config
        sample_config = sample_dir / "config.yml"
        config_content = """
platform:
  name: "Voither"
  version: "1.0.0"
  
modules:
  - name: "BRRE"
    type: "reasoning_engine"
  - name: "AUTOAGENCY"
    type: "automation"
  - name: "E2E Pipeline"
    type: "workflow"

compliance:
  standards: ["HIPAA", "LGPD", "FHIR R4", "IEC 62304"]
"""
        
        sample_config.write_text(config_content, encoding='utf-8')
        print("📝 Created sample documentation files")
    
    def save_metadata(self):
        """Save processing metadata."""
        self.metadata["processed_files"] = self.processed_files
        self.metadata["statistics"]["parsings_count"] = len(self.processed_files)
        
        # Calculate content size
        total_size = 0
        for file_path in self.processed_files:
            if Path(file_path).exists():
                total_size += Path(file_path).stat().st_size
        
        self.metadata["statistics"]["content_size"] = total_size
        
        # Save metadata
        metadata_file = self.target_dir / "metadata.json"
        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump(self.metadata, f, indent=2, ensure_ascii=False)


def main():
    parser = argparse.ArgumentParser(description='Process documentation for Voither landing page')
    parser.add_argument('--source', required=True, help='Source documentation directory')
    parser.add_argument('--target', required=True, help='Target background directory')
    parser.add_argument('--timestamp', required=True, help='Processing timestamp')
    
    args = parser.parse_args()
    
    processor = DocumentProcessor(args.source, args.target, args.timestamp)
    processor.process_all()


if __name__ == "__main__":
    main()