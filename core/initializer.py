"""
Project Initializer
Creates new scientific book project structure.
"""

import os
import yaml
from pathlib import Path

def initialize_project(args):
    """
    Initialize a new scientific book project.
    """
    print("=" * 60)
    print("INITIALIZING SCIENTIFIC BOOK PROJECT")
    print("=" * 60)

    # Create directories
    create_directory_structure()

    # Create configuration file
    create_config_file(args)

    # Create manuscript template
    create_manuscript_template(args)

    # Create experiment tracking file
    create_experiment_tracker()

    # Create README
    create_project_readme(args)

    print("\n" + "=" * 60)
    print("PROJECT INITIALIZED!")
    print("=" * 60)
    print(f"\nTitle: {args.title}")
    print(f"Author: {args.author}")
    print(f"Topic: {args.topic}")
    print(f"Target Pages: {args.target_pages}")
    print("\nNext steps:")
    print("1. Edit book_config.yaml with your specific details")
    print("2. Start writing in manuscript.md")
    print("3. Run: python create_scientific_book.py research --query 'your topic'")
    print("=" * 60)


def create_directory_structure():
    """Create project directory structure."""
    directories = [
        "outputs",
        "outputs/research",
        "outputs/experiment_design",
        "outputs/data_analysis",
        "outputs/figures",
        "outputs/chapters",
        "experiments",
        "data",
        "references",
        "assets"
    ]

    for directory in directories:
        os.makedirs(directory, exist_ok=True)

    print("✓ Created directory structure")


def create_config_file(args):
    """Create book_config.yaml with sensible defaults."""

    # Topic-specific keywords and benchmarks
    topic_configs = {
        "productivity": {
            "keywords": [
                "developer productivity",
                "software engineering effectiveness",
                "cognitive load programming",
                "deep work developers",
                "focus and flow state"
            ],
            "benchmarks": [
                "Deep Work by Cal Newport",
                "Agilmente by Estanislao Bachrach",
                "Thinking, Fast and Slow by Daniel Kahneman"
            ]
        },
        "architecture": {
            "keywords": [
                "software architecture patterns",
                "system design principles",
                "architectural decision making",
                "technical debt management"
            ],
            "benchmarks": [
                "Clean Architecture by Robert Martin",
                "Domain-Driven Design by Eric Evans",
                "Software Architecture in Practice"
            ]
        },
        "ai": {
            "keywords": [
                "AI-assisted development",
                "developer productivity AI",
                "code generation effectiveness",
                "AI pair programming"
            ],
            "benchmarks": [
                "AI-Augmented Development (emerging topic)",
                "The Pragmatic Programmer",
                "Accelerate by Nicole Forsgren"
            ]
        },
        "philosophy": {
            "keywords": [
                "philosophy of software",
                "ethics in system design",
                "ontology software systems",
                "stoicism for engineers"
            ],
            "benchmarks": [
                "The Tao of Programming",
                "Zen and the Art of Motorcycle Maintenance",
                "Meditations by Marcus Aurelius"
            ]
        }
    }

    topic_config = topic_configs.get(args.topic, topic_configs["productivity"])

    config = {
        "book": {
            "title": args.title,
            "subtitle": "Evidence-Based Insights for Software Engineers",
            "author": args.author,
            "topic": args.topic,
            "target_words": 75000,
            "target_pages": args.target_pages,
            "target_chapters": 12
        },
        "research": {
            "databases": ["arxiv", "google_scholar", "acm_digital_library"],
            "keywords": topic_config["keywords"]
        },
        "benchmarks": topic_config["benchmarks"],
        "experiments": {
            "planned": [],
            "completed": []
        },
        "writing": {
            "tone": "accessible_expert",
            "style": "evidence_based",
            "balance": {
                "technical": 60,
                "narrative": 40
            }
        },
        "citations": {
            "style": "apa",
            "min_per_chapter": 10
        },
        "validation": {
            "check_logical_fallacies": True,
            "require_evidence": True,
            "flag_absolute_statements": True
        }
    }

    with open("book_config.yaml", "w") as f:
        yaml.dump(config, f, default_flow_style=False, sort_keys=False)

    print("✓ Created book_config.yaml from template")


