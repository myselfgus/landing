#!/usr/bin/env python3
"""
Sync latest docs knowledge from the docs repository
"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path

try:
    import requests
    import yaml
except ImportError as e:
    print(f"Missing required package: {e}")
    sys.exit(1)

def sync_docs_knowledge(docs_repo, output_path, timestamp):
    """Sync latest knowledge from docs repository"""
    print(f"🔄 Syncing knowledge from {docs_repo}...")
    
    output_path = Path(output_path)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # GitHub API base URL
    api_base = "https://api.github.com"
    
    try:
        # Get repository contents
        response = requests.get(f"{api_base}/repos/{docs_repo}/contents")
        
        if response.status_code == 200:
            contents = response.json()
            
            knowledge_base = {
                "timestamp": timestamp,
                "source_repo": docs_repo,
                "files": {},
                "summary": {
                    "total_files": 0,
                    "markdown_files": 0,
                    "total_size": 0
                }
            }
            
            # Process each file
            for item in contents:
                if item["type"] == "file" and item["name"].endswith(('.md', '.txt', '.json')):
                    file_response = requests.get(item["download_url"])
                    
                    if file_response.status_code == 200:
                        content = file_response.text
                        
                        knowledge_base["files"][item["name"]] = {
                            "content": content,
                            "size": len(content),
                            "path": item["path"],
                            "last_modified": item.get("last_modified", ""),
                            "sha": item["sha"]
                        }
                        
                        knowledge_base["summary"]["total_files"] += 1
                        knowledge_base["summary"]["total_size"] += len(content)
                        
                        if item["name"].endswith('.md'):
                            knowledge_base["summary"]["markdown_files"] += 1
            
            # Save knowledge base
            knowledge_file = output_path / "docs_knowledge.json"
            with open(knowledge_file, 'w') as f:
                json.dump(knowledge_base, f, indent=2)
            
            # Create summary report
            summary_file = output_path / "sync_summary.md"
            with open(summary_file, 'w') as f:
                f.write(f"# Docs Knowledge Sync Report\n\n")
                f.write(f"**Timestamp**: {timestamp}\n")
                f.write(f"**Source Repository**: {docs_repo}\n")
                f.write(f"**Total Files**: {knowledge_base['summary']['total_files']}\n")
                f.write(f"**Markdown Files**: {knowledge_base['summary']['markdown_files']}\n")
                f.write(f"**Total Size**: {knowledge_base['summary']['total_size']:,} bytes\n\n")
                
                f.write("## Files Synced:\n\n")
                for filename, file_data in knowledge_base["files"].items():
                    f.write(f"- **{filename}**: {file_data['size']:,} bytes\n")
            
            print(f"✅ Knowledge sync completed!")
            print(f"Files synced: {knowledge_base['summary']['total_files']}")
            print(f"Total size: {knowledge_base['summary']['total_size']:,} bytes")
            
            return knowledge_base
            
        else:
            print(f"❌ Failed to access repository: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ Error syncing docs knowledge: {e}")
        return None

def main():
    parser = argparse.ArgumentParser(description="Sync docs knowledge for AI agents")
    parser.add_argument("--docs-repo", required=True, help="Docs repository (owner/repo)")
    parser.add_argument("--output", required=True, help="Output directory for knowledge base")
    parser.add_argument("--timestamp", required=True, help="Sync timestamp")
    
    args = parser.parse_args()
    
    result = sync_docs_knowledge(args.docs_repo, args.output, args.timestamp)
    
    return 0 if result else 1

if __name__ == "__main__":
    sys.exit(main())