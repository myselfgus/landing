#!/usr/bin/env python3
"""
Create staging preview for approval
"""

import argparse
import sys
import shutil
from pathlib import Path

def create_staging_preview(staging_dir, current_source, preview_output, base_url):
    """Create preview environment for staging approval"""
    print("🔍 Creating staging preview...")
    
    staging_path = Path(staging_dir)
    current_path = Path(current_source)
    preview_path = Path(preview_output)
    
    # Create preview directory
    preview_path.mkdir(parents=True, exist_ok=True)
    
    # Copy current source as base
    for file_path in current_path.glob("*"):
        if file_path.is_file() and not file_path.name.startswith('.'):
            shutil.copy2(file_path, preview_path / file_path.name)
    
    # Overlay staging files
    staging_files_copied = 0
    for file_path in staging_path.glob("*"):
        if file_path.is_file() and file_path.suffix in ['.html', '.css', '.tsx', '.js']:
            target_path = preview_path / file_path.name
            shutil.copy2(file_path, target_path)
            staging_files_copied += 1
    
    # Copy staging assets
    assets_path = staging_path / "assets"
    if assets_path.exists():
        preview_assets = preview_path / "assets"
        preview_assets.mkdir(exist_ok=True)
        for asset_file in assets_path.glob("*"):
            if asset_file.is_file():
                shutil.copy2(asset_file, preview_assets / asset_file.name)
    
    # Copy audit results for preview
    audit_path = staging_path.parent / "audit"
    if audit_path.exists():
        preview_audit = preview_path / "audit"
        preview_audit.mkdir(exist_ok=True)
        for audit_file in audit_path.rglob("*"):
            if audit_file.is_file():
                relative_path = audit_file.relative_to(audit_path)
                target_path = preview_audit / relative_path
                target_path.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(audit_file, target_path)
    
    # Create preview index with navigation
    preview_index = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Staging Preview - AI Agents</title>
    <style>
        body {{ 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            margin: 0; padding: 20px; background: #f0f2f5;
        }}
        .preview-header {{
            background: #1976d2; color: white; padding: 20px; border-radius: 8px; margin-bottom: 20px;
        }}
        .preview-nav {{
            display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px;
            margin-bottom: 30px;
        }}
        .nav-card {{
            background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            text-decoration: none; color: #333; transition: transform 0.2s;
        }}
        .nav-card:hover {{ transform: translateY(-2px); }}
        .nav-card h3 {{ margin: 0 0 10px 0; color: #1976d2; }}
        .nav-card p {{ margin: 0; color: #666; font-size: 0.9em; }}
        .preview-frame {{
            background: white; border-radius: 8px; overflow: hidden; box-shadow: 0 2px 8px rgba(0,0,0,0.15);
        }}
        iframe {{ width: 100%; height: 80vh; border: none; }}
    </style>
</head>
<body>
    <div class="preview-header">
        <h1>🤖 AI Agents Staging Preview</h1>
        <p>Review the generated improvements before deployment</p>
    </div>
    
    <div class="preview-nav">
        <a href="index.html" class="nav-card">
            <h3>🏠 Main Site</h3>
            <p>View the enhanced landing page</p>
        </a>
        <a href="audit/quality-report.html" class="nav-card">
            <h3>📊 Quality Report</h3>
            <p>Comprehensive quality analysis</p>
        </a>
        <a href="audit/todos/master_checklist.md" class="nav-card">
            <h3>📋 Todo Lists</h3>
            <p>Parallel quality checklists</p>
        </a>
        <a href="docs/" class="nav-card">
            <h3>📚 Documentation</h3>
            <p>Implementation guides and changes</p>
        </a>
    </div>
    
    <div class="preview-frame">
        <iframe src="index.html" title="Staging Preview"></iframe>
    </div>
    
    <script>
        // Add navigation functionality
        document.querySelectorAll('.nav-card').forEach(card => {{
            card.addEventListener('click', (e) => {{
                e.preventDefault();
                const iframe = document.querySelector('iframe');
                iframe.src = card.getAttribute('href');
            }});
        }});
    </script>
</body>
</html>"""
    
    # Write preview index
    with open(preview_path / "preview.html", 'w') as f:
        f.write(preview_index)
    
    preview_url = f"{base_url}/staging-preview/"
    
    print(f"✅ Staging preview created!")
    print(f"Files copied: {staging_files_copied}")
    print(f"Preview URL: {preview_url}")
    print(f"::set-output name=preview-url::{preview_url}")
    
    return preview_url

def main():
    parser = argparse.ArgumentParser(description="Create staging preview")
    parser.add_argument("--staging-dir", required=True, help="Staging directory")
    parser.add_argument("--current-source", required=True, help="Current source directory")
    parser.add_argument("--preview-output", required=True, help="Preview output directory")
    parser.add_argument("--base-url", required=True, help="Base URL for preview")
    
    args = parser.parse_args()
    
    result = create_staging_preview(
        args.staging_dir, args.current_source, args.preview_output, args.base_url
    )
    
    return 0 if result else 1

if __name__ == "__main__":
    sys.exit(main())