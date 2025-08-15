#!/usr/bin/env python3
"""
Embeddings and Vector Generation Script for Voither Landing Page

This script generates semantic embeddings and vector representations of the processed content.
"""

import argparse
import json
import os
import numpy as np
from pathlib import Path
from typing import Dict, List, Any
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class EmbeddingGenerator:
    """Generates embeddings and vector representations of content."""
    
    def __init__(self, input_dir: str, output_dir: str):
        self.input_dir = Path(input_dir)
        self.output_dir = Path(output_dir)
        self.vectorizer = TfidfVectorizer(
            max_features=1000,
            stop_words='english',
            ngram_range=(1, 2)
        )
        self.documents = []
        self.document_metadata = []
    
    def generate_all(self):
        """Main function to generate all embeddings."""
        print("🧮 Starting embedding generation...")
        
        # Ensure output directory exists
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Load and prepare documents
        self.load_documents()
        
        if not self.documents:
            print("⚠️  No documents found. Creating sample embeddings.")
            self.create_sample_embeddings()
            return
        
        # Generate TF-IDF vectors
        self.generate_tfidf_embeddings()
        
        # Generate similarity matrices
        self.generate_similarity_matrices()
        
        # Generate concept embeddings
        self.generate_concept_embeddings()
        
        # Save embedding metadata
        self.save_embedding_metadata()
        
        print("✅ Embedding generation complete.")
    
    def load_documents(self):
        """Load all processed documents."""
        parsings_dir = self.input_dir / "parsings"
        
        if not parsings_dir.exists():
            return
        
        # Load markdown parsings
        markdown_dir = parsings_dir / "markdown"
        if markdown_dir.exists():
            for json_file in markdown_dir.glob("*.json"):
                try:
                    with open(json_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    
                    self.documents.append(data.get('content', ''))
                    self.document_metadata.append({
                        "source": str(json_file.relative_to(self.input_dir)),
                        "title": data.get('title', 'Untitled'),
                        "type": "markdown",
                        "concepts": data.get('concepts', [])
                    })
                    
                except Exception as e:
                    print(f"❌ Error loading {json_file}: {e}")
        
        # Load structured content
        structured_dir = parsings_dir / "structured"
        if structured_dir.exists():
            for json_file in structured_dir.glob("*.json"):
                try:
                    with open(json_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    
                    # Convert structured data to text for embedding
                    text_content = self.structured_to_text(data.get('data', {}))
                    self.documents.append(text_content)
                    self.document_metadata.append({
                        "source": str(json_file.relative_to(self.input_dir)),
                        "title": json_file.stem,
                        "type": "structured",
                        "concepts": []
                    })
                    
                except Exception as e:
                    print(f"❌ Error loading {json_file}: {e}")
        
        print(f"📚 Loaded {len(self.documents)} documents for embedding.")
    
    def structured_to_text(self, data: Dict) -> str:
        """Convert structured data to text for embedding."""
        def extract_text(obj, texts=None):
            if texts is None:
                texts = []
            
            if isinstance(obj, dict):
                for key, value in obj.items():
                    texts.append(str(key))
                    extract_text(value, texts)
            elif isinstance(obj, list):
                for item in obj:
                    extract_text(item, texts)
            else:
                texts.append(str(obj))
            
            return texts
        
        texts = extract_text(data)
        return ' '.join(texts)
    
    def generate_tfidf_embeddings(self):
        """Generate TF-IDF embeddings for all documents."""
        try:
            # Fit TF-IDF vectorizer
            tfidf_matrix = self.vectorizer.fit_transform(self.documents)
            
            # Save TF-IDF vectors
            embeddings_data = {
                "vectors": tfidf_matrix.toarray().tolist(),
                "feature_names": self.vectorizer.get_feature_names_out().tolist(),
                "documents": self.document_metadata,
                "method": "tfidf",
                "vocabulary_size": len(self.vectorizer.vocabulary_),
                "document_count": len(self.documents)
            }
            
            output_file = self.output_dir / "tfidf_embeddings.json"
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(embeddings_data, f, indent=2, ensure_ascii=False)
            
            print(f"📊 Generated TF-IDF embeddings: {tfidf_matrix.shape}")
            
        except Exception as e:
            print(f"❌ Error generating TF-IDF embeddings: {e}")
    
    def generate_similarity_matrices(self):
        """Generate document similarity matrices."""
        try:
            # Load TF-IDF embeddings
            embeddings_file = self.output_dir / "tfidf_embeddings.json"
            if not embeddings_file.exists():
                return
            
            with open(embeddings_file, 'r', encoding='utf-8') as f:
                embeddings_data = json.load(f)
            
            vectors = np.array(embeddings_data["vectors"])
            
            # Calculate cosine similarity
            similarity_matrix = cosine_similarity(vectors)
            
            # Find most similar documents for each document
            similarities = []
            for i, doc_similarities in enumerate(similarity_matrix):
                # Get top 5 most similar documents (excluding self)
                similar_indices = np.argsort(doc_similarities)[::-1][1:6]
                
                similarities.append({
                    "document_index": i,
                    "document_title": self.document_metadata[i]["title"],
                    "similar_documents": [
                        {
                            "index": int(idx),
                            "title": self.document_metadata[idx]["title"],
                            "similarity": float(doc_similarities[idx])
                        }
                        for idx in similar_indices
                        if doc_similarities[idx] > 0.1  # Only include meaningful similarities
                    ]
                })
            
            # Save similarity data
            similarity_data = {
                "similarity_matrix": similarity_matrix.tolist(),
                "document_similarities": similarities,
                "method": "cosine_similarity",
                "threshold": 0.1
            }
            
            output_file = self.output_dir / "document_similarities.json"
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(similarity_data, f, indent=2, ensure_ascii=False)
            
            print(f"🔗 Generated similarity matrix: {similarity_matrix.shape}")
            
        except Exception as e:
            print(f"❌ Error generating similarity matrices: {e}")
    
    def generate_concept_embeddings(self):
        """Generate embeddings for extracted concepts."""
        try:
            # Collect all concepts
            all_concepts = set()
            concept_documents = {}
            
            for i, metadata in enumerate(self.document_metadata):
                for concept in metadata.get("concepts", []):
                    all_concepts.add(concept)
                    if concept not in concept_documents:
                        concept_documents[concept] = []
                    concept_documents[concept].append(i)
            
            if not all_concepts:
                print("⚠️  No concepts found for embedding.")
                return
            
            # Create concept vectors based on document co-occurrence
            concept_vectors = {}
            
            for concept in all_concepts:
                # Create a vector for this concept based on TF-IDF of documents containing it
                doc_indices = concept_documents[concept]
                
                if hasattr(self, 'vectorizer') and len(doc_indices) > 0:
                    # Get average TF-IDF vector for documents containing this concept
                    embeddings_file = self.output_dir / "tfidf_embeddings.json"
                    if embeddings_file.exists():
                        with open(embeddings_file, 'r', encoding='utf-8') as f:
                            embeddings_data = json.load(f)
                        
                        vectors = np.array(embeddings_data["vectors"])
                        concept_vector = np.mean(vectors[doc_indices], axis=0)
                        concept_vectors[concept] = concept_vector.tolist()
            
            # Save concept embeddings
            concept_data = {
                "concept_vectors": concept_vectors,
                "concept_documents": concept_documents,
                "total_concepts": len(all_concepts),
                "method": "document_cooccurrence"
            }
            
            output_file = self.output_dir / "concept_embeddings.json"
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(concept_data, f, indent=2, ensure_ascii=False)
            
            print(f"🎯 Generated concept embeddings for {len(all_concepts)} concepts")
            
        except Exception as e:
            print(f"❌ Error generating concept embeddings: {e}")
    
    def create_sample_embeddings(self):
        """Create sample embeddings when no documents are available."""
        print("📝 Creating sample embeddings...")
        
        # Sample documents for Voither
        sample_docs = [
            "BRRE reasoning engine operates in lived time kairos clinical decision making",
            "AUTOAGENCY automates documentation orders scheduling billing with auditing",
            "E2E Pipeline connects speech to signal decision paperwork with ROI",
            "MEDSCRIBE clinical documentation assistant medical scribing",
            "HOLOFRACTOR patient data analysis medical insights",
            "PEER-AI collaborative intelligence system medical consultation",
            "Compliance that compiles HIPAA LGPD FHIR standards into code",
            "Rhizomatic memory signal layers knowledge graph representations"
        ]
        
        sample_metadata = [
            {"title": f"Sample Document {i+1}", "type": "sample", "concepts": []}
            for i in range(len(sample_docs))
        ]
        
        # Generate TF-IDF for sample docs
        tfidf_matrix = self.vectorizer.fit_transform(sample_docs)
        
        embeddings_data = {
            "vectors": tfidf_matrix.toarray().tolist(),
            "feature_names": self.vectorizer.get_feature_names_out().tolist(),
            "documents": sample_metadata,
            "method": "tfidf_sample",
            "vocabulary_size": len(self.vectorizer.vocabulary_),
            "document_count": len(sample_docs),
            "note": "Sample embeddings generated - replace with actual docs content"
        }
        
        output_file = self.output_dir / "tfidf_embeddings.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(embeddings_data, f, indent=2, ensure_ascii=False)
        
        print("✅ Created sample TF-IDF embeddings")
    
    def save_embedding_metadata(self):
        """Save metadata about the embedding generation process."""
        metadata = {
            "input_directory": str(self.input_dir),
            "output_directory": str(self.output_dir),
            "document_count": len(self.documents),
            "embedding_methods": ["tfidf", "cosine_similarity"],
            "features": {
                "max_features": 1000,
                "ngram_range": [1, 2],
                "stop_words": "english"
            },
            "files_generated": [
                "tfidf_embeddings.json",
                "document_similarities.json",
                "concept_embeddings.json",
                "embedding_metadata.json"
            ]
        }
        
        output_file = self.output_dir / "embedding_metadata.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)


def main():
    parser = argparse.ArgumentParser(description='Generate embeddings for processed documentation')
    parser.add_argument('--input', required=True, help='Input background directory')
    parser.add_argument('--output', required=True, help='Output vectors directory')
    
    args = parser.parse_args()
    
    generator = EmbeddingGenerator(args.input, args.output)
    generator.generate_all()


if __name__ == "__main__":
    main()