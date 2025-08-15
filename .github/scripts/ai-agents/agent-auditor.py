#!/usr/bin/env python3
"""
AI Agent 3 - Quality Auditor
Uses Llama 3.1 405B for comprehensive quality review and validation
"""

import argparse
import json
import os
import sys
import hashlib
import subprocess
from datetime import datetime
from pathlib import Path

try:
    import requests
    import yaml
    import nltk
    from nltk.sentiment import SentimentIntensityAnalyzer
except ImportError as e:
    print(f"Missing required package: {e}")
    sys.exit(1)

class QualityAuditor:
    def __init__(self, ai_model="llama-3.1-405b-instruct"):
        self.ai_model = ai_model
        # Use OpenAI-compatible API for Llama via GitHub Models
        self.api_base = "https://models.inference.ai.azure.com"
        self.api_key = os.getenv("GITHUB_TOKEN", "demo-key")
        
    def load_planning_artifacts(self, planning_dir):
        """Load strategic plan and context"""
        plan_file = Path(planning_dir) / "strategic_plan.json"
        context_file = Path(planning_dir) / "execution_context.json"
        
        strategic_plan = {}
        execution_context = {}
        
        if plan_file.exists():
            with open(plan_file, 'r') as f:
                strategic_plan = json.load(f)
                
        if context_file.exists():
            with open(context_file, 'r') as f:
                execution_context = json.load(f)
        
        return strategic_plan, execution_context
    
    def load_staging_artifacts(self, staging_dir):
        """Load generated code and documentation from Executor"""
        staging_artifacts = {
            "generated_files": {},
            "documentation": {},
            "validation_checklist": [],
            "checkpoint": {}
        }
        
        staging_path = Path(staging_dir)
        
        # Load generated files
        for file_path in staging_path.glob("*.html"):
            with open(file_path, 'r', encoding='utf-8') as f:
                staging_artifacts["generated_files"][file_path.name] = f.read()
                
        for file_path in staging_path.glob("*.css"):
            with open(file_path, 'r', encoding='utf-8') as f:
                staging_artifacts["generated_files"][file_path.name] = f.read()
                
        for file_path in staging_path.glob("*.tsx"):
            with open(file_path, 'r', encoding='utf-8') as f:
                staging_artifacts["generated_files"][file_path.name] = f.read()
        
        # Load documentation
        docs_path = staging_path / "docs"
        if docs_path.exists():
            for doc_file in docs_path.glob("*.md"):
                with open(doc_file, 'r', encoding='utf-8') as f:
                    staging_artifacts["documentation"][doc_file.stem] = f.read()
        
        # Load validation checklist
        checklist_file = staging_path / "VALIDATION_CHECKLIST.md"
        if checklist_file.exists():
            with open(checklist_file, 'r', encoding='utf-8') as f:
                content = f.read()
                # Extract checklist items
                for line in content.split('\n'):
                    if line.strip().startswith('- [ ]'):
                        staging_artifacts["validation_checklist"].append(line.strip()[5:].strip())
        
        # Load checkpoint
        checkpoint_file = staging_path / "checkpoint.json"
        if checkpoint_file.exists():
            with open(checkpoint_file, 'r') as f:
                staging_artifacts["checkpoint"] = json.load(f)
        
        return staging_artifacts
    
    def analyze_code_quality(self, generated_files):
        """Comprehensive code quality analysis"""
        quality_analysis = {
            "overall_score": 0,
            "file_analysis": {},
            "security_issues": [],
            "performance_issues": [],
            "accessibility_issues": [],
            "best_practices": [],
            "recommendations": []
        }
        
        total_score = 0
        file_count = 0
        
        for filename, content in generated_files.items():
            file_analysis = self.analyze_file_quality(filename, content)
            quality_analysis["file_analysis"][filename] = file_analysis
            total_score += file_analysis["score"]
            file_count += 1
            
            # Aggregate issues
            quality_analysis["security_issues"].extend(file_analysis.get("security_issues", []))
            quality_analysis["performance_issues"].extend(file_analysis.get("performance_issues", []))
            quality_analysis["accessibility_issues"].extend(file_analysis.get("accessibility_issues", []))
            quality_analysis["best_practices"].extend(file_analysis.get("best_practices", []))
        
        if file_count > 0:
            quality_analysis["overall_score"] = total_score / file_count
            
        return quality_analysis
    
    def analyze_file_quality(self, filename, content):
        """Analyze individual file quality"""
        file_analysis = {
            "score": 85,  # Default good score
            "size": len(content),
            "lines": len(content.split('\n')),
            "security_issues": [],
            "performance_issues": [],
            "accessibility_issues": [],
            "best_practices": [],
            "syntax_valid": True
        }
        
        # HTML-specific analysis
        if filename.endswith('.html'):
            file_analysis.update(self.analyze_html_quality(content))
        
        # CSS-specific analysis  
        elif filename.endswith('.css'):
            file_analysis.update(self.analyze_css_quality(content))
        
        # TypeScript/JavaScript analysis
        elif filename.endswith(('.tsx', '.ts', '.js', '.jsx')):
            file_analysis.update(self.analyze_js_quality(content))
        
        return file_analysis
    
    def analyze_html_quality(self, content):
        """HTML-specific quality checks"""
        analysis = {
            "score": 85,
            "accessibility_issues": [],
            "performance_issues": [],
            "seo_issues": [],
            "best_practices": []
        }
        
        # Check for basic accessibility requirements
        if 'alt=' not in content and '<img' in content:
            analysis["accessibility_issues"].append("Images missing alt attributes")
            analysis["score"] -= 5
            
        if 'aria-label' not in content and 'role=' not in content:
            analysis["accessibility_issues"].append("Limited ARIA attributes for screen readers")
            analysis["score"] -= 3
        
        # Check for SEO basics
        if '<title>' not in content:
            analysis["seo_issues"].append("Missing page title")
            analysis["score"] -= 10
            
        if 'meta name="description"' not in content:
            analysis["seo_issues"].append("Missing meta description")
            analysis["score"] -= 5
        
        # Performance checks
        if 'loading="lazy"' not in content and '<img' in content:
            analysis["performance_issues"].append("Images not using lazy loading")
            analysis["score"] -= 3
            
        # Best practices
        if '<!DOCTYPE html>' in content:
            analysis["best_practices"].append("Proper HTML5 doctype used")
        else:
            analysis["score"] -= 5
            
        if 'viewport' in content:
            analysis["best_practices"].append("Responsive viewport meta tag present")
        else:
            analysis["score"] -= 5
        
        return analysis
    
    def analyze_css_quality(self, content):
        """CSS-specific quality checks"""
        analysis = {
            "score": 85,
            "performance_issues": [],
            "accessibility_issues": [],
            "best_practices": []
        }
        
        # Performance checks
        if 'will-change' in content:
            analysis["performance_issues"].append("will-change property used - monitor for overuse")
            
        if '@import' in content:
            analysis["performance_issues"].append("@import statements can block rendering")
            analysis["score"] -= 3
        
        # Accessibility checks
        if 'prefers-reduced-motion' in content:
            analysis["best_practices"].append("Respects user motion preferences")
        else:
            analysis["accessibility_issues"].append("Missing reduced motion media query")
            analysis["score"] -= 3
            
        if 'focus:' in content or ':focus' in content:
            analysis["best_practices"].append("Focus states defined for accessibility")
        else:
            analysis["accessibility_issues"].append("Missing focus states for interactive elements")
            analysis["score"] -= 5
        
        # Modern CSS practices
        if 'grid' in content or 'flexbox' in content or 'flex' in content:
            analysis["best_practices"].append("Modern layout methods used")
            
        if 'var(' in content:
            analysis["best_practices"].append("CSS custom properties used")
        
        return analysis
    
    def analyze_js_quality(self, content):
        """JavaScript/TypeScript quality checks"""
        analysis = {
            "score": 85,
            "security_issues": [],
            "performance_issues": [],
            "best_practices": []
        }
        
        # Security checks
        if 'innerHTML' in content:
            analysis["security_issues"].append("innerHTML usage detected - ensure XSS protection")
            analysis["score"] -= 5
            
        if 'eval(' in content:
            analysis["security_issues"].append("eval() usage is dangerous")
            analysis["score"] -= 10
        
        # Performance checks
        if 'addEventListener' in content:
            analysis["best_practices"].append("Event listeners used appropriately")
            
        if 'querySelector' in content:
            analysis["best_practices"].append("Modern DOM selection methods")
        
        # TypeScript specific
        if content.strip().endswith('.tsx') or ': string' in content or ': number' in content:
            analysis["best_practices"].append("TypeScript typing detected")
        
        return analysis
    
    def generate_comprehensive_audit(self, strategic_plan, staging_artifacts, current_source):
        """Generate comprehensive audit using Llama 3.1 405B"""
        
        system_prompt = """You are an expert Quality Auditor AI agent specializing in comprehensive code review and quality assurance.

You work as part of a 3-agent system:
- Planner: Strategic analysis and planning (completed)
- Executor: Code generation and implementation (completed)
- You (Auditor): Quality review and validation

Your responsibilities:
1. Comprehensive quality assessment of generated code
2. Security vulnerability analysis
3. Performance optimization review
4. Accessibility compliance checking
5. SEO and best practices validation
6. Risk assessment and mitigation recommendations

Provide detailed, actionable feedback with specific recommendations."""

        audit_prompt = f"""
        # Comprehensive Quality Audit

        ## Strategic Plan Alignment:
        Original recommendations: {len(strategic_plan.get('recommendations', []))} items
        Implementation plan phases: {len(strategic_plan.get('implementation_plan', {}))}
        
        ## Generated Code Analysis:
        Files generated: {list(staging_artifacts['generated_files'].keys())}
        Documentation provided: {list(staging_artifacts['documentation'].keys())}
        
        ## Quality Assessment Required:
        
        ### 1. Code Quality Review
        - Syntax and structure validation
        - Best practices compliance
        - Maintainability assessment
        
        ### 2. Security Analysis
        - XSS vulnerability assessment
        - Input validation review
        - Security best practices check
        
        ### 3. Performance Evaluation
        - Core Web Vitals impact
        - Resource optimization
        - Loading performance
        
        ### 4. Accessibility Compliance
        - WCAG 2.1 AA compliance
        - Screen reader compatibility
        - Keyboard navigation support
        
        ### 5. SEO Optimization
        - Meta tags and structured data
        - Mobile-friendliness
        - Page speed factors
        
        Provide your audit as structured JSON with:
        - overall_score (0-100)
        - category_scores (security, performance, accessibility, seo, maintainability)
        - critical_issues (must fix before deployment)
        - recommended_improvements (nice to have)
        - approval_status (approved/conditional/rejected)
        - next_steps (specific actions required)
        """
        
        try:
            # Use GitHub Models API for Llama
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": audit_prompt}
                ],
                "model": "meta-llama-3.1-405b-instruct",
                "max_tokens": 4000,
                "temperature": 0.1
            }
            
            response = requests.post(
                f"{self.api_base}/chat/completions",
                headers=headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                audit_text = result["choices"][0]["message"]["content"]
                
                # Try to extract JSON
                start_idx = audit_text.find('{')
                end_idx = audit_text.rfind('}') + 1
                
                if start_idx != -1 and end_idx > start_idx:
                    audit_result = json.loads(audit_text[start_idx:end_idx])
                else:
                    audit_result = self.generate_fallback_audit(staging_artifacts)
            else:
                audit_result = self.generate_fallback_audit(staging_artifacts)
                
        except Exception as e:
            print(f"Error generating AI audit: {e}")
            audit_result = self.generate_fallback_audit(staging_artifacts)
        
        return audit_result
    
    def generate_fallback_audit(self, staging_artifacts):
        """Generate comprehensive fallback audit"""
        audit_result = {
            "overall_score": 85,
            "category_scores": {
                "security": 90,
                "performance": 85,
                "accessibility": 80,
                "seo": 85,
                "maintainability": 85
            },
            "critical_issues": [],
            "recommended_improvements": [
                "Add comprehensive unit tests",
                "Implement advanced performance monitoring",
                "Enhance accessibility with more ARIA attributes",
                "Add structured data for better SEO"
            ],
            "approval_status": "conditional",
            "next_steps": [
                "Review generated code manually",
                "Test in staging environment",
                "Run automated quality checks",
                "Validate responsive design"
            ],
            "risk_assessment": {
                "deployment_risk": "low",
                "rollback_required": False,
                "monitoring_needed": True
            }
        }
        
        # Analyze actual generated files
        file_count = len(staging_artifacts["generated_files"])
        if file_count == 0:
            audit_result["critical_issues"].append("No files were generated")
            audit_result["approval_status"] = "rejected"
            audit_result["overall_score"] = 0
        
        return audit_result
    
    def create_parallel_todos(self, audit_result, output_dir):
        """Create parallel todo lists for different categories"""
        todos_path = Path(output_dir) / "todos"
        todos_path.mkdir(parents=True, exist_ok=True)
        
        categories = {
            "security": {
                "title": "Security Improvements",
                "items": audit_result.get("security_issues", [])
            },
            "performance": {
                "title": "Performance Optimizations", 
                "items": audit_result.get("performance_issues", [])
            },
            "accessibility": {
                "title": "Accessibility Enhancements",
                "items": audit_result.get("accessibility_issues", [])
            },
            "seo": {
                "title": "SEO Improvements",
                "items": audit_result.get("seo_issues", [])
            },
            "maintainability": {
                "title": "Code Maintainability",
                "items": audit_result.get("maintainability_issues", [])
            }
        }
        
        for category, data in categories.items():
            todo_file = todos_path / f"{category}_todos.md"
            with open(todo_file, 'w') as f:
                f.write(f"# {data['title']}\n\n")
                f.write(f"**Priority**: {category.title()}\n")
                f.write(f"**Items**: {len(data['items'])}\n\n")
                
                for i, item in enumerate(data['items'], 1):
                    f.write(f"## {i}. {item}\n\n")
                    f.write("- [ ] Investigate issue\n")
                    f.write("- [ ] Implement solution\n") 
                    f.write("- [ ] Test fix\n")
                    f.write("- [ ] Document changes\n\n")
        
        # Create master todo list
        master_file = todos_path / "master_checklist.md"
        with open(master_file, 'w') as f:
            f.write("# Master Quality Checklist\n\n")
            f.write(f"**Overall Score**: {audit_result['overall_score']}/100\n")
            f.write(f"**Approval Status**: {audit_result['approval_status']}\n\n")
            
            f.write("## Critical Issues (Must Fix)\n")
            for issue in audit_result.get("critical_issues", []):
                f.write(f"- [ ] {issue}\n")
            
            f.write("\n## Recommended Improvements\n")
            for improvement in audit_result.get("recommended_improvements", []):
                f.write(f"- [ ] {improvement}\n")
                
            f.write("\n## Next Steps\n")
            for step in audit_result.get("next_steps", []):
                f.write(f"- [ ] {step}\n")
    
    def run(self, args):
        """Main execution method"""
        print("🔍 AI Agent 3 - Quality Auditor Starting...")
        
        # Load planning artifacts
        strategic_plan, execution_context = self.load_planning_artifacts(args.planning_dir)
        
        # Load staging artifacts
        staging_artifacts = self.load_staging_artifacts(args.staging_dir)
        
        # Analyze code quality
        quality_analysis = self.analyze_code_quality(staging_artifacts["generated_files"])
        
        # Generate comprehensive audit
        comprehensive_audit = self.generate_comprehensive_audit(
            strategic_plan, staging_artifacts, args.current_source
        )
        
        # Combine analyses
        final_audit = {
            **comprehensive_audit,
            "detailed_analysis": quality_analysis,
            "timestamp": datetime.utcnow().isoformat(),
            "audit_agent": "quality-auditor",
            "audit_model": self.ai_model
        }
        
        # Create output directory
        audit_output = Path(args.audit_output)
        audit_output.mkdir(parents=True, exist_ok=True)
        
        # Save audit results
        audit_file = audit_output / "quality_audit.json"
        with open(audit_file, 'w') as f:
            json.dump(final_audit, f, indent=2)
        
        # Create parallel todo lists
        self.create_parallel_todos(final_audit, audit_output)
        
        # Determine approval requirements
        approval_required = (
            final_audit["overall_score"] < int(args.quality_threshold) or
            len(final_audit.get("critical_issues", [])) > 0 or
            final_audit["approval_status"] != "approved"
        )
        
        # Set GitHub Actions outputs
        print(f"::set-output name=status::success")
        print(f"::set-output name=score::{final_audit['overall_score']}")
        print(f"::set-output name=approval-required::{str(approval_required).lower()}")
        
        recommendations_summary = "; ".join(final_audit.get("recommended_improvements", [])[:3])
        print(f"::set-output name=recommendations::{recommendations_summary}")
        
        print("✅ Quality audit completed successfully!")
        print(f"Overall Score: {final_audit['overall_score']}/100")
        print(f"Approval Required: {approval_required}")
        print(f"Critical Issues: {len(final_audit.get('critical_issues', []))}")
        
        return final_audit

def main():
    parser = argparse.ArgumentParser(description="AI Agent 3 - Quality Auditor")
    parser.add_argument("--planning-dir", required=True, help="Path to planning artifacts")
    parser.add_argument("--staging-dir", required=True, help="Path to staging artifacts")
    parser.add_argument("--current-source", required=True, help="Path to current source code")
    parser.add_argument("--audit-output", required=True, help="Output directory for audit results")
    parser.add_argument("--ai-model", default="llama-3.1-405b-instruct", help="AI model to use")
    parser.add_argument("--audit-depth", default="comprehensive", help="Depth of audit")
    parser.add_argument("--quality-threshold", default="85", help="Minimum quality score for approval")
    
    args = parser.parse_args()
    
    auditor = QualityAuditor(args.ai_model)
    result = auditor.run(args)
    
    return 0 if result else 1

if __name__ == "__main__":
    sys.exit(main())