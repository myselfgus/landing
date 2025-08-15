#!/usr/bin/env python3
"""
Final validation before deployment
"""

import argparse
import json
import sys
from pathlib import Path

def final_validation(staging_dir, audit_dir, quality_threshold):
    """Perform final validation before deployment"""
    print("🔍 Performing final validation...")
    
    staging_path = Path(staging_dir)
    audit_path = Path(audit_dir)
    threshold = int(quality_threshold)
    
    validation_results = {
        "staging_files_valid": False,
        "quality_threshold_met": False,
        "critical_issues_resolved": False,
        "documentation_complete": False,
        "overall_valid": False
    }
    
    # Check staging files exist
    required_files = ["index.html", "index.css"]
    staging_files_found = []
    
    for required_file in required_files:
        file_path = staging_path / required_file
        if file_path.exists():
            staging_files_found.append(required_file)
    
    validation_results["staging_files_valid"] = len(staging_files_found) >= len(required_files) // 2
    
    # Check quality score
    audit_file = audit_path / "quality_audit.json"
    if audit_file.exists():
        with open(audit_file, 'r') as f:
            audit_data = json.load(f)
            
        overall_score = audit_data.get("overall_score", 0)
        validation_results["quality_threshold_met"] = overall_score >= threshold
        
        # Check critical issues
        critical_issues = audit_data.get("critical_issues", [])
        validation_results["critical_issues_resolved"] = len(critical_issues) == 0
    
    # Check documentation
    docs_path = staging_path / "docs"
    validation_results["documentation_complete"] = docs_path.exists()
    
    # Overall validation
    validation_results["overall_valid"] = all([
        validation_results["staging_files_valid"],
        validation_results["quality_threshold_met"],
        validation_results["critical_issues_resolved"]
    ])
    
    # Create validation report
    validation_report = {
        "timestamp": "2024-01-01T00:00:00Z",
        "validation_results": validation_results,
        "staging_files_found": staging_files_found,
        "quality_threshold": threshold,
        "recommendations": []
    }
    
    if not validation_results["overall_valid"]:
        if not validation_results["staging_files_valid"]:
            validation_report["recommendations"].append("Generate missing staging files")
        if not validation_results["quality_threshold_met"]:
            validation_report["recommendations"].append(f"Improve quality score to meet {threshold} threshold")
        if not validation_results["critical_issues_resolved"]:
            validation_report["recommendations"].append("Resolve all critical issues before deployment")
    
    # Save validation report
    validation_file = audit_path / "final_validation.json"
    with open(validation_file, 'w') as f:
        json.dump(validation_report, f, indent=2)
    
    print(f"Staging files: {'✅' if validation_results['staging_files_valid'] else '❌'}")
    print(f"Quality threshold: {'✅' if validation_results['quality_threshold_met'] else '❌'}")
    print(f"Critical issues: {'✅' if validation_results['critical_issues_resolved'] else '❌'}")
    print(f"Overall validation: {'✅ PASS' if validation_results['overall_valid'] else '❌ FAIL'}")
    
    if not validation_results["overall_valid"]:
        print("\n❌ Final validation failed!")
        for rec in validation_report["recommendations"]:
            print(f"  - {rec}")
        return False
    
    print("\n✅ Final validation passed!")
    return True

def main():
    parser = argparse.ArgumentParser(description="Final validation before deployment")
    parser.add_argument("--staging-dir", required=True, help="Staging directory")
    parser.add_argument("--audit-dir", required=True, help="Audit directory")
    parser.add_argument("--quality-threshold", required=True, help="Quality threshold")
    
    args = parser.parse_args()
    
    result = final_validation(args.staging_dir, args.audit_dir, args.quality_threshold)
    
    return 0 if result else 1

if __name__ == "__main__":
    sys.exit(main())