"""
AI Client - Wrapper for Claude and Gemini CLIs
Uses headless CLIs instead of API calls
"""

import subprocess
import json
from typing import Optional, Literal

def call_ai(
    prompt: str,
    provider: Literal["claude", "gemini"] = "claude",
    temperature: float = 1.0,
    max_tokens: int = 4000
) -> str:
    """
    Call AI using headless CLI (Claude or Gemini).

    Args:
        prompt: The prompt to send
        provider: Which AI to use ("claude" or "gemini")
        temperature: Temperature setting (not always supported)
        max_tokens: Max tokens (not always supported)

    Returns:
        str: AI response
    """
    try:
        if provider == "claude":
            return call_claude_cli(prompt)
        elif provider == "gemini":
            return call_gemini_cli(prompt)
        else:
            raise ValueError(f"Unknown provider: {provider}")
    except Exception as e:
        print(f"  Error calling {provider}: {e}")
        return None


def call_claude_cli(prompt: str) -> str:
    """
    Call Claude using headless CLI.

    Usage: claude --print "your prompt"
    """
    try:
        result = subprocess.run(
            ['claude', '--print'],
            input=prompt,
            capture_output=True,
            text=True,
            timeout=120
        )

        if result.returncode != 0:
            raise Exception(f"Claude CLI error: {result.stderr}")

        return result.stdout.strip()
    except subprocess.TimeoutExpired:
        raise Exception("Claude CLI timeout")
    except FileNotFoundError:
        raise Exception("Claude CLI not found. Install with: npm install -g @anthropic-ai/claude-cli")
    except Exception as e:
        raise Exception(f"Claude CLI error: {str(e)}")


def call_gemini_cli(prompt: str) -> str:
    """
    Call Gemini using headless CLI.

    Model: gemini-2.0-flash
    Usage: gemini "your prompt"
    """
    try:
        result = subprocess.run(
            ['gemini', prompt],
            capture_output=True,
            text=True,
            timeout=120
        )

        if result.returncode != 0:
            raise Exception(f"Gemini CLI error: {result.stderr}")

        return result.stdout.strip()
    except subprocess.TimeoutExpired:
        raise Exception("Gemini CLI timeout")
    except FileNotFoundError:
        raise Exception("Gemini CLI not found. Install Gemini CLI first")
    except Exception as e:
        raise Exception(f"Gemini CLI error: {str(e)}")


def call_ai_json(
    prompt: str,
    provider: Literal["claude", "gemini"] = "claude"
) -> dict:
    """
    Call AI and parse response as JSON.

    Adds instruction to respond in JSON format.
    """
    json_prompt = f"""{prompt}

IMPORTANT: Respond with valid JSON only. No markdown, no explanations, just pure JSON.
"""

    response = call_ai(json_prompt, provider=provider)

    if not response:
        return {}

    # Try to extract JSON if wrapped in markdown
    if "```json" in response:
        start = response.find("```json") + 7
        end = response.find("```", start)
        response = response[start:end].strip()
    elif "```" in response:
        start = response.find("```") + 3
        end = response.find("```", start)
        response = response[start:end].strip()

    try:
        return json.loads(response)
    except json.JSONDecodeError as e:
        print(f"  Warning: Failed to parse JSON: {e}")
        print(f"  Response was: {response[:200]}...")
        return {"raw_response": response}


# Test function
def test_ai_clients():
    """Test both AI clients."""
    print("Testing AI Clients...")
    print("-" * 60)

    # Test Claude
    print("\n1. Testing Claude CLI...")
    try:
        response = call_claude_cli("Say 'Claude works!' and nothing else")
        print(f"   Response: {response}")
        print("   ✓ Claude CLI working")
    except Exception as e:
        print(f"   ✗ Claude error: {e}")

    # Test Gemini
    print("\n2. Testing Gemini CLI...")
    try:
        response = call_gemini_cli("Say 'Gemini works!' and nothing else")
        print(f"   Response: {response}")
        print("   ✓ Gemini CLI working")
    except Exception as e:
        print(f"   ✗ Gemini error: {e}")

    print("\n" + "-" * 60)
    print("AI Client tests complete!")


if __name__ == "__main__":
    test_ai_clients()
