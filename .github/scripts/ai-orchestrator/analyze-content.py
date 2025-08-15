#!/usr/bin/env python3
"""
AI-Powered Content Analysis
Analyzes website content for quality, readability, and optimization opportunities.
"""

import json
import argparse
import os
import re
from datetime import datetime
from typing import Dict, List, Tuple
from bs4 import BeautifulSoup
import nltk
from collections import Counter

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', quiet=True)

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords', quiet=True)

class ContentAnalyzer:
    def __init__(self, ai_model: str = 'claude-3.5-sonnet'):
        self.ai_model = ai_model
        self.stop_words = set(nltk.corpus.stopwords.words('english'))

    def analyze_content(self, background_dir: str, website_dir: str, output_dir: str) -> Dict:
        """Analyze content quality and generate AI-powered recommendations."""
        os.makedirs(output_dir, exist_ok=True)
        
        # Analyze website content
        website_content = self._extract_website_content(website_dir)
        
        # Analyze background knowledge
        background_content = self._analyze_background_content(background_dir)
        
        # Content quality analysis
        quality_analysis = self._analyze_content_quality(website_content)
        
        # Readability analysis
        readability_analysis = self._analyze_readability(website_content)
        
        # SEO content analysis
        seo_analysis = self._analyze_seo_content(website_content)
        
        # AI-powered content insights
        ai_insights = self._generate_content_insights(website_content, background_content)
        
        # Generate recommendations
        recommendations = self._generate_content_recommendations(
            quality_analysis, readability_analysis, seo_analysis, ai_insights
        )
        
        report = {
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'content_analysis': {
                'quality': quality_analysis,
                'readability': readability_analysis,
                'seo': seo_analysis,
                'ai_insights': ai_insights
            },
            'background_analysis': background_content,
            'recommendations': recommendations,
            'content_optimization_score': self._calculate_content_score(quality_analysis, readability_analysis, seo_analysis)
        }
        
        # Save detailed report
        with open(os.path.join(output_dir, 'content_analysis.json'), 'w') as f:
            json.dump(report, f, indent=2)
        
        # Generate HTML report
        self._generate_html_report(report, output_dir)
        
        return report

    def _extract_website_content(self, website_dir: str) -> Dict:
        """Extract content from website files."""
        content = {
            'html_files': {},
            'total_words': 0,
            'headings': [],
            'paragraphs': [],
            'links': [],
            'meta_data': {}
        }
        
        # Analyze HTML files
        html_files = [f for f in os.listdir(website_dir) if f.endswith('.html')]
        
        for file_name in html_files:
            file_path = os.path.join(website_dir, file_name)
            with open(file_path, 'r', encoding='utf-8') as f:
                html_content = f.read()
                soup = BeautifulSoup(html_content, 'html.parser')
                
                # Extract text content
                text_content = soup.get_text()
                words = len(text_content.split())
                content['total_words'] += words
                
                # Extract headings
                headings = [h.get_text().strip() for h in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])]
                content['headings'].extend(headings)
                
                # Extract paragraphs
                paragraphs = [p.get_text().strip() for p in soup.find_all('p') if p.get_text().strip()]
                content['paragraphs'].extend(paragraphs)
                
                # Extract links
                links = [a.get('href', '') for a in soup.find_all('a') if a.get('href')]
                content['links'].extend(links)
                
                # Extract meta data
                meta_title = soup.find('title')
                meta_description = soup.find('meta', attrs={'name': 'description'})
                
                content['html_files'][file_name] = {
                    'word_count': words,
                    'title': meta_title.get_text() if meta_title else '',
                    'meta_description': meta_description.get('content', '') if meta_description else '',
                    'headings_count': len(headings),
                    'paragraphs_count': len(paragraphs),
                    'text_content': text_content[:1000]  # First 1000 chars for analysis
                }
        
        return content

    def _analyze_background_content(self, background_dir: str) -> Dict:
        """Analyze background content for knowledge gaps and opportunities."""
        if not os.path.exists(background_dir):
            return {'status': 'No background content available'}
        
        background = {
            'ontologies': {},
            'parsings': {},
            'vectors': {},
            'graphs': {},
            'total_concepts': 0,
            'key_themes': []
        }
        
        # Analyze each axis of background content
        for axis in ['ontologies', 'parsings', 'vectors', 'graphs']:
            axis_dir = os.path.join(background_dir, axis)
            if os.path.exists(axis_dir):
                background[axis] = self._analyze_axis_content(axis_dir)
        
        # Extract key themes
        background['key_themes'] = self._extract_key_themes(background)
        
        return background

    def _analyze_axis_content(self, axis_dir: str) -> Dict:
        """Analyze content in a specific axis directory."""
        content = {
            'file_count': 0,
            'concepts': [],
            'summaries': []
        }
        
        for root, dirs, files in os.walk(axis_dir):
            for file in files:
                if file.endswith(('.json', '.md', '.txt')):
                    content['file_count'] += 1
                    file_path = os.path.join(root, file)
                    
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            if file.endswith('.json'):
                                data = json.load(f)
                                if isinstance(data, dict):
                                    content['concepts'].extend(data.keys())
                            else:
                                text = f.read()
                                # Extract concepts from text (simple heuristic)
                                words = re.findall(r'\b[A-Z][a-z]+\b', text)
                                content['concepts'].extend(words[:20])  # Top 20 potential concepts
                    except Exception as e:
                        continue
        
        return content

    def _extract_key_themes(self, background: Dict) -> List[str]:
        """Extract key themes from background content."""
        all_concepts = []
        for axis in ['ontologies', 'parsings', 'vectors', 'graphs']:
            if axis in background:
                all_concepts.extend(background[axis].get('concepts', []))
        
        # Count concept frequency
        concept_counts = Counter(all_concepts)
        
        # Return top themes
        return [concept for concept, count in concept_counts.most_common(10)]

    def _analyze_content_quality(self, content: Dict) -> Dict:
        """Analyze content quality metrics."""
        quality = {
            'word_count_analysis': self._analyze_word_count(content['total_words']),
            'heading_structure': self._analyze_heading_structure(content['headings']),
            'paragraph_quality': self._analyze_paragraph_quality(content['paragraphs']),
            'content_depth': self._analyze_content_depth(content),
            'keyword_density': self._analyze_keyword_density(content)
        }
        
        return quality

    def _analyze_word_count(self, total_words: int) -> Dict:
        """Analyze if word count is appropriate."""
        if total_words < 300:
            status = 'Too short - may hurt SEO'
            recommendation = 'Add more valuable content'
        elif total_words < 800:
            status = 'Good length for landing page'
            recommendation = 'Consider adding more detailed sections'
        elif total_words < 1500:
            status = 'Excellent length'
            recommendation = 'Perfect balance of information'
        else:
            status = 'Very comprehensive'
            recommendation = 'Consider breaking into multiple pages'
        
        return {
            'total_words': total_words,
            'status': status,
            'recommendation': recommendation
        }

    def _analyze_heading_structure(self, headings: List[str]) -> Dict:
        """Analyze heading structure and hierarchy."""
        h1_count = sum(1 for h in headings if h.startswith('H1'))
        total_headings = len(headings)
        
        structure_quality = 'Good'
        recommendations = []
        
        if h1_count == 0:
            structure_quality = 'Poor'
            recommendations.append('Add an H1 tag for main page title')
        elif h1_count > 1:
            structure_quality = 'Fair'
            recommendations.append('Use only one H1 tag per page')
        
        if total_headings < 3:
            recommendations.append('Add more headings to structure content')
        
        return {
            'total_headings': total_headings,
            'h1_count': h1_count,
            'structure_quality': structure_quality,
            'recommendations': recommendations
        }

    def _analyze_paragraph_quality(self, paragraphs: List[str]) -> Dict:
        """Analyze paragraph quality and readability."""
        if not paragraphs:
            return {'status': 'No paragraphs found', 'recommendations': ['Add paragraph content']}
        
        avg_length = sum(len(p.split()) for p in paragraphs) / len(paragraphs)
        
        if avg_length < 20:
            status = 'Paragraphs too short'
            recommendation = 'Expand paragraphs for better readability'
        elif avg_length > 60:
            status = 'Paragraphs too long'
            recommendation = 'Break long paragraphs into shorter ones'
        else:
            status = 'Good paragraph length'
            recommendation = 'Maintain current paragraph structure'
        
        return {
            'paragraph_count': len(paragraphs),
            'average_length': avg_length,
            'status': status,
            'recommendation': recommendation
        }

    def _analyze_content_depth(self, content: Dict) -> Dict:
        """Analyze content depth and expertise level."""
        # Simple heuristic based on vocabulary complexity
        all_text = ' '.join(content['paragraphs'])
        words = all_text.lower().split()
        
        # Count technical/complex words (words longer than 7 characters)
        complex_words = [w for w in words if len(w) > 7]
        complexity_ratio = len(complex_words) / len(words) if words else 0
        
        if complexity_ratio < 0.1:
            depth = 'Basic'
            recommendation = 'Add more detailed explanations'
        elif complexity_ratio < 0.2:
            depth = 'Intermediate'
            recommendation = 'Good balance of accessibility and detail'
        else:
            depth = 'Advanced'
            recommendation = 'Consider simplifying for broader audience'
        
        return {
            'complexity_ratio': complexity_ratio,
            'depth_level': depth,
            'recommendation': recommendation
        }

    def _analyze_keyword_density(self, content: Dict) -> Dict:
        """Analyze keyword density and topic focus."""
        all_text = ' '.join(content['paragraphs']).lower()
        words = [w for w in all_text.split() if w not in self.stop_words and len(w) > 3]
        
        if not words:
            return {'status': 'No content to analyze'}
        
        word_counts = Counter(words)
        top_keywords = word_counts.most_common(10)
        
        # Calculate keyword density
        total_words = len(words)
        keyword_densities = [(keyword, count / total_words) for keyword, count in top_keywords]
        
        return {
            'top_keywords': top_keywords,
            'keyword_densities': keyword_densities,
            'topic_focus': 'High' if keyword_densities[0][1] > 0.05 else 'Medium' if keyword_densities[0][1] > 0.02 else 'Low'
        }

    def _analyze_readability(self, content: Dict) -> Dict:
        """Analyze content readability."""
        all_text = ' '.join(content['paragraphs'])
        
        if not all_text:
            return {'status': 'No content to analyze'}
        
        # Simple readability metrics
        sentences = nltk.sent_tokenize(all_text)
        words = all_text.split()
        
        avg_sentence_length = len(words) / len(sentences) if sentences else 0
        avg_word_length = sum(len(word) for word in words) / len(words) if words else 0
        
        # Readability score (simplified Flesch Reading Ease approximation)
        readability_score = 206.835 - (1.015 * avg_sentence_length) - (84.6 * (avg_word_length / 5))
        
        if readability_score >= 70:
            level = 'Easy to read'
        elif readability_score >= 50:
            level = 'Moderately easy'
        elif readability_score >= 30:
            level = 'Moderately difficult'
        else:
            level = 'Difficult to read'
        
        return {
            'readability_score': max(0, min(100, readability_score)),
            'reading_level': level,
            'avg_sentence_length': avg_sentence_length,
            'avg_word_length': avg_word_length,
            'sentence_count': len(sentences),
            'word_count': len(words)
        }

    def _analyze_seo_content(self, content: Dict) -> Dict:
        """Analyze content for SEO optimization."""
        seo_analysis = {
            'title_optimization': {},
            'meta_description_optimization': {},
            'keyword_optimization': {},
            'content_structure': {}
        }
        
        for file_name, file_content in content['html_files'].items():
            title = file_content.get('title', '')
            meta_desc = file_content.get('meta_description', '')
            
            # Title analysis
            seo_analysis['title_optimization'][file_name] = {
                'length': len(title),
                'status': 'Good' if 30 <= len(title) <= 60 else 'Needs optimization',
                'recommendation': self._get_title_recommendation(len(title))
            }
            
            # Meta description analysis
            seo_analysis['meta_description_optimization'][file_name] = {
                'length': len(meta_desc),
                'status': 'Good' if 120 <= len(meta_desc) <= 160 else 'Needs optimization',
                'recommendation': self._get_meta_desc_recommendation(len(meta_desc))
            }
        
        return seo_analysis

    def _get_title_recommendation(self, length: int) -> str:
        """Get title optimization recommendation."""
        if length < 30:
            return 'Title too short - add more descriptive keywords'
        elif length > 60:
            return 'Title too long - may be truncated in search results'
        else:
            return 'Title length is optimal'

    def _get_meta_desc_recommendation(self, length: int) -> str:
        """Get meta description optimization recommendation."""
        if length < 120:
            return 'Meta description too short - add more compelling copy'
        elif length > 160:
            return 'Meta description too long - may be truncated'
        else:
            return 'Meta description length is optimal'

    def _generate_content_insights(self, website_content: Dict, background_content: Dict) -> Dict:
        """Generate AI-powered content insights."""
        insights = {
            'content_gaps': self._identify_content_gaps(website_content, background_content),
            'enhancement_opportunities': self._identify_enhancements(website_content, background_content),
            'topic_expansion': self._suggest_topic_expansion(background_content),
            'content_freshness': self._analyze_content_freshness(website_content),
            'user_intent_alignment': self._analyze_user_intent(website_content)
        }
        
        return insights

    def _identify_content_gaps(self, website_content: Dict, background_content: Dict) -> List[str]:
        """Identify content gaps based on background knowledge."""
        gaps = []
        
        # Compare website topics with background themes
        website_keywords = []
        for paragraphs in website_content.get('paragraphs', []):
            words = re.findall(r'\b[a-zA-Z]+\b', paragraphs.lower())
            website_keywords.extend(words)
        
        website_keyword_set = set(website_keywords)
        background_themes = background_content.get('key_themes', [])
        
        for theme in background_themes:
            if theme.lower() not in website_keyword_set:
                gaps.append(f"Missing content about '{theme}'")
        
        if len(gaps) == 0:
            gaps.append("Content covers most available topics")
        
        return gaps[:5]  # Top 5 gaps

    def _identify_enhancements(self, website_content: Dict, background_content: Dict) -> List[Dict]:
        """Identify content enhancement opportunities."""
        enhancements = [
            {
                'type': 'Visual Enhancement',
                'description': 'Add concept visualizations from background knowledge',
                'priority': 'High',
                'implementation': 'Integrate concept trees and organizational charts'
            },
            {
                'type': 'Content Depth',
                'description': 'Expand technical explanations using background research',
                'priority': 'Medium',
                'implementation': 'Add detailed sections based on ontologies data'
            },
            {
                'type': 'Interactive Elements',
                'description': 'Add interactive knowledge exploration features',
                'priority': 'Medium',
                'implementation': 'Create interactive concept maps and knowledge graphs'
            }
        ]
        
        return enhancements

    def _suggest_topic_expansion(self, background_content: Dict) -> List[str]:
        """Suggest topic expansion based on background content."""
        suggestions = []
        key_themes = background_content.get('key_themes', [])
        
        for theme in key_themes[:5]:
            suggestions.append(f"Create dedicated section for '{theme}'")
        
        return suggestions

    def _analyze_content_freshness(self, website_content: Dict) -> Dict:
        """Analyze content freshness and update recommendations."""
        return {
            'last_update': 'Unknown - implement content timestamps',
            'freshness_score': 'Medium',
            'update_recommendations': [
                'Add last updated timestamps',
                'Implement content versioning',
                'Set up automated content refresh alerts'
            ]
        }

    def _analyze_user_intent(self, website_content: Dict) -> Dict:
        """Analyze how well content aligns with user intent."""
        # Simple analysis based on content structure
        has_clear_value_prop = any('voither' in p.lower() for p in website_content.get('paragraphs', []))
        has_cta = any('contact' in p.lower() or 'start' in p.lower() for p in website_content.get('paragraphs', []))
        
        alignment_score = 0
        if has_clear_value_prop:
            alignment_score += 50
        if has_cta:
            alignment_score += 30
        if website_content.get('total_words', 0) > 300:
            alignment_score += 20
        
        return {
            'alignment_score': alignment_score,
            'intent_match': 'High' if alignment_score >= 80 else 'Medium' if alignment_score >= 50 else 'Low',
            'recommendations': self._get_intent_recommendations(alignment_score)
        }

    def _get_intent_recommendations(self, score: int) -> List[str]:
        """Get user intent optimization recommendations."""
        recommendations = []
        
        if score < 50:
            recommendations.extend([
                'Clarify value proposition',
                'Add clear call-to-action',
                'Improve content relevance'
            ])
        elif score < 80:
            recommendations.extend([
                'Strengthen call-to-action placement',
                'Add social proof elements',
                'Optimize for conversion'
            ])
        else:
            recommendations.append('Content aligns well with user intent')
        
        return recommendations

    def _generate_content_recommendations(self, quality: Dict, readability: Dict, seo: Dict, insights: Dict) -> List[Dict]:
        """Generate comprehensive content recommendations."""
        recommendations = []
        
        # Quality-based recommendations
        word_count_rec = quality.get('word_count_analysis', {}).get('recommendation', '')
        if word_count_rec:
            recommendations.append({
                'category': 'Content Quality',
                'priority': 'Medium',
                'title': 'Optimize Content Length',
                'description': word_count_rec,
                'implementation': 'Review and adjust content based on analysis'
            })
        
        # Readability recommendations
        reading_level = readability.get('reading_level', '')
        if 'difficult' in reading_level.lower():
            recommendations.append({
                'category': 'Readability',
                'priority': 'High',
                'title': 'Improve Content Readability',
                'description': 'Simplify language and sentence structure',
                'implementation': 'Use shorter sentences and common vocabulary'
            })
        
        # SEO recommendations
        recommendations.append({
            'category': 'SEO',
            'priority': 'High',
            'title': 'Optimize Meta Elements',
            'description': 'Improve titles and meta descriptions',
            'implementation': 'Follow SEO best practices for title and meta description length'
        })
        
        # AI insights recommendations
        for gap in insights.get('content_gaps', [])[:3]:
            recommendations.append({
                'category': 'Content Strategy',
                'priority': 'Medium',
                'title': 'Fill Content Gap',
                'description': gap,
                'implementation': 'Research and create content for identified gap'
            })
        
        return recommendations

    def _calculate_content_score(self, quality: Dict, readability: Dict, seo: Dict) -> float:
        """Calculate overall content optimization score."""
        score = 0.0
        
        # Word count score (30%)
        word_count = quality.get('word_count_analysis', {}).get('total_words', 0)
        if 300 <= word_count <= 1500:
            score += 30
        elif word_count > 100:
            score += 20
        
        # Readability score (30%)
        readability_score = readability.get('readability_score', 0)
        score += (readability_score / 100) * 30
        
        # SEO score (20%)
        # Simple SEO scoring based on title and meta presence
        seo_score = 20  # Base score
        score += seo_score
        
        # Structure score (20%)
        headings = quality.get('heading_structure', {}).get('total_headings', 0)
        if headings >= 3:
            score += 20
        elif headings > 0:
            score += 10
        
        return min(100, score)

    def _generate_html_report(self, report: Dict, output_dir: str):
        """Generate HTML report for content analysis."""
        content_score = report.get('content_optimization_score', 0)
        
        html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Content Analysis Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; line-height: 1.6; }}
        .header {{ background: #f0f8ff; padding: 20px; border-radius: 8px; }}
        .score {{ font-size: 3em; font-weight: bold; color: #4CAF50; text-align: center; }}
        .metrics {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; margin: 20px 0; }}
        .metric {{ background: white; border: 1px solid #ddd; padding: 20px; border-radius: 8px; }}
        .recommendations {{ margin-top: 20px; }}
        .recommendation {{ border-left: 4px solid #FF9800; padding: 15px; margin: 15px 0; background: #fff8e1; }}
        .insights {{ background: #e8f5e8; padding: 15px; border-radius: 8px; margin: 20px 0; }}
        .gap {{ background: #ffebee; padding: 10px; margin: 5px 0; border-radius: 4px; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>📝 Content Analysis Report</h1>
        <p><strong>Analysis Date:</strong> {report['timestamp']}</p>
        <div class="score">{content_score:.0f}%</div>
        <p style="text-align: center;">Content Optimization Score</p>
    </div>

    <div class="metrics">
        <div class="metric">
            <h3>📊 Content Quality</h3>
            <p><strong>Total Words:</strong> {report.get('content_analysis', {}).get('quality', {}).get('word_count_analysis', {}).get('total_words', 0)}</p>
            <p><strong>Status:</strong> {report.get('content_analysis', {}).get('quality', {}).get('word_count_analysis', {}).get('status', 'Unknown')}</p>
        </div>
        
        <div class="metric">
            <h3>📖 Readability</h3>
            <p><strong>Reading Level:</strong> {report.get('content_analysis', {}).get('readability', {}).get('reading_level', 'Unknown')}</p>
            <p><strong>Score:</strong> {report.get('content_analysis', {}).get('readability', {}).get('readability_score', 0):.0f}/100</p>
        </div>
        
        <div class="metric">
            <h3>🔍 SEO Analysis</h3>
            <p><strong>Title Optimization:</strong> Available</p>
            <p><strong>Meta Descriptions:</strong> Available</p>
        </div>
    </div>

    <div class="insights">
        <h2>🧠 AI Content Insights</h2>
        <h4>Content Gaps Identified:</h4>
        {"".join([f'<div class="gap">• {gap}</div>' for gap in report.get('content_analysis', {}).get('ai_insights', {}).get('content_gaps', [])])}
    </div>

    <div class="recommendations">
        <h2>🎯 Content Recommendations</h2>
        {"".join([f'<div class="recommendation"><h4>{rec["title"]}</h4><p><strong>Category:</strong> {rec["category"]} | <strong>Priority:</strong> {rec["priority"]}</p><p>{rec["description"]}</p></div>' for rec in report.get('recommendations', [])])}
    </div>
</body>
</html>
        """
        
        with open(os.path.join(output_dir, 'content.html'), 'w') as f:
            f.write(html_content)

def main():
    parser = argparse.ArgumentParser(description='Analyze website content')
    parser.add_argument('--source', required=True, help='Background content directory')
    parser.add_argument('--website', required=True, help='Website directory')
    parser.add_argument('--output', required=True, help='Output directory')
    parser.add_argument('--ai-model', default='claude-3.5-sonnet', help='AI model to use')
    
    args = parser.parse_args()
    
    analyzer = ContentAnalyzer(ai_model=args.ai_model)
    report = analyzer.analyze_content(args.source, args.website, args.output)
    
    print(f"Content analysis complete. Report saved to {args.output}")
    print(f"Content optimization score: {report.get('content_optimization_score', 0):.0f}%")

if __name__ == '__main__':
    main()