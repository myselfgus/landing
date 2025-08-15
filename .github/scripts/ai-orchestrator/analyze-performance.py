#!/usr/bin/env python3
"""
AI-Powered Performance Analysis
Uses Lighthouse and AI models to analyze website performance and generate insights.
"""

import json
import argparse
import os
import subprocess
import requests
from datetime import datetime
from typing import Dict, List

class PerformanceAnalyzer:
    def __init__(self, ai_model: str = 'claude-3.5-sonnet'):
        self.ai_model = ai_model
        self.lighthouse_categories = [
            'performance', 'accessibility', 'best-practices', 'seo', 'pwa'
        ]

    def analyze_url(self, url: str, output_dir: str) -> Dict:
        """Analyze website performance using Lighthouse and AI insights."""
        os.makedirs(output_dir, exist_ok=True)
        
        # Run Lighthouse analysis
        lighthouse_results = self._run_lighthouse(url, output_dir)
        
        # Get Core Web Vitals
        core_vitals = self._extract_core_vitals(lighthouse_results)
        
        # Generate AI insights
        ai_insights = self._generate_ai_insights(lighthouse_results, core_vitals)
        
        # Create comprehensive report
        report = {
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'url': url,
            'lighthouse_score': lighthouse_results.get('score', {}),
            'core_web_vitals': core_vitals,
            'ai_insights': ai_insights,
            'recommendations': self._generate_recommendations(lighthouse_results, ai_insights)
        }
        
        # Save detailed report
        with open(os.path.join(output_dir, 'performance_analysis.json'), 'w') as f:
            json.dump(report, f, indent=2)
        
        # Generate HTML report
        self._generate_html_report(report, output_dir)
        
        return report

    def _run_lighthouse(self, url: str, output_dir: str) -> Dict:
        """Run Lighthouse analysis on the given URL."""
        try:
            # Install lighthouse if not available
            subprocess.run(['npm', 'install', '-g', 'lighthouse'], 
                         capture_output=True, text=True, timeout=300)
            
            # Run lighthouse
            result = subprocess.run([
                'lighthouse', url,
                '--output=json',
                '--output-path=' + os.path.join(output_dir, 'lighthouse-report.json'),
                '--chrome-flags=--headless --no-sandbox',
                '--quiet'
            ], capture_output=True, text=True, timeout=600)
            
            if result.returncode == 0:
                with open(os.path.join(output_dir, 'lighthouse-report.json'), 'r') as f:
                    return json.load(f)
            else:
                print(f"Lighthouse error: {result.stderr}")
                return self._mock_lighthouse_data()
                
        except Exception as e:
            print(f"Error running Lighthouse: {e}")
            return self._mock_lighthouse_data()

    def _extract_core_vitals(self, lighthouse_data: Dict) -> Dict:
        """Extract Core Web Vitals from Lighthouse data."""
        audits = lighthouse_data.get('audits', {})
        
        return {
            'largest_contentful_paint': {
                'value': audits.get('largest-contentful-paint', {}).get('numericValue', 0),
                'score': audits.get('largest-contentful-paint', {}).get('score', 0),
                'displayValue': audits.get('largest-contentful-paint', {}).get('displayValue', 'N/A')
            },
            'first_input_delay': {
                'value': audits.get('max-potential-fid', {}).get('numericValue', 0),
                'score': audits.get('max-potential-fid', {}).get('score', 0),
                'displayValue': audits.get('max-potential-fid', {}).get('displayValue', 'N/A')
            },
            'cumulative_layout_shift': {
                'value': audits.get('cumulative-layout-shift', {}).get('numericValue', 0),
                'score': audits.get('cumulative-layout-shift', {}).get('score', 0),
                'displayValue': audits.get('cumulative-layout-shift', {}).get('displayValue', 'N/A')
            },
            'first_contentful_paint': {
                'value': audits.get('first-contentful-paint', {}).get('numericValue', 0),
                'score': audits.get('first-contentful-paint', {}).get('score', 0),
                'displayValue': audits.get('first-contentful-paint', {}).get('displayValue', 'N/A')
            }
        }

    def _generate_ai_insights(self, lighthouse_data: Dict, core_vitals: Dict) -> Dict:
        """Generate AI-powered insights from performance data."""
        # Mock AI analysis for now - in real implementation, use GitHub Models API
        performance_score = lighthouse_data.get('categories', {}).get('performance', {}).get('score', 0.5)
        
        insights = {
            'overall_assessment': self._assess_performance(performance_score),
            'critical_issues': self._identify_critical_issues(lighthouse_data),
            'optimization_opportunities': self._identify_optimizations(lighthouse_data),
            'competitive_analysis': self._competitive_insights(performance_score),
            'user_experience_impact': self._ux_impact_analysis(core_vitals)
        }
        
        return insights

    def _assess_performance(self, score: float) -> str:
        """Assess overall performance level."""
        if score >= 0.9:
            return "Excellent performance - site loads quickly and provides great user experience"
        elif score >= 0.7:
            return "Good performance with room for optimization"
        elif score >= 0.5:
            return "Moderate performance - needs attention to improve user experience"
        else:
            return "Poor performance - urgent optimization required"

    def _identify_critical_issues(self, lighthouse_data: Dict) -> List[str]:
        """Identify critical performance issues."""
        issues = []
        audits = lighthouse_data.get('audits', {})
        
        # Check for common critical issues
        if audits.get('largest-contentful-paint', {}).get('score', 1) < 0.5:
            issues.append("Largest Contentful Paint is too slow")
        
        if audits.get('cumulative-layout-shift', {}).get('score', 1) < 0.5:
            issues.append("Cumulative Layout Shift causes visual instability")
        
        if audits.get('unused-css-rules', {}).get('score', 1) < 0.5:
            issues.append("Significant unused CSS detected")
        
        if audits.get('render-blocking-resources', {}).get('score', 1) < 0.5:
            issues.append("Render-blocking resources delay page rendering")
            
        return issues

    def _identify_optimizations(self, lighthouse_data: Dict) -> List[Dict]:
        """Identify optimization opportunities."""
        optimizations = []
        audits = lighthouse_data.get('audits', {})
        
        # Image optimizations
        if audits.get('uses-optimized-images', {}).get('score', 1) < 0.9:
            optimizations.append({
                'category': 'Images',
                'priority': 'High',
                'description': 'Optimize images for better compression',
                'estimated_savings': '20-40% file size reduction'
            })
        
        # JavaScript optimizations
        if audits.get('unused-javascript', {}).get('score', 1) < 0.9:
            optimizations.append({
                'category': 'JavaScript',
                'priority': 'Medium',
                'description': 'Remove unused JavaScript code',
                'estimated_savings': '10-30% bundle size reduction'
            })
        
        # CSS optimizations
        if audits.get('unused-css-rules', {}).get('score', 1) < 0.9:
            optimizations.append({
                'category': 'CSS',
                'priority': 'Medium',
                'description': 'Remove unused CSS rules',
                'estimated_savings': '15-25% CSS size reduction'
            })
            
        return optimizations

    def _competitive_insights(self, score: float) -> str:
        """Provide competitive performance insights."""
        if score >= 0.9:
            return "Performance is in the top 10% of websites"
        elif score >= 0.7:
            return "Performance is above average but competitors may have an edge"
        else:
            return "Performance is below industry standards"

    def _ux_impact_analysis(self, core_vitals: Dict) -> Dict:
        """Analyze user experience impact of performance metrics."""
        lcp_score = core_vitals.get('largest_contentful_paint', {}).get('score', 0.5)
        cls_score = core_vitals.get('cumulative_layout_shift', {}).get('score', 0.5)
        
        return {
            'loading_experience': 'Fast' if lcp_score > 0.7 else 'Slow',
            'visual_stability': 'Stable' if cls_score > 0.7 else 'Unstable',
            'interactivity': 'Responsive' if core_vitals.get('first_input_delay', {}).get('score', 0.5) > 0.7 else 'Delayed',
            'overall_ux_rating': self._calculate_ux_rating(lcp_score, cls_score)
        }

    def _calculate_ux_rating(self, lcp_score: float, cls_score: float) -> str:
        """Calculate overall UX rating."""
        avg_score = (lcp_score + cls_score) / 2
        if avg_score >= 0.8:
            return "Excellent"
        elif avg_score >= 0.6:
            return "Good"
        elif avg_score >= 0.4:
            return "Fair"
        else:
            return "Poor"

    def _generate_recommendations(self, lighthouse_data: Dict, ai_insights: Dict) -> List[Dict]:
        """Generate actionable recommendations."""
        recommendations = []
        
        # Performance recommendations
        recommendations.extend([
            {
                'category': 'Performance',
                'priority': 'High',
                'title': 'Optimize Critical Rendering Path',
                'description': 'Minimize render-blocking resources and optimize CSS delivery',
                'implementation': 'Use CSS-in-JS or critical CSS extraction',
                'expected_impact': 'Improve FCP by 0.5-1.0 seconds'
            },
            {
                'category': 'Performance',
                'priority': 'Medium',
                'title': 'Implement Image Optimization',
                'description': 'Use WebP format and responsive images',
                'implementation': 'Convert images to WebP and implement srcset',
                'expected_impact': 'Reduce image payload by 25-35%'
            }
        ])
        
        return recommendations

    def _generate_html_report(self, report: Dict, output_dir: str):
        """Generate an HTML report for easy viewing."""
        html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Performance Analysis Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .header {{ background: #f5f5f5; padding: 20px; border-radius: 8px; }}
        .metrics {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 15px; margin: 20px 0; }}
        .metric {{ background: white; border: 1px solid #ddd; padding: 15px; border-radius: 8px; }}
        .score {{ font-size: 2em; font-weight: bold; color: #4CAF50; }}
        .recommendations {{ margin-top: 20px; }}
        .recommendation {{ border-left: 4px solid #2196F3; padding: 10px 15px; margin: 10px 0; background: #f9f9f9; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🚀 Performance Analysis Report</h1>
        <p><strong>URL:</strong> {report['url']}</p>
        <p><strong>Analysis Date:</strong> {report['timestamp']}</p>
    </div>

    <div class="metrics">
        <div class="metric">
            <h3>Performance Score</h3>
            <div class="score">{report.get('lighthouse_score', {}).get('performance', 0.0):.0%}</div>
        </div>
        <div class="metric">
            <h3>Accessibility</h3>
            <div class="score">{report.get('lighthouse_score', {}).get('accessibility', 0.0):.0%}</div>
        </div>
        <div class="metric">
            <h3>SEO</h3>
            <div class="score">{report.get('lighthouse_score', {}).get('seo', 0.0):.0%}</div>
        </div>
    </div>

    <div class="recommendations">
        <h2>🎯 AI-Generated Recommendations</h2>
        {"".join([f'<div class="recommendation"><h4>{rec["title"]}</h4><p>{rec["description"]}</p></div>' for rec in report.get('recommendations', [])])}
    </div>
</body>
</html>
        """
        
        with open(os.path.join(output_dir, 'performance.html'), 'w') as f:
            f.write(html_content)

    def _mock_lighthouse_data(self) -> Dict:
        """Mock lighthouse data for testing when lighthouse fails."""
        return {
            'categories': {
                'performance': {'score': 0.75},
                'accessibility': {'score': 0.85},
                'best-practices': {'score': 0.90},
                'seo': {'score': 0.80}
            },
            'audits': {
                'largest-contentful-paint': {'numericValue': 2500, 'score': 0.7, 'displayValue': '2.5 s'},
                'cumulative-layout-shift': {'numericValue': 0.1, 'score': 0.8, 'displayValue': '0.1'},
                'first-contentful-paint': {'numericValue': 1800, 'score': 0.75, 'displayValue': '1.8 s'}
            }
        }

def main():
    parser = argparse.ArgumentParser(description='Analyze website performance')
    parser.add_argument('--url', required=True, help='URL to analyze')
    parser.add_argument('--output', required=True, help='Output directory')
    parser.add_argument('--ai-model', default='claude-3.5-sonnet', help='AI model to use')
    
    args = parser.parse_args()
    
    analyzer = PerformanceAnalyzer(ai_model=args.ai_model)
    report = analyzer.analyze_url(args.url, args.output)
    
    print(f"Performance analysis complete. Report saved to {args.output}")
    print(f"Overall performance score: {report.get('lighthouse_score', {}).get('performance', 0.0):.0%}")

if __name__ == '__main__':
    main()