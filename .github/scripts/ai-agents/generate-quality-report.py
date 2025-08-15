#!/usr/bin/env python3
"""
Generate quality report with visual dashboard
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

def generate_quality_report(audit_dir, output_file, format_types):
    """Generate comprehensive quality report"""
    print("📊 Generating quality report...")
    
    audit_path = Path(audit_dir)
    output_path = Path(output_file)
    
    # Load audit data
    audit_file = audit_path / "quality_audit.json"
    audit_data = {}
    
    if audit_file.exists():
        with open(audit_file, 'r') as f:
            audit_data = json.load(f)
    
    formats = format_types.split(',')
    
    # Generate HTML report
    if 'html' in formats:
        html_content = generate_html_report(audit_data)
        html_file = output_path.parent / f"{output_path.stem}.html"
        with open(html_file, 'w') as f:
            f.write(html_content)
        print(f"✅ HTML report: {html_file}")
    
    # Generate JSON report
    if 'json' in formats:
        json_file = output_path.parent / f"{output_path.stem}.json"
        with open(json_file, 'w') as f:
            json.dump(audit_data, f, indent=2)
        print(f"✅ JSON report: {json_file}")
    
    # Generate Markdown report
    if 'markdown' in formats:
        markdown_content = generate_markdown_report(audit_data)
        md_file = output_path.parent / f"{output_path.stem}.md"
        with open(md_file, 'w') as f:
            f.write(markdown_content)
        print(f"✅ Markdown report: {md_file}")
    
    return True

def generate_html_report(audit_data):
    """Generate interactive HTML quality report"""
    overall_score = audit_data.get('overall_score', 0)
    category_scores = audit_data.get('category_scores', {})
    
    # Determine score color
    if overall_score >= 90:
        score_color = "#4CAF50"  # Green
    elif overall_score >= 70:
        score_color = "#FF9800"  # Orange
    else:
        score_color = "#F44336"  # Red
    
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Agents Quality Report</title>
    <style>
        * {{ box-sizing: border-box; }}
        body {{ 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            margin: 0; padding: 20px; background: #f5f5f5; color: #333;
        }}
        .container {{ max-width: 1200px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        .header {{ text-align: center; margin-bottom: 40px; }}
        .score-circle {{ 
            width: 150px; height: 150px; border-radius: 50%; 
            background: conic-gradient({score_color} {overall_score * 3.6}deg, #e0e0e0 0deg);
            display: flex; align-items: center; justify-content: center;
            margin: 20px auto; position: relative;
        }}
        .score-circle::before {{
            content: ''; width: 120px; height: 120px; border-radius: 50%;
            background: white; position: absolute;
        }}
        .score-text {{ 
            font-size: 2.5em; font-weight: bold; color: {score_color}; z-index: 1;
        }}
        .categories {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin: 30px 0; }}
        .category-card {{ 
            background: #fafafa; padding: 20px; border-radius: 8px; border-left: 4px solid #2196F3;
        }}
        .category-score {{ 
            font-size: 1.5em; font-weight: bold; color: #2196F3; margin-bottom: 10px;
        }}
        .issues-section {{ margin: 30px 0; }}
        .issue-item {{ 
            background: #fff3cd; padding: 15px; margin: 10px 0; border-radius: 5px; border-left: 4px solid #ffc107;
        }}
        .critical-issue {{ 
            background: #f8d7da; border-left-color: #dc3545;
        }}
        .recommendation {{ 
            background: #d4edda; border-left-color: #28a745;
        }}
        .status-badge {{ 
            display: inline-block; padding: 5px 10px; border-radius: 15px; font-size: 0.8em; font-weight: bold;
        }}
        .approved {{ background: #28a745; color: white; }}
        .conditional {{ background: #ffc107; color: black; }}
        .rejected {{ background: #dc3545; color: white; }}
        .timestamp {{ color: #666; font-size: 0.9em; text-align: center; margin-top: 30px; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🤖 AI Agents Quality Report</h1>
            <p>Comprehensive analysis by the AI Agents Collaborative System</p>
            
            <div class="score-circle">
                <div class="score-text">{overall_score}</div>
            </div>
            
            <span class="status-badge {audit_data.get('approval_status', 'pending')}">
                {audit_data.get('approval_status', 'pending').upper()}
            </span>
        </div>
        
        <div class="categories">"""
    
    for category, score in category_scores.items():
        html_content += f"""
            <div class="category-card">
                <div class="category-score">{score}/100</div>
                <h3>{category.replace('_', ' ').title()}</h3>
                <div style="width: 100%; height: 10px; background: #e0e0e0; border-radius: 5px; overflow: hidden;">
                    <div style="width: {score}%; height: 100%; background: #2196F3;"></div>
                </div>
            </div>"""
    
    html_content += """
        </div>
        
        <div class="issues-section">"""
    
    # Critical issues
    critical_issues = audit_data.get('critical_issues', [])
    if critical_issues:
        html_content += """
            <h2>🚨 Critical Issues</h2>"""
        for issue in critical_issues:
            html_content += f'<div class="issue-item critical-issue">{issue}</div>'
    
    # Recommendations
    recommendations = audit_data.get('recommended_improvements', [])
    if recommendations:
        html_content += """
            <h2>💡 Recommendations</h2>"""
        for rec in recommendations:
            html_content += f'<div class="issue-item recommendation">{rec}</div>'
    
    html_content += f"""
        </div>
        
        <div class="timestamp">
            Generated: {audit_data.get('timestamp', datetime.utcnow().isoformat())}
        </div>
    </div>
</body>
</html>"""
    
    return html_content

