from services.llm import generate_ai_solution
from sqlalchemy.ext.asyncio import AsyncSession

def create_guide_prompt(business_data: dict, assessment: str) -> str:
    """
    Формирует подробный prompt для генерации пошагового руководства.
    Prompt включает детали о бизнесе и оценку работы текущего AI-агента.
    """
    prompt = f"""
    Based on the following business details and the performance assessment of the current AI agent, 
    please generate a detailed, step-by-step guide for improving or integrating an AI agent for this business.

    Business Details:
    - Name: {business_data.get("name")}
    - Industry: {business_data.get("industry")}
    - Target Audience: {business_data.get("audience", "Not specified")}
    - Key Tasks: {", ".join(business_data.get("key_tasks", []))}
    - Existing Technologies: {", ".join(business_data.get("existing_tech", [])) or "None"}
    - Budget: {business_data.get("budget", "Not specified")}
    - Description: {business_data.get("description", "No description provided")}
    - Competitors: {", ".join(business_data.get("competitors", [])) or "None"}
    - Strategic Goals: {", ".join(business_data.get("goals", [])) or "Not specified"}
    - Pain Points: {", ".join(business_data.get("pain_points", [])) or "None"}
    - Current Solution: {business_data.get("current_solution", "Not provided")}

    Performance Assessment of the current AI agent:
    {assessment}

    Based on the above information, provide a detailed, actionable, and step-by-step guide that includes:
    1. Recommended improvements or fine-tuning for the current AI agent.
    2. Specific steps for integrating or switching to a better AI solution if needed.
    3. Infrastructure and technology recommendations.
    4. Additional tips for cost optimization and scalability.

    Please format the guide as a numbered list with clear instructions.
    """
    return prompt.strip()

async def generate_guide(business_data: dict, assessment: str) -> str:
    """
    Генерирует руководство на основе деталей бизнеса и оценки текущего AI-агента.
    Вызывает LLM с созданным prompt'ом.
    """
    prompt = create_guide_prompt(business_data, assessment)
    guide = await generate_ai_solution(prompt)
    return guide

async def save_guide_to_db(db: AsyncSession, request_data: dict, guide: str):
    """Save generated guide to database."""
    # TODO: Implement guide saving logic
    pass
