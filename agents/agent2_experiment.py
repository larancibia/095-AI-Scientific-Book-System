"""
Agent 2: Experiment Designer
Designs rigorous experiments to test hypotheses.
"""

import os
import sys
import yaml
from pathlib import Path
from datetime import datetime

# Add parent directory to path to import core modules
sys.path.insert(0, str(Path(__file__).parent.parent))
from core.ai_client import call_ai

def design_experiment(args):
    """
    Design a scientific experiment to test a hypothesis.
    """
    print("=" * 60)
    print("EXPERIMENT DESIGNER - Creating Research Protocol")
    print("=" * 60)
    print(f"\nHypothesis: {args.hypothesis}")
    print(f"Participants: {args.participants}")
    print(f"Duration: {args.duration} weeks\n")

    # Generate experiment design with AI
    design = generate_experiment_design(
        hypothesis=args.hypothesis,
        participants=args.participants,
        duration=args.duration
    )

    # Save experiment protocol
    save_experiment_protocol(design, args.hypothesis)

    print("\n" + "=" * 60)
    print("EXPERIMENT DESIGN COMPLETE!")
    print("=" * 60)
    print(f"\nProtocol: outputs/experiment_design/protocol.md")
    print(f"Data Collection Template: outputs/experiment_design/data_template.csv")
    print(f"Statistical Plan: outputs/experiment_design/statistical_analysis_plan.md")


def generate_experiment_design(hypothesis: str, participants: int, duration: int) -> dict:
    """
    Use AI to design a rigorous experiment.
    """
    print("Designing experiment with AI...")

    try:
        prompt = f"""You are an experimental design expert helping to create rigorous experiments for a technical book.

**Hypothesis to Test:**
{hypothesis}

**Constraints:**
- Participants: {participants} people
- Duration: {duration} weeks
- Context: Software developers/engineers
- Must be practically feasible (not requiring expensive equipment)
- Must produce measurable, quantifiable results

**Your Task:**
Design a complete experimental protocol including:

1. **Null Hypothesis (H0) and Alternative Hypothesis (H1)**
   - Be specific and measurable

2. **Experimental Design Type**
   - Choose: A/B test, factorial design, repeated measures, etc.
   - Justify your choice

3. **Independent Variables (what you manipulate)**
   - Define clearly
   - Specify levels/conditions

4. **Dependent Variables (what you measure)**
   - List all metrics
   - Specify measurement method
   - Indicate units

5. **Control Variables (what you keep constant)**
   - List everything that could confound results

6. **Randomization Strategy**
   - How to assign participants to conditions

7. **Data Collection Procedure**
   - Day-by-day or week-by-week protocol
   - What data to collect when
   - Tools/methods for collection

8. **Sample Size Justification**
   - Is {participants} enough for statistical power?
   - What effect size can we detect?

9. **Statistical Analysis Plan**
   - What statistical tests to use
   - Significance level (alpha)
   - How to handle missing data

10. **Potential Threats to Validity**
    - Internal validity issues
    - External validity concerns
    - How to mitigate

11. **Ethical Considerations**
    - Informed consent
    - Privacy/data protection
    - Potential harms

12. **Timeline**
    - Week-by-week breakdown

Format as structured YAML that can be parsed.
"""

        # Use AI client (tries Claude, falls back to Gemini if needed)
        ai_response = call_ai(prompt, provider="claude", max_tokens=4000)

        if not ai_response:
            print("  Claude failed, trying Gemini...")
            ai_response = call_ai(prompt, provider="gemini")

        if not ai_response:
            print("  Both AIs failed, using template")
            return create_template_design(hypothesis, participants, duration)

        # Try to extract YAML if present
        if "```yaml" in ai_response:
            yaml_start = ai_response.find("```yaml") + 7
            yaml_end = ai_response.find("```", yaml_start)
            yaml_content = ai_response[yaml_start:yaml_end].strip()
            try:
                design = yaml.safe_load(yaml_content)
            except:
                design = {"full_text": ai_response}
        else:
            design = {"full_text": ai_response}

        design['raw_response'] = ai_response
        return design

    except Exception as e:
        print(f"  Error calling AI: {e}")
        return create_template_design(hypothesis, participants, duration)


def create_template_design(hypothesis: str, participants: int, duration: int) -> dict:
    """
    Create a template experiment design.
    """
    return {
        "hypothesis": hypothesis,
        "participants": participants,
        "duration_weeks": duration,
        "design_type": "A/B Test",
        "null_hypothesis": "There is no difference between control and treatment groups",
        "alternative_hypothesis": hypothesis,
        "independent_variables": [
            {
                "name": "intervention",
                "levels": ["control", "treatment"]
            }
        ],
        "dependent_variables": [
            {
                "name": "primary_outcome",
                "measurement": "To be defined",
                "unit": "To be defined"
            }
        ],
        "timeline": [
            {"week": 1, "activity": "Baseline measurements"},
            {"week": 2, "activity": "Begin intervention"},
            {"week": duration, "activity": "Final measurements"}
        ],
        "statistical_analysis": {
            "test": "Independent t-test",
            "alpha": 0.05,
            "power": 0.80
        }
    }


def save_experiment_protocol(design: dict, hypothesis: str):
    """
    Save experiment protocol files.
    """
    os.makedirs("outputs/experiment_design", exist_ok=True)

    # Save main protocol
    with open("outputs/experiment_design/protocol.md", "w") as f:
        f.write(f"# Experimental Protocol\n\n")
        f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n")
        f.write(f"**Hypothesis:** {hypothesis}\n\n")
        f.write("---\n\n")

        if 'raw_response' in design:
            f.write(design['raw_response'])
        else:
            f.write(f"```yaml\n{yaml.dump(design, default_flow_style=False)}\n```\n")

    print("  ✓ Saved: outputs/experiment_design/protocol.md")

    # Save data collection template
    create_data_template(design)

    # Save YAML config
    with open("outputs/experiment_design/experiment_config.yaml", "w") as f:
        yaml.dump(design, f, default_flow_style=False)

    print("  ✓ Saved: outputs/experiment_design/experiment_config.yaml")


def create_data_template(design: dict):
    """
    Create CSV template for data collection.
    """
    csv_content = "participant_id,group,week,date,"

    # Add dependent variables as columns
    if 'dependent_variables' in design:
        for dv in design['dependent_variables']:
            if isinstance(dv, dict):
                csv_content += f"{dv.get('name', 'metric')},"

    csv_content = csv_content.rstrip(',') + "\n"

    # Add example row
    csv_content += "001,control,1,2025-01-01,\n"

    with open("outputs/experiment_design/data_template.csv", "w") as f:
        f.write(csv_content)

    print("  ✓ Saved: outputs/experiment_design/data_template.csv")
