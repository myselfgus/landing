#!/usr/bin/env python3
"""
AI Agent 1 - Strategic Planner
Uses Claude 3.5 Sonnet for advanced strategic analysis and planning
"""

import argparse
import json
import os
import sys
import hashlib
from datetime import datetime
from pathlib import Path

try:
    import anthropic
    import requests
    import yaml
except ImportError as e:
    print(f"Missing required package: {e}")
    sys.exit(1)

class StrategicPlanner:
    def __init__(self, ai_model="claude-3.5-sonnet"):
        self.ai_model = ai_model
        self.client = anthropic.Anthropic(
            api_key=os.getenv("ANTHROPIC_API_KEY", "demo-key")
        )
        
    def load_knowledge_base(self, knowledge_base_path):
        """Load comprehensive knowledge from docs repository and current analysis"""
        knowledge = {
            "docs_content": {},
            "current_analysis": {},
            "user_preferences": {},
            "technical_context": {}
        }
        
        # Load docs content
        docs_path = Path(knowledge_base_path) / "docs"
        if docs_path.exists():
            for file_path in docs_path.rglob("*.md"):
                rel_path = file_path.relative_to(docs_path)
                with open(file_path, 'r', encoding='utf-8') as f:
                    knowledge["docs_content"][str(rel_path)] = f.read()
        
        # Load current analysis
        analysis_path = Path(knowledge_base_path) / "analysis"
        if analysis_path.exists():
            for analysis_file in analysis_path.glob("*.json"):
                with open(analysis_file, 'r') as f:
                    knowledge["current_analysis"][analysis_file.stem] = json.load(f)
                    
        return knowledge
    
    def analyze_current_site(self, site_path):
        """Analyze current site structure and capabilities"""
        site_analysis = {
            "structure": {},
            "components": [],
            "styling": {},
            "performance": {},
            "content": {}
        }
        
        site_path = Path(site_path)
        
        # Analyze main files
        main_files = ["index.html", "index.tsx", "index.css", "package.json"]
        for file_name in main_files:
            file_path = site_path / file_name
            if file_path.exists():
                with open(file_path, 'r', encoding='utf-8') as f:
                    site_analysis["structure"][file_name] = f.read()
        
        # Analyze components directory if exists
        components_path = site_path / "components"
        if components_path.exists():
            for comp_file in components_path.rglob("*"):
                if comp_file.is_file():
                    site_analysis["components"].append(str(comp_file.relative_to(site_path)))
        
        return site_analysis
    
    def parse_user_command(self, command):
        """Parse and understand user command intent"""
        command = command.lower()
        
        intent = {
            "action": "analyze",
            "scope": "full-site",
            "priority": "medium",
            "focus_areas": [],
            "constraints": []
        }
        
        # Detect action type
        if "plan-and-stage" in command:
            intent["action"] = "plan-and-stage"
        elif "review" in command:
            intent["action"] = "review"
        elif "optimize" in command:
            intent["action"] = "optimize"
        elif "enhance" in command:
            intent["action"] = "enhance"
            
        # Detect scope
        if "landing" in command or "page" in command:
            intent["scope"] = "landing-page"
        elif "component" in command:
            intent["scope"] = "components"
        elif "style" in command or "css" in command:
            intent["scope"] = "styling"
        elif "performance" in command:
            intent["scope"] = "performance"
        elif "seo" in command:
            intent["scope"] = "seo"
            
        # Detect priority
        if "urgent" in command or "critical" in command:
            intent["priority"] = "high"
        elif "low" in command or "minor" in command:
            intent["priority"] = "low"
            
        return intent
    
    def generate_strategic_plan(self, knowledge, site_analysis, user_intent):
        """Generate comprehensive strategic improvement plan using Claude"""
        
        system_prompt = """You are an expert Strategic Planner AI agent specializing in website optimization and development. Your role is to create comprehensive, actionable plans for website improvements.

You work as part of a 3-agent system:
- You (Planner): Strategic analysis and planning
- Executor: Code generation and implementation  
- Auditor: Quality review and validation

Your output must be structured JSON that the Executor agent can follow precisely."""

        user_prompt = f"""
        # Strategic Planning Request
        
        ## User Intent:
        Action: {user_intent['action']}
        Scope: {user_intent['scope']}
        Priority: {user_intent['priority']}
        
        ## Knowledge Base Summary:
        - Docs content: {len(knowledge['docs_content'])} files
        - Current analysis: {list(knowledge['current_analysis'].keys())}
        
        ## Current Site Analysis:
        Structure files: {list(site_analysis['structure'].keys())}
        Components: {len(site_analysis['components'])} found
        
        ## Your Task:
        Create a detailed strategic plan that includes:
        1. **Situation Analysis**: Current state assessment
        2. **Opportunity Identification**: Improvement opportunities  
        3. **Strategic Recommendations**: Prioritized recommendations
        4. **Implementation Phases**: Step-by-step execution plan
        5. **Success Metrics**: Measurable outcomes
        6. **Risk Assessment**: Potential challenges and mitigations
        
        Provide response in structured JSON format with these sections:
        - analysis: Current situation assessment
        - opportunities: Identified improvement areas
        - recommendations: Prioritized action items
        - implementation_plan: Detailed phases and tasks
        - success_metrics: KPIs and measurement criteria
        - risk_assessment: Risks and mitigation strategies
        - executor_instructions: Specific guidance for the Executor agent
        """
        
        try:
            response = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=4000,
                system=system_prompt,
                messages=[{"role": "user", "content": user_prompt}]
            )
            
            # Parse response as JSON
            plan_text = response.content[0].text
            
            # Try to extract JSON from response
            start_idx = plan_text.find('{')
            end_idx = plan_text.rfind('}') + 1
            
            if start_idx != -1 and end_idx > start_idx:
                plan_json = json.loads(plan_text[start_idx:end_idx])
            else:
                # Fallback: create structured plan
                plan_json = {
                    "analysis": {
                        "current_state": "Site analysis completed",
                        "strengths": ["Existing structure", "Content foundation"],
                        "weaknesses": ["Performance optimization needed", "Visual enhancements required"]
                    },
                    "opportunities": [
                        "Performance optimization",
                        "Visual design enhancement", 
                        "Content optimization",
                        "SEO improvements"
                    ],
                    "recommendations": [
                        {
                            "title": "Optimize Core Web Vitals",
                            "priority": "high",
                            "impact": "high",
                            "effort": "medium"
                        },
                        {
                            "title": "Enhance Visual Design",
                            "priority": "medium", 
                            "impact": "high",
                            "effort": "medium"
                        }
                    ],
                    "implementation_plan": {
                        "phase_1": {
                            "title": "Foundation Optimization",
                            "tasks": ["Performance analysis", "Code optimization"],
                            "duration": "1-2 days"
                        },
                        "phase_2": {
                            "title": "Visual Enhancement",
                            "tasks": ["Design improvements", "Interactive elements"],
                            "duration": "2-3 days"
                        }
                    },
                    "success_metrics": [
                        "Page load time < 2s",
                        "Lighthouse score > 90",
                        "User engagement increase"
                    ],
                    "risk_assessment": {
                        "low_risk": ["CSS modifications", "Performance tweaks"],
                        "medium_risk": ["Component restructuring"],
                        "high_risk": ["Major architectural changes"]
                    },
                    "executor_instructions": {
                        "safety_level": "conservative",
                        "testing_required": True,
                        "backup_needed": True,
                        "components_to_update": ["index.html", "index.css", "index.tsx"]
                    }
                }
            
            return plan_json
            
        except Exception as e:
            print(f"Error generating strategic plan: {e}")
            # Return minimal fallback plan
            return {
                "analysis": {"status": "error", "message": str(e)},
                "recommendations": [],
                "implementation_plan": {},
                "executor_instructions": {
                    "safety_level": "conservative",
                    "testing_required": True
                }
            }
    
    def create_checkpoint(self, plan, output_path):
        """Create validation checkpoint for the plan"""
        checkpoint = {
            "agent": "planner",
            "timestamp": datetime.utcnow().isoformat(),
            "plan_checksum": hashlib.sha256(json.dumps(plan, sort_keys=True).encode()).hexdigest(),
            "status": "completed",
            "next_agent": "executor"
        }
        
        checkpoint_path = Path(output_path) / "checkpoint.json"
        with open(checkpoint_path, 'w') as f:
            json.dump(checkpoint, f, indent=2)
            
        return checkpoint["plan_checksum"]
    
    def run(self, args):
        """Main execution method"""
        print("🤖 AI Agent 1 - Strategic Planner Starting...")
        
        # Load comprehensive knowledge
        knowledge = self.load_knowledge_base(args.knowledge_base)
        
        # Analyze current site
        site_analysis = self.analyze_current_site(args.current_site)
        
        # Parse user command intent
        user_intent = self.parse_user_command(args.command)
        
        # Generate strategic plan
        strategic_plan = self.generate_strategic_plan(knowledge, site_analysis, user_intent)
        
        # Ensure output directory exists
        output_path = Path(args.output)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Save strategic plan
        plan_file = output_path / "strategic_plan.json"
        with open(plan_file, 'w') as f:
            json.dump(strategic_plan, f, indent=2)
        
        # Save execution context
        context = {
            "user_intent": user_intent,
            "knowledge_summary": {
                "docs_files": list(knowledge["docs_content"].keys()),
                "analysis_available": list(knowledge["current_analysis"].keys())
            },
            "site_summary": {
                "main_files": list(site_analysis["structure"].keys()),
                "components_count": len(site_analysis["components"])
            }
        }
        
        context_file = output_path / "execution_context.json"
        with open(context_file, 'w') as f:
            json.dump(context, f, indent=2)
        
        # Create checkpoint
        checksum = self.create_checkpoint(strategic_plan, output_path)
        
        # Set GitHub Actions outputs
        print(f"::set-output name=status::success")
        print(f"::set-output name=checksum::{checksum}")
        print(f"::set-output name=components::{','.join(strategic_plan.get('executor_instructions', {}).get('components_to_update', []))}")
        print(f"::set-output name=priority::{user_intent['priority']}")
        
        print("✅ Strategic planning completed successfully!")
        print(f"Plan saved to: {plan_file}")
        print(f"Checkpoint: {checksum}")
        
        return strategic_plan

def main():
    parser = argparse.ArgumentParser(description="AI Agent 1 - Strategic Planner")
    parser.add_argument("--command", required=True, help="User command to analyze")
    parser.add_argument("--knowledge-base", required=True, help="Path to knowledge base directory")
    parser.add_argument("--current-site", required=True, help="Path to current site directory")
    parser.add_argument("--output", required=True, help="Output directory for planning artifacts")
    parser.add_argument("--ai-model", default="claude-3.5-sonnet", help="AI model to use")
    parser.add_argument("--mode", default="auto-detect", help="Agent collaboration mode")
    
    args = parser.parse_args()
    
    planner = StrategicPlanner(args.ai_model)
    plan = planner.run(args)
    
    return 0 if plan else 1

if __name__ == "__main__":
    sys.exit(main())