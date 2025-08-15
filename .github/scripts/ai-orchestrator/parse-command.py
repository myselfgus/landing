#!/usr/bin/env python3
"""
AI Orchestrator Command Parser
Parses user commands from GitHub comments and determines what actions to take.
"""

import json
import re
import argparse
import os
from typing import Dict, List, Set

class AICommandParser:
    def __init__(self):
        self.commands = {
            # Performance commands
            'performance': ['performance', 'speed', 'lighthouse', 'metrics', 'load'],
            'content': ['content', 'text', 'copy', 'writing', 'readability'],
            'visual': ['visual', 'design', 'ui', 'ux', 'layout', 'graphics'],
            'seo': ['seo', 'search', 'ranking', 'meta', 'keywords'],
            'code': ['code', 'quality', 'refactor', 'clean', 'optimize'],
            'full': ['full', 'complete', 'all', 'everything', 'comprehensive'],
            'security': ['security', 'vulnerability', 'safety', 'audit'],
            'accessibility': ['accessibility', 'a11y', 'wcag', 'inclusive'],
        }
        
        self.ai_models = {
            'claude': 'claude-3.5-sonnet',
            'gpt': 'gpt-4',
            'llama': 'llama-3.1-405b',
            'openai': 'gpt-4',
            'anthropic': 'claude-3.5-sonnet'
        }
        
        self.modes = {
            'analyze': 'analysis-only',
            'implement': 'auto-implement', 
            'suggest': 'suggestions-only',
            'create-issues': 'create-issues',
            'report': 'report-only'
        }

    def parse_comment(self, comment_body: str) -> Dict:
        """Parse GitHub comment for AI orchestrator commands."""
        if not comment_body:
            return self._default_response()
            
        comment_lower = comment_body.lower()
        
        # Extract AI model preference
        ai_model = self._extract_ai_model(comment_lower)
        
        # Extract tasks to perform
        tasks = self._extract_tasks(comment_lower)
        
        # Extract mode (analyze, implement, suggest, etc.)
        mode = self._extract_mode(comment_lower)
        
        # Extract priority level
        priority = self._extract_priority(comment_lower)
        
        # Extract context/focus areas
        context = self._extract_context(comment_body)
        
        return {
            'ai_model': ai_model,
            'tasks': ','.join(tasks),
            'mode': mode,
            'priority': priority,
            'context': context,
            'raw_command': comment_body
        }

    def _extract_ai_model(self, comment: str) -> str:
        """Extract preferred AI model from comment."""
        for keyword, model in self.ai_models.items():
            if keyword in comment:
                return model
        return 'claude-3.5-sonnet'  # default

    def _extract_tasks(self, comment: str) -> List[str]:
        """Extract tasks to perform from comment."""
        tasks = set()
        
        # Check for specific task keywords
        for task_type, keywords in self.commands.items():
            if any(keyword in comment for keyword in keywords):
                tasks.add(task_type)
                
        # If 'full' is requested, add all tasks
        if 'full' in tasks:
            tasks = {'performance', 'content', 'visual', 'seo', 'code', 'security', 'accessibility'}
            
        # Default to content analysis if no specific tasks found
        if not tasks:
            tasks = {'content', 'performance'}
            
        return list(tasks)

    def _extract_mode(self, comment: str) -> str:
        """Extract operation mode from comment."""
        for keyword, mode in self.modes.items():
            if keyword in comment:
                return mode
        return 'analysis-only'  # default

    def _extract_priority(self, comment: str) -> str:
        """Extract priority level from comment."""
        if any(word in comment for word in ['urgent', 'critical', 'asap', 'emergency']):
            return 'critical'
        elif any(word in comment for word in ['high', 'important', 'priority']):
            return 'high'
        elif any(word in comment for word in ['low', 'later', 'when possible']):
            return 'low'
        return 'medium'

    def _extract_context(self, comment: str) -> str:
        """Extract context and specific requirements from comment."""
        # Look for specific mentions of features, pages, components
        context_patterns = [
            r'landing\s+page',
            r'voither\s+\w+',
            r'medical\s*scribe',
            r'background\s+content',
            r'visual\s+\w+',
            r'concept\s+tree',
            r'organization\s+chart'
        ]
        
        contexts = []
        for pattern in context_patterns:
            matches = re.findall(pattern, comment, re.IGNORECASE)
            contexts.extend(matches)
            
        return ', '.join(contexts) if contexts else 'general site improvement'

    def _default_response(self) -> Dict:
        """Default response when no specific command is found."""
        return {
            'ai_model': 'claude-3.5-sonnet',
            'tasks': 'content,performance',
            'mode': 'analysis-only',
            'priority': 'medium',
            'context': 'automated analysis trigger',
            'raw_command': ''
        }

def main():
    parser = argparse.ArgumentParser(description='Parse AI orchestrator commands')
    parser.add_argument('--event-type', required=True, help='GitHub event type')
    parser.add_argument('--comment-body', default='', help='Comment body text')
    parser.add_argument('--analysis-type', default='auto', help='Manual analysis type')
    parser.add_argument('--ai-model', default='claude-3.5-sonnet', help='AI model to use')
    
    args = parser.parse_args()
    
    orchestrator = AICommandParser()
    
    # Parse command based on event type
    if args.event_type in ['issue_comment', 'pull_request_review_comment']:
        result = orchestrator.parse_comment(args.comment_body)
    elif args.event_type == 'workflow_dispatch':
        # Manual trigger with specific parameters
        result = {
            'ai_model': args.ai_model,
            'tasks': args.analysis_type if args.analysis_type != 'auto' else 'content,performance',
            'mode': 'analysis-only',
            'priority': 'medium',
            'context': 'manual workflow dispatch',
            'raw_command': f'Manual trigger: {args.analysis_type}'
        }
    elif args.event_type == 'schedule':
        # Scheduled analysis
        result = {
            'ai_model': 'claude-3.5-sonnet',
            'tasks': 'performance,content,seo',
            'mode': 'analysis-only',
            'priority': 'low',
            'context': 'scheduled weekly analysis',
            'raw_command': 'Automated weekly analysis'
        }
    else:
        result = orchestrator._default_response()
    
    # Output results for GitHub Actions
    if 'GITHUB_OUTPUT' in os.environ:
        with open(os.environ['GITHUB_OUTPUT'], 'a') as f:
            for key, value in result.items():
                f.write(f"{key.replace('_', '-')}={value}\n")
    
    # Also output as JSON for debugging
    print(json.dumps(result, indent=2))

if __name__ == '__main__':
    main()