def generate_markdown_report(audit_data):
    """Generate Markdown quality report"""
    overall_score = audit_data.get('overall_score', 0)
    category_scores = audit_data.get('category_scores', {})
    
    markdown_content = f"""# 🤖 AI Agents Quality Report

**Overall Score**: {overall_score}/100  
**Status**: {audit_data.get('approval_status', 'pending').upper()}  
**Generated**: {audit_data.get('timestamp', datetime.utcnow().isoformat())}

## 📊 Category Scores

| Category | Score | Status |
|----------|-------|--------|"""
    
    for category, score in category_scores.items():
        status = "✅ Pass" if score >= 80 else "⚠️ Review" if score >= 60 else "❌ Fail"
        markdown_content += f"\n| {category.replace('_', ' ').title()} | {score}/100 | {status} |"
    
    # Critical issues
    critical_issues = audit_data.get('critical_issues', [])
    if critical_issues:
        markdown_content += f"""

## 🚨 Critical Issues

"""
        for i, issue in enumerate(critical_issues, 1):
            markdown_content += f"{i}. **{issue}**\n"
    
    # Recommendations
    recommendations = audit_data.get('recommended_improvements', [])
    if recommendations:
        markdown_content += f"""

## 💡 Recommendations

"""
        for i, rec in enumerate(recommendations, 1):
            markdown_content += f"{i}. {rec}\n"
    
    # Next steps
    next_steps = audit_data.get('next_steps', [])
    if next_steps:
        markdown_content += f"""

## 🚀 Next Steps

"""
        for i, step in enumerate(next_steps, 1):
            markdown_content += f"{i}. {step}\n"
    
    return markdown_content

def main():
    parser = argparse.ArgumentParser(description="Generate quality reports")
    parser.add_argument("--audit-dir", required=True, help="Audit directory path")
    parser.add_argument("--output", required=True, help="Output file path (without extension)")
    parser.add_argument("--format", required=True, help="Output formats (html,json,markdown)")
    
    args = parser.parse_args()
    
    result = generate_quality_report(args.audit_dir, args.output, args.format)
    
    return 0 if result else 1

if __name__ == "__main__":
    sys.exit(main())