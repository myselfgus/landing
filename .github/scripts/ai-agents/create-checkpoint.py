#!/usr/bin/env python3
"""
Create and validate checkpoints between AI agents
"""

import argparse
import json
import sys
import hashlib
from datetime import datetime
from pathlib import Path

def create_checkpoint(agent, output_path, checksum_file):
    """Create validation checkpoint"""
    print(f"🔒 Creating checkpoint for {agent} agent...")
    
    output_path = Path(output_path)
    
    # Calculate checksum of all files in output directory
    files_data = {}
    total_content = ""
    
    for file_path in output_path.rglob("*"):
        if file_path.is_file() and not file_path.name.startswith('.'):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    relative_path = file_path.relative_to(output_path)
                    files_data[str(relative_path)] = {
                        "size": len(content),
                        "checksum": hashlib.sha256(content.encode()).hexdigest()
                    }
                    total_content += content
            except:
                # Skip binary files
                pass
    
    # Create checkpoint data
    checkpoint = {
        "agent": agent,
        "timestamp": datetime.utcnow().isoformat(),
        "files": files_data,
        "total_files": len(files_data),
        "content_checksum": hashlib.sha256(total_content.encode()).hexdigest(),
        "status": "completed"
    }
    
    # Save checkpoint
    checkpoint_path = Path(checksum_file)
    with open(checkpoint_path, 'w') as f:
        json.dump(checkpoint, f, indent=2)
    
    print(f"✅ Checkpoint created: {checkpoint['content_checksum']}")
    print(f"Files included: {len(files_data)}")
    
    return checkpoint["content_checksum"]

def validate_checkpoint(checkpoint_file, expected_checksum):
    """Validate checkpoint integrity"""
    print(f"🔍 Validating checkpoint...")
    
    try:
        with open(checkpoint_file, 'r') as f:
            checkpoint = json.load(f)
        
        actual_checksum = checkpoint["content_checksum"]
        
        if expected_checksum and actual_checksum != expected_checksum:
            print(f"❌ Checkpoint validation failed!")
            print(f"Expected: {expected_checksum}")
            print(f"Actual: {actual_checksum}")
            return False
        
        print(f"✅ Checkpoint validation successful!")
        print(f"Agent: {checkpoint['agent']}")
        print(f"Files: {checkpoint['total_files']}")
        print(f"Checksum: {actual_checksum}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error validating checkpoint: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description="Create and validate AI agent checkpoints")
    parser.add_argument("--agent", help="Agent name")
    parser.add_argument("--output", help="Output directory to checkpoint")
    parser.add_argument("--checksum-file", help="Checkpoint file path")
    parser.add_argument("--checkpoint", help="Checkpoint file to validate")
    parser.add_argument("--expected-checksum", help="Expected checksum value")
    
    args = parser.parse_args()
    
    # Auto-detect operation based on arguments
    if args.agent and args.output and args.checksum_file:
        # Create checkpoint
        result = create_checkpoint(args.agent, args.output, args.checksum_file)
        return 0 if result else 1
    elif args.checkpoint:
        # Validate checkpoint
        result = validate_checkpoint(args.checkpoint, args.expected_checksum)
        return 0 if result else 1
    else:
        parser.print_help()
        return 1

if __name__ == "__main__":
    sys.exit(main())