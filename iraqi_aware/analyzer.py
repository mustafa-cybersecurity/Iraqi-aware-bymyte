"""
AI Vision Analyzer Module for Iraqi Aware.

This module interfaces with different AI vision models (OpenAI, NVIDIA, Ollama)
to analyze screenshots for potential cybersecurity threats.
"""

import base64
import json
import requests
from typing import Dict, Any, Optional
from openai import OpenAI
from config import AppConfig

SYSTEM_PROMPT = """
You are a highly skilled, expert cybersecurity analyst. Your job is to analyze the provided screenshot of a user's screen and identify any potential cybersecurity threats or privacy risks.
Look out for:
1. Phishing emails or websites.
2. Suspicious pop-ups, such as fake tech support warnings.
3. Downloading of dangerous or unknown files.
4. Plaintext passwords being typed or exposed.
5. Malicious or fraudulent activity.

You MUST respond ONLY with a strictly formatted JSON object. Do not include any markdown formatting (like ```json), explanations, or extra text.

The JSON object must have exactly these three keys:
- "severity": A string that must be one of: "none", "low", "medium", "high". Use "none" if there is no threat.
- "title": A concise, clear title describing the threat (if any). Empty string if no threat.
- "advice": Professional, actionable advice on what the user should do immediately. Empty string if no threat.

Example valid response:
{"severity": "high", "title": "Fake Tech Support Pop-up Detected", "advice": "Do not click any links or call the number. Close the browser tab immediately."}
"""

class ThreatAnalyzer:
    """Analyzes screenshots for threats using the configured AI provider."""

    def __init__(self, config: AppConfig):
        self.config = config

    def analyze_image(self, image_path: str) -> Optional[Dict[str, Any]]:
        """
        Reads an image file, encodes it, and sends it to the configured AI provider.
        Returns a dictionary with severity, title, and advice, or None if analysis fails or no threat.
        """
        try:
            with open(image_path, "rb") as image_file:
                base64_image = base64.b64encode(image_file.read()).decode('utf-8')
        except Exception as e:
            print(f"Failed to read image for analysis: {e}")
            return None

        if self.config.provider == "openai":
            return self._analyze_openai(base64_image)
        elif self.config.provider == "nvidia":
            return self._analyze_nvidia(base64_image)
        elif self.config.provider == "ollama":
            return self._analyze_ollama(base64_image)
        else:
            print(f"Unknown provider: {self.config.provider}")
            return None

    def _parse_response(self, content: str) -> Optional[Dict[str, Any]]:
        """Parses the JSON response from the AI."""
        try:
            # Try to strip markdown code blocks if the model erroneously included them
            content = content.strip()
            if content.startswith("```json"):
                content = content[7:]
            if content.startswith("```"):
                content = content[3:]
            if content.endswith("```"):
                content = content[:-3]
            content = content.strip()

            result = json.loads(content)

            # Validate format
            if all(k in result for k in ("severity", "title", "advice")):
                # Normalize severity
                result["severity"] = result["severity"].lower()
                if result["severity"] not in ("none", "low", "medium", "high"):
                    result["severity"] = "none"

                # If no threat, we can just return None to avoid triggering alerts
                if result["severity"] == "none":
                    return None

                return result
            else:
                print("Invalid JSON structure from AI.")
                return None
        except json.JSONDecodeError as e:
            print(f"Failed to parse AI JSON response: {e}. Raw content: {content}")
            return None

    def _analyze_openai(self, base64_image: str) -> Optional[Dict[str, Any]]:
        try:
            client = OpenAI(api_key=self.config.api_key)
            model = self.config.model if self.config.model else "gpt-4o"

            response = client.chat.completions.create(
                model=model,
                messages=[
                    {
                        "role": "system",
                        "content": SYSTEM_PROMPT
                    },
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": "Analyze this screenshot for cybersecurity threats."},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{base64_image}",
                                }
                            },
                        ],
                    }
                ],
                max_tokens=300,
            )
            content = response.choices[0].message.content
            return self._parse_response(content)
        except Exception as e:
            print(f"OpenAI analysis failed: {e}")
            return None

    def _analyze_nvidia(self, base64_image: str) -> Optional[Dict[str, Any]]:
        # Using OpenAI compatible endpoint format for Nvidia AI Cloud if possible,
        # but adapting for standard requests just in case it's a direct API
        try:
            client = OpenAI(
                base_url="https://integrate.api.nvidia.com/v1",
                api_key=self.config.api_key
            )
            model = self.config.model if self.config.model else "meta/llama-3.2-90b-vision-instruct"

            response = client.chat.completions.create(
                model=model,
                messages=[
                    {
                        "role": "system",
                        "content": SYSTEM_PROMPT
                    },
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": "Analyze this screenshot for cybersecurity threats."},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{base64_image}",
                                }
                            },
                        ],
                    }
                ],
                max_tokens=300,
            )
            content = response.choices[0].message.content
            return self._parse_response(content)
        except Exception as e:
            print(f"NVIDIA analysis failed: {e}")
            return None

    def _analyze_ollama(self, base64_image: str) -> Optional[Dict[str, Any]]:
        try:
            # Ollama API typically runs locally
            url = self.config.local_url if self.config.local_url else "http://localhost:11434/api/generate"
            model = self.config.model if self.config.model else "llava"

            payload = {
                "model": model,
                "prompt": SYSTEM_PROMPT + "\n\nAnalyze this screenshot for cybersecurity threats.",
                "images": [base64_image],
                "stream": False,
                "format": "json" # Ollama supports forcing JSON output
            }

            response = requests.post(url, json=payload, timeout=30)
            response.raise_for_status()

            result_data = response.json()
            content = result_data.get("response", "")
            return self._parse_response(content)

        except Exception as e:
            print(f"Ollama analysis failed: {e}")
            return None
