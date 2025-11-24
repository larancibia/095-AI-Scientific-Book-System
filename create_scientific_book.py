#!/usr/bin/env python3
"""
AI Scientific Book Creation System
Create evidence-based technical non-fiction books with scientific rigor.
"""

import argparse
import sys
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(
        description="AI Scientific Book System - Create bestsellers with evidence",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Initialize new book project
  python create_scientific_book.py init --title "The Productive Developer" --topic productivity

  # Research scientific papers
  python create_scientific_book.py research --query "developer productivity studies"

  # Design experiment
  python create_scientific_book.py design-experiment --hypothesis "Pomodoro improves focus"

  # Analyze experimental data
  python create_scientific_book.py analyze-data --data experiments/results.csv

  # Write chapter with evidence
  python create_scientific_book.py write-chapter --chapter 4 --type experimental

  # Validate all arguments and claims
  python create_scientific_book.py validate

  # Humanize technical content
  python create_scientific_book.py humanize

  # Export to PDF
  python create_scientific_book.py export --format pdf
        """
    )

    subparsers = parser.add_subparsers(dest='command', help='Command to run')

    # Init command
    init_parser = subparsers.add_parser('init', help='Initialize new book project')
    init_parser.add_argument('--title', required=True, help='Book title')
    init_parser.add_argument('--topic', required=True,
                            choices=['productivity', 'architecture', 'ai', 'philosophy', 'custom'],
                            help='Book topic/genre')
    init_parser.add_argument('--author', required=True, help='Author name')
    init_parser.add_argument('--target-pages', type=int, default=280, help='Target page count')

    # Research command
    research_parser = subparsers.add_parser('research', help='Search and synthesize research')
    research_parser.add_argument('--query', required=True, help='Research query')
    research_parser.add_argument('--databases', nargs='+',
                                choices=['arxiv', 'scholar', 'pubmed', 'acm'],
                                default=['arxiv', 'scholar'],
                                help='Databases to search')
    research_parser.add_argument('--limit', type=int, default=50, help='Max papers to retrieve')

    # Design experiment command
    experiment_parser = subparsers.add_parser('design-experiment',
                                             help='Design scientific experiment')
    experiment_parser.add_argument('--hypothesis', required=True, help='Hypothesis to test')
    experiment_parser.add_argument('--participants', type=int, default=50,
                                  help='Number of participants')
    experiment_parser.add_argument('--duration', type=int, default=4,
                                  help='Duration in weeks')

    # Analyze data command
    analyze_parser = subparsers.add_parser('analyze-data', help='Analyze experimental data')
    analyze_parser.add_argument('--data', required=True, help='Path to data file (CSV)')
    analyze_parser.add_argument('--visualize', action='store_true',
                               help='Generate visualizations')

    # Write chapter command
    write_parser = subparsers.add_parser('write-chapter', help='Write book chapter')
    write_parser.add_argument('--chapter', type=int, required=True, help='Chapter number')
    write_parser.add_argument('--type', choices=['intro', 'experimental', 'framework', 'application'],
                             default='experimental', help='Chapter type')
    write_parser.add_argument('--length', type=int, default=5000,
                             help='Target word count')

    # Validate command
    validate_parser = subparsers.add_parser('validate', help='Validate arguments and claims')
    validate_parser.add_argument('--strict', action='store_true',
                                help='Strict validation mode')

    # Humanize command
    humanize_parser = subparsers.add_parser('humanize', help='Make content more engaging')
    humanize_parser.add_argument('--chapter', type=int, help='Specific chapter (or all)')
    humanize_parser.add_argument('--balance', type=int, default=40,
                                help='Narrative balance (0-100, default 40)')

    # Export command
    export_parser = subparsers.add_parser('export', help='Export manuscript')
    export_parser.add_argument('--format', choices=['pdf', 'epub', 'latex', 'markdown'],
                              default='pdf', help='Export format')
    export_parser.add_argument('--output', help='Output file path')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    # Route to appropriate handler
    if args.command == 'init':
        from core.initializer import initialize_project
        initialize_project(args)
    elif args.command == 'research':
        from agents.agent1_research import run_research
        run_research(args)
    elif args.command == 'design-experiment':
        from agents.agent2_experiment import design_experiment
        design_experiment(args)
    elif args.command == 'analyze-data':
        from agents.agent3_analyzer import analyze_data
        analyze_data(args)
    elif args.command == 'write-chapter':
        from core.chapter_writer import write_chapter
        write_chapter(args)
    elif args.command == 'validate':
        from agents.agent4_validator import validate_arguments
        validate_arguments(args)
    elif args.command == 'humanize':
        from agents.agent6_humanizer import humanize_content
        humanize_content(args)
    elif args.command == 'export':
        from tools.exporter import export_manuscript
        export_manuscript(args)
    else:
        print(f"Unknown command: {args.command}")
        sys.exit(1)

if __name__ == "__main__":
    main()