def create_manuscript_template(args):
    """Create manuscript.md template."""

    template = f"""# {args.title}

**By {args.author}**

---

## Part I: Foundation

### Chapter 1: The Problem

[Start with a compelling anecdote or case study]

[Present data showing the scale of the problem]

[Explain why current solutions fall short]

---

### Chapter 2: The Science Behind It

[Introduce the scientific foundation]

[Review key research findings]

[Build theoretical framework]

---

### Chapter 3: Why Current Approaches Fail

[Analyze existing solutions]

[Present empirical evidence of limitations]

[Set stage for your framework]

---

## Part II: The Framework

### Chapter 4: [Principle 1]

**Hypothesis:** [Your testable claim]

**Evidence:** [Cite research or your experiments]

**Application:** [How developers use this]

**Example:** [Real-world case study]

---

### Chapter 5: [Principle 2]

[Repeat structure]

---

### Chapter 6: [Principle 3]

[Repeat structure]

---

## Part III: Application

### Chapter 7: For Individual Developers

[Practical tactics and tools]

---

### Chapter 8: For Teams

[Team-level practices]

---

### Chapter 9: For Organizations

[Organizational patterns]

---

## Part IV: Advanced Topics

### Chapter 10: Edge Cases & Limitations

[When the framework doesn't apply]

[Acknowledge limitations honestly]

---

### Chapter 11: Future Directions

[Research needed]

[Emerging trends]

[Open questions]

---

## Appendices

### Appendix A: Experimental Methodology

[Detailed experimental protocols]

---

### Appendix B: Statistical Analysis

[Detailed statistical results]

---

### Appendix C: Resources & Tools

[Links to tools, datasets, further reading]

---

## References

[Bibliography will be auto-generated]
"""

    with open("manuscript.md", "w") as f:
        f.write(template)

    print("✓ Created manuscript.md template")


def create_experiment_tracker():
    """Create experiment tracking file."""

    tracker = """# Experiment Tracker

## Planned Experiments

| ID | Hypothesis | Status | Start Date | End Date | Participants |
|----|------------|--------|------------|----------|--------------|
| E01 | [Your hypothesis] | Planned | TBD | TBD | TBD |

## In Progress

| ID | Hypothesis | Started | Progress | Notes |
|----|------------|---------|----------|-------|
| - | - | - | - | - |

## Completed

| ID | Hypothesis | Result | P-value | Effect Size | Conclusion |
|----|------------|--------|---------|-------------|------------|
| - | - | - | - | - | - |

## Notes

- Add notes about experimental findings
- Track issues or unexpected results
- Document lessons learned
"""

    with open("experiments/tracker.md", "w") as f:
        f.write(tracker)

    print("✓ Created experiment tracker")


def create_project_readme(args):
    """Create project README."""

    readme = f"""# {args.title}

**Author:** {args.author}
**Topic:** {args.topic.title()}
**Target:** {args.target_pages} pages

## Project Structure

```
├── manuscript.md              # Main manuscript
├── book_config.yaml          # Configuration
├── outputs/                  # Generated reports
│   ├── research/             # Literature synthesis
│   ├── experiment_design/    # Experimental protocols
│   ├── data_analysis/        # Statistical results
│   └── figures/              # Charts and graphs
├── experiments/              # Experiment tracking
├── data/                     # Raw data
└── references/               # Bibliography
```

## Workflow

1. **Research:** Find scientific evidence
   ```bash
   python ../create_scientific_book.py research --query "your topic"
   ```

2. **Design Experiments:** Create rigorous protocols
   ```bash
   python ../create_scientific_book.py design-experiment --hypothesis "your claim"
   ```

3. **Run Experiments:** (Do this yourself)

4. **Analyze Data:** Generate statistical results
   ```bash
   python ../create_scientific_book.py analyze-data --data data/results.csv
   ```

5. **Write Chapters:** Evidence-based writing
   ```bash
   python ../create_scientific_book.py write-chapter --chapter 4
   ```

6. **Validate:** Check logical rigor
   ```bash
   python ../create_scientific_book.py validate
   ```

7. **Humanize:** Make it engaging
   ```bash
   python ../create_scientific_book.py humanize
   ```

8. **Export:** Generate final PDF
   ```bash
   python ../create_scientific_book.py export --format pdf
   ```

## Status

- [ ] Research phase
- [ ] Experiments designed
- [ ] Data collected
- [ ] Data analyzed
- [ ] Chapters written
- [ ] Arguments validated
- [ ] Narrative polished
- [ ] Final export

## Notes

[Your project notes]
"""

    with open("PROJECT_README.md", "w") as f:
        f.write(readme)

    print("✓ Created PROJECT_README.md")
