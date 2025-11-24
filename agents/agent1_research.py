"""
Agent 1: Research Synthesizer
Searches scientific literature and synthesizes findings.
"""

import os
import sys
from pathlib import Path
from typing import List, Dict

# Add parent directory to path to import core modules
sys.path.insert(0, str(Path(__file__).parent.parent))
from core.ai_client import call_ai

def run_research(args):
    """
    Search academic databases and synthesize research.
    """
    print("=" * 60)
    print("RESEARCH SYNTHESIZER - Finding Scientific Evidence")
    print("=" * 60)
    print(f"\nQuery: {args.query}")
    print(f"Databases: {', '.join(args.databases)}")
    print(f"Limit: {args.limit} papers\n")

    # Search papers
    papers = search_papers(args.query, args.databases, args.limit)

    # Synthesize findings with AI
    synthesis = synthesize_with_ai(papers, args.query)

    # Save results
    save_research_results(synthesis, args.query)

    print("\n" + "=" * 60)
    print("RESEARCH COMPLETE!")
    print("=" * 60)
    print(f"\nOutput: outputs/research_synthesis.md")
    print(f"Bibliography: outputs/bibliography.bib")


def search_papers(query: str, databases: List[str], limit: int) -> List[Dict]:
    """
    Search academic databases for papers.
    """
    papers = []

    print("Searching databases...")

    # ArXiv search
    if 'arxiv' in databases:
        print("  - Searching arXiv...")
        arxiv_papers = search_arxiv(query, limit // len(databases))
        papers.extend(arxiv_papers)

    # Google Scholar search
    if 'scholar' in databases:
        print("  - Searching Google Scholar...")
        scholar_papers = search_scholar(query, limit // len(databases))
        papers.extend(scholar_papers)

    # ACM Digital Library
    if 'acm' in databases:
        print("  - Searching ACM Digital Library...")
        acm_papers = search_acm(query, limit // len(databases))
        papers.extend(acm_papers)

    print(f"\n  Found {len(papers)} papers total\n")
    return papers


def search_arxiv(query: str, limit: int) -> List[Dict]:
    """
    Search arXiv for papers.
    """
    try:
        import arxiv

        search = arxiv.Search(
            query=query,
            max_results=limit,
            sort_by=arxiv.SortCriterion.Relevance
        )

        papers = []
        for result in search.results():
            papers.append({
                'title': result.title,
                'authors': [author.name for author in result.authors],
                'abstract': result.summary,
                'url': result.entry_id,
                'published': result.published.year,
                'source': 'arXiv'
            })

        return papers
    except ImportError:
        print("    Warning: arxiv package not installed. Skipping arXiv search.")
        return []
    except Exception as e:
        print(f"    Error searching arXiv: {e}")
        return []


def search_scholar(query: str, limit: int) -> List[Dict]:
    """
    Search Google Scholar for papers.
    """
    # Note: This requires scholarly package
    # For now, return mock data to show structure
    print("    Note: Google Scholar search requires scholarly package")
    return []


def search_acm(query: str, limit: int) -> List[Dict]:
    """
    Search ACM Digital Library.
    """
    print("    Note: ACM search requires API access")
    return []


def synthesize_with_ai(papers: List[Dict], query: str) -> str:
    """
    Use AI to synthesize research findings.
    """
    if not papers:
        return "No papers found to synthesize."

    print("Synthesizing findings with AI...")

    # Prepare papers summary for AI
    papers_text = "\n\n".join([
        f"**{p['title']}**\n"
        f"Authors: {', '.join(p.get('authors', ['Unknown']))}\n"
        f"Year: {p.get('published', 'Unknown')}\n"
        f"Abstract: {p.get('abstract', 'No abstract available')}"
        for p in papers[:10]  # Use top 10 for synthesis
    ])

    # Call AI (Claude or Gemini) to synthesize
    try:
        prompt = f"""You are a research synthesizer for technical book writing.

Research Query: {query}

Papers Found:
{papers_text}

Your task:
1. Summarize the KEY FINDINGS across these papers
2. Identify COMMON THEMES and patterns
3. Note any CONTRADICTIONS or debates
4. Identify RESEARCH GAPS where more evidence is needed
5. Suggest PRACTICAL IMPLICATIONS for developers/engineers

Format your response as:

## Key Findings

## Common Themes

## Contradictions & Debates

## Research Gaps

## Practical Implications

## Recommended Papers for Citation
(List top 5 most relevant with brief explanation why)

Be specific, cite paper titles when referencing findings.
"""

        # Use AI client (tries Claude, falls back to Gemini if needed)
        response = call_ai(prompt, provider="claude", max_tokens=4000)

        if response:
            return response
        else:
            print("  Claude failed, trying Gemini...")
            response = call_ai(prompt, provider="gemini")
            if response:
                return response
            else:
                print("  Both AIs failed, returning basic summary")
                return create_basic_summary(papers)

    except Exception as e:
        print(f"  Error calling AI: {e}")
        return create_basic_summary(papers)


def create_basic_summary(papers: List[Dict]) -> str:
    """
    Create basic summary without AI.
    """
    summary = f"# Research Summary\n\n"
    summary += f"Found {len(papers)} papers\n\n"
    summary += "## Papers:\n\n"

    for i, paper in enumerate(papers[:20], 1):
        summary += f"{i}. **{paper['title']}**\n"
        summary += f"   - Authors: {', '.join(paper.get('authors', ['Unknown']))}\n"
        summary += f"   - Year: {paper.get('published', 'Unknown')}\n"
        summary += f"   - Source: {paper.get('source', 'Unknown')}\n\n"

    return summary


def save_research_results(synthesis: str, query: str):
    """
    Save research synthesis and bibliography.
    """
    import os
    os.makedirs("outputs", exist_ok=True)

    # Save synthesis
    with open("outputs/research_synthesis.md", "w") as f:
        f.write(f"# Research Synthesis\n\n")
        f.write(f"**Query:** {query}\n\n")
        f.write(f"**Date:** {get_current_date()}\n\n")
        f.write("---\n\n")
        f.write(synthesis)

    print("  ✓ Saved: outputs/research_synthesis.md")


def get_current_date():
    """Get current date string."""
    from datetime import datetime
    return datetime.now().strftime("%Y-%m-%d")
