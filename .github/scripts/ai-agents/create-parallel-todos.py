#!/usr/bin/env python3
"""
Create parallel todo lists for quality auditing
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

def create_parallel_todos(audit_dir, output_dir, categories):
    """Create categorized todo lists for quality improvements"""
    print("📋 Creating parallel todo lists...")
    
    audit_path = Path(audit_dir)
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Load audit results
    audit_file = audit_path / "quality_audit.json"
    audit_data = {}
    
    if audit_file.exists():
        with open(audit_file, 'r') as f:
            audit_data = json.load(f)
    
    # Define categories
    category_list = categories.split(',') if categories else [
        'security', 'performance', 'accessibility', 'seo', 'maintainability'
    ]
    
    todo_lists = {}
    
    for category in category_list:
        todo_lists[category] = {
            "title": category.replace('_', ' ').title(),
            "items": [],
            "priority": "medium",
            "estimated_effort": "2-4 hours"
        }
    
    # Extract issues from audit
    if "detailed_analysis" in audit_data:
        analysis = audit_data["detailed_analysis"]
        
        # Security issues
        security_issues = analysis.get("security_issues", [])
        todo_lists["security"]["items"].extend(security_issues)
        if security_issues:
            todo_lists["security"]["priority"] = "high"
        
        # Performance issues
        performance_issues = analysis.get("performance_issues", [])
        todo_lists["performance"]["items"].extend(performance_issues)
        
        # Accessibility issues
        accessibility_issues = analysis.get("accessibility_issues", [])
        todo_lists["accessibility"]["items"].extend(accessibility_issues)
        
        # SEO improvements (from recommendations)
        seo_recommendations = [
            item for item in audit_data.get("recommended_improvements", [])
            if "seo" in item.lower() or "meta" in item.lower() or "search" in item.lower()
        ]
        todo_lists["seo"]["items"].extend(seo_recommendations)
        
        # Maintainability improvements
        maintainability_items = [
            item for item in audit_data.get("recommended_improvements", [])
            if "test" in item.lower() or "document" in item.lower() or "refactor" in item.lower()
        ]
        todo_lists["maintainability"]["items"].extend(maintainability_items)
    
    # Create individual todo files
    for category, todo_data in todo_lists.items():
        todo_file = output_path / f"{category}_todos.md"
        
        with open(todo_file, 'w') as f:
            f.write(f"# {todo_data['title']} Todo List\n\n")
            f.write(f"**Category**: {category.title()}\n")
            f.write(f"**Priority**: {todo_data['priority']}\n")
            f.write(f"**Estimated Effort**: {todo_data['estimated_effort']}\n")
            f.write(f"**Items**: {len(todo_data['items'])}\n")
            f.write(f"**Created**: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}\n\n")
            
            if todo_data['items']:
                f.write("## Tasks\n\n")
                for i, item in enumerate(todo_data['items'], 1):
                    f.write(f"### {i}. {item}\n\n")
                    f.write("**Steps:**\n")
                    f.write("- [ ] Analyze the issue\n")
                    f.write("- [ ] Research solutions\n")
                    f.write("- [ ] Implement fix\n")
                    f.write("- [ ] Test thoroughly\n")
                    f.write("- [ ] Document changes\n")
                    f.write("- [ ] Code review\n\n")
                    
                    f.write("**Acceptance Criteria:**\n")
                    f.write("- [ ] Issue is resolved\n")
                    f.write("- [ ] No regressions introduced\n")
                    f.write("- [ ] Tests pass\n")
                    f.write("- [ ] Documentation updated\n\n")
                    
                    f.write("---\n\n")
            else:
                f.write("## ✅ No issues found in this category!\n\n")
                f.write("This category has passed all quality checks.\n")
    
    # Create master checklist
    master_file = output_path / "master_checklist.md"
    with open(master_file, 'w') as f:
        f.write("# Master Quality Checklist\n\n")
        f.write(f"**Generated**: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}\n")
        f.write(f"**Overall Score**: {audit_data.get('overall_score', 'N/A')}/100\n")
        f.write(f"**Approval Status**: {audit_data.get('approval_status', 'pending')}\n\n")
        
        # Critical issues
        critical_issues = audit_data.get("critical_issues", [])
        if critical_issues:
            f.write("## 🚨 Critical Issues (Must Fix Before Deployment)\n\n")
            for issue in critical_issues:
                f.write(f"- [ ] **CRITICAL**: {issue}\n")
            f.write("\n")
        
        # Category summaries
        f.write("## 📋 Category Summaries\n\n")
        for category, todo_data in todo_lists.items():
            item_count = len(todo_data['items'])
            status = "✅ PASS" if item_count == 0 else f"⚠️ {item_count} items"
            f.write(f"- **{todo_data['title']}**: {status}\n")
        
        f.write("\n## 🎯 Recommended Improvements\n\n")
        for improvement in audit_data.get("recommended_improvements", []):
            f.write(f"- [ ] {improvement}\n")
        
        f.write("\n## 🚀 Next Steps\n\n")
        for step in audit_data.get("next_steps", []):
            f.write(f"- [ ] {step}\n")
        
        # Deployment checklist
        f.write("\n## 🚢 Deployment Checklist\n\n")
        f.write("- [ ] All critical issues resolved\n")
        f.write("- [ ] Quality score above threshold\n")
        f.write("- [ ] Manual testing completed\n")
        f.write("- [ ] Performance testing passed\n")
        f.write("- [ ] Accessibility testing passed\n")
        f.write("- [ ] Security review completed\n")
        f.write("- [ ] Documentation updated\n")
        f.write("- [ ] Backup created\n")
        f.write("- [ ] Rollback plan ready\n")
        f.write("- [ ] Stakeholder approval obtained\n")
    
    # Create summary report
    summary_file = output_path / "summary.json"
    summary_data = {
        "timestamp": datetime.utcnow().isoformat(),
        "categories": category_list,
        "total_items": sum(len(todo_data['items']) for todo_data in todo_lists.values()),
        "critical_issues": len(audit_data.get("critical_issues", [])),
        "overall_score": audit_data.get("overall_score", 0),
        "approval_status": audit_data.get("approval_status", "pending"),
        "category_breakdown": {
            category: len(todo_data['items']) 
            for category, todo_data in todo_lists.items()
        }
    }
    
    with open(summary_file, 'w') as f:
        json.dump(summary_data, f, indent=2)
    
    print(f"✅ Parallel todo lists created!")
    print(f"Categories: {len(category_list)}")
    print(f"Total items: {summary_data['total_items']}")
    print(f"Critical issues: {summary_data['critical_issues']}")
    
    return summary_data

def main():
    parser = argparse.ArgumentParser(description="Create parallel todo lists for quality auditing")
    parser.add_argument("--audit-dir", required=True, help="Audit results directory")
    parser.add_argument("--output", required=True, help="Output directory for todo lists")
    parser.add_argument("--categories", required=True, help="Comma-separated list of categories")
    
    args = parser.parse_args()
    
    result = create_parallel_todos(args.audit_dir, args.output, args.categories)
    
    return 0 if result else 1

if __name__ == "__main__":
    sys.exit(main())