#!/usr/bin/env python3
"""
Knowledge Graph Creation Script for Voither Landing Page

This script creates knowledge graphs and relationship mappings from processed content.
"""

import argparse
import json
import os
from pathlib import Path
from typing import Dict, List, Any, Set, Tuple
import re


class KnowledgeGraphBuilder:
    """Builds knowledge graphs from processed documentation."""
    
    def __init__(self, input_dir: str, output_dir: str):
        self.input_dir = Path(input_dir)
        self.output_dir = Path(output_dir)
        self.entities = {}
        self.relationships = []
        self.concepts = set()
        self.entity_types = {
            'product': [],
            'technology': [],
            'concept': [],
            'process': [],
            'standard': [],
            'feature': []
        }
    
    def build_all(self):
        """Main function to build knowledge graphs."""
        print("🕸️  Starting knowledge graph construction...")
        
        # Ensure output directory exists
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Extract entities and relationships
        self.extract_entities()
        self.extract_relationships()
        self.build_concept_hierarchy()
        
        # Generate graph files
        self.generate_graph_json()
        self.generate_cypher_queries()
        self.generate_graphml()
        self.generate_relationship_matrix()
        
        # Save graph metadata
        self.save_graph_metadata()
        
        print("✅ Knowledge graph construction complete.")
    
    def extract_entities(self):
        """Extract entities from all processed content."""
        print("🔍 Extracting entities...")
        
        # Extract from ontologies
        self.extract_from_ontologies()
        
        # Extract from parsings
        self.extract_from_parsings()
        
        # Extract Voither-specific entities
        self.extract_voither_entities()
        
        print(f"📊 Extracted {len(self.entities)} entities")
    
    def extract_from_ontologies(self):
        """Extract entities from ontology data."""
        ontologies_dir = self.input_dir / "ontologies"
        
        if not ontologies_dir.exists():
            return
        
        # Load concepts
        concepts_file = ontologies_dir / "concepts" / "concepts.json"
        if concepts_file.exists():
            try:
                with open(concepts_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                for item in data.get('items', []):
                    if isinstance(item, dict) and 'term' in item:
                        entity_id = self.normalize_entity_id(item['term'])
                        self.entities[entity_id] = {
                            "id": entity_id,
                            "name": item['term'],
                            "type": "concept",
                            "category": item.get('category', 'general'),
                            "source": "ontology_concepts"
                        }
                        self.entity_types['concept'].append(entity_id)
                        self.concepts.add(item['term'])
                        
            except Exception as e:
                print(f"❌ Error loading concepts: {e}")
        
        # Load taxonomies
        taxonomies_file = ontologies_dir / "taxonomies" / "taxonomies.json"
        if taxonomies_file.exists():
            try:
                with open(taxonomies_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                for item in data.get('items', []):
                    if isinstance(item, dict) and 'name' in item:
                        entity_id = self.normalize_entity_id(item['name'])
                        self.entities[entity_id] = {
                            "id": entity_id,
                            "name": item['name'],
                            "type": "taxonomy",
                            "items": item.get('items', []),
                            "source": "ontology_taxonomies"
                        }
                        self.entity_types['concept'].append(entity_id)
                        
            except Exception as e:
                print(f"❌ Error loading taxonomies: {e}")
        
        # Load frameworks
        frameworks_file = ontologies_dir / "frameworks" / "frameworks.json"
        if frameworks_file.exists():
            try:
                with open(frameworks_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                for item in data.get('items', []):
                    if isinstance(item, dict) and 'type' in item:
                        entity_id = self.normalize_entity_id(item['type'])
                        self.entities[entity_id] = {
                            "id": entity_id,
                            "name": item['type'],
                            "type": "framework",
                            "description": item.get('description', ''),
                            "source": "ontology_frameworks"
                        }
                        self.entity_types['technology'].append(entity_id)
                        
            except Exception as e:
                print(f"❌ Error loading frameworks: {e}")
    
    def extract_from_parsings(self):
        """Extract entities from parsing data."""
        parsings_dir = self.input_dir / "parsings"
        
        if not parsings_dir.exists():
            return
        
        # Extract from markdown parsings
        markdown_dir = parsings_dir / "markdown"
        if markdown_dir.exists():
            for json_file in markdown_dir.glob("*.json"):
                try:
                    with open(json_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    
                    # Extract from headings
                    for heading in data.get('headings', []):
                        text = heading.get('text', '')
                        if text and len(text) > 3:
                            entity_id = self.normalize_entity_id(text)
                            if entity_id not in self.entities:
                                self.entities[entity_id] = {
                                    "id": entity_id,
                                    "name": text,
                                    "type": "topic",
                                    "level": heading.get('level', 1),
                                    "source": f"parsing_{json_file.stem}"
                                }
                                self.entity_types['concept'].append(entity_id)
                    
                    # Extract from concepts
                    for concept in data.get('concepts', []):
                        if concept and len(concept) > 2:
                            entity_id = self.normalize_entity_id(concept)
                            if entity_id not in self.entities:
                                self.entities[entity_id] = {
                                    "id": entity_id,
                                    "name": concept,
                                    "type": "extracted_concept",
                                    "source": f"parsing_{json_file.stem}"
                                }
                                self.entity_types['concept'].append(entity_id)
                                self.concepts.add(concept)
                    
                except Exception as e:
                    print(f"❌ Error extracting from {json_file}: {e}")
    
    def extract_voither_entities(self):
        """Extract Voither-specific entities."""
        voither_entities = {
            # Products
            "MEDSCRIBE": {"type": "product", "category": "clinical_documentation"},
            "HOLOFRACTOR": {"type": "product", "category": "data_analysis"},
            "PEER-AI": {"type": "product", "category": "collaborative_intelligence"},
            
            # Technologies
            "BRRE": {"type": "technology", "category": "reasoning_engine"},
            "AUTOAGENCY": {"type": "technology", "category": "automation"},
            "E2E_Pipeline": {"type": "technology", "category": "workflow"},
            
            # Concepts
            "kairos": {"type": "concept", "category": "temporal"},
            "lived_time": {"type": "concept", "category": "temporal"},
            "clinical_time": {"type": "concept", "category": "temporal"},
            "compliance_that_compiles": {"type": "concept", "category": "methodology"},
            "rhizomatic_memory": {"type": "concept", "category": "architecture"},
            "signal_layers": {"type": "concept", "category": "architecture"},
            
            # Standards
            "HIPAA": {"type": "standard", "category": "privacy"},
            "LGPD": {"type": "standard", "category": "privacy"},
            "FHIR_R4": {"type": "standard", "category": "interoperability"},
            "IEC_62304": {"type": "standard", "category": "medical_device"},
            
            # Processes
            "speech_to_signal": {"type": "process", "category": "workflow"},
            "clinical_documentation": {"type": "process", "category": "workflow"},
            "automated_billing": {"type": "process", "category": "workflow"}
        }
        
        for name, props in voither_entities.items():
            entity_id = self.normalize_entity_id(name)
            if entity_id not in self.entities:
                self.entities[entity_id] = {
                    "id": entity_id,
                    "name": name.replace('_', ' '),
                    "type": props["type"],
                    "category": props["category"],
                    "source": "voither_predefined"
                }
                self.entity_types[props["type"]].append(entity_id)
    
    def extract_relationships(self):
        """Extract relationships between entities."""
        print("🔗 Extracting relationships...")
        
        # Define relationship patterns
        self.define_voither_relationships()
        
        # Extract relationships from text content
        self.extract_textual_relationships()
        
        # Infer hierarchical relationships
        self.infer_hierarchical_relationships()
        
        print(f"🔗 Extracted {len(self.relationships)} relationships")
    
    def define_voither_relationships(self):
        """Define known Voither relationships."""
        known_relationships = [
            # Technology relationships
            ("BRRE", "kairos", "IMPLEMENTS"),
            ("BRRE", "clinical_time", "PROCESSES"),
            ("AUTOAGENCY", "clinical_documentation", "AUTOMATES"),
            ("AUTOAGENCY", "automated_billing", "AUTOMATES"),
            ("E2E_Pipeline", "speech_to_signal", "INCLUDES"),
            
            # Product relationships
            ("MEDSCRIBE", "BRRE", "USES"),
            ("MEDSCRIBE", "clinical_documentation", "FACILITATES"),
            ("HOLOFRACTOR", "signal_layers", "ANALYZES"),
            ("PEER-AI", "rhizomatic_memory", "LEVERAGES"),
            
            # Compliance relationships
            ("compliance_that_compiles", "HIPAA", "ENFORCES"),
            ("compliance_that_compiles", "LGPD", "ENFORCES"),
            ("compliance_that_compiles", "FHIR_R4", "IMPLEMENTS"),
            ("compliance_that_compiles", "IEC_62304", "COMPLIES_WITH"),
            
            # Architectural relationships
            ("rhizomatic_memory", "signal_layers", "CONTAINS"),
            ("signal_layers", "knowledge_graph", "FORMS"),
            
            # Temporal relationships
            ("kairos", "lived_time", "REPRESENTS"),
            ("clinical_time", "kairos", "INSTANCE_OF"),
        ]
        
        for source, target, rel_type in known_relationships:
            source_id = self.normalize_entity_id(source)
            target_id = self.normalize_entity_id(target)
            
            if source_id in self.entities and target_id in self.entities:
                self.relationships.append({
                    "source": source_id,
                    "target": target_id,
                    "type": rel_type,
                    "source_name": self.entities[source_id]["name"],
                    "target_name": self.entities[target_id]["name"],
                    "confidence": 1.0,
                    "origin": "predefined"
                })
    
    def extract_textual_relationships(self):
        """Extract relationships from text content."""
        parsings_dir = self.input_dir / "parsings" / "markdown"
        
        if not parsings_dir.exists():
            return
        
        relationship_patterns = [
            (r'(\w+)\s+(?:uses|utilizes|employs)\s+(\w+)', "USES"),
            (r'(\w+)\s+(?:includes|contains|comprises)\s+(\w+)', "INCLUDES"),
            (r'(\w+)\s+(?:implements|realizes|executes)\s+(\w+)', "IMPLEMENTS"),
            (r'(\w+)\s+(?:is|are)\s+(?:a|an)\s+(\w+)', "IS_A"),
            (r'(\w+)\s+(?:connects to|integrates with)\s+(\w+)', "CONNECTS_TO"),
        ]
        
        for json_file in parsings_dir.glob("*.json"):
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                content = data.get('content', '')
                
                for pattern, rel_type in relationship_patterns:
                    matches = re.findall(pattern, content, re.IGNORECASE)
                    
                    for source, target in matches:
                        source_id = self.normalize_entity_id(source)
                        target_id = self.normalize_entity_id(target)
                        
                        if (source_id in self.entities and target_id in self.entities and
                            not self.relationship_exists(source_id, target_id, rel_type)):
                            
                            self.relationships.append({
                                "source": source_id,
                                "target": target_id,
                                "type": rel_type,
                                "source_name": self.entities[source_id]["name"],
                                "target_name": self.entities[target_id]["name"],
                                "confidence": 0.7,
                                "origin": f"extracted_from_{json_file.stem}"
                            })
                            
            except Exception as e:
                print(f"❌ Error extracting relationships from {json_file}: {e}")
    
    def infer_hierarchical_relationships(self):
        """Infer hierarchical relationships between entities."""
        # Group entities by type for hierarchical inference
        for entity_type, entity_ids in self.entity_types.items():
            for i, entity_id in enumerate(entity_ids):
                # Create type relationships
                type_entity_id = self.normalize_entity_id(f"{entity_type}_category")
                
                if type_entity_id not in self.entities:
                    self.entities[type_entity_id] = {
                        "id": type_entity_id,
                        "name": f"{entity_type.title()} Category",
                        "type": "category",
                        "source": "inferred"
                    }
                
                if not self.relationship_exists(entity_id, type_entity_id, "BELONGS_TO"):
                    self.relationships.append({
                        "source": entity_id,
                        "target": type_entity_id,
                        "type": "BELONGS_TO",
                        "source_name": self.entities[entity_id]["name"],
                        "target_name": self.entities[type_entity_id]["name"],
                        "confidence": 0.9,
                        "origin": "type_hierarchy"
                    })
    
    def build_concept_hierarchy(self):
        """Build hierarchical structure of concepts."""
        print("🏗️  Building concept hierarchy...")
        
        # Create main concept categories
        main_categories = {
            "voither_platform": "Voither Platform",
            "medical_concepts": "Medical Concepts",
            "technical_architecture": "Technical Architecture",
            "compliance_standards": "Compliance Standards",
            "automation_processes": "Automation Processes"
        }
        
        for cat_id, cat_name in main_categories.items():
            if cat_id not in self.entities:
                self.entities[cat_id] = {
                    "id": cat_id,
                    "name": cat_name,
                    "type": "main_category",
                    "source": "hierarchy"
                }
        
        # Assign entities to main categories
        category_mappings = {
            "voither_platform": ["MEDSCRIBE", "HOLOFRACTOR", "PEER-AI"],
            "technical_architecture": ["BRRE", "AUTOAGENCY", "E2E_Pipeline", "rhizomatic_memory", "signal_layers"],
            "medical_concepts": ["kairos", "lived_time", "clinical_time", "clinical_documentation"],
            "compliance_standards": ["HIPAA", "LGPD", "FHIR_R4", "IEC_62304", "compliance_that_compiles"],
            "automation_processes": ["speech_to_signal", "automated_billing"]
        }
        
        for category, entity_names in category_mappings.items():
            for entity_name in entity_names:
                entity_id = self.normalize_entity_id(entity_name)
                if entity_id in self.entities:
                    if not self.relationship_exists(entity_id, category, "BELONGS_TO_CATEGORY"):
                        self.relationships.append({
                            "source": entity_id,
                            "target": category,
                            "type": "BELONGS_TO_CATEGORY",
                            "source_name": self.entities[entity_id]["name"],
                            "target_name": self.entities[category]["name"],
                            "confidence": 0.95,
                            "origin": "manual_categorization"
                        })
    
    def normalize_entity_id(self, name: str) -> str:
        """Normalize entity name to create consistent IDs."""
        return re.sub(r'[^a-zA-Z0-9_]', '_', name.lower().strip())
    
    def relationship_exists(self, source: str, target: str, rel_type: str) -> bool:
        """Check if a relationship already exists."""
        for rel in self.relationships:
            if (rel["source"] == source and rel["target"] == target and 
                rel["type"] == rel_type):
                return True
        return False
    
    def generate_graph_json(self):
        """Generate JSON representation of the knowledge graph."""
        graph_data = {
            "nodes": list(self.entities.values()),
            "edges": self.relationships,
            "statistics": {
                "total_nodes": len(self.entities),
                "total_edges": len(self.relationships),
                "node_types": {k: len(v) for k, v in self.entity_types.items()},
                "edge_types": {}
            },
            "metadata": {
                "generated_at": "2025-08-14T23:58:00Z",
                "format": "knowledge_graph_json",
                "version": "1.0"
            }
        }
        
        # Count edge types
        for rel in self.relationships:
            rel_type = rel["type"]
            graph_data["statistics"]["edge_types"][rel_type] = \
                graph_data["statistics"]["edge_types"].get(rel_type, 0) + 1
        
        output_file = self.output_dir / "knowledge_graph.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(graph_data, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Saved knowledge graph JSON: {len(self.entities)} nodes, {len(self.relationships)} edges")
    
    def generate_cypher_queries(self):
        """Generate Cypher queries for Neo4j import."""
        cypher_queries = []
        
        # Create node queries
        cypher_queries.append("// Create nodes")
        for entity in self.entities.values():
            cypher_queries.append(
                f"CREATE (n:{entity['type'].title()} {{id: '{entity['id']}', "
                f"name: '{entity['name']}', type: '{entity['type']}', "
                f"source: '{entity.get('source', 'unknown')}'}});"
            )
        
        cypher_queries.append("\n// Create relationships")
        for rel in self.relationships:
            cypher_queries.append(
                f"MATCH (a {{id: '{rel['source']}'}}), (b {{id: '{rel['target']}'}}) "
                f"CREATE (a)-[r:{rel['type']} {{confidence: {rel['confidence']}, "
                f"origin: '{rel['origin']}'}}]->(b);"
            )
        
        output_file = self.output_dir / "knowledge_graph.cypher"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(cypher_queries))
        
        print(f"🔧 Generated Cypher queries file")
    
    def generate_graphml(self):
        """Generate GraphML format for visualization tools."""
        graphml_content = ['<?xml version="1.0" encoding="UTF-8"?>']
        graphml_content.append('<graphml xmlns="http://graphml.graphdrawing.org/xmlns">')
        graphml_content.append('  <key id="name" for="node" attr.name="name" attr.type="string"/>')
        graphml_content.append('  <key id="type" for="node" attr.name="type" attr.type="string"/>')
        graphml_content.append('  <key id="relationship" for="edge" attr.name="relationship" attr.type="string"/>')
        graphml_content.append('  <key id="confidence" for="edge" attr.name="confidence" attr.type="double"/>')
        graphml_content.append('  <graph id="voither_knowledge_graph" edgedefault="directed">')
        
        # Add nodes
        for entity in self.entities.values():
            graphml_content.append(f'    <node id="{entity["id"]}">')
            graphml_content.append(f'      <data key="name">{entity["name"]}</data>')
            graphml_content.append(f'      <data key="type">{entity["type"]}</data>')
            graphml_content.append('    </node>')
        
        # Add edges
        for i, rel in enumerate(self.relationships):
            graphml_content.append(f'    <edge id="e{i}" source="{rel["source"]}" target="{rel["target"]}">')
            graphml_content.append(f'      <data key="relationship">{rel["type"]}</data>')
            graphml_content.append(f'      <data key="confidence">{rel["confidence"]}</data>')
            graphml_content.append('    </edge>')
        
        graphml_content.append('  </graph>')
        graphml_content.append('</graphml>')
        
        output_file = self.output_dir / "knowledge_graph.graphml"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(graphml_content))
        
        print(f"📊 Generated GraphML file for visualization")
    
    def generate_relationship_matrix(self):
        """Generate relationship matrix for analysis."""
        entity_list = list(self.entities.keys())
        matrix_size = len(entity_list)
        
        # Create adjacency matrix
        adjacency_matrix = [[0 for _ in range(matrix_size)] for _ in range(matrix_size)]
        
        entity_index = {entity: i for i, entity in enumerate(entity_list)}
        
        for rel in self.relationships:
            source_idx = entity_index.get(rel["source"])
            target_idx = entity_index.get(rel["target"])
            
            if source_idx is not None and target_idx is not None:
                adjacency_matrix[source_idx][target_idx] = 1
        
        matrix_data = {
            "entity_list": [self.entities[eid]["name"] for eid in entity_list],
            "entity_ids": entity_list,
            "adjacency_matrix": adjacency_matrix,
            "matrix_size": matrix_size,
            "relationships_mapped": len(self.relationships)
        }
        
        output_file = self.output_dir / "relationship_matrix.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(matrix_data, f, indent=2, ensure_ascii=False)
        
        print(f"📈 Generated relationship matrix: {matrix_size}x{matrix_size}")
    
    def save_graph_metadata(self):
        """Save metadata about the knowledge graph."""
        metadata = {
            "input_directory": str(self.input_dir),
            "output_directory": str(self.output_dir),
            "total_entities": len(self.entities),
            "total_relationships": len(self.relationships),
            "entity_distribution": {k: len(v) for k, v in self.entity_types.items()},
            "relationship_types": list(set(rel["type"] for rel in self.relationships)),
            "files_generated": [
                "knowledge_graph.json",
                "knowledge_graph.cypher", 
                "knowledge_graph.graphml",
                "relationship_matrix.json",
                "graph_metadata.json"
            ],
            "format_support": {
                "json": "General purpose, web applications",
                "cypher": "Neo4j graph database import",
                "graphml": "Visualization tools (Gephi, Cytoscape)",
                "matrix": "Mathematical analysis, algorithms"
            }
        }
        
        output_file = self.output_dir / "graph_metadata.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)


def main():
    parser = argparse.ArgumentParser(description='Create knowledge graph from processed documentation')
    parser.add_argument('--input', required=True, help='Input background directory')
    parser.add_argument('--output', required=True, help='Output graphs directory')
    
    args = parser.parse_args()
    
    builder = KnowledgeGraphBuilder(args.input, args.output)
    builder.build_all()


if __name__ == "__main__":
    main()