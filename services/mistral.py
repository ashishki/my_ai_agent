import os
from mistralai import Mistral
from dotenv import load_dotenv
from services.filter import is_safe_response
from services.cache import get_cached_response, cache_response

load_dotenv()
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
client = Mistral(api_key=MISTRAL_API_KEY)

async def analyze_business_with_mistral(business_data: dict) -> str:
    """Quick analysis with basic data using Mistral."""
    prompt = f"""
    Analyze the following business data and suggest improvements:
    {business_data}
    """
    cache_key = f"mistral:{hash(prompt)}"
    cached_response = await get_cached_response(cache_key)
    if cached_response:
        print("[CACHE] Using cached response for Mistral")
        return cached_response

    messages = [
        {"role": "system", "content": "You are an expert in business analysis."},
        {"role": "user", "content": prompt}
    ]

    # Здесь можно обернуть синхронный вызов в executor, если нет асинхронного метода:
    import asyncio
    from concurrent.futures import ThreadPoolExecutor
    loop = asyncio.get_running_loop()
    response = await loop.run_in_executor(
        None,
        lambda: client.chat.complete(model="mistral-small-latest", messages=messages)
    )
    
    result = response.choices[0].message.content
    if not is_safe_response(result):
        return "Response cannot be provided due to ethical guidelines."

    await cache_response(cache_key, result)
    return result

async def generate_mistral_solution(prompt: str) -> str:
    """Generates detailed AI solution using Mistral for comprehensive business analysis."""
    cache_key = f"mistral:detail:{hash(prompt)}"
    cached_response = await get_cached_response(cache_key)
    if cached_response:
        print("[CACHE] Using cached detailed response for Mistral")
        return cached_response

    messages = [
        {"role": "system", "content": "You are an expert in business analysis and AI solution recommendations."},
        {"role": "user", "content": prompt}
    ]

    # Again, wrapping synchronous call if needed:
    import asyncio
    from concurrent.futures import ThreadPoolExecutor
    loop = asyncio.get_running_loop()
    response = await loop.run_in_executor(
        None,
        lambda: client.chat.complete(model="mistral-small-latest", messages=messages)
    )
    
    result = response.choices[0].message.content
    if not is_safe_response(result):
        return "Response cannot be provided due to ethical guidelines."

    await cache_response(cache_key, result)
    return result
