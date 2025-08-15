#!/usr/bin/env python3
"""
Documentation Processing Script for Voither Landing Page

This script processes documentation from the docs repository and organizes it
into the 4 invariant axes: ontologies, parsings, vectors, graphs.
"""

import argparse
import json
import math
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
        self.existing_metadata = {}
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
        """Main processing function with incremental updates."""
        print(f"🔄 Starting incremental documentation processing...")
        print(f"📂 Source: {self.source_dir}")
        print(f"🎯 Target: {self.target_dir}")
        
        # Load existing metadata to understand current state
        self.load_existing_metadata()
        
        # Ensure target directories exist
        self.ensure_target_structure()
        
        # Process different file types incrementally
        self.process_markdown_files()
        self.process_yaml_config_files()
        self.process_text_files()
        self.extract_ontologies()
        
        # Generate visual concept representations
        self.generate_concept_trees()
        self.generate_hierarchy_maps()
        
        # Generate/update index files
        self.generate_indexes()
        
        # Save metadata
        self.save_metadata()
        
        print(f"✅ Incremental processing complete. Processed {len(self.processed_files)} files.")
    
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
    
    def load_existing_metadata(self):
        """Load existing metadata to maintain incremental updates."""
        metadata_file = self.target_dir / "metadata.json"
        if metadata_file.exists():
            try:
                with open(metadata_file, 'r', encoding='utf-8') as f:
                    self.existing_metadata = json.load(f)
                print(f"📊 Loaded existing metadata with {len(self.existing_metadata.get('sync_history', []))} sync records")
            except Exception as e:
                print(f"⚠️  Could not load existing metadata: {e}")
                self.existing_metadata = {}
        else:
            print("📊 No existing metadata found - starting fresh")
    
    def generate_concept_trees(self):
        """Generate visual concept trees and hierarchies."""
        print("🌳 Generating concept trees and visual hierarchies...")
        
        # Collect all concepts from processed files
        all_concepts = self.collect_all_concepts()
        
        # Generate hierarchical concept tree
        concept_tree = self.build_concept_hierarchy(all_concepts)
        
        # Save concept tree for visual representation
        tree_file = self.target_dir / "ontologies" / "concept_tree.json"
        with open(tree_file, 'w', encoding='utf-8') as f:
            json.dump(concept_tree, f, indent=2, ensure_ascii=False)
        
        # Generate HTML representation for landing page
        html_tree = self.generate_html_tree(concept_tree)
        html_file = self.target_dir / "ontologies" / "concept_tree.html"
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html_tree)
        
        # Generate SVG visualization
        svg_tree = self.generate_svg_tree(concept_tree)
        svg_file = self.target_dir / "ontologies" / "concept_tree.svg"
        with open(svg_file, 'w', encoding='utf-8') as f:
            f.write(svg_tree)
        
        print(f"🌳 Generated concept tree with {len(all_concepts)} unique concepts")
    
    def generate_hierarchy_maps(self):
        """Generate organizational charts and hierarchy maps."""
        print("🗺️  Generating hierarchy maps and organizational charts...")
        
        # Create Voither ecosystem hierarchy
        voither_hierarchy = {
            "name": "Voither Ecosystem",
            "type": "organization",
            "children": [
                {
                    "name": "Products",
                    "type": "category",
                    "children": [
                        {"name": "MEDSCRIBE", "type": "product", "description": "Clinical documentation system"},
                        {"name": "HOLOFRACTOR", "type": "product", "description": "Data analysis platform"},
                        {"name": "PEER-AI", "type": "product", "description": "Collaborative intelligence"}
                    ]
                },
                {
                    "name": "Technologies",
                    "type": "category", 
                    "children": [
                        {"name": "BRRE", "type": "technology", "description": "Biological Reasoning and Reality Engine"},
                        {"name": "AUTOAGENCY", "type": "technology", "description": "Autonomous agency framework"},
                        {"name": "E2E Pipeline", "type": "technology", "description": "End-to-end processing pipeline"}
                    ]
                },
                {
                    "name": "Concepts",
                    "type": "category",
                    "children": [
                        {"name": "kairos", "type": "concept", "description": "Strategic timing and opportunity"},
                        {"name": "AUTODOCS", "type": "concept", "description": "Automated documentation"},
                        {"name": "fidedignidade conceitual", "type": "concept", "description": "Conceptual fidelity"}
                    ]
                }
            ]
        }
        
        # Save hierarchy map
        hierarchy_file = self.target_dir / "ontologies" / "hierarchy_map.json"
        with open(hierarchy_file, 'w', encoding='utf-8') as f:
            json.dump(voither_hierarchy, f, indent=2, ensure_ascii=False)
        
        # Generate interactive HTML orgchart
        orgchart_html = self.generate_orgchart_html(voither_hierarchy)
        orgchart_file = self.target_dir / "ontologies" / "orgchart.html"
        with open(orgchart_file, 'w', encoding='utf-8') as f:
            f.write(orgchart_html)
        
        print("🗺️  Generated organizational hierarchy maps")
    
    def process_markdown_files(self):
        """Process all markdown files from the source incrementally."""
        if not self.source_dir.exists():
            print(f"⚠️  Source directory {self.source_dir} does not exist. Creating sample structure.")
            self.create_sample_structure()
            return
            
        markdown_files = list(self.source_dir.rglob("*.md"))
        
        for md_file in markdown_files:
            try:
                content = md_file.read_text(encoding='utf-8')
                
                # Check if this file was already processed (incremental update)
                output_file = self.target_dir / "parsings" / "markdown" / f"{md_file.stem}.json"
                skip_processing = False
                
                if output_file.exists():
                    try:
                        with open(output_file, 'r', encoding='utf-8') as f:
                            existing_data = json.load(f)
                            # Check if content has changed
                            if existing_data.get("content") == content:
                                print(f"⏭️  Skipping unchanged file: {md_file.name}")
                                skip_processing = True
                            else:
                                print(f"🔄 Updating modified file: {md_file.name}")
                    except:
                        print(f"📄 Reprocessing file due to read error: {md_file.name}")
                
                if not skip_processing:
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
                        "processed_at": self.timestamp,
                        "content_hash": hash(content)  # Simple hash for change detection
                    }
                    
                    # Save to parsings directory
                    with open(output_file, 'w', encoding='utf-8') as f:
                        json.dump(parsed_content, f, indent=2, ensure_ascii=False)
                    
                    print(f"📄 Processed: {md_file.name}")
                
                self.processed_files.append(str(md_file))
                self.metadata["statistics"]["total_files"] += 1
                
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
        """Save processing metadata to a separate file (not overwriting main metadata)."""
        self.metadata["processed_files"] = self.processed_files
        self.metadata["statistics"]["parsings_count"] = len(self.processed_files)
        
        # Calculate content size
        total_size = 0
        for file_path in self.processed_files:
            if Path(file_path).exists():
                total_size += Path(file_path).stat().st_size
        
        self.metadata["statistics"]["content_size"] = total_size
        
        # Save processing metadata to a separate file to avoid overwriting main metadata
        processing_metadata_file = self.target_dir / "processing_metadata.json"
        with open(processing_metadata_file, 'w', encoding='utf-8') as f:
            json.dump(self.metadata, f, indent=2, ensure_ascii=False)
        
        print(f"📊 Saved processing metadata to {processing_metadata_file.name}")
    
    def collect_all_concepts(self) -> List[Dict]:
        """Collect all concepts from processed files and existing data."""
        concepts = []
        
        # Predefined Voither concepts
        voither_concepts = [
            {"name": "MEDSCRIBE", "type": "product", "category": "clinical", "level": 1},
            {"name": "HOLOFRACTOR", "type": "product", "category": "analytics", "level": 1},
            {"name": "PEER-AI", "type": "product", "category": "collaboration", "level": 1},
            {"name": "BRRE", "type": "technology", "category": "reasoning", "level": 2},
            {"name": "AUTOAGENCY", "type": "technology", "category": "automation", "level": 2},
            {"name": "kairos", "type": "concept", "category": "temporal", "level": 3},
            {"name": "fidedignidade conceitual", "type": "concept", "category": "quality", "level": 3},
            {"name": "AUTODOCS", "type": "concept", "category": "automation", "level": 3}
        ]
        concepts.extend(voither_concepts)
        
        # Extract concepts from processed markdown files
        parsings_dir = self.target_dir / "parsings" / "markdown"
        if parsings_dir.exists():
            for json_file in parsings_dir.glob("*.json"):
                try:
                    with open(json_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        for concept in data.get("concepts", []):
                            concepts.append({
                                "name": concept,
                                "type": "extracted",
                                "category": "document_derived", 
                                "level": 4,
                                "source": json_file.stem
                            })
                except Exception as e:
                    print(f"⚠️  Could not load concepts from {json_file}: {e}")
        
        return concepts
    
    def build_concept_hierarchy(self, concepts: List[Dict]) -> Dict:
        """Build hierarchical concept tree."""
        tree = {
            "name": "Voither Knowledge Base",
            "type": "root",
            "children": []
        }
        
        # Group concepts by type
        by_type = {}
        for concept in concepts:
            concept_type = concept.get("type", "unknown")
            if concept_type not in by_type:
                by_type[concept_type] = []
            by_type[concept_type].append(concept)
        
        # Build tree structure
        for concept_type, type_concepts in by_type.items():
            type_node = {
                "name": concept_type.title(),
                "type": "category",
                "children": []
            }
            
            # Group by category within type
            by_category = {}
            for concept in type_concepts:
                category = concept.get("category", "general")
                if category not in by_category:
                    by_category[category] = []
                by_category[category].append(concept)
            
            for category, category_concepts in by_category.items():
                category_node = {
                    "name": category.title(),
                    "type": "subcategory", 
                    "children": [
                        {
                            "name": concept["name"],
                            "type": "concept",
                            "level": concept.get("level", 5),
                            "source": concept.get("source", "system")
                        }
                        for concept in category_concepts
                    ]
                }
                type_node["children"].append(category_node)
            
            tree["children"].append(type_node)
        
        return tree
    
    def generate_html_tree(self, tree: Dict) -> str:
        """Generate HTML representation of concept tree."""
        html = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Voither Concept Tree</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 20px; background: #f5f7fa; }
        .tree { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        .tree ul { list-style: none; padding-left: 20px; }
        .tree li { margin: 8px 0; }
        .tree-node { 
            padding: 8px 12px; 
            border-radius: 4px; 
            cursor: pointer;
            transition: all 0.3s ease;
        }
        .root { background: #667eea; color: white; font-weight: bold; }
        .category { background: #764ba2; color: white; }
        .subcategory { background: #f093fb; color: white; }
        .concept { background: #e3f2fd; color: #1565c0; border-left: 4px solid #2196f3; }
        .tree-node:hover { transform: translateX(5px); box-shadow: 0 2px 8px rgba(0,0,0,0.15); }
        .children { display: none; }
        .expanded .children { display: block; }
        .toggle { font-weight: bold; margin-right: 8px; }
    </style>
</head>
<body>
    <div class="tree">
        <h1>🌳 Voither Knowledge Concept Tree</h1>
        <p><em>Generated at: """ + self.timestamp + """</em></p>
"""
        
        def render_node(node, level=0):
            name = node.get("name", "Unknown")
            node_type = node.get("type", "unknown")
            children = node.get("children", [])
            
            classes = f"tree-node {node_type}"
            toggle = "▼" if children else "●"
            
            html_node = f'<li><div class="{classes}" onclick="toggleNode(this)">'
            html_node += f'<span class="toggle">{toggle}</span>{name}</div>'
            
            if children:
                html_node += '<ul class="children">'
                for child in children:
                    html_node += render_node(child, level + 1)
                html_node += '</ul>'
            
            html_node += '</li>'
            return html_node
        
        html += '<ul>' + render_node(tree) + '</ul>'
        
        html += """
    </div>
    <script>
        function toggleNode(element) {
            const parent = element.parentElement;
            parent.classList.toggle('expanded');
            const toggle = element.querySelector('.toggle');
            if (parent.classList.contains('expanded')) {
                toggle.textContent = '▲';
            } else {
                toggle.textContent = '▼';
            }
        }
        
        // Expand first level by default
        document.querySelectorAll('.tree > ul > li').forEach(li => {
            li.classList.add('expanded');
            const toggle = li.querySelector('.toggle');
            if (toggle) toggle.textContent = '▲';
        });
    </script>
</body>
</html>"""
        return html
    
    def generate_svg_tree(self, tree: Dict) -> str:
        """Generate SVG visualization of concept tree."""
        svg = """<svg width="800" height="600" xmlns="http://www.w3.org/2000/svg">
    <defs>
        <style>
            .root-text { font: bold 16px sans-serif; fill: #333; }
            .category-text { font: bold 14px sans-serif; fill: #666; }
            .concept-text { font: 12px sans-serif; fill: #999; }
            .tree-line { stroke: #ccc; stroke-width: 2; }
            .root-circle { fill: #667eea; stroke: #333; stroke-width: 2; }
            .category-circle { fill: #764ba2; stroke: #333; stroke-width: 1; }
            .concept-circle { fill: #e3f2fd; stroke: #2196f3; stroke-width: 1; }
        </style>
    </defs>
    
    <g transform="translate(400,50)">
        <!-- Root node -->
        <circle cx="0" cy="0" r="25" class="root-circle"/>
        <text x="0" y="5" text-anchor="middle" class="root-text">Voither</text>
        
        <!-- Category nodes -->"""
        
        categories = tree.get("children", [])
        angle_step = 360 / max(len(categories), 1)
        
        for i, category in enumerate(categories):
            angle = i * angle_step * 3.14159 / 180
            x = 150 * math.cos(angle)
            y = 150 * math.sin(angle)
            
            svg += f'''
        <line x1="0" y1="0" x2="{x}" y2="{y}" class="tree-line"/>
        <circle cx="{x}" cy="{y}" r="20" class="category-circle"/>
        <text x="{x}" y="{y+5}" text-anchor="middle" class="category-text">{category.get("name", "")}</text>'''
        
        svg += """
    </g>
    <text x="400" y="580" text-anchor="middle" class="concept-text">Generated: """ + self.timestamp + """</text>
</svg>"""
        return svg
    
    def generate_orgchart_html(self, hierarchy: Dict) -> str:
        """Generate interactive organizational chart."""
        html = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Voither Ecosystem Organization</title>
    <style>
        body { font-family: 'Segoe UI', sans-serif; margin: 0; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; }
        .orgchart { max-width: 1200px; margin: 20px auto; padding: 20px; }
        .org-title { text-align: center; color: white; font-size: 2em; margin-bottom: 30px; }
        .org-level { display: flex; justify-content: center; margin: 30px 0; flex-wrap: wrap; gap: 20px; }
        .org-node { 
            background: white; 
            border-radius: 8px; 
            padding: 20px; 
            box-shadow: 0 4px 15px rgba(0,0,0,0.2); 
            text-align: center;
            min-width: 180px;
            transition: all 0.3s ease;
        }
        .org-node:hover { transform: translateY(-5px); box-shadow: 0 8px 25px rgba(0,0,0,0.3); }
        .org-root { background: linear-gradient(135deg, #667eea, #764ba2); color: white; font-size: 1.2em; }
        .org-category { background: linear-gradient(135deg, #f093fb, #f5576c); color: white; }
        .org-item { background: #f8f9fa; border-left: 4px solid #007bff; }
        .org-name { font-weight: bold; margin-bottom: 8px; }
        .org-desc { font-size: 0.9em; opacity: 0.8; }
        .connection { height: 2px; background: rgba(255,255,255,0.3); margin: -15px auto 15px; width: 60%; }
    </style>
</head>
<body>
    <div class="orgchart">
        <h1 class="org-title">🏢 Voither Ecosystem Organization</h1>
        
        <!-- Root Level -->
        <div class="org-level">
            <div class="org-node org-root">
                <div class="org-name">""" + hierarchy.get("name", "Voither") + """</div>
                <div class="org-desc">Complete Ecosystem</div>
            </div>
        </div>
        
        <div class="connection"></div>
        
        <!-- Category Level -->
        <div class="org-level">"""
        
        for category in hierarchy.get("children", []):
            html += f'''
            <div class="org-node org-category">
                <div class="org-name">{category.get("name", "")}</div>
                <div class="org-desc">{category.get("type", "").title()}</div>
            </div>'''
        
        html += """
        </div>
        
        <div class="connection"></div>
        
        <!-- Items Level -->
        <div class="org-level">"""
        
        for category in hierarchy.get("children", []):
            for item in category.get("children", []):
                html += f'''
            <div class="org-node org-item">
                <div class="org-name">{item.get("name", "")}</div>
                <div class="org-desc">{item.get("description", "")}</div>
            </div>'''
        
        html += f"""
        </div>
        
        <div style="text-align: center; color: white; margin-top: 40px; opacity: 0.8;">
            <p>Generated: {self.timestamp}</p>
        </div>
    </div>
</body>
</html>"""
        return html


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