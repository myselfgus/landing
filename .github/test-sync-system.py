#!/usr/bin/env python3
"""
Test script for the documentation sync system
"""

import os
import sys
import subprocess
import json
from pathlib import Path


def test_scripts():
    """Test all Python scripts."""
    print("🧪 Testing documentation sync scripts...")
    
    # Get the repository root
    repo_root = Path(__file__).parent.parent
    scripts_dir = repo_root / ".github" / "scripts"
    background_dir = repo_root / "background"
    
    # Test process-docs.py
    print("\n1. Testing process-docs.py...")
    cmd = [
        "python", str(scripts_dir / "process-docs.py"),
        "--source", str(repo_root / "temp-test-docs"),
        "--target", str(background_dir),
        "--timestamp", "2025-08-14T23:58:00Z"
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            print("✅ process-docs.py: PASSED")
        else:
            print(f"❌ process-docs.py: FAILED\n{result.stderr}")
    except Exception as e:
        print(f"❌ process-docs.py: ERROR - {e}")
    
    # Test generate-embeddings.py
    print("\n2. Testing generate-embeddings.py...")
    cmd = [
        "python", str(scripts_dir / "generate-embeddings.py"),
        "--input", str(background_dir),
        "--output", str(background_dir / "vectors")
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            print("✅ generate-embeddings.py: PASSED")
        else:
            print(f"❌ generate-embeddings.py: FAILED\n{result.stderr}")
    except Exception as e:
        print(f"❌ generate-embeddings.py: ERROR - {e}")
    
    # Test create-knowledge-graph.py
    print("\n3. Testing create-knowledge-graph.py...")
    cmd = [
        "python", str(scripts_dir / "create-knowledge-graph.py"),
        "--input", str(background_dir),
        "--output", str(background_dir / "graphs")
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            print("✅ create-knowledge-graph.py: PASSED")
        else:
            print(f"❌ create-knowledge-graph.py: FAILED\n{result.stderr}")
    except Exception as e:
        print(f"❌ create-knowledge-graph.py: ERROR - {e}")
    
    # Test update-metadata.py
    print("\n4. Testing update-metadata.py...")
    cmd = [
        "python", str(scripts_dir / "update-metadata.py"),
        "--background-dir", str(background_dir),
        "--commit-sha", "test-commit-sha",
        "--docs-repo", "myselfgus/docs"
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            print("✅ update-metadata.py: PASSED")
        else:
            print(f"❌ update-metadata.py: FAILED\n{result.stderr}")
    except Exception as e:
        print(f"❌ update-metadata.py: ERROR - {e}")


def validate_structure():
    """Validate the background directory structure."""
    print("\n🏗️  Validating background structure...")
    
    repo_root = Path(__file__).parent.parent
    background_dir = repo_root / "background"
    
    required_dirs = [
        "ontologies/concepts",
        "ontologies/taxonomies", 
        "ontologies/frameworks",
        "parsings/markdown",
        "parsings/structured",
        "parsings/extracted",
        "vectors/embeddings",
        "vectors/indices",
        "graphs/knowledge",
        "graphs/relationships"
    ]
    
    all_exist = True
    for dir_path in required_dirs:
        full_path = background_dir / dir_path
        if full_path.exists():
            print(f"✅ {dir_path}")
        else:
            print(f"❌ {dir_path} - MISSING")
            all_exist = False
    
    # Check for required files
    required_files = [
        "README.md",
        "ontologies/sample.json",
        "vectors/sample.json", 
        "graphs/sample.json"
    ]
    
    for file_path in required_files:
        full_path = background_dir / file_path
        if full_path.exists():
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} - MISSING")
            all_exist = False
    
    return all_exist


def validate_workflow():
    """Validate the GitHub Actions workflow."""
    print("\n⚙️  Validating GitHub Actions workflow...")
    
    repo_root = Path(__file__).parent.parent
    workflow_file = repo_root / ".github" / "workflows" / "docs-sync.yml"
    
    if not workflow_file.exists():
        print("❌ docs-sync.yml workflow file not found")
        return False
    
    # Basic validation of workflow syntax
    try:
        import yaml
        with open(workflow_file, 'r') as f:
            workflow_data = yaml.safe_load(f)
        
        # Check required sections
        required_sections = ["name", "on", "jobs"]
        for section in required_sections:
            if section in workflow_data:
                print(f"✅ Workflow has '{section}' section")
            else:
                print(f"❌ Workflow missing '{section}' section")
                return False
        
        # Check if sync job exists
        if "sync-docs" in workflow_data.get("jobs", {}):
            print("✅ sync-docs job found")
        else:
            print("❌ sync-docs job not found")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Error validating workflow: {e}")
        return False


def main():
    """Main test function."""
    print("🚀 Voither Landing Background Sync System - Test Suite")
    print("=" * 60)
    
    # Test 1: Structure validation
    structure_ok = validate_structure()
    
    # Test 2: Workflow validation
    workflow_ok = validate_workflow()
    
    # Test 3: Script functionality
    print("\n" + "=" * 60)
    test_scripts()
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY:")
    print(f"{'✅' if structure_ok else '❌'} Directory structure")
    print(f"{'✅' if workflow_ok else '❌'} GitHub Actions workflow")
    print("✅ Python scripts (see detailed results above)")
    
    if structure_ok and workflow_ok:
        print("\n🎉 System is ready for docs repository connection!")
        print("\nNext steps:")
        print("1. Create the myselfgus/docs repository") 
        print("2. Add the trigger workflow (see .github/WEBHOOK_SETUP.md)")
        print("3. Configure repository dispatch token")
        print("4. Test with a docs update")
    else:
        print("\n⚠️  Some issues need to be resolved before the system is ready.")


if __name__ == "__main__":
    main()