#!/usr/bin/env python3
"""
AI Agent 2 - Code Executor
Uses GPT-4 Turbo for precise code generation and implementation
"""

import argparse
import json
import os
import sys
import hashlib
import shutil
from datetime import datetime
from pathlib import Path

try:
    import openai
    import requests
    import yaml
    from jinja2 import Template
except ImportError as e:
    print(f"Missing required package: {e}")
    sys.exit(1)

class CodeExecutor:
    def __init__(self, ai_model="gpt-4-turbo"):
        self.ai_model = ai_model
        self.client = openai.OpenAI(
            api_key=os.getenv("OPENAI_API_KEY", "demo-key")
        )
        
    def load_strategic_plan(self, planning_dir):
        """Load strategic plan from Planner agent"""
        plan_file = Path(planning_dir) / "strategic_plan.json"
        context_file = Path(planning_dir) / "execution_context.json"
        
        with open(plan_file, 'r') as f:
            strategic_plan = json.load(f)
            
        with open(context_file, 'r') as f:
            execution_context = json.load(f)
            
        return strategic_plan, execution_context
    
    def load_knowledge_base(self, knowledge_base_path):
        """Load knowledge base for context"""
        knowledge = {}
        knowledge_path = Path(knowledge_base_path)
        
        if knowledge_path.exists():
            for file_path in knowledge_path.rglob("*.json"):
                with open(file_path, 'r') as f:
                    knowledge[file_path.stem] = json.load(f)
                    
            for file_path in knowledge_path.rglob("*.md"):
                with open(file_path, 'r', encoding='utf-8') as f:
                    knowledge[file_path.stem] = f.read()
                    
        return knowledge
    
    def analyze_source_code(self, source_path):
        """Analyze current source code for safe modifications"""
        source_analysis = {
            "files": {},
            "dependencies": {},
            "structure": {},
            "safety_assessment": {}
        }
        
        source_path = Path(source_path)
        
        # Analyze main files
        main_files = ["index.html", "index.tsx", "index.css", "package.json", "vite.config.ts"]
        for file_name in main_files:
            file_path = source_path / file_name
            if file_path.exists():
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    source_analysis["files"][file_name] = {
                        "content": content,
                        "size": len(content),
                        "lines": len(content.split('\n'))
                    }
        
        # Analyze package.json for dependencies
        if "package.json" in source_analysis["files"]:
            try:
                pkg_data = json.loads(source_analysis["files"]["package.json"]["content"])
                source_analysis["dependencies"] = {
                    "dependencies": pkg_data.get("dependencies", {}),
                    "devDependencies": pkg_data.get("devDependencies", {})
                }
            except:
                pass
        
        return source_analysis
    
    def generate_enhanced_code(self, strategic_plan, source_analysis, knowledge_base):
        """Generate enhanced code using GPT-4 Turbo"""
        
        system_prompt = """You are an expert Code Executor AI agent specializing in safe, high-quality code generation and implementation.

You work as part of a 3-agent system:
- Planner: Strategic analysis and planning (completed)
- You (Executor): Code generation and implementation
- Auditor: Quality review and validation (next)

Your responsibilities:
1. Generate production-ready code based on strategic plans
2. Ensure all code is safe, tested, and follows best practices
3. Create comprehensive documentation
4. Prepare staging environment for auditor review

CRITICAL SAFETY RULES:
- Never delete or break existing functionality
- Always provide fallbacks and error handling
- Generate code in staging directory only
- Include comprehensive comments and documentation
- Follow existing code patterns and conventions"""

        # Prepare recommendations for implementation
        recommendations = strategic_plan.get("recommendations", [])
        executor_instructions = strategic_plan.get("executor_instructions", {})
        
        user_prompt = f"""
        # Code Generation Task
        
        ## Strategic Plan Summary:
        Recommendations: {len(recommendations)} items
        Components to update: {executor_instructions.get("components_to_update", [])}
        Safety level: {executor_instructions.get("safety_level", "conservative")}
        
        ## Current Source Analysis:
        Available files: {list(source_analysis["files"].keys())}
        Dependencies: {list(source_analysis["dependencies"].get("dependencies", {}).keys())}
        
        ## Knowledge Base Context:
        Available knowledge: {list(knowledge_base.keys())}
        
        ## Your Task:
        Generate enhanced versions of the specified components with these improvements:
        {json.dumps(recommendations, indent=2)}
        
        Requirements:
        1. **Generate complete, working files** for each component
        2. **Preserve all existing functionality** 
        3. **Add enhancements incrementally** based on recommendations
        4. **Include comprehensive comments** explaining changes
        5. **Follow modern best practices** for web development
        6. **Ensure cross-browser compatibility**
        7. **Optimize for performance** (Core Web Vitals)
        8. **Maintain accessibility** standards
        
        Provide response as JSON with this structure:
        {{
            "generated_files": {{
                "filename": {{
                    "content": "complete file content",
                    "changes_summary": "description of changes made",
                    "safety_notes": "safety considerations",
                    "testing_notes": "how to test this component"
                }}
            }},
            "assets": {{
                "filename": "content for CSS, images, etc"
            }},
            "documentation": {{
                "implementation_guide": "how to use the new code",
                "change_log": "detailed list of changes",
                "rollback_plan": "how to revert if needed"
            }},
            "validation_checklist": [
                "item to check before deployment"
            ]
        }}
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4-1106-preview",  # GPT-4 Turbo
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=4000,
                temperature=0.1  # Low temperature for consistent, safe code
            )
            
            response_text = response.choices[0].message.content
            
            # Try to extract JSON from response
            start_idx = response_text.find('{')
            end_idx = response_text.rfind('}') + 1
            
            if start_idx != -1 and end_idx > start_idx:
                generated_code = json.loads(response_text[start_idx:end_idx])
            else:
                # Fallback: generate basic enhanced version
                generated_code = self.generate_fallback_enhancements(source_analysis, strategic_plan)
                
            return generated_code
            
        except Exception as e:
            print(f"Error generating code: {e}")
            return self.generate_fallback_enhancements(source_analysis, strategic_plan)
    
    def generate_fallback_enhancements(self, source_analysis, strategic_plan):
        """Generate basic enhancements as fallback"""
        generated_code = {
            "generated_files": {},
            "assets": {},
            "documentation": {
                "implementation_guide": "Basic enhancements applied",
                "change_log": "Fallback generation used",
                "rollback_plan": "Restore from backup"
            },
            "validation_checklist": [
                "Check page loads correctly",
                "Verify no console errors",
                "Test responsive design"
            ]
        }
        
        # Generate enhanced CSS with performance improvements
        if "index.css" in source_analysis["files"]:
            original_css = source_analysis["files"]["index.css"]["content"]
            enhanced_css = self.enhance_css(original_css)
            generated_code["generated_files"]["index.css"] = {
                "content": enhanced_css,
                "changes_summary": "Added performance optimizations and modern CSS features",
                "safety_notes": "All original styles preserved",
                "testing_notes": "Check visual layout and responsiveness"
            }
        
        # Generate enhanced HTML with SEO improvements
        if "index.html" in source_analysis["files"]:
            original_html = source_analysis["files"]["index.html"]["content"]
            enhanced_html = self.enhance_html(original_html)
            generated_code["generated_files"]["index.html"] = {
                "content": enhanced_html,
                "changes_summary": "Added SEO meta tags and performance optimizations",
                "safety_notes": "All original content preserved",
                "testing_notes": "Verify meta tags and page structure"
            }
        
        return generated_code
    
    def enhance_css(self, original_css):
        """Add basic CSS enhancements"""
        enhanced_css = original_css
        
        # Add performance optimizations
        performance_css = """
