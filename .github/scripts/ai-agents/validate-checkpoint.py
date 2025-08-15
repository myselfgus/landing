#!/usr/bin/env python3
"""
Validate checkpoint integrity
"""

import argparse
import json
import sys
from pathlib import Path

def validate_checkpoint(checkpoint_file, expected_checksum):
    """Validate checkpoint integrity"""
    print(f"🔍 Validating checkpoint: {checkpoint_file}")
    
    try:
        checkpoint_path = Path(checkpoint_file)
        if not checkpoint_path.exists():
            print(f"❌ Checkpoint file not found: {checkpoint_file}")
            return False
            
        with open(checkpoint_path, 'r') as f:
            checkpoint = json.load(f)
        
        actual_checksum = checkpoint.get("content_checksum", "")
        
        if expected_checksum and actual_checksum != expected_checksum:
            print(f"❌ Checkpoint validation failed!")
            print(f"Expected: {expected_checksum}")
            print(f"Actual: {actual_checksum}")
            return False
        
        print(f"✅ Checkpoint validation successful!")
        print(f"Agent: {checkpoint.get('agent', 'unknown')}")
        print(f"Files: {checkpoint.get('total_files', 0)}")
        print(f"Checksum: {actual_checksum}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error validating checkpoint: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description="Validate AI agent checkpoint")
    parser.add_argument("--checkpoint", required=True, help="Checkpoint file to validate")
    parser.add_argument("--expected-checksum", help="Expected checksum value")
    
    args = parser.parse_args()
    
    result = validate_checkpoint(args.checkpoint, args.expected_checksum)
    
    return 0 if result else 1

if __name__ == "__main__":
    sys.exit(main())