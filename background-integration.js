/**
 * Background Content Integration Example
 * 
 * This example shows how to integrate the background knowledge base
 * into the Voither landing page for enhanced context and content.
 */

// Background content loader
class BackgroundContentLoader {
    constructor() {
        this.basePath = './background';
        this.cache = new Map();
    }

    async loadMetadata() {
        try {
            const response = await fetch(`${this.basePath}/metadata.json`);
            return await response.json();
        } catch (error) {
            console.warn('Background metadata not available:', error);
            return null;
        }
    }

    async loadOntologies() {
        try {
            const response = await fetch(`${this.basePath}/ontologies/sample.json`);
            return await response.json();
        } catch (error) {
            console.warn('Ontologies not available:', error);
            return null;
        }
    }

    async loadKnowledgeGraph() {
        try {
            const response = await fetch(`${this.basePath}/graphs/sample.json`);
            return await response.json();
        } catch (error) {
            console.warn('Knowledge graph not available:', error);
            return null;
        }
    }

    async searchContent(query) {
        try {
            const response = await fetch(`${this.basePath}/content_index.json`);
            const index = await response.json();
            
            // Simple search implementation
            const results = index.search_index?.filter(item => 
                item.keywords.some(keyword => 
                    keyword.toLowerCase().includes(query.toLowerCase())
                ) || item.title.toLowerCase().includes(query.toLowerCase())
            ) || [];
            
            return results;
        } catch (error) {
            console.warn('Content search not available:', error);
            return [];
        }
    }

    async getRelatedConcepts(concept) {
        const graph = await this.loadKnowledgeGraph();
        if (!graph) return [];

        const relatedNodes = [];
        const conceptNode = graph.nodes.find(node => 
            node.name.toLowerCase() === concept.toLowerCase()
        );

        if (conceptNode) {
            // Find connected nodes
            graph.edges.forEach(edge => {
                if (edge.source === conceptNode.id) {
                    const targetNode = graph.nodes.find(n => n.id === edge.target);
                    if (targetNode) relatedNodes.push(targetNode);
                }
                if (edge.target === conceptNode.id) {
                    const sourceNode = graph.nodes.find(n => n.id === edge.source);
                    if (sourceNode) relatedNodes.push(sourceNode);
                }
            });
        }

        return relatedNodes;
    }
}

// Content enhancement for landing page
class ContentEnhancer {
    constructor() {
        this.loader = new BackgroundContentLoader();
        this.initialized = false;
    }

    async initialize() {
        if (this.initialized) return;
        
        this.metadata = await this.loader.loadMetadata();
        this.ontologies = await this.loader.loadOntologies();
        this.graph = await this.loader.loadKnowledgeGraph();
        
        this.initialized = true;
        console.log('Background content system initialized');
    }

    async enhanceTextContent() {
        await this.initialize();
        
        // Find text elements that could be enhanced
        const textElements = document.querySelectorAll('[data-key]');
        
        textElements.forEach(async (element) => {
            const key = element.getAttribute('data-key');
            const text = element.textContent;
            
            // Check if any concepts from our knowledge base appear in the text
            if (this.ontologies?.concepts) {
                this.ontologies.concepts.forEach(concept => {
                    if (text.toLowerCase().includes(concept.term.toLowerCase())) {
                        this.addConceptTooltip(element, concept);
                    }
                });
            }
        });
    }

    addConceptTooltip(element, concept) {
        // Add tooltip or enhancement for recognized concepts
        element.style.position = 'relative';
        element.title = `${concept.term}: ${concept.definition}`;
        
        // Optional: Add visual indicator
        if (!element.classList.contains('concept-enhanced')) {
            element.classList.add('concept-enhanced');
            
            // Add subtle styling for enhanced concepts
            const style = document.createElement('style');
            style.textContent = `
                .concept-enhanced {
                    border-bottom: 1px dotted var(--highlight-color);
                    cursor: help;
                }
            `;
            if (!document.querySelector('#concept-enhancement-styles')) {
                style.id = 'concept-enhancement-styles';
                document.head.appendChild(style);
            }
        }
    }

