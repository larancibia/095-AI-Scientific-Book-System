#!/usr/bin/env python3
"""
Coherent Chapter Generator
Uses embeddings to maintain consistency across chapters.
"""

import sys
from pathlib import Path

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.embeddings import BookEmbeddings
from core.ai_client import call_ai


def generate_chapter_with_coherence(
    chapter_num: int,
    chapter_title: str,
    outline: str,
    book_dir: str = ".",
    provider: str = "claude"
):
    """
    Generate a chapter using embeddings for coherence.

    Args:
        chapter_num: Chapter number
        chapter_title: Chapter title
        outline: Chapter outline/instructions
        book_dir: Book project directory
        provider: AI provider (claude or gemini)
    """
    print(f"\n{'='*60}")
    print(f"GENERATING CHAPTER {chapter_num}: {chapter_title}")
    print(f"{'='*60}\n")

    # Initialize embeddings
    embeddings = BookEmbeddings(book_dir)

    # Get context from previous chapters
    context = ""
    if chapter_num > 1:
        print(f"  Retrieving context from previous chapters...")
        context = embeddings.get_chapter_context(chapter_num)
        print(f"  ✓ Got context from {chapter_num-1} previous chapters\n")

    # Build prompt with context
    prompt = f"""You are writing Chapter {chapter_num} of "El Desarrollador Ágil", a technical book on developer productivity.

**Chapter {chapter_num}: {chapter_title}**

{outline}

{'**IMPORTANT - Maintain consistency with previous chapters:**' if context else ''}
{context if context else ''}

**Requirements:**
- Write in Spanish (España/Latin America neutral)
- 4,000-5,000 words
- Scientific rigor (cite sources)
- Balance: 60% technical, 40% narrative
- Include:
  * Opening hook (compelling anecdote)
  * Scientific evidence (studies, data)
  * Practical frameworks
  * Code examples where relevant
  * Takeaways section
- Style: Like "Agilmente" by Bachrach - accessible but rigorous
- Format: Markdown

Write the COMPLETE chapter now.
"""

    print(f"  Generating chapter with {provider}...")

    # Generate with AI
    chapter_content = call_ai(prompt, provider=provider, max_tokens=8000)

    if not chapter_content:
        print(f"  ✗ Failed to generate chapter")
        return None

    # Save chapter
    output_path = Path(book_dir) / "outputs" / "chapters" / f"chapter{chapter_num:02d}_{chapter_title.lower().replace(' ', '_')}.md"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(chapter_content)

    word_count = len(chapter_content.split())
    print(f"  ✓ Chapter saved: {output_path}")
    print(f"  ✓ Word count: {word_count:,}")

    # Index the new chapter
    if embeddings.collection:
        print(f"  Indexing chapter for future coherence...")
        embeddings.index_chapter(
            chapter_num=chapter_num,
            content=chapter_content,
            metadata={
                "title": chapter_title,
                "word_count": word_count
            }
        )
        print(f"  ✓ Chapter indexed\n")

    return chapter_content


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Generate coherent book chapters")
    parser.add_argument("--chapter", type=int, required=True, help="Chapter number")
    parser.add_argument("--title", required=True, help="Chapter title")
    parser.add_argument("--outline", required=True, help="Chapter outline")
    parser.add_argument("--provider", default="claude", choices=["claude", "gemini"])
    parser.add_argument("--book-dir", default=".", help="Book directory")

    args = parser.parse_args()

    generate_chapter_with_coherence(
        chapter_num=args.chapter,
        chapter_title=args.title,
        outline=args.outline,
        book_dir=args.book_dir,
        provider=args.provider
    )
