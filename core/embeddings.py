"""
Embeddings Engine - Semantic Coherence System
Uses ChromaDB to maintain consistency across chapters
"""

import os
import sys
from pathlib import Path
from typing import List, Dict

try:
    import chromadb
    from chromadb.config import Settings
except ImportError:
    chromadb = None
    print("Warning: chromadb not installed. Install with: pip install chromadb")


class BookEmbeddings:
    """Manages semantic embeddings for book coherence."""

    def __init__(self, book_dir: str = "."):
        """Initialize embeddings database."""
        self.book_dir = Path(book_dir)
        self.embeddings_dir = self.book_dir / "book_embeddings"

        if chromadb is None:
            print("ChromaDB not available - coherence checking disabled")
            self.client = None
            self.collection = None
            return

        # Create embeddings directory
        self.embeddings_dir.mkdir(exist_ok=True)

        # Initialize ChromaDB client
        self.client = chromadb.PersistentClient(path=str(self.embeddings_dir))

        # Get or create collection
        self.collection = self.client.get_or_create_collection(
            name="book_chapters",
            metadata={"description": "Technical book chapters for coherence"}
        )

        print(f"✓ Embeddings database initialized: {self.embeddings_dir}")

    def index_chapter(self, chapter_num: int, content: str, metadata: Dict = None):
        """
        Index a chapter for semantic search.

        Args:
            chapter_num: Chapter number
            content: Full chapter text
            metadata: Additional metadata (title, word_count, etc)
        """
        if self.collection is None:
            print("  Skipping indexing (ChromaDB not available)")
            return

        # Chunk the chapter into paragraphs
        chunks = self._chunk_text(content)

        print(f"  Indexing Chapter {chapter_num}: {len(chunks)} chunks...")

        # Prepare data for ChromaDB
        ids = [f"chapter_{chapter_num}_chunk_{i}" for i in range(len(chunks))]
        metadatas = [{
            "chapter": chapter_num,
            "chunk_index": i,
            **(metadata or {})
        } for i in range(len(chunks))]

        # Add to collection
        self.collection.add(
            documents=chunks,
            ids=ids,
            metadatas=metadatas
        )

        print(f"  ✓ Chapter {chapter_num} indexed ({len(chunks)} chunks)")

    def query_similar(self, query: str, n_results: int = 5) -> List[Dict]:
        """
        Find similar content in existing chapters.

        Args:
            query: Text to search for
            n_results: Number of results to return

        Returns:
            List of similar chunks with metadata
        """
        if self.collection is None:
            return []

        results = self.collection.query(
            query_texts=[query],
            n_results=n_results
        )

        return results

    def get_chapter_context(self, chapter_num: int) -> str:
        """
        Get context from previous chapters for coherence.

        Args:
            chapter_num: Current chapter number

        Returns:
            str: Context summary from previous chapters
        """
        if self.collection is None or chapter_num <= 1:
            return ""

        # Get all chunks from previous chapters
        all_docs = self.collection.get(
            where={"chapter": {"$lt": chapter_num}}
        )

        if not all_docs or not all_docs['documents']:
            return ""

        # Return summary of key points
        context = "\n\n".join(all_docs['documents'][:10])
        return f"Context from previous chapters:\n{context[:2000]}..."

    def check_consistency(self, new_content: str, chapter_num: int) -> Dict:
        """
        Check if new content is consistent with existing chapters.

        Returns:
            Dict with consistency warnings/suggestions
        """
        if self.collection is None:
            return {"status": "skipped", "warnings": []}

        # Query for similar content
        results = self.query_similar(new_content[:500], n_results=5)

        warnings = []
        suggestions = []

        # Analyze results
        if results and results['documents']:
            for i, (doc, meta) in enumerate(zip(results['documents'][0], results['metadatas'][0])):
                if meta.get('chapter', 0) < chapter_num:
                    suggestions.append({
                        "from_chapter": meta['chapter'],
                        "similar_content": doc[:200],
                        "suggestion": "Ensure terminology is consistent"
                    })

        return {
            "status": "checked",
            "warnings": warnings,
            "suggestions": suggestions
        }

    def _chunk_text(self, text: str, chunk_size: int = 500) -> List[str]:
        """Split text into semantic chunks."""
        # Simple paragraph-based chunking
        paragraphs = text.split('\n\n')

        chunks = []
        current_chunk = ""

        for para in paragraphs:
            if len(current_chunk) + len(para) < chunk_size:
                current_chunk += para + "\n\n"
            else:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = para + "\n\n"

        if current_chunk:
            chunks.append(current_chunk.strip())

        return chunks


# Utility functions
def index_existing_chapters(book_dir: str = "."):
    """Index all existing chapters in the book."""
    embeddings = BookEmbeddings(book_dir)

    chapters_dir = Path(book_dir) / "outputs" / "chapters"

    if not chapters_dir.exists():
        print("No chapters directory found")
        return embeddings

    # Find all chapter files
    chapter_files = sorted(chapters_dir.glob("chapter*.md"))

    for chapter_file in chapter_files:
        # Extract chapter number from filename
        try:
            chapter_num = int(chapter_file.stem.replace("chapter", "").replace("_cerebro", "").replace("_deep_work", "")[:2])
        except:
            continue

        # Read and index
        content = chapter_file.read_text()
        if len(content) > 100:  # Only index if has real content
            embeddings.index_chapter(
                chapter_num=chapter_num,
                content=content,
                metadata={"filename": chapter_file.name}
            )

    return embeddings


if __name__ == "__main__":
    # Test indexing
    print("Testing embeddings system...")
    embeddings = index_existing_chapters(".")
    print("\nEmbeddings system ready!")
