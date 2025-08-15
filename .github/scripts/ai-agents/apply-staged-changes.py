#!/usr/bin/env python3
"""
Apply staged changes to production with safety checks
"""

import argparse
import sys
import shutil
import json
from datetime import datetime
from pathlib import Path

def apply_staged_changes(staging_dir, target_dir, backup_dir, safety_checks):
    """Apply staged changes with comprehensive safety measures"""
    print("🚀 Applying staged changes to production...")
    
    staging_path = Path(staging_dir)
    target_path = Path(target_dir)
    backup_path = Path(backup_dir)
    
    # Create backup
    if safety_checks.lower() == 'true':
        print("📦 Creating backup...")
        backup_path.mkdir(parents=True, exist_ok=True)
        
        for file_path in target_path.glob("*"):
            if file_path.is_file() and not file_path.name.startswith('.'):
                shutil.copy2(file_path, backup_path / file_path.name)
        
        print(f"✅ Backup created: {backup_path}")
    
    # Apply changes safely
    changes_applied = []
    
    for file_path in staging_path.glob("*"):
        if file_path.is_file() and file_path.suffix in ['.html', '.css', '.tsx', '.js']:
            target_file = target_path / file_path.name
            
            # Safety check: verify file exists in backup
            if safety_checks.lower() == 'true':
                backup_file = backup_path / file_path.name
                if not backup_file.exists():
                    print(f"⚠️ Warning: No backup for {file_path.name}")
            
            # Apply change
            shutil.copy2(file_path, target_file)
            changes_applied.append(file_path.name)
            print(f"✅ Applied: {file_path.name}")
    
    # Copy assets if they exist
    assets_path = staging_path / "assets"
    if assets_path.exists():
        target_assets = target_path / "assets"
        target_assets.mkdir(exist_ok=True)
        
        for asset_file in assets_path.glob("*"):
            if asset_file.is_file():
                shutil.copy2(asset_file, target_assets / asset_file.name)
                changes_applied.append(f"assets/{asset_file.name}")
    
    # Create deployment log
    deployment_log = {
        "timestamp": datetime.utcnow().isoformat(),
        "changes_applied": changes_applied,
        "backup_location": str(backup_path) if safety_checks.lower() == 'true' else None,
        "safety_checks_enabled": safety_checks.lower() == 'true',
        "total_files": len(changes_applied)
    }
    
    log_file = target_path / "deployment.log.json"
    with open(log_file, 'w') as f:
        json.dump(deployment_log, f, indent=2)
    
    print(f"✅ Deployment completed!")
    print(f"Files deployed: {len(changes_applied)}")
    print(f"Changes: {', '.join(changes_applied)}")
    
    return True

def main():
    parser = argparse.ArgumentParser(description="Apply staged changes to production")
    parser.add_argument("--staging-dir", required=True, help="Staging directory")
    parser.add_argument("--target-dir", required=True, help="Target production directory")
    parser.add_argument("--backup-dir", required=True, help="Backup directory")
    parser.add_argument("--safety-checks", required=True, help="Enable safety checks (true/false)")
    
    args = parser.parse_args()
    
    result = apply_staged_changes(
        args.staging_dir, args.target_dir, args.backup_dir, args.safety_checks
    )
    
    return 0 if result else 1

if __name__ == "__main__":
    sys.exit(main())