    async addContextualSidebar() {
        await this.initialize();
        
        // Create contextual sidebar with related concepts
        const sidebar = document.createElement('div');
        sidebar.id = 'contextual-sidebar';
        sidebar.innerHTML = `
            <div class="context-panel">
                <h3>Related Concepts</h3>
                <div id="related-concepts"></div>
                <h3>Quick Search</h3>
                <input type="text" id="context-search" placeholder="Search knowledge base...">
                <div id="search-results"></div>
            </div>
        `;
        
        // Add CSS for sidebar
        const sidebarStyles = `
            #contextual-sidebar {
                position: fixed;
                right: -300px;
                top: 50%;
                transform: translateY(-50%);
                width: 280px;
                background: var(--bg-secondary);
                border: 1px solid var(--grid-color);
                border-radius: 8px;
                padding: 1rem;
                transition: right 0.3s ease;
                z-index: 1000;
                max-height: 80vh;
                overflow-y: auto;
            }
            
            #contextual-sidebar:hover,
            #contextual-sidebar.active {
                right: 10px;
            }
            
            .context-panel h3 {
                margin: 0 0 0.5rem 0;
                font-size: 0.9rem;
                color: var(--text-primary);
            }
            
            #context-search {
                width: 100%;
                padding: 0.5rem;
                border: 1px solid var(--grid-color);
                border-radius: 4px;
                background: var(--bg-primary);
                color: var(--text-primary);
                margin-bottom: 0.5rem;
            }
            
            .search-result {
                padding: 0.25rem 0;
                font-size: 0.8rem;
                color: var(--text-secondary);
                border-bottom: 1px solid var(--grid-color);
            }
        `;
        
        const styleSheet = document.createElement('style');
        styleSheet.textContent = sidebarStyles;
        document.head.appendChild(styleSheet);
        
        document.body.appendChild(sidebar);
        
        // Add search functionality
        const searchInput = document.getElementById('context-search');
        const searchResults = document.getElementById('search-results');
        
        searchInput.addEventListener('input', async (e) => {
            const query = e.target.value;
            if (query.length > 2) {
                const results = await this.loader.searchContent(query);
                this.displaySearchResults(results, searchResults);
            } else {
                searchResults.innerHTML = '';
            }
        });
    }

    displaySearchResults(results, container) {
        container.innerHTML = '';
        
        if (results.length === 0) {
            container.innerHTML = '<div class="search-result">No results found</div>';
            return;
        }
        
        results.slice(0, 5).forEach(result => {
            const resultDiv = document.createElement('div');
            resultDiv.className = 'search-result';
            resultDiv.innerHTML = `
                <strong>${result.title}</strong><br>
                <small>${result.category} - ${result.type}</small>
            `;
            container.appendChild(resultDiv);
        });
    }

    async addSmartTooltips() {
        await this.initialize();
        
        // Add intelligent tooltips for technical terms
        const technicalTerms = [
            'BRRE', 'AUTOAGENCY', 'HOLOFRACTOR', 'MEDSCRIBE', 'PEER-AI',
            'kairos', 'E2E Pipeline', 'lived time', 'clinical time'
        ];
        
        technicalTerms.forEach(async (term) => {
            const regex = new RegExp(`\\b${term}\\b`, 'gi');
            this.highlightTerm(term, regex);
        });
    }

    highlightTerm(term, regex) {
        // Walk through text nodes and highlight terms
        const walker = document.createTreeWalker(
            document.body,
            NodeFilter.SHOW_TEXT,
            null,
            false
        );
        
        const textNodes = [];
        let node;
        
        while (node = walker.nextNode()) {
            if (regex.test(node.textContent)) {
                textNodes.push(node);
            }
        }
        
        textNodes.forEach(textNode => {
            const parent = textNode.parentNode;
            const newHTML = textNode.textContent.replace(regex, 
                `<span class="smart-tooltip" data-term="${term}">$&</span>`
            );
            
            const wrapper = document.createElement('div');
            wrapper.innerHTML = newHTML;
            
            while (wrapper.firstChild) {
                parent.insertBefore(wrapper.firstChild, textNode);
            }
            parent.removeChild(textNode);
        });
    }
}

// Initialize content enhancement when page loads
document.addEventListener('DOMContentLoaded', async () => {
    const enhancer = new ContentEnhancer();
    
    // Add enhancements progressively
    await enhancer.enhanceTextContent();
    await enhancer.addSmartTooltips();
    
    // Optional: Add contextual sidebar (can be enabled/disabled)
    // await enhancer.addContextualSidebar();
    
    console.log('Voither background content integration complete');
});

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { BackgroundContentLoader, ContentEnhancer };
}