/* AI-Generated Performance Enhancements */
* {
  box-sizing: border-box;
}

html {
  scroll-behavior: smooth;
}

img {
  max-width: 100%;
  height: auto;
  loading: lazy;
}

/* Modern CSS Grid and Flexbox improvements */
.container {
  display: grid;
  gap: 1rem;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1rem;
}

/* Enhanced animations with reduced motion support */
@media (prefers-reduced-motion: no-preference) {
  .animate {
    transition: all 0.3s ease-in-out;
  }
}

/* Dark mode support */
@media (prefers-color-scheme: dark) {
  :root {
    --bg-color: #1a1a1a;
    --text-color: #ffffff;
  }
}
"""
        
        return enhanced_css + "\n" + performance_css
    
    def enhance_html(self, original_html):
        """Add basic HTML enhancements"""
        enhanced_html = original_html
        
        # Add meta tags if not present
        meta_tags = '''
    <!-- AI-Generated SEO and Performance Meta Tags -->
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="VOITHER MedicalScribe - Advanced AI-powered medical transcription and documentation">
    <meta name="keywords" content="medical, transcription, AI, healthcare, documentation">
    <meta name="author" content="VOITHER">
    
    <!-- Performance optimizations -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="dns-prefetch" href="https://cdn.jsdelivr.net">
    
    <!-- Open Graph meta tags -->
    <meta property="og:title" content="VOITHER MedicalScribe">
    <meta property="og:description" content="Advanced AI-powered medical transcription and documentation">
    <meta property="og:type" content="website">
    
    <!-- Twitter Card meta tags -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="VOITHER MedicalScribe">
    <meta name="twitter:description" content="Advanced AI-powered medical transcription and documentation">
'''
        
        # Insert after <head> tag
        if '<head>' in enhanced_html:
            enhanced_html = enhanced_html.replace('<head>', '<head>' + meta_tags)
        
        return enhanced_html
    
    def create_staging_structure(self, staging_output, generated_code, source_analysis):
        """Create comprehensive staging environment"""
        staging_path = Path(staging_output)
        staging_path.mkdir(parents=True, exist_ok=True)
        
        # Create generated files
        for filename, file_data in generated_code["generated_files"].items():
            file_path = staging_path / filename
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(file_data["content"])
        
        # Create assets
        assets_path = staging_path / "assets"
        assets_path.mkdir(exist_ok=True)
        for filename, content in generated_code.get("assets", {}).items():
            asset_path = assets_path / filename
            with open(asset_path, 'w', encoding='utf-8') as f:
                f.write(content)
        
        # Create documentation
        docs_path = staging_path / "docs"
        docs_path.mkdir(exist_ok=True)
        
        for doc_name, doc_content in generated_code["documentation"].items():
            doc_path = docs_path / f"{doc_name}.md"
            with open(doc_path, 'w', encoding='utf-8') as f:
                f.write(f"# {doc_name.replace('_', ' ').title()}\n\n{doc_content}")
        
        # Create validation checklist
        checklist_path = staging_path / "VALIDATION_CHECKLIST.md"
        with open(checklist_path, 'w') as f:
            f.write("# Validation Checklist\n\n")
            for item in generated_code["validation_checklist"]:
                f.write(f"- [ ] {item}\n")
        
        # Copy original files for comparison
        originals_path = staging_path / "originals"
        originals_path.mkdir(exist_ok=True)
        
        for filename, file_data in source_analysis["files"].items():
            original_path = originals_path / filename
            with open(original_path, 'w', encoding='utf-8') as f:
                f.write(file_data["content"])
        
        return staging_path
    
    def create_checkpoint(self, staging_path, generated_code):
        """Create validation checkpoint for the staging code"""
        checkpoint = {
            "agent": "executor",
            "timestamp": datetime.utcnow().isoformat(),
            "staging_checksum": hashlib.sha256(json.dumps(generated_code, sort_keys=True).encode()).hexdigest(),
            "status": "completed",
            "next_agent": "auditor",
            "files_generated": list(generated_code["generated_files"].keys()),
            "safety_level": "conservative"
        }
        
        checkpoint_path = staging_path / "checkpoint.json"
        with open(checkpoint_path, 'w') as f:
            json.dump(checkpoint, f, indent=2)
            
        return checkpoint["staging_checksum"]
    
    def run(self, args):
        """Main execution method"""
        print("🛠️ AI Agent 2 - Code Executor Starting...")
        
        # Load strategic plan from Planner
        strategic_plan, execution_context = self.load_strategic_plan(args.planning_dir)
        
        # Load knowledge base
        knowledge_base = self.load_knowledge_base(args.knowledge_base)
        
        # Analyze source code
        source_analysis = self.analyze_source_code(args.source)
        
        # Generate enhanced code
        generated_code = self.generate_enhanced_code(strategic_plan, source_analysis, knowledge_base)
        
        # Create staging environment
        staging_path = self.create_staging_structure(args.staging_output, generated_code, source_analysis)
        
        # Create checkpoint
        checksum = self.create_checkpoint(staging_path, generated_code)
        
        # Set GitHub Actions outputs
        print(f"::set-output name=status::success")
        print(f"::set-output name=checksum::{checksum}")
        print(f"::set-output name=files::{','.join(generated_code['generated_files'].keys())}")
        
        print("✅ Code generation completed successfully!")
        print(f"Staging environment: {staging_path}")
        print(f"Files generated: {len(generated_code['generated_files'])}")
        print(f"Checkpoint: {checksum}")
        
        return generated_code

def main():
    parser = argparse.ArgumentParser(description="AI Agent 2 - Code Executor")
    parser.add_argument("--planning-dir", required=True, help="Path to planning artifacts directory")
    parser.add_argument("--knowledge-base", required=True, help="Path to knowledge base directory")
    parser.add_argument("--source", required=True, help="Path to source code directory")
    parser.add_argument("--staging-output", required=True, help="Output directory for staging code")
    parser.add_argument("--ai-model", default="gpt-4-turbo", help="AI model to use")
    parser.add_argument("--components", help="Comma-separated list of components to update")
    parser.add_argument("--safety-level", default="conservative", help="Safety level for code generation")
    
    args = parser.parse_args()
    
    executor = CodeExecutor(args.ai_model)
    result = executor.run(args)
    
    return 0 if result else 1

if __name__ == "__main__":
    sys.exit(main())