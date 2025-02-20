from typing import Dict, Any
from services.llm import generate_ai_solution, analyze_business_data
from services.mistral import analyze_business_with_mistral, generate_mistral_solution

def create_detailed_prompt(business_data: Dict[str, Any]) -> str:
    """Creates detailed prompt for comprehensive analysis"""
    sections = {
        "Name": business_data.get("name"),
        "Industry": business_data.get("industry"),
        "Target Audience": business_data.get("audience"),
        "Key Tasks": ", ".join(business_data.get("key_tasks", [])),
        "Existing Technologies": ", ".join(business_data.get("existing_tech", [])) or "None",
        "Budget": business_data.get("budget", "Not specified"),
        "Description": business_data.get("description", "No description provided"),
        "Competitors": ", ".join(business_data.get("competitors", [])) or "None",
        "Strategic Goals": ", ".join(business_data.get("goals", [])) or "Not specified",
        "Pain Points": ", ".join(business_data.get("pain_points", [])) or "None",
        "Current Solution": business_data.get("current_solution", "Not provided")
    }

    prompt = "Analyze the following business details and suggest the most appropriate AI solution:\n\n"
    prompt += "\n".join(f"{key}: {value}" for key, value in sections.items())
    prompt += "\n\nBased on this information, what AI agent would best suit this business?"
    prompt += "\nPlease provide a detailed recommendation including possible improvements and integration steps."
    return prompt.strip()

async def analyze_business_request(business_data: Dict[str, Any], model: str = "openai") -> str:
    """Unified business analysis function that supports different models."""
    prompt = create_detailed_prompt(business_data)
    
    if model == "mistral":
        return await generate_mistral_solution(prompt)
    else:
        return await generate_ai_solution(prompt)

