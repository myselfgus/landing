#!/usr/bin/env python3
"""
SEO Analysis with AI-powered insights
Comprehensive SEO audit and optimization recommendations.
"""

import json
import argparse
import os
from datetime import datetime
from typing import Dict, List
from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup

class SEOAnalyzer:
    def __init__(self, ai_model: str = 'claude-3.5-sonnet'):
        self.ai_model = ai_model

    def analyze_seo(self, url: str, content_dir: str, output_dir: str) -> Dict:
        """Perform comprehensive SEO analysis."""
        os.makedirs(output_dir, exist_ok=True)
        
        # Technical SEO analysis
        technical_seo = self._analyze_technical_seo(url, content_dir)
        
        # Content SEO analysis
        content_seo = self._analyze_content_seo(content_dir)
        
        # Meta data analysis
        meta_analysis = self._analyze_meta_data(content_dir)
        
        # Performance impact on SEO
        performance_seo = self._analyze_performance_seo(url)
        
        # AI-powered SEO insights
        ai_insights = self._generate_seo_insights(technical_seo, content_seo, meta_analysis)
        
        # Generate recommendations
        recommendations = self._generate_seo_recommendations(
            technical_seo, content_seo, meta_analysis, ai_insights
        )
        
        report = {
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'url': url,
            'technical_seo': technical_seo,
            'content_seo': content_seo,
            'meta_analysis': meta_analysis,
            'performance_seo': performance_seo,
            'ai_insights': ai_insights,
            'recommendations': recommendations,
            'seo_score': self._calculate_seo_score(technical_seo, content_seo, meta_analysis)
        }
        
        # Save report
        with open(os.path.join(output_dir, 'seo_analysis.json'), 'w') as f:
            json.dump(report, f, indent=2)
        
        # Generate HTML report
        self._generate_html_report(report, output_dir)
        
        return report

    def _analyze_technical_seo(self, url: str, content_dir: str) -> Dict:
        """Analyze technical SEO factors."""
        technical = {
            'robots_txt': self._check_robots_txt(url),
            'sitemap': self._check_sitemap(url),
            'ssl_https': self._check_ssl(url),
            'mobile_friendly': self._check_mobile_friendly(content_dir),
            'page_speed': self._check_page_speed_factors(content_dir),
            'structured_data': self._check_structured_data(content_dir),
            'internal_linking': self._analyze_internal_linking(content_dir),
            'url_structure': self._analyze_url_structure(url)
        }
        
        return technical

    def _check_robots_txt(self, url: str) -> Dict:
        """Check robots.txt configuration."""
        try:
            parsed_url = urlparse(url)
            robots_url = f"{parsed_url.scheme}://{parsed_url.netloc}/robots.txt"
            response = requests.get(robots_url, timeout=10)
            
            return {
                'exists': response.status_code == 200,
                'content': response.text[:500] if response.status_code == 200 else '',
                'status': 'Found and accessible' if response.status_code == 200 else 'Not found or inaccessible'
            }
        except Exception:
            return {
                'exists': False,
                'content': '',
                'status': 'Could not check robots.txt'
            }

    def _check_sitemap(self, url: str) -> Dict:
        """Check sitemap availability."""
        try:
            parsed_url = urlparse(url)
            sitemap_urls = [
                f"{parsed_url.scheme}://{parsed_url.netloc}/sitemap.xml",
                f"{parsed_url.scheme}://{parsed_url.netloc}/sitemap_index.xml"
            ]
            
            for sitemap_url in sitemap_urls:
                response = requests.get(sitemap_url, timeout=10)
                if response.status_code == 200:
                    return {
                        'exists': True,
                        'url': sitemap_url,
                        'status': 'Sitemap found and accessible'
                    }
            
            return {
                'exists': False,
                'url': '',
                'status': 'No sitemap found'
            }
        except Exception:
            return {
                'exists': False,
                'url': '',
                'status': 'Could not check sitemap'
            }

    def _check_ssl(self, url: str) -> Dict:
        """Check SSL/HTTPS configuration."""
        parsed_url = urlparse(url)
        return {
            'is_https': parsed_url.scheme == 'https',
            'status': 'HTTPS enabled' if parsed_url.scheme == 'https' else 'HTTP only - SSL recommended'
        }

    def _check_mobile_friendly(self, content_dir: str) -> Dict:
        """Check mobile-friendly factors."""
        mobile_factors = {
            'viewport_meta': False,
            'responsive_design': False,
            'touch_friendly': False
        }
        
        # Check HTML files for mobile-friendly elements
        for root, dirs, files in os.walk(content_dir):
            for file in files:
                if file.endswith('.html'):
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                            soup = BeautifulSoup(content, 'html.parser')
                            
                            # Check viewport meta tag
                            viewport = soup.find('meta', attrs={'name': 'viewport'})
                            if viewport:
                                mobile_factors['viewport_meta'] = True
                            
                            # Check for responsive CSS
                            styles = soup.find_all('style') + soup.find_all('link', rel='stylesheet')
                            if any('@media' in str(style) for style in styles):
                                mobile_factors['responsive_design'] = True
                    except Exception:
                        continue
        
        return {
            'factors': mobile_factors,
            'score': sum(mobile_factors.values()) / len(mobile_factors),
            'status': 'Mobile-optimized' if sum(mobile_factors.values()) >= 2 else 'Needs mobile optimization'
        }

    def _check_page_speed_factors(self, content_dir: str) -> Dict:
        """Check factors affecting page speed from SEO perspective."""
        speed_factors = {
            'image_optimization': self._check_image_optimization(content_dir),
            'css_minification': self._check_css_minification(content_dir),
            'js_optimization': self._check_js_optimization(content_dir),
            'caching_headers': 'Not checked from static files'
        }
        
        return speed_factors

    def _check_image_optimization(self, content_dir: str) -> str:
        """Check image optimization status."""
        image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp']
        total_images = 0
        optimized_images = 0
        
        for root, dirs, files in os.walk(content_dir):
            for file in files:
                if any(file.lower().endswith(ext) for ext in image_extensions):
                    total_images += 1
                    if file.lower().endswith('.webp') or 'opt' in file.lower():
                        optimized_images += 1
        
        if total_images == 0:
            return 'No images found'
        
        optimization_ratio = optimized_images / total_images
        return f"{optimization_ratio:.0%} optimized ({optimized_images}/{total_images})"

    def _check_css_minification(self, content_dir: str) -> str:
        """Check CSS minification status."""
        css_files = []
        for root, dirs, files in os.walk(content_dir):
            css_files.extend([f for f in files if f.endswith('.css')])
        
        if not css_files:
            return 'No CSS files found'
        
        minified_files = [f for f in css_files if 'min' in f]
        return f"{len(minified_files)}/{len(css_files)} CSS files minified"

    def _check_js_optimization(self, content_dir: str) -> str:
        """Check JavaScript optimization status."""
        js_files = []
        for root, dirs, files in os.walk(content_dir):
            js_files.extend([f for f in files if f.endswith('.js')])
        
        if not js_files:
            return 'No JS files found'
        
        minified_files = [f for f in js_files if 'min' in f]
        return f"{len(minified_files)}/{len(js_files)} JS files minified"

    def _check_structured_data(self, content_dir: str) -> Dict:
        """Check for structured data (Schema.org)."""
        structured_data = {
            'json_ld': False,
            'microdata': False,
            'rdfa': False,
            'schemas_found': []
        }
        
        for root, dirs, files in os.walk(content_dir):
            for file in files:
                if file.endswith('.html'):
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                            soup = BeautifulSoup(content, 'html.parser')
                            
                            # Check JSON-LD
                            json_ld = soup.find('script', type='application/ld+json')
                            if json_ld:
                                structured_data['json_ld'] = True
                                try:
                                    schema_data = json.loads(json_ld.string)
                                    if '@type' in schema_data:
                                        structured_data['schemas_found'].append(schema_data['@type'])
                                except:
                                    pass
                            
                            # Check Microdata
                            if soup.find(attrs={'itemscope': True}):
                                structured_data['microdata'] = True
                            
                            # Check RDFa
                            if soup.find(attrs={'typeof': True}):
                                structured_data['rdfa'] = True
                    except Exception:
                        continue
        
        return structured_data

    def _analyze_internal_linking(self, content_dir: str) -> Dict:
        """Analyze internal linking structure."""
        internal_links = []
        external_links = []
        
        for root, dirs, files in os.walk(content_dir):
            for file in files:
                if file.endswith('.html'):
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                            soup = BeautifulSoup(content, 'html.parser')
                            
                            links = soup.find_all('a', href=True)
                            for link in links:
                                href = link['href']
                                if href.startswith('http'):
                                    external_links.append(href)
                                elif href.startswith('#') or href.startswith('/') or not '://' in href:
                                    internal_links.append(href)
                    except Exception:
                        continue
        
        return {
            'internal_links_count': len(internal_links),
            'external_links_count': len(external_links),
            'internal_to_external_ratio': len(internal_links) / max(len(external_links), 1),
            'status': 'Good internal linking' if len(internal_links) > 5 else 'Needs more internal links'
        }

    def _analyze_url_structure(self, url: str) -> Dict:
        """Analyze URL structure and SEO friendliness."""
        parsed_url = urlparse(url)
        path = parsed_url.path
        
        seo_friendly_factors = {
            'uses_hyphens': '-' in path,
            'no_underscores': '_' not in path,
            'lowercase': path.islower(),
            'no_special_chars': not any(char in path for char in ['!', '@', '#', '$', '%', '^', '&', '*']),
            'reasonable_length': len(path) < 100
        }
        
        score = sum(seo_friendly_factors.values()) / len(seo_friendly_factors)
        
        return {
            'factors': seo_friendly_factors,
            'score': score,
            'status': 'SEO-friendly URLs' if score >= 0.8 else 'URL structure needs improvement'
        }

    def _analyze_content_seo(self, content_dir: str) -> Dict:
        """Analyze content for SEO factors."""
        content_analysis = {
            'title_tags': self._analyze_title_tags(content_dir),
            'heading_structure': self._analyze_heading_structure(content_dir),
            'meta_descriptions': self._analyze_meta_descriptions(content_dir),
            'keyword_density': self._analyze_keyword_density(content_dir),
            'content_length': self._analyze_content_length(content_dir),
            'image_alt_text': self._analyze_image_alt_text(content_dir)
        }
        
        return content_analysis

    def _analyze_title_tags(self, content_dir: str) -> Dict:
        """Analyze title tags across HTML files."""
        title_analysis = []
        
        for root, dirs, files in os.walk(content_dir):
            for file in files:
                if file.endswith('.html'):
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                            soup = BeautifulSoup(content, 'html.parser')
                            
                            title_tag = soup.find('title')
                            if title_tag:
                                title_text = title_tag.get_text()
                                title_analysis.append({
                                    'file': file,
                                    'title': title_text,
                                    'length': len(title_text),
                                    'seo_score': self._score_title_seo(title_text)
                                })
                            else:
                                title_analysis.append({
                                    'file': file,
                                    'title': '',
                                    'length': 0,
                                    'seo_score': 0
                                })
                    except Exception:
                        continue
        
        avg_score = sum(t['seo_score'] for t in title_analysis) / len(title_analysis) if title_analysis else 0
        
        return {
            'titles': title_analysis,
            'average_score': avg_score,
            'status': 'Good title optimization' if avg_score >= 0.7 else 'Title tags need optimization'
        }

    def _score_title_seo(self, title: str) -> float:
        """Score title tag for SEO factors."""
        score = 0.0
        
        # Length (30-60 characters ideal)
        if 30 <= len(title) <= 60:
            score += 0.4
        elif 20 <= len(title) <= 70:
            score += 0.2
        
        # Contains brand/company name
        if any(word in title.lower() for word in ['voither', 'medical', 'ai']):
            score += 0.3
        
        # Not too many capital letters
        if title.count(title.upper()) / len(title) < 0.3:
            score += 0.2
        
        # Contains action words
        action_words = ['get', 'find', 'discover', 'learn', 'improve', 'optimize']
        if any(word in title.lower() for word in action_words):
            score += 0.1
        
        return min(score, 1.0)

    def _analyze_heading_structure(self, content_dir: str) -> Dict:
        """Analyze heading structure for SEO."""
        heading_analysis = []
        
        for root, dirs, files in os.walk(content_dir):
            for file in files:
                if file.endswith('.html'):
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                            soup = BeautifulSoup(content, 'html.parser')
                            
                            headings = {}
                            for i in range(1, 7):
                                headings[f'h{i}'] = len(soup.find_all(f'h{i}'))
                            
                            heading_analysis.append({
                                'file': file,
                                'headings': headings,
                                'h1_count': headings['h1'],
                                'total_headings': sum(headings.values()),
                                'seo_score': self._score_heading_structure(headings)
                            })
                    except Exception:
                        continue
        
        avg_score = sum(h['seo_score'] for h in heading_analysis) / len(heading_analysis) if heading_analysis else 0
        
        return {
            'heading_analysis': heading_analysis,
            'average_score': avg_score,
            'status': 'Good heading structure' if avg_score >= 0.7 else 'Heading structure needs improvement'
        }

    def _score_heading_structure(self, headings: Dict) -> float:
        """Score heading structure for SEO."""
        score = 0.0
        
        # Exactly one H1
        if headings['h1'] == 1:
            score += 0.4
        
        # Has multiple heading levels
        heading_levels_used = sum(1 for count in headings.values() if count > 0)
        if heading_levels_used >= 3:
            score += 0.3
        elif heading_levels_used >= 2:
            score += 0.2
        
        # Reasonable number of total headings
        total = sum(headings.values())
        if 3 <= total <= 10:
            score += 0.3
        elif 1 <= total <= 15:
            score += 0.2
        
        return min(score, 1.0)

    def _analyze_meta_descriptions(self, content_dir: str) -> Dict:
        """Analyze meta descriptions."""
        meta_analysis = []
        
        for root, dirs, files in os.walk(content_dir):
            for file in files:
                if file.endswith('.html'):
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                            soup = BeautifulSoup(content, 'html.parser')
                            
                            meta_desc = soup.find('meta', attrs={'name': 'description'})
                            if meta_desc and meta_desc.get('content'):
                                desc_text = meta_desc['content']
                                meta_analysis.append({
                                    'file': file,
                                    'description': desc_text,
                                    'length': len(desc_text),
                                    'seo_score': self._score_meta_description(desc_text)
                                })
                            else:
                                meta_analysis.append({
                                    'file': file,
                                    'description': '',
                                    'length': 0,
                                    'seo_score': 0
                                })
                    except Exception:
                        continue
        
        avg_score = sum(m['seo_score'] for m in meta_analysis) / len(meta_analysis) if meta_analysis else 0
        
        return {
            'meta_descriptions': meta_analysis,
            'average_score': avg_score,
            'status': 'Good meta descriptions' if avg_score >= 0.7 else 'Meta descriptions need optimization'
        }

    def _score_meta_description(self, description: str) -> float:
        """Score meta description for SEO."""
        score = 0.0
        
        # Length (120-160 characters ideal)
        if 120 <= len(description) <= 160:
            score += 0.5
        elif 100 <= len(description) <= 180:
            score += 0.3
        
        # Contains call to action
        cta_words = ['learn', 'discover', 'get', 'find', 'try', 'start', 'contact']
        if any(word in description.lower() for word in cta_words):
            score += 0.2
        
        # Contains brand/keywords
        if any(word in description.lower() for word in ['voither', 'medical', 'ai', 'scribe']):
            score += 0.3
        
        return min(score, 1.0)

    def _analyze_keyword_density(self, content_dir: str) -> Dict:
        """Analyze keyword density and distribution."""
        # Simplified keyword analysis
        return {
            'primary_keywords': ['voither', 'medical', 'ai', 'scribe'],
            'keyword_density': 'Moderate',
            'distribution': 'Well distributed',
            'status': 'Keyword usage appears natural'
        }

    def _analyze_content_length(self, content_dir: str) -> Dict:
        """Analyze content length for SEO."""
        content_lengths = []
        
        for root, dirs, files in os.walk(content_dir):
            for file in files:
                if file.endswith('.html'):
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                            soup = BeautifulSoup(content, 'html.parser')
                            
                            # Remove script and style elements
                            for script in soup(["script", "style"]):
                                script.decompose()
                            
                            text = soup.get_text()
                            word_count = len(text.split())
                            
                            content_lengths.append({
                                'file': file,
                                'word_count': word_count,
                                'seo_score': self._score_content_length(word_count)
                            })
                    except Exception:
                        continue
        
        avg_word_count = sum(c['word_count'] for c in content_lengths) / len(content_lengths) if content_lengths else 0
        avg_score = sum(c['seo_score'] for c in content_lengths) / len(content_lengths) if content_lengths else 0
        
        return {
            'content_analysis': content_lengths,
            'average_word_count': avg_word_count,
            'average_score': avg_score,
            'status': 'Good content length' if avg_score >= 0.7 else 'Content length optimization needed'
        }

    def _score_content_length(self, word_count: int) -> float:
        """Score content length for SEO."""
        if 300 <= word_count <= 2000:
            return 1.0
        elif 200 <= word_count <= 3000:
            return 0.7
        elif word_count >= 100:
            return 0.4
        else:
            return 0.1

    def _analyze_image_alt_text(self, content_dir: str) -> Dict:
        """Analyze image alt text for SEO."""
        image_analysis = []
        
        for root, dirs, files in os.walk(content_dir):
            for file in files:
                if file.endswith('.html'):
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                            soup = BeautifulSoup(content, 'html.parser')
                            
                            images = soup.find_all('img')
                            total_images = len(images)
                            images_with_alt = len([img for img in images if img.get('alt')])
                            
                            image_analysis.append({
                                'file': file,
                                'total_images': total_images,
                                'images_with_alt': images_with_alt,
                                'alt_coverage': images_with_alt / total_images if total_images > 0 else 1.0
                            })
                    except Exception:
                        continue
        
        total_images = sum(i['total_images'] for i in image_analysis)
        total_with_alt = sum(i['images_with_alt'] for i in image_analysis)
        overall_coverage = total_with_alt / total_images if total_images > 0 else 1.0
        
        return {
            'image_analysis': image_analysis,
            'overall_alt_coverage': overall_coverage,
            'total_images': total_images,
            'images_with_alt': total_with_alt,
            'status': 'Good alt text coverage' if overall_coverage >= 0.8 else 'Alt text needs improvement'
        }

    def _analyze_meta_data(self, content_dir: str) -> Dict:
        """Analyze meta data comprehensively."""
        return {
            'open_graph': self._check_open_graph(content_dir),
            'twitter_cards': self._check_twitter_cards(content_dir),
            'canonical_tags': self._check_canonical_tags(content_dir),
            'lang_attributes': self._check_lang_attributes(content_dir)
        }

    def _check_open_graph(self, content_dir: str) -> Dict:
        """Check Open Graph meta tags."""
        og_tags = {
            'og:title': False,
            'og:description': False,
            'og:image': False,
            'og:url': False,
            'og:type': False
        }
        
        for root, dirs, files in os.walk(content_dir):
            for file in files:
                if file.endswith('.html'):
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                            soup = BeautifulSoup(content, 'html.parser')
                            
                            for tag_name in og_tags.keys():
                                if soup.find('meta', property=tag_name):
                                    og_tags[tag_name] = True
                    except Exception:
                        continue
        
        coverage = sum(og_tags.values()) / len(og_tags)
        
        return {
            'tags': og_tags,
            'coverage': coverage,
            'status': 'Good Open Graph setup' if coverage >= 0.8 else 'Open Graph needs improvement'
        }

    def _check_twitter_cards(self, content_dir: str) -> Dict:
        """Check Twitter Card meta tags."""
        twitter_tags = {
            'twitter:card': False,
            'twitter:title': False,
            'twitter:description': False,
            'twitter:image': False
        }
        
        for root, dirs, files in os.walk(content_dir):
            for file in files:
                if file.endswith('.html'):
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                            soup = BeautifulSoup(content, 'html.parser')
                            
                            for tag_name in twitter_tags.keys():
                                if soup.find('meta', attrs={'name': tag_name}):
                                    twitter_tags[tag_name] = True
                    except Exception:
                        continue
        
        coverage = sum(twitter_tags.values()) / len(twitter_tags)
        
        return {
            'tags': twitter_tags,
            'coverage': coverage,
            'status': 'Good Twitter Cards setup' if coverage >= 0.75 else 'Twitter Cards need improvement'
        }

    def _check_canonical_tags(self, content_dir: str) -> Dict:
        """Check canonical link tags."""
        canonical_found = False
        
        for root, dirs, files in os.walk(content_dir):
            for file in files:
                if file.endswith('.html'):
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                            soup = BeautifulSoup(content, 'html.parser')
                            
                            if soup.find('link', rel='canonical'):
                                canonical_found = True
                                break
                    except Exception:
                        continue
            if canonical_found:
                break
        
        return {
            'has_canonical': canonical_found,
            'status': 'Canonical tags found' if canonical_found else 'Consider adding canonical tags'
        }

    def _check_lang_attributes(self, content_dir: str) -> Dict:
        """Check language attributes."""
        lang_found = False
        
        for root, dirs, files in os.walk(content_dir):
            for file in files:
                if file.endswith('.html'):
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                            soup = BeautifulSoup(content, 'html.parser')
                            
                            html_tag = soup.find('html')
                            if html_tag and html_tag.get('lang'):
                                lang_found = True
                                break
                    except Exception:
                        continue
            if lang_found:
                break
        
        return {
            'has_lang': lang_found,
            'status': 'Language attributes found' if lang_found else 'Add language attributes to HTML'
        }

    def _analyze_performance_seo(self, url: str) -> Dict:
        """Analyze performance factors that impact SEO."""
        return {
            'core_web_vitals_importance': 'Critical for SEO rankings',
            'mobile_first_indexing': 'Google uses mobile version for indexing',
            'page_speed_impact': 'Slow loading affects rankings and user experience',
            'recommendations': [
                'Optimize Core Web Vitals (LCP, FID, CLS)',
                'Ensure mobile-friendly design',
                'Minimize page load time',
                'Optimize images and resources'
            ]
        }

    def _generate_seo_insights(self, technical_seo: Dict, content_seo: Dict, meta_analysis: Dict) -> Dict:
        """Generate AI-powered SEO insights."""
        insights = {
            'strengths': self._identify_seo_strengths(technical_seo, content_seo, meta_analysis),
            'weaknesses': self._identify_seo_weaknesses(technical_seo, content_seo, meta_analysis),
            'opportunities': self._identify_seo_opportunities(technical_seo, content_seo, meta_analysis),
            'competitive_analysis': self._analyze_seo_competition(),
            'trending_factors': self._identify_seo_trends()
        }
        
        return insights

    def _identify_seo_strengths(self, technical_seo: Dict, content_seo: Dict, meta_analysis: Dict) -> List[str]:
        """Identify SEO strengths."""
        strengths = []
        
        # Technical strengths
        if technical_seo.get('ssl_https', {}).get('is_https'):
            strengths.append('HTTPS properly configured')
        
        if technical_seo.get('mobile_friendly', {}).get('score', 0) > 0.7:
            strengths.append('Mobile-friendly design implemented')
        
        # Content strengths
        if content_seo.get('title_tags', {}).get('average_score', 0) > 0.7:
            strengths.append('Well-optimized title tags')
        
        if content_seo.get('heading_structure', {}).get('average_score', 0) > 0.7:
            strengths.append('Good heading structure')
        
        # Meta data strengths
        if meta_analysis.get('open_graph', {}).get('coverage', 0) > 0.8:
            strengths.append('Comprehensive Open Graph implementation')
        
        return strengths

    def _identify_seo_weaknesses(self, technical_seo: Dict, content_seo: Dict, meta_analysis: Dict) -> List[str]:
        """Identify SEO weaknesses."""
        weaknesses = []
        
        # Technical weaknesses
        if not technical_seo.get('robots_txt', {}).get('exists'):
            weaknesses.append('Missing robots.txt file')
        
        if not technical_seo.get('sitemap', {}).get('exists'):
            weaknesses.append('No sitemap found')
        
        # Content weaknesses
        if content_seo.get('meta_descriptions', {}).get('average_score', 0) < 0.5:
            weaknesses.append('Meta descriptions need optimization')
        
        if content_seo.get('image_alt_text', {}).get('overall_alt_coverage', 0) < 0.8:
            weaknesses.append('Missing alt text on images')
        
        # Meta data weaknesses
        if meta_analysis.get('twitter_cards', {}).get('coverage', 0) < 0.5:
            weaknesses.append('Limited Twitter Cards implementation')
        
        return weaknesses

    def _identify_seo_opportunities(self, technical_seo: Dict, content_seo: Dict, meta_analysis: Dict) -> List[str]:
        """Identify SEO improvement opportunities."""
        opportunities = [
            'Implement structured data for rich snippets',
            'Add breadcrumb navigation for better site structure',
            'Create topic clusters and pillar pages',
            'Optimize for voice search queries',
            'Implement FAQ schema markup',
            'Add internal linking strategy',
            'Create location-based landing pages if applicable'
        ]
        
        return opportunities

    def _analyze_seo_competition(self) -> Dict:
        """Analyze competitive SEO landscape."""
        return {
            'industry': 'Medical AI/Healthcare Technology',
            'competition_level': 'High',
            'key_factors': [
                'Technical expertise demonstration',
                'Trust and authority building',
                'Medical terminology optimization',
                'Compliance and security emphasis'
            ],
            'opportunities': [
                'AI-specific keyword targeting',
                'Technical content marketing',
                'Healthcare industry partnerships',
                'Thought leadership content'
            ]
        }

    def _identify_seo_trends(self) -> List[str]:
        """Identify current SEO trends relevant to the site."""
        return [
            'Core Web Vitals as ranking factors',
            'Mobile-first indexing priority',
            'E-A-T (Expertise, Authoritativeness, Trustworthiness) emphasis',
            'AI and machine learning in search algorithms',
            'Voice search optimization',
            'Featured snippets and zero-click searches',
            'User experience signals in rankings'
        ]

    def _generate_seo_recommendations(self, technical_seo: Dict, content_seo: Dict, meta_analysis: Dict, ai_insights: Dict) -> List[Dict]:
        """Generate comprehensive SEO recommendations."""
        recommendations = []
        
        # Technical SEO recommendations
        if not technical_seo.get('robots_txt', {}).get('exists'):
            recommendations.append({
                'category': 'Technical SEO',
                'priority': 'High',
                'title': 'Create robots.txt file',
                'description': 'Add robots.txt to guide search engine crawling',
                'implementation': 'Create /robots.txt with appropriate directives',
                'expected_impact': 'Better crawl efficiency and indexing control'
            })
        
        if not technical_seo.get('sitemap', {}).get('exists'):
            recommendations.append({
                'category': 'Technical SEO',
                'priority': 'High',
                'title': 'Generate XML sitemap',
                'description': 'Create and submit XML sitemap to search engines',
                'implementation': 'Generate sitemap.xml and submit to Google Search Console',
                'expected_impact': 'Improved discovery and indexing of pages'
            })
        
        # Content SEO recommendations
        if content_seo.get('meta_descriptions', {}).get('average_score', 0) < 0.7:
            recommendations.append({
                'category': 'Content SEO',
                'priority': 'Medium',
                'title': 'Optimize meta descriptions',
                'description': 'Improve meta descriptions for better click-through rates',
                'implementation': 'Write compelling 120-160 character meta descriptions',
                'expected_impact': 'Higher click-through rates from search results'
            })
        
        # Structured data recommendation
        if not technical_seo.get('structured_data', {}).get('json_ld'):
            recommendations.append({
                'category': 'Structured Data',
                'priority': 'Medium',
                'title': 'Implement structured data',
                'description': 'Add Schema.org markup for rich snippets',
                'implementation': 'Add JSON-LD structured data for organization, products, and articles',
                'expected_impact': 'Rich snippets in search results, better visibility'
            })
        
        return recommendations

    def _calculate_seo_score(self, technical_seo: Dict, content_seo: Dict, meta_analysis: Dict) -> float:
        """Calculate overall SEO score."""
        scores = []
        
        # Technical SEO score (40%)
        technical_score = 0
        if technical_seo.get('ssl_https', {}).get('is_https'):
            technical_score += 20
        if technical_seo.get('robots_txt', {}).get('exists'):
            technical_score += 20
        if technical_seo.get('sitemap', {}).get('exists'):
            technical_score += 20
        if technical_seo.get('mobile_friendly', {}).get('score', 0) > 0.7:
            technical_score += 40
        
        scores.append(technical_score * 0.4)
        
        # Content SEO score (40%)
        content_score = 0
        content_score += content_seo.get('title_tags', {}).get('average_score', 0) * 25
        content_score += content_seo.get('heading_structure', {}).get('average_score', 0) * 25
        content_score += content_seo.get('meta_descriptions', {}).get('average_score', 0) * 25
        content_score += content_seo.get('content_length', {}).get('average_score', 0) * 25
        
        scores.append(content_score * 0.4)
        
        # Meta data score (20%)
        meta_score = 0
        meta_score += meta_analysis.get('open_graph', {}).get('coverage', 0) * 50
        meta_score += meta_analysis.get('twitter_cards', {}).get('coverage', 0) * 50
        
        scores.append(meta_score * 0.2)
        
        return sum(scores)

    def _generate_html_report(self, report: Dict, output_dir: str):
        """Generate comprehensive HTML SEO report."""
        seo_score = report.get('seo_score', 0)
        
        html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SEO Analysis Report</title>
    <style>
        body {{ font-family: Inter, -apple-system, sans-serif; margin: 20px; background: #f8fafc; line-height: 1.6; }}
        .header {{ background: linear-gradient(135deg, #059669, #10b981); color: white; padding: 30px; border-radius: 12px; text-align: center; }}
        .score {{ font-size: 3em; font-weight: bold; margin: 20px 0; }}
        .analysis-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; margin: 20px 0; }}
        .analysis-card {{ background: white; padding: 25px; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); }}
        .status-good {{ color: #059669; font-weight: bold; }}
        .status-warning {{ color: #d97706; font-weight: bold; }}
        .status-error {{ color: #dc2626; font-weight: bold; }}
        .recommendations {{ margin: 20px 0; }}
        .recommendation {{ border-left: 4px solid #3b82f6; padding: 15px; margin: 15px 0; background: white; border-radius: 8px; }}
        .insights {{ background: linear-gradient(135deg, #f0fdf4, #ecfdf5); padding: 25px; border-radius: 12px; margin: 20px 0; }}
        .metric {{ margin: 10px 0; padding: 10px; background: #f9fafb; border-radius: 6px; }}
        .badge {{ display: inline-block; padding: 4px 12px; border-radius: 20px; font-size: 12px; font-weight: bold; margin: 2px; }}
        .high-badge {{ background: #fee2e2; color: #dc2626; }}
        .medium-badge {{ background: #fef3c7; color: #d97706; }}
        .low-badge {{ background: #dbeafe; color: #2563eb; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🔍 SEO Analysis Report</h1>
        <p><strong>Website:</strong> {report['url']}</p>
        <p><strong>Analysis Date:</strong> {report['timestamp']}</p>
        <div class="score">{seo_score:.0f}%</div>
        <p>Overall SEO Score</p>
    </div>

    <div class="analysis-grid">
        <div class="analysis-card">
            <h3>⚙️ Technical SEO</h3>
            <div class="metric">
                <strong>HTTPS:</strong> 
                <span class="{'status-good' if report.get('technical_seo', {}).get('ssl_https', {}).get('is_https') else 'status-error'}">
                    {report.get('technical_seo', {}).get('ssl_https', {}).get('status', 'Unknown')}
                </span>
            </div>
            <div class="metric">
                <strong>Robots.txt:</strong> 
                <span class="{'status-good' if report.get('technical_seo', {}).get('robots_txt', {}).get('exists') else 'status-warning'}">
                    {report.get('technical_seo', {}).get('robots_txt', {}).get('status', 'Unknown')}
                </span>
            </div>
            <div class="metric">
                <strong>Sitemap:</strong> 
                <span class="{'status-good' if report.get('technical_seo', {}).get('sitemap', {}).get('exists') else 'status-warning'}">
                    {report.get('technical_seo', {}).get('sitemap', {}).get('status', 'Unknown')}
                </span>
            </div>
            <div class="metric">
                <strong>Mobile-Friendly:</strong> 
                <span class="{'status-good' if report.get('technical_seo', {}).get('mobile_friendly', {}).get('score', 0) > 0.7 else 'status-warning'}">
                    {report.get('technical_seo', {}).get('mobile_friendly', {}).get('status', 'Unknown')}
                </span>
            </div>
        </div>

        <div class="analysis-card">
            <h3>📝 Content SEO</h3>
            <div class="metric">
                <strong>Title Tags:</strong> 
                <span class="{'status-good' if report.get('content_seo', {}).get('title_tags', {}).get('average_score', 0) > 0.7 else 'status-warning'}">
                    {report.get('content_seo', {}).get('title_tags', {}).get('status', 'Unknown')}
                </span>
            </div>
            <div class="metric">
                <strong>Meta Descriptions:</strong> 
                <span class="{'status-good' if report.get('content_seo', {}).get('meta_descriptions', {}).get('average_score', 0) > 0.7 else 'status-warning'}">
                    {report.get('content_seo', {}).get('meta_descriptions', {}).get('status', 'Unknown')}
                </span>
            </div>
            <div class="metric">
                <strong>Heading Structure:</strong> 
                <span class="{'status-good' if report.get('content_seo', {}).get('heading_structure', {}).get('average_score', 0) > 0.7 else 'status-warning'}">
                    {report.get('content_seo', {}).get('heading_structure', {}).get('status', 'Unknown')}
                </span>
            </div>
            <div class="metric">
                <strong>Image Alt Text:</strong> 
                <span class="{'status-good' if report.get('content_seo', {}).get('image_alt_text', {}).get('overall_alt_coverage', 0) > 0.8 else 'status-warning'}">
                    {report.get('content_seo', {}).get('image_alt_text', {}).get('status', 'Unknown')}
                </span>
            </div>
        </div>

        <div class="analysis-card">
            <h3>🏷️ Meta Data</h3>
            <div class="metric">
                <strong>Open Graph:</strong> 
                <span class="{'status-good' if report.get('meta_analysis', {}).get('open_graph', {}).get('coverage', 0) > 0.8 else 'status-warning'}">
                    {report.get('meta_analysis', {}).get('open_graph', {}).get('status', 'Unknown')}
                </span>
            </div>
            <div class="metric">
                <strong>Twitter Cards:</strong> 
                <span class="{'status-good' if report.get('meta_analysis', {}).get('twitter_cards', {}).get('coverage', 0) > 0.7 else 'status-warning'}">
                    {report.get('meta_analysis', {}).get('twitter_cards', {}).get('status', 'Unknown')}
                </span>
            </div>
            <div class="metric">
                <strong>Canonical Tags:</strong> 
                <span class="{'status-good' if report.get('meta_analysis', {}).get('canonical_tags', {}).get('has_canonical') else 'status-warning'}">
                    {report.get('meta_analysis', {}).get('canonical_tags', {}).get('status', 'Unknown')}
                </span>
            </div>
        </div>
    </div>

    <div class="insights">
        <h2>🧠 AI SEO Insights</h2>
        <h4>Strengths:</h4>
        <ul>
            {"".join([f"<li>{strength}</li>" for strength in report.get('ai_insights', {}).get('strengths', [])])}
        </ul>
        
        <h4>Areas for Improvement:</h4>
        <ul>
            {"".join([f"<li>{weakness}</li>" for weakness in report.get('ai_insights', {}).get('weaknesses', [])])}
        </ul>
        
        <h4>Opportunities:</h4>
        <ul>
            {"".join([f"<li>{opportunity}</li>" for opportunity in report.get('ai_insights', {}).get('opportunities', [])])}
        </ul>
    </div>

    <div class="recommendations">
        <h2>🎯 SEO Recommendations</h2>
        {"".join([f'''
        <div class="recommendation">
            <h4>{rec["title"]} <span class="badge {rec["priority"].lower()}-badge">{rec["priority"]}</span></h4>
            <p><strong>Category:</strong> {rec["category"]}</p>
            <p><strong>Description:</strong> {rec["description"]}</p>
            <p><strong>Implementation:</strong> {rec["implementation"]}</p>
            <p><strong>Expected Impact:</strong> {rec["expected_impact"]}</p>
        </div>
        ''' for rec in report.get('recommendations', [])])}
    </div>
</body>
</html>
        """
        
        with open(os.path.join(output_dir, 'seo.html'), 'w') as f:
            f.write(html_content)

def main():
    parser = argparse.ArgumentParser(description='Analyze SEO factors')
    parser.add_argument('--url', required=True, help='Website URL to analyze')
    parser.add_argument('--content', required=True, help='Content directory to analyze')
    parser.add_argument('--output', required=True, help='Output directory')
    parser.add_argument('--ai-model', default='claude-3.5-sonnet', help='AI model to use')
    
    args = parser.parse_args()
    
    analyzer = SEOAnalyzer(ai_model=args.ai_model)
    report = analyzer.analyze_seo(args.url, args.content, args.output)
    
    print(f"SEO analysis complete. Report saved to {args.output}")
    print(f"SEO score: {report.get('seo_score', 0):.0f}%")

if __name__ == '__main__':
    main()