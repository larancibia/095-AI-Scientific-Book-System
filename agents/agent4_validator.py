"""
Agent 4: Argument Validator
Validates logical consistency and evidence for all claims.
"""

import os
import anthropic
from pathlib import Path

LOGICAL_FALLACIES = [
    "Ad hominem",
    "Straw man",
    "False dichotomy",
    "Slippery slope",
    "Appeal to authority (without evidence)",
    "Correlation implies causation",
    "Hasty generalization",
    "Cherry picking data",
    "Post hoc ergo propter hoc",
    "Circular reasoning"
]

def validate_arguments(args):
    """
    Validate all arguments and claims in the manuscript.
    """
    print("=" * 60)
    print("ARGUMENT VALIDATOR - Checking Logical Rigor")
    print("=" * 60)
    print(f"\nMode: {'STRICT' if args.strict else 'Standard'}\n")

    # Read manuscript
    manuscript = read_manuscript()

    if not manuscript:
        print("Error: manuscript.md not found")
        return

    # Validate with AI
    report = validate_with_ai(manuscript, args.strict)

    # Save validation report
    save_validation_report(report)

    print("\n" + "=" * 60)
    print("VALIDATION COMPLETE!")
    print("=" * 60)
    print(f"\nReport: outputs/argument_validation_report.md")


def read_manuscript():
    """Read the manuscript file."""
    manuscript_path = Path("manuscript.md")
    if manuscript_path.exists():
        return manuscript_path.read_text()
    return None


def validate_with_ai(manuscript: str, strict: bool) -> str:
    """
    Use AI to validate arguments and check for logical fallacies.
    """
    print("Analyzing manuscript for logical rigor...")

    try:
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            print("  Warning: ANTHROPIC_API_KEY not set.")
            return create_basic_validation(manuscript)

        client = anthropic.Anthropic(api_key=api_key)

        fallacies_list = "\n".join([f"- {f}" for f in LOGICAL_FALLACIES])

        prompt = f"""You are a critical thinking expert and scientific reviewer.

Your task: Analyze this technical manuscript for logical rigor and evidence-based claims.

**Manuscript:**
{manuscript[:8000]}

**Check for:**

1. **Logical Fallacies**
   Common fallacies to watch for:
   {fallacies_list}

2. **Unsupported Claims**
   - Absolute statements without evidence ("always", "never", "all")
   - Generalizations from limited data
   - Claims lacking citations

3. **Correlation vs Causation Errors**
   - Are causal claims properly supported?
   - Are correlations presented as mere associations?

4. **Cherry-Picked Data**
   - Are counterexamples ignored?
   - Is conflicting evidence acknowledged?

5. **Strength of Evidence**
   - Rate each major claim's evidence quality (1-5 stars)
   - Anecdote (1 star) vs. Controlled experiment (5 stars)

6. **Missing Qualifiers**
   - Should "X causes Y" be "X may contribute to Y"?
   - Are limitations acknowledged?

7. **Argument Structure**
   - Are premises clearly stated?
   - Do conclusions follow logically?

**Output Format:**

## Executive Summary
[Overall assessment - is this rigorous or not?]

## Critical Issues (Must Fix)
[Logical fallacies, unsupported major claims]

## Warnings (Should Fix)
[Weak evidence, missing qualifiers, overgeneralizations]

## Suggestions (Consider)
[Ways to strengthen arguments]

## Strengths
[What's done well]

## Evidence Quality Table
| Claim | Evidence Type | Quality (1-5★) | Recommendation |
|-------|--------------|---------------|----------------|
| ...   | ...          | ...           | ...            |

Be {"extremely strict and" if strict else ""} specific. Quote exact passages when flagging issues.
"""

        message = client.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=4000,
            messages=[{"role": "user", "content": prompt}]
        )

        return message.content[0].text

    except Exception as e:
        print(f"  Error: {e}")
        return create_basic_validation(manuscript)


def create_basic_validation(manuscript: str) -> str:
    """
    Create basic validation without AI.
    """
    issues = []

    # Check for absolute statements
    absolutes = ["always", "never", "all ", "none ", "every ", "impossible"]
    for word in absolutes:
        if word in manuscript.lower():
            issues.append(f"- Found absolute statement: '{word}' - consider qualifying")

    # Check for weasel words
    weasels = ["might", "possibly", "arguably", "perhaps", "maybe"]
    for word in weasels:
        count = manuscript.lower().count(word)
        if count > 5:
            issues.append(f"- Overuse of '{word}' ({count} times) - be more specific")

    report = "# Validation Report\n\n"
    report += "## Automated Checks\n\n"

    if issues:
        report += "\n".join(issues)
    else:
        report += "No automated issues found.\n"

    report += "\n\n**Note:** Full validation requires ANTHROPIC_API_KEY.\n"

    return report


def save_validation_report(report: str):
    """Save validation report."""
    os.makedirs("outputs", exist_ok=True)

    with open("outputs/argument_validation_report.md", "w") as f:
        f.write("# Argument Validation Report\n\n")
        f.write(f"**Generated:** {get_timestamp()}\n\n")
        f.write("---\n\n")
        f.write(report)

    print("  ✓ Saved validation report")


def get_timestamp():
    """Get current timestamp."""
    from datetime import datetime
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
