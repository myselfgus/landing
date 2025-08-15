#!/usr/bin/env python3
"""
AI-Powered Recommendation Generator
Generates comprehensive recommendations based on all analysis results.
"""

import json
import argparse
import os
from datetime import datetime
from typing import Dict, List

class RecommendationGenerator:
    def __init__(self, ai_model: str = 'claude-3.5-sonnet'):
        self.ai_model = ai_model

    def generate_recommendations(self, analysis_dir: str, background_dir: str, output_dir: str, context: str = '') -> Dict:
        """Generate comprehensive AI-powered recommendations."""
        os.makedirs(output_dir, exist_ok=True)
        
        # Load all analysis results
        analysis_data = self._load_analysis_data(analysis_dir)
        background_data = self._load_background_data(background_dir)
        
        # Generate prioritized recommendations
        recommendations = {
            'critical': self._generate_critical_recommendations(analysis_data),
            'high': self._generate_high_priority_recommendations(analysis_data, background_data),
            'medium': self._generate_medium_priority_recommendations(analysis_data, background_data),
            'low': self._generate_low_priority_recommendations(analysis_data)
        }
        
        # Generate implementation roadmap
        roadmap = self._create_implementation_roadmap(recommendations)
        
        # Generate AI insights and strategic recommendations
        ai_insights = self._generate_ai_strategic_insights(analysis_data, background_data, context)
        
        # Calculate impact scores
        impact_analysis = self._calculate_impact_scores(recommendations)
        
        report = {
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'context': context,
            'ai_model': self.ai_model,
            'recommendations': recommendations,
            'implementation_roadmap': roadmap,
            'ai_strategic_insights': ai_insights,
            'impact_analysis': impact_analysis,
            'summary': self._generate_executive_summary(recommendations, ai_insights, impact_analysis)
        }
        
        # Save comprehensive report
        with open(os.path.join(output_dir, 'comprehensive_recommendations.json'), 'w') as f:
            json.dump(report, f, indent=2)
        
        # Generate summary for GitHub comments
        self._generate_summary_markdown(report, output_dir)
        
        # Generate detailed HTML report
        self._generate_html_report(report, output_dir)
        
        return report

    def _load_analysis_data(self, analysis_dir: str) -> Dict:
        """Load all analysis results."""
        data = {}
        
        if not os.path.exists(analysis_dir):
            return data
        
        analysis_files = [
            'performance_analysis.json',
            'content_analysis.json',
            'visual_enhancements.json',
            'seo_analysis.json',
            'code_analysis.json'
        ]
        
        for file_name in analysis_files:
            file_path = os.path.join(analysis_dir, file_name.replace('_analysis', ''), file_name)
            if os.path.exists(file_path):
                try:
                    with open(file_path, 'r') as f:
                        data[file_name.replace('_analysis.json', '')] = json.load(f)
                except Exception as e:
                    print(f"Warning: Could not load {file_name}: {e}")
                    continue
        
        return data

    def _load_background_data(self, background_dir: str) -> Dict:
        """Load background content data."""
        if not os.path.exists(background_dir):
            return {}
        
        # Load metadata if available
        metadata_path = os.path.join(background_dir, 'metadata.json')
        if os.path.exists(metadata_path):
            try:
                with open(metadata_path, 'r') as f:
                    return json.load(f)
            except Exception:
                pass
        
        return {'status': 'Background data available but no metadata found'}

    def _generate_critical_recommendations(self, analysis_data: Dict) -> List[Dict]:
        """Generate critical priority recommendations that need immediate attention."""
        critical = []
        
        # Performance critical issues
        performance = analysis_data.get('performance', {})
        performance_score = performance.get('lighthouse_score', {}).get('performance', 1.0)
        if performance_score < 0.5:
            critical.append({
                'category': 'Performance',
                'title': 'Critical Performance Issues Detected',
                'description': 'Website performance is severely impacting user experience',
                'impact': 'High user bounce rate, poor SEO rankings, lost conversions',
                'action_required': 'Immediate optimization of Core Web Vitals',
                'estimated_effort': '2-3 days',
                'expected_improvement': '40-60% performance increase'
            })
        
        # Content critical issues
        content = analysis_data.get('content', {})
        content_score = content.get('content_optimization_score', 100)
        if content_score < 40:
            critical.append({
                'category': 'Content',
                'title': 'Critical Content Quality Issues',
                'description': 'Content quality is below acceptable standards',
                'impact': 'Poor user engagement, low conversion rates',
                'action_required': 'Complete content review and optimization',
                'estimated_effort': '3-5 days',
                'expected_improvement': '50-70% content quality increase'
            })
        
        # SEO critical issues
        seo = analysis_data.get('seo', {})
        if seo and seo.get('critical_issues'):
            critical.append({
                'category': 'SEO',
                'title': 'Critical SEO Problems',
                'description': 'Major SEO issues preventing search visibility',
                'impact': 'Poor search rankings, reduced organic traffic',
                'action_required': 'Fix meta tags, improve page structure',
                'estimated_effort': '1-2 days',
                'expected_improvement': '30-50% SEO score increase'
            })
        
        return critical

    def _generate_high_priority_recommendations(self, analysis_data: Dict, background_data: Dict) -> List[Dict]:
        """Generate high priority recommendations for significant improvements."""
        high_priority = []
        
        # Visual enhancement opportunities
        visual = analysis_data.get('visual', {})
        if visual.get('visual_enhancement_score', 0) < 75:
            high_priority.append({
                'category': 'Visual Design',
                'title': 'Implement Interactive Visual Elements',
                'description': 'Add concept trees, organizational charts, and interactive knowledge graphs',
                'impact': 'Enhanced user engagement, better content comprehension',
                'action_required': 'Integrate generated visual assets and interactive components',
                'estimated_effort': '3-4 days',
                'expected_improvement': 'Significantly improved user experience'
            })
        
        # Content enhancement with background knowledge
        content = analysis_data.get('content', {})
        content_gaps = content.get('content_analysis', {}).get('ai_insights', {}).get('content_gaps', [])
        if content_gaps:
            high_priority.append({
                'category': 'Content Strategy',
                'title': 'Fill Content Gaps with Background Knowledge',
                'description': f'Address {len(content_gaps)} identified content gaps using available background research',
                'impact': 'More comprehensive content, better topic coverage',
                'action_required': 'Integrate background knowledge into website content',
                'estimated_effort': '2-3 days',
                'expected_improvement': 'Richer, more authoritative content'
            })
        
        # Performance optimization
        performance = analysis_data.get('performance', {})
        if performance.get('ai_insights', {}).get('optimization_opportunities'):
            high_priority.append({
                'category': 'Performance',
                'title': 'Implement Performance Optimizations',
                'description': 'Apply identified performance improvements for better user experience',
                'impact': 'Faster load times, better Core Web Vitals scores',
                'action_required': 'Optimize images, minimize CSS/JS, improve caching',
                'estimated_effort': '2-3 days',
                'expected_improvement': '20-40% performance improvement'
            })
        
        # AI-powered automation
        high_priority.append({
            'category': 'Automation',
            'title': 'Enhance AI Orchestrator Capabilities',
            'description': 'Integrate GitHub Models for real-time AI analysis and content generation',
            'impact': 'Automated content optimization, real-time insights',
            'action_required': 'Configure GitHub Models API, implement AI workflows',
            'estimated_effort': '3-5 days',
            'expected_improvement': 'Continuous site optimization with AI'
        })
        
        return high_priority

    def _generate_medium_priority_recommendations(self, analysis_data: Dict, background_data: Dict) -> List[Dict]:
        """Generate medium priority recommendations for ongoing improvements."""
        medium_priority = []
        
        # Content freshness and maintenance
        medium_priority.append({
            'category': 'Content Maintenance',
            'title': 'Implement Content Versioning and Freshness Tracking',
            'description': 'Add timestamps and version control for content updates',
            'impact': 'Better content management, improved SEO signals',
            'action_required': 'Add content metadata, implement update tracking',
            'estimated_effort': '1-2 days',
            'expected_improvement': 'Better content lifecycle management'
        })
        
        # Enhanced analytics and monitoring
        medium_priority.append({
            'category': 'Analytics',
            'title': 'Advanced Performance Monitoring',
            'description': 'Implement comprehensive monitoring and analytics dashboard',
            'impact': 'Better insights into user behavior and site performance',
            'action_required': 'Set up monitoring tools, create dashboards',
            'estimated_effort': '2-3 days',
            'expected_improvement': 'Data-driven optimization decisions'
        })
        
        # Accessibility improvements
        medium_priority.append({
            'category': 'Accessibility',
            'title': 'Enhance Website Accessibility',
            'description': 'Improve WCAG compliance and inclusive design',
            'impact': 'Broader audience reach, better user experience for all',
            'action_required': 'Audit accessibility, implement ARIA labels, improve contrast',
            'estimated_effort': '2-3 days',
            'expected_improvement': 'WCAG 2.1 AA compliance'
        })
        
        # Advanced SEO features
        medium_priority.append({
            'category': 'SEO Enhancement',
            'title': 'Implement Advanced SEO Features',
            'description': 'Add structured data, improve internal linking, optimize for voice search',
            'impact': 'Better search visibility, rich snippets, voice search optimization',
            'action_required': 'Implement schema markup, optimize content structure',
            'estimated_effort': '2-3 days',
            'expected_improvement': '15-25% increase in organic visibility'
        })
        
        return medium_priority

    def _generate_low_priority_recommendations(self, analysis_data: Dict) -> List[Dict]:
        """Generate low priority recommendations for future enhancements."""
        low_priority = []
        
        # Progressive Web App features
        low_priority.append({
            'category': 'PWA',
            'title': 'Progressive Web App Implementation',
            'description': 'Add service workers, offline capabilities, and app-like features',
            'impact': 'Enhanced mobile experience, offline access',
            'action_required': 'Implement PWA manifest, service workers, caching strategy',
            'estimated_effort': '3-5 days',
            'expected_improvement': 'App-like experience on mobile devices'
        })
        
        # Advanced interactivity
        low_priority.append({
            'category': 'Interactivity',
            'title': 'Advanced Interactive Features',
            'description': 'Add chatbot, interactive demos, and personalization',
            'impact': 'Enhanced user engagement, personalized experience',
            'action_required': 'Implement AI chatbot, create interactive demos',
            'estimated_effort': '5-7 days',
            'expected_improvement': 'Highly engaging user experience'
        })
        
        # Internationalization
        low_priority.append({
            'category': 'i18n',
            'title': 'Multi-language Support',
            'description': 'Implement internationalization for global reach',
            'impact': 'Expanded global audience, improved accessibility',
            'action_required': 'Set up i18n framework, translate content',
            'estimated_effort': '4-6 days',
            'expected_improvement': 'Global market accessibility'
        })
        
        return low_priority

    def _create_implementation_roadmap(self, recommendations: Dict) -> Dict:
        """Create a phased implementation roadmap."""
        return {
            'phase_1_immediate': {
                'duration': '1-2 weeks',
                'focus': 'Critical issues and high-impact improvements',
                'tasks': [rec['title'] for rec in recommendations.get('critical', [])] + 
                        [rec['title'] for rec in recommendations.get('high', [])[:2]]
            },
            'phase_2_short_term': {
                'duration': '2-4 weeks',
                'focus': 'Medium priority enhancements and optimization',
                'tasks': [rec['title'] for rec in recommendations.get('high', [])][2:] + 
                        [rec['title'] for rec in recommendations.get('medium', [])[:3]]
            },
            'phase_3_medium_term': {
                'duration': '1-2 months',
                'focus': 'Advanced features and long-term improvements',
                'tasks': [rec['title'] for rec in recommendations.get('medium', [])][3:] + 
                        [rec['title'] for rec in recommendations.get('low', [])[:2]]
            },
            'phase_4_long_term': {
                'duration': '2-3 months',
                'focus': 'Innovation and future-proofing',
                'tasks': [rec['title'] for rec in recommendations.get('low', [])][2:]
            }
        }

    def _generate_ai_strategic_insights(self, analysis_data: Dict, background_data: Dict, context: str) -> Dict:
        """Generate strategic AI insights and future recommendations."""
        return {
            'overall_assessment': self._assess_overall_site_maturity(analysis_data),
            'competitive_positioning': self._analyze_competitive_position(analysis_data),
            'growth_opportunities': self._identify_growth_opportunities(analysis_data, background_data),
            'technology_recommendations': self._recommend_technologies(analysis_data),
            'ai_integration_strategy': self._create_ai_integration_strategy(context),
            'future_proofing': self._suggest_future_proofing_measures(analysis_data)
        }

    def _assess_overall_site_maturity(self, analysis_data: Dict) -> Dict:
        """Assess overall website maturity level."""
        scores = []
        
        # Collect scores from different analyses
        if 'performance' in analysis_data:
            perf_score = analysis_data['performance'].get('lighthouse_score', {}).get('performance', 0.5)
            scores.append(perf_score * 100)
        
        if 'content' in analysis_data:
            content_score = analysis_data['content'].get('content_optimization_score', 50)
            scores.append(content_score)
        
        if 'visual' in analysis_data:
            visual_score = analysis_data['visual'].get('visual_enhancement_score', 50)
            scores.append(visual_score)
        
        avg_score = sum(scores) / len(scores) if scores else 50
        
        if avg_score >= 80:
            maturity = 'Advanced'
            description = 'Website demonstrates high technical and content quality'
        elif avg_score >= 60:
            maturity = 'Intermediate'
            description = 'Website has solid foundation with room for optimization'
        elif avg_score >= 40:
            maturity = 'Developing'
            description = 'Website needs significant improvements across multiple areas'
        else:
            maturity = 'Basic'
            description = 'Website requires fundamental improvements'
        
        return {
            'maturity_level': maturity,
            'overall_score': avg_score,
            'description': description,
            'strengths': self._identify_strengths(analysis_data),
            'weaknesses': self._identify_weaknesses(analysis_data)
        }

    def _identify_strengths(self, analysis_data: Dict) -> List[str]:
        """Identify website strengths."""
        strengths = []
        
        # Performance strengths
        performance = analysis_data.get('performance', {})
        perf_score = performance.get('lighthouse_score', {}).get('performance', 0.5)
        if perf_score > 0.7:
            strengths.append('Good performance optimization')
        
        # Content strengths
        content = analysis_data.get('content', {})
        content_score = content.get('content_optimization_score', 50)
        if content_score > 70:
            strengths.append('High-quality content')
        
        # Visual strengths
        visual = analysis_data.get('visual', {})
        if visual.get('visual_enhancement_score', 0) > 60:
            strengths.append('Strong visual design foundation')
        
        if not strengths:
            strengths.append('Potential for significant improvement across all areas')
        
        return strengths

    def _identify_weaknesses(self, analysis_data: Dict) -> List[str]:
        """Identify website weaknesses."""
        weaknesses = []
        
        # Performance weaknesses
        performance = analysis_data.get('performance', {})
        perf_score = performance.get('lighthouse_score', {}).get('performance', 0.5)
        if perf_score < 0.6:
            weaknesses.append('Performance optimization needed')
        
        # Content weaknesses
        content = analysis_data.get('content', {})
        content_score = content.get('content_optimization_score', 50)
        if content_score < 60:
            weaknesses.append('Content quality requires improvement')
        
        # Visual weaknesses
        visual = analysis_data.get('visual', {})
        if visual.get('visual_enhancement_score', 0) < 50:
            weaknesses.append('Limited visual engagement elements')
        
        return weaknesses

    def _analyze_competitive_position(self, analysis_data: Dict) -> Dict:
        """Analyze competitive positioning."""
        performance = analysis_data.get('performance', {})
        perf_score = performance.get('lighthouse_score', {}).get('performance', 0.5)
        
        if perf_score >= 0.8:
            position = 'Leading'
            description = 'Performance exceeds industry standards'
        elif perf_score >= 0.6:
            position = 'Competitive'
            description = 'Performance meets industry standards'
        else:
            position = 'Behind'
            description = 'Performance below industry standards'
        
        return {
            'position': position,
            'description': description,
            'benchmark_comparison': f'{perf_score * 100:.0f}% vs industry average 65%',
            'competitive_advantages': ['AI-powered automation', 'Comprehensive background knowledge'],
            'areas_for_improvement': ['Performance optimization', 'Visual engagement']
        }

    def _identify_growth_opportunities(self, analysis_data: Dict, background_data: Dict) -> List[Dict]:
        """Identify growth opportunities."""
        opportunities = [
            {
                'area': 'AI-Powered Content Generation',
                'description': 'Leverage background knowledge for automated content creation',
                'potential_impact': 'High',
                'implementation_complexity': 'Medium'
            },
            {
                'area': 'Interactive Knowledge Exploration',
                'description': 'Create interactive tools for exploring medical AI concepts',
                'potential_impact': 'High',
                'implementation_complexity': 'High'
            },
            {
                'area': 'Personalized User Experience',
                'description': 'Use AI to personalize content based on user interests',
                'potential_impact': 'Medium',
                'implementation_complexity': 'High'
            }
        ]
        
        return opportunities

    def _recommend_technologies(self, analysis_data: Dict) -> Dict:
        """Recommend technologies for improvement."""
        return {
            'performance_tools': ['Vite for faster builds', 'Image optimization services', 'CDN implementation'],
            'ai_integration': ['GitHub Models API', 'OpenAI GPT integration', 'Hugging Face transformers'],
            'analytics': ['Google Analytics 4', 'Hotjar for UX insights', 'Core Web Vitals monitoring'],
            'development': ['TypeScript for better code quality', 'Tailwind CSS for efficient styling', 'React Query for data fetching']
        }

    def _create_ai_integration_strategy(self, context: str) -> Dict:
        """Create strategy for AI integration."""
        return {
            'immediate_steps': [
                'Configure GitHub Models API access',
                'Implement AI-powered content analysis',
                'Set up automated recommendation generation'
            ],
            'medium_term_goals': [
                'Real-time content optimization',
                'Predictive user experience improvements',
                'Automated A/B testing with AI insights'
            ],
            'long_term_vision': [
                'Fully autonomous website optimization',
                'AI-driven content strategy',
                'Predictive user behavior modeling'
            ],
            'required_resources': [
                'GitHub Models API credits',
                'AI/ML expertise',
                'Data infrastructure setup'
            ]
        }

    def _suggest_future_proofing_measures(self, analysis_data: Dict) -> List[str]:
        """Suggest measures for future-proofing the website."""
        return [
            'Implement headless CMS for content flexibility',
            'Use modern web standards (Web Components, ES modules)',
            'Design for emerging devices (AR/VR, voice interfaces)',
            'Build with scalability in mind (microservices, edge computing)',
            'Prepare for AI regulation compliance',
            'Implement sustainable web design practices'
        ]

    def _calculate_impact_scores(self, recommendations: Dict) -> Dict:
        """Calculate impact scores for recommendations."""
        impact_scores = {}
        
        for priority_level, recs in recommendations.items():
            total_impact = 0
            for rec in recs:
                # Simple impact scoring based on category and priority
                category_weight = {
                    'Performance': 25,
                    'Content': 20,
                    'Visual Design': 15,
                    'SEO': 20,
                    'Automation': 15,
                    'Accessibility': 10
                }.get(rec.get('category', ''), 10)
                
                priority_multiplier = {
                    'critical': 1.0,
                    'high': 0.8,
                    'medium': 0.6,
                    'low': 0.4
                }.get(priority_level, 0.5)
                
                impact = category_weight * priority_multiplier
                total_impact += impact
            
            impact_scores[priority_level] = total_impact
        
        return {
            'by_priority': impact_scores,
            'total_potential_impact': sum(impact_scores.values()),
            'recommended_focus': max(impact_scores.items(), key=lambda x: x[1])[0] if impact_scores else 'critical'
        }

    def _generate_executive_summary(self, recommendations: Dict, ai_insights: Dict, impact_analysis: Dict) -> Dict:
        """Generate executive summary of recommendations."""
        total_recs = sum(len(recs) for recs in recommendations.values())
        critical_count = len(recommendations.get('critical', []))
        
        return {
            'total_recommendations': total_recs,
            'critical_issues': critical_count,
            'overall_maturity': ai_insights.get('overall_assessment', {}).get('maturity_level', 'Unknown'),
            'recommended_priority': impact_analysis.get('recommended_focus', 'critical'),
            'estimated_total_effort': '2-4 weeks for immediate improvements',
            'expected_roi': 'High - significant improvements in user experience and performance',
            'key_next_steps': [
                'Address critical performance issues immediately',
                'Implement visual enhancements for better engagement',
                'Integrate AI-powered automation for continuous optimization',
                'Establish monitoring and analytics for data-driven decisions'
            ]
        }

    def _generate_summary_markdown(self, report: Dict, output_dir: str):
        """Generate markdown summary for GitHub comments."""
        summary = report.get('summary', {})
        critical_recs = report.get('recommendations', {}).get('critical', [])
        high_recs = report.get('recommendations', {}).get('high', [])
        
        markdown_content = f"""## 🤖 AI Orchestrator Analysis Complete

### 📊 Executive Summary
- **Total Recommendations**: {summary.get('total_recommendations', 0)}
- **Critical Issues**: {summary.get('critical_issues', 0)}
- **Website Maturity**: {summary.get('overall_maturity', 'Unknown')}
- **Recommended Focus**: {summary.get('recommended_priority', 'critical').title()}

### 🚨 Critical Actions Required
{"".join([f"- **{rec['title']}**: {rec['description']}" for rec in critical_recs[:3]])}

### 🎯 High Priority Improvements
{"".join([f"- **{rec['title']}**: {rec['description']}" for rec in high_recs[:3]])}

### 📈 Expected Impact
- **Effort Required**: {summary.get('estimated_total_effort', '2-4 weeks')}
- **Expected ROI**: {summary.get('expected_roi', 'High')}

### 🛠️ Implementation Roadmap
View the detailed implementation plan in the analysis reports for phased execution.

---
*Generated by AI Orchestrator on {report['timestamp']}*
"""
        
        with open(os.path.join(output_dir, 'summary.md'), 'w') as f:
            f.write(markdown_content)

    def _generate_html_report(self, report: Dict, output_dir: str):
        """Generate comprehensive HTML report."""
        summary = report.get('summary', {})
        ai_insights = report.get('ai_strategic_insights', {})
        
        html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Orchestrator Comprehensive Report</title>
    <style>
        body {{ font-family: Inter, -apple-system, sans-serif; margin: 0; padding: 20px; background: #f8fafc; line-height: 1.6; }}
        .header {{ background: linear-gradient(135deg, #1e3a8a, #3b82f6); color: white; padding: 40px; border-radius: 16px; text-align: center; }}
        .summary-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin: 30px 0; }}
        .summary-card {{ background: white; padding: 25px; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); text-align: center; }}
        .summary-number {{ font-size: 2.5em; font-weight: bold; color: #3b82f6; }}
        .recommendations {{ margin: 30px 0; }}
        .priority-section {{ background: white; margin: 20px 0; padding: 25px; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); }}
        .critical {{ border-left: 5px solid #ef4444; }}
        .high {{ border-left: 5px solid #f59e0b; }}
        .medium {{ border-left: 5px solid #3b82f6; }}
        .low {{ border-left: 5px solid #10b981; }}
        .recommendation {{ margin: 15px 0; padding: 15px; background: #f9fafb; border-radius: 8px; }}
        .roadmap {{ background: white; padding: 25px; border-radius: 12px; margin: 20px 0; }}
        .phase {{ margin: 20px 0; padding: 15px; background: #f0f9ff; border-radius: 8px; border-left: 4px solid #3b82f6; }}
        .insights {{ background: linear-gradient(135deg, #ecfdf5, #f0fdf4); padding: 25px; border-radius: 12px; margin: 20px 0; }}
        .badge {{ display: inline-block; padding: 4px 12px; border-radius: 20px; font-size: 12px; font-weight: bold; margin: 2px; }}
        .critical-badge {{ background: #fee2e2; color: #dc2626; }}
        .high-badge {{ background: #fef3c7; color: #d97706; }}
        .medium-badge {{ background: #dbeafe; color: #2563eb; }}
        .low-badge {{ background: #d1fae5; color: #059669; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🤖 AI Orchestrator Comprehensive Report</h1>
        <p>Generated on {report['timestamp']}</p>
        <p><strong>AI Model:</strong> {report['ai_model']}</p>
    </div>

    <div class="summary-grid">
        <div class="summary-card">
            <div class="summary-number">{summary.get('total_recommendations', 0)}</div>
            <div>Total Recommendations</div>
        </div>
        <div class="summary-card">
            <div class="summary-number">{summary.get('critical_issues', 0)}</div>
            <div>Critical Issues</div>
        </div>
        <div class="summary-card">
            <div class="summary-number">{summary.get('overall_maturity', 'Unknown')}</div>
            <div>Website Maturity</div>
        </div>
        <div class="summary-card">
            <div class="summary-number">{report.get('impact_analysis', {}).get('total_potential_impact', 0):.0f}</div>
            <div>Impact Score</div>
        </div>
    </div>

    <div class="recommendations">
        <h2>📋 Prioritized Recommendations</h2>
        
        {"".join([f'''
        <div class="priority-section {priority}">
            <h3>🚨 {priority.title()} Priority</h3>
            {"".join([f'''
            <div class="recommendation">
                <h4>{rec["title"]} <span class="badge {priority}-badge">{rec["category"]}</span></h4>
                <p><strong>Description:</strong> {rec["description"]}</p>
                <p><strong>Impact:</strong> {rec.get("impact", "Not specified")}</p>
                <p><strong>Effort:</strong> {rec.get("estimated_effort", "Not specified")}</p>
                <p><strong>Expected Improvement:</strong> {rec.get("expected_improvement", "Not specified")}</p>
            </div>
            ''' for rec in recs])}
        </div>
        ''' for priority, recs in report.get('recommendations', {}).items() if recs])}
    </div>

    <div class="roadmap">
        <h2>🛣️ Implementation Roadmap</h2>
        {"".join([f'''
        <div class="phase">
            <h4>Phase {i+1}: {phase_data.get("focus", "")}</h4>
            <p><strong>Duration:</strong> {phase_data.get("duration", "")}</p>
            <ul>
                {"".join([f"<li>{task}</li>" for task in phase_data.get("tasks", [])])}
            </ul>
        </div>
        ''' for i, (phase_name, phase_data) in enumerate(report.get('implementation_roadmap', {}).items())])}
    </div>

    <div class="insights">
        <h2>🧠 AI Strategic Insights</h2>
        <div class="summary-grid">
            <div class="summary-card">
                <h4>Overall Assessment</h4>
                <p><strong>Maturity:</strong> {ai_insights.get('overall_assessment', {}).get('maturity_level', 'Unknown')}</p>
                <p><strong>Score:</strong> {ai_insights.get('overall_assessment', {}).get('overall_score', 0):.0f}%</p>
            </div>
            <div class="summary-card">
                <h4>Competitive Position</h4>
                <p><strong>Position:</strong> {ai_insights.get('competitive_positioning', {}).get('position', 'Unknown')}</p>
                <p>{ai_insights.get('competitive_positioning', {}).get('description', '')}</p>
            </div>
        </div>
        
        <h4>Growth Opportunities</h4>
        {"".join([f'''
        <div class="recommendation">
            <h5>{opp["area"]}</h5>
            <p>{opp["description"]}</p>
            <span class="badge medium-badge">Impact: {opp["potential_impact"]}</span>
            <span class="badge low-badge">Complexity: {opp["implementation_complexity"]}</span>
        </div>
        ''' for opp in ai_insights.get('growth_opportunities', [])])}
    </div>

    <div class="insights">
        <h2>🎯 Key Next Steps</h2>
        <ul>
            {"".join([f"<li>{step}</li>" for step in summary.get('key_next_steps', [])])}
        </ul>
    </div>
</body>
</html>
        """
        
        with open(os.path.join(output_dir, 'comprehensive_report.html'), 'w') as f:
            f.write(html_content)

def main():
    parser = argparse.ArgumentParser(description='Generate AI-powered recommendations')
    parser.add_argument('--analysis-dir', required=True, help='Analysis results directory')
    parser.add_argument('--background-dir', required=True, help='Background content directory')
    parser.add_argument('--output', required=True, help='Output directory')
    parser.add_argument('--ai-model', default='claude-3.5-sonnet', help='AI model to use')
    parser.add_argument('--context', default='', help='Context for recommendations')
    
    args = parser.parse_args()
    
    generator = RecommendationGenerator(ai_model=args.ai_model)
    report = generator.generate_recommendations(
        args.analysis_dir, 
        args.background_dir, 
        args.output, 
        args.context
    )
    
    print(f"Recommendations generation complete. Report saved to {args.output}")
    print(f"Total recommendations: {report.get('summary', {}).get('total_recommendations', 0)}")
    print(f"Critical issues: {report.get('summary', {}).get('critical_issues', 0)}")

if __name__ == '__main__':
    main()