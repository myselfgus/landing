#!/usr/bin/env python3
"""
Metadata Update Script for Voither Landing Page

This script updates content metadata and synchronization information.
"""

import argparse
import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any


class MetadataUpdater:
    """Updates metadata for the background content system."""
    
    def __init__(self, background_dir: str, commit_sha: str, docs_repo: str):
        self.background_dir = Path(background_dir)
        self.commit_sha = commit_sha
        self.docs_repo = docs_repo
        self.timestamp = datetime.utcnow().isoformat() + 'Z'
        self.existing_metadata = {}
        self.sync_history = []
    
    def update_all(self):
        """Main function to update all metadata incrementally."""
        print("📊 Incrementally updating content metadata...")
        
        # Load existing metadata
        self.load_existing_metadata()
        
        # Update sync history (append new entry)
        self.update_sync_history()
        
        # Collect current statistics
        stats = self.collect_statistics()
        
        # Update main metadata (incremental)
        self.update_main_metadata(stats)
        
        # Generate/update content index
        self.generate_content_index()
        
        # Update configuration
        self.update_configuration()
        
        print("✅ Incremental metadata update complete.")
    
    def load_existing_metadata(self):
        """Load existing metadata to maintain sync history."""
        metadata_file = self.background_dir / "metadata.json"
        self.existing_metadata = {}
        
        if metadata_file.exists():
            try:
                with open(metadata_file, 'r', encoding='utf-8') as f:
                    self.existing_metadata = json.load(f)
                sync_count = len(self.existing_metadata.get('sync_history', []))
                print(f"📊 Loaded existing metadata with {sync_count} sync records")
            except Exception as e:
                print(f"⚠️  Could not load existing metadata: {e}")
                self.existing_metadata = {}
        else:
            print("📊 No existing metadata found - starting fresh")
    
    def collect_statistics(self) -> Dict[str, Any]:
        """Collect statistics about the background content."""
        stats = {
            "directories": {},
            "files": {},
            "total_size": 0,
            "content_types": {}
        }
        
        # Scan each main directory
        main_dirs = ["ontologies", "parsings", "vectors", "graphs"]
        
        for main_dir in main_dirs:
            dir_path = self.background_dir / main_dir
            if dir_path.exists():
                dir_stats = self.scan_directory(dir_path)
                stats["directories"][main_dir] = dir_stats
                stats["total_size"] += dir_stats["total_size"]
                
                # Merge file counts
                for file_type, count in dir_stats["file_types"].items():
                    stats["content_types"][file_type] = \
                        stats["content_types"].get(file_type, 0) + count
        
        return stats
    
    def scan_directory(self, directory: Path) -> Dict[str, Any]:
        """Scan a directory and collect statistics."""
        stats = {
            "total_files": 0,
            "total_size": 0,
            "subdirectories": {},
            "file_types": {},
            "last_modified": None
        }
        
        if not directory.exists():
            return stats
        
        latest_mtime = 0
        
        for item in directory.rglob("*"):
            if item.is_file():
                stats["total_files"] += 1
                file_size = item.stat().st_size
                stats["total_size"] += file_size
                
                # Track file types
                file_ext = item.suffix.lower()
                if not file_ext:
                    file_ext = "no_extension"
                stats["file_types"][file_ext] = \
                    stats["file_types"].get(file_ext, 0) + 1
                
                # Track modification time
                mtime = item.stat().st_mtime
                if mtime > latest_mtime:
                    latest_mtime = mtime
                    stats["last_modified"] = datetime.fromtimestamp(mtime).isoformat() + 'Z'
            
            elif item.is_dir() and item.parent == directory:
                # Count subdirectories
                subdir_name = item.name
                subdir_stats = self.scan_directory(item)
                stats["subdirectories"][subdir_name] = subdir_stats
        
        return stats
    
    def update_main_metadata(self, stats: Dict[str, Any]):
        """Update the main metadata file."""
        metadata = {
            "sync_info": {
                "last_sync": self.timestamp,
                "commit_sha": self.commit_sha,
                "docs_repository": self.docs_repo,
                "sync_trigger": "docs_repository_update"
            },
            "content_statistics": stats,
            "organization": {
                "axes": [
                    {
                        "name": "ontologies",
                        "description": "Conceptual frameworks and taxonomies",
                        "subdirectories": ["concepts", "taxonomies", "frameworks"]
                    },
                    {
                        "name": "parsings", 
                        "description": "Structured content analysis",
                        "subdirectories": ["markdown", "structured", "extracted"]
                    },
                    {
                        "name": "vectors",
                        "description": "Semantic representations",
                        "subdirectories": ["embeddings", "indices"]
                    },
                    {
                        "name": "graphs",
                        "description": "Knowledge relationships and connections", 
                        "subdirectories": ["knowledge", "relationships"]
                    }
                ]
            },
            "quality_metrics": self.calculate_quality_metrics(stats),
            "system_info": {
                "format_version": "1.0",
                "generator": "docs-sync-automation",
                "encoding": "utf-8"
            }
        }
        
        # Include the updated sync history
        metadata["sync_history"] = self.sync_history
        
        # Save updated metadata
        metadata_file = self.background_dir / "metadata.json"
        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)
        
        print(f"📄 Updated main metadata: {stats['total_size']} bytes total")
    
    def calculate_quality_metrics(self, stats: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate quality metrics for the content."""
        metrics = {
            "completeness": {},
            "coverage": {},
            "freshness": self.timestamp
        }
        
        # Check completeness of each axis
        required_dirs = ["ontologies", "parsings", "vectors", "graphs"]
        for dir_name in required_dirs:
            dir_stats = stats["directories"].get(dir_name, {})
            file_count = dir_stats.get("total_files", 0)
            
            metrics["completeness"][dir_name] = {
                "file_count": file_count,
                "has_content": file_count > 0,
                "size_bytes": dir_stats.get("total_size", 0)
            }
        
        # Calculate overall coverage
        total_dirs_with_content = sum(
            1 for dir_name in required_dirs 
            if metrics["completeness"][dir_name]["has_content"]
        )
        
        metrics["coverage"]["axes_populated"] = total_dirs_with_content
        metrics["coverage"]["total_axes"] = len(required_dirs)
        metrics["coverage"]["coverage_percentage"] = \
            (total_dirs_with_content / len(required_dirs)) * 100
        
        return metrics
    
    def update_sync_history(self):
        """Update the synchronization history incrementally."""
        history_entry = {
            "timestamp": self.timestamp,
            "commit_sha": self.commit_sha,
            "docs_repository": self.docs_repo,
            "sync_type": "automatic",
            "status": "completed"
        }
        
        # Get existing sync history from loaded metadata  
        existing_history = self.existing_metadata.get("sync_history", [])
        
        # Check if this exact sync already exists (avoid duplicates)
        if not any(entry.get("commit_sha") == self.commit_sha and 
                  entry.get("timestamp") == self.timestamp 
                  for entry in existing_history):
            existing_history.append(history_entry)
            print(f"➕ Added new sync record for commit {self.commit_sha}")
        else:
            print(f"⏭️  Sync record already exists for commit {self.commit_sha}")
            
        # Keep only last 20 sync records (increased from 10 for better history)
        self.sync_history = existing_history[-20:]
        
        print(f"📈 Updated sync history: {len(self.sync_history)} total records")
    
    def generate_content_index(self):
        """Generate a comprehensive content index."""
        index = {
            "generated_at": self.timestamp,
            "structure": {},
            "quick_access": {
                "latest_ontologies": [],
                "latest_parsings": [],
                "vector_files": [],
                "graph_files": []
            },
            "search_index": []
        }
        
        # Build structure index
        main_dirs = ["ontologies", "parsings", "vectors", "graphs"]
        
        for main_dir in main_dirs:
            dir_path = self.background_dir / main_dir
            if dir_path.exists():
                index["structure"][main_dir] = self.build_directory_index(dir_path)
        
        # Build quick access lists
        self.build_quick_access_index(index)
        
        # Build search index
        self.build_search_index(index)
        
        # Save content index
        index_file = self.background_dir / "content_index.json"
        with open(index_file, 'w', encoding='utf-8') as f:
            json.dump(index, f, indent=2, ensure_ascii=False)
        
        print(f"🔍 Generated content index with {len(index['search_index'])} searchable items")
    
    def build_directory_index(self, directory: Path) -> Dict[str, Any]:
        """Build index for a directory."""
        index = {
            "files": [],
            "subdirectories": {}
        }
        
        for item in directory.iterdir():
            if item.is_file():
                file_info = {
                    "name": item.name,
                    "path": str(item.relative_to(self.background_dir)),
                    "size": item.stat().st_size,
                    "modified": datetime.fromtimestamp(item.stat().st_mtime).isoformat() + 'Z',
                    "type": item.suffix.lower() or "no_extension"
                }
                index["files"].append(file_info)
            
            elif item.is_dir():
                index["subdirectories"][item.name] = self.build_directory_index(item)
        
        return index
    
    def build_quick_access_index(self, index: Dict[str, Any]):
        """Build quick access references."""
        # Find latest files in each category
        for main_dir in ["ontologies", "parsings", "vectors", "graphs"]:
            if main_dir in index["structure"]:
                files = self.collect_all_files(index["structure"][main_dir])
                
                # Sort by modification time (most recent first)
                files.sort(key=lambda x: x["modified"], reverse=True)
                
                # Add to quick access
                key_name = f"latest_{main_dir}"
                index["quick_access"][key_name] = files[:5]  # Top 5 most recent
        
        # Specific file type shortcuts
        all_files = []
        for main_dir in index["structure"].values():
            all_files.extend(self.collect_all_files(main_dir))
        
        # Vector files
        index["quick_access"]["vector_files"] = [
            f for f in all_files 
            if any(keyword in f["name"].lower() 
                   for keyword in ["embedding", "vector", "tfidf"])
        ]
        
        # Graph files
        index["quick_access"]["graph_files"] = [
            f for f in all_files 
            if any(keyword in f["name"].lower() 
                   for keyword in ["graph", "relationship", "cypher"])
        ]
    
    def collect_all_files(self, directory_index: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Recursively collect all files from directory index."""
        files = directory_index.get("files", []).copy()
        
        for subdir_index in directory_index.get("subdirectories", {}).values():
            files.extend(self.collect_all_files(subdir_index))
        
        return files
    
    def build_search_index(self, index: Dict[str, Any]):
        """Build searchable content index."""
        search_items = []
        
        # Index all files
        for main_dir, dir_index in index["structure"].items():
            files = self.collect_all_files(dir_index)
            
            for file_info in files:
                search_item = {
                    "title": file_info["name"],
                    "path": file_info["path"],
                    "category": main_dir,
                    "type": "file",
                    "keywords": self.extract_keywords(file_info["name"]),
                    "size": file_info["size"],
                    "modified": file_info["modified"]
                }
                
                # Add content-based keywords if JSON file
                if file_info["type"] == ".json":
                    content_keywords = self.extract_content_keywords(
                        self.background_dir / file_info["path"]
                    )
                    search_item["keywords"].extend(content_keywords)
                
                search_items.append(search_item)
        
        index["search_index"] = search_items
    
    def extract_keywords(self, filename: str) -> List[str]:
        """Extract keywords from filename."""
        import re
        
        # Remove extension and split on common separators
        name_without_ext = filename.rsplit('.', 1)[0]
        keywords = re.split(r'[_\-\s]+', name_without_ext.lower())
        
        # Filter out very short keywords
        keywords = [kw for kw in keywords if len(kw) > 2]
        
        return keywords
    
    def extract_content_keywords(self, file_path: Path) -> List[str]:
        """Extract keywords from JSON content."""
        try:
            if not file_path.exists():
                return []
            
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            keywords = set()
            
            def extract_from_obj(obj):
                if isinstance(obj, dict):
                    for key, value in obj.items():
                        keywords.add(key.lower())
                        if isinstance(value, str) and len(value) < 50:
                            keywords.add(value.lower())
                        extract_from_obj(value)
                elif isinstance(obj, list):
                    for item in obj:
                        extract_from_obj(item)
                elif isinstance(obj, str) and len(obj) < 30:
                    keywords.add(obj.lower())
            
            extract_from_obj(data)
            
            # Filter and clean keywords
            valid_keywords = []
            for kw in keywords:
                if isinstance(kw, str) and 3 <= len(kw) <= 20 and kw.isalnum():
                    valid_keywords.append(kw)
            
            return valid_keywords[:20]  # Limit to top 20 keywords
            
        except Exception as e:
            print(f"⚠️  Error extracting keywords from {file_path}: {e}")
            return []
    
    def update_configuration(self):
        """Update configuration files."""
        config = {
            "background_system": {
                "version": "1.0.0",
                "last_updated": self.timestamp,
                "axes": {
                    "ontologies": {
                        "enabled": True,
                        "description": "Conceptual frameworks and taxonomies",
                        "processing": ["extraction", "categorization", "hierarchies"]
                    },
                    "parsings": {
                        "enabled": True,
                        "description": "Structured content analysis",
                        "processing": ["markdown", "yaml", "text_extraction"]
                    },
                    "vectors": {
                        "enabled": True,
                        "description": "Semantic representations",
                        "processing": ["tfidf", "embeddings", "similarity_matrices"]
                    },
                    "graphs": {
                        "enabled": True,
                        "description": "Knowledge relationships",
                        "processing": ["entity_extraction", "relationship_mapping", "graph_formats"]
                    }
                }
            },
            "sync_configuration": {
                "docs_repository": self.docs_repo,
                "trigger_events": ["repository_dispatch", "workflow_dispatch"],
                "auto_processing": True,
                "output_formats": ["json", "cypher", "graphml"],
                "retention": {
                    "sync_history_records": 10,
                    "max_file_age_days": 90
                }
            },
            "integration": {
                "landing_page": {
                    "context_injection": True,
                    "search_integration": True,
                    "semantic_enhancement": True
                },
                "api_endpoints": {
                    "content_search": "/api/background/search",
                    "concept_lookup": "/api/background/concepts",
                    "graph_query": "/api/background/graph"
                }
            }
        }
        
        config_file = self.background_dir / "config.json"
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        
        print(f"⚙️  Updated system configuration")


def main():
    parser = argparse.ArgumentParser(description='Update content metadata and synchronization info')
    parser.add_argument('--background-dir', required=True, help='Background directory path')
    parser.add_argument('--commit-sha', required=True, help='Current commit SHA')
    parser.add_argument('--docs-repo', required=True, help='Source docs repository')
    
    args = parser.parse_args()
    
    updater = MetadataUpdater(args.background_dir, args.commit_sha, args.docs_repo)
    updater.update_all()


if __name__ == "__main__":
    main()