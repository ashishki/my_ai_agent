from openai import AsyncOpenAI
from config import settings
from services.filter import is_safe_response
from services.cache import get_cached_response, cache_response
from datetime import datetime
from services.logger import logger

# Set API key
client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

async def analyze_business_data(business_data: dict, request_id: str) -> str:
    """Analyzes business data and returns recommendations."""
    start_time = datetime.now()
    try:
        logger.info(f"[{request_id}] Starting OpenAI request")
        prompt = f"""
        Analyze the following business data and provide recommendations:
        {business_data}
        """
        cache_key = f"openai:{hash(prompt)}"
        cached_response = await get_cached_response(cache_key)
        if cached_response:
            print("[CACHE] Using cached response for OpenAI")
            return cached_response

        response = await client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )

        duration = (datetime.now() - start_time).total_seconds()
        logger.info(f"[{request_id}] OpenAI request completed in {duration}s")
        
        result = response.choices[0].message.content

        if not is_safe_response(result):
            return "Response cannot be provided due to ethical guidelines."

        await cache_response(cache_key, result)
        return result
        
    except Exception as e:
        logger.error(f"[{request_id}] OpenAI API error: {str(e)}")
        raise

async def generate_ai_solution(prompt: str) -> str:
    """
    Generates a solution based on the prompt using OpenAI's API.
    This function caches the result to save on API calls.
    """
    cache_key = f"ai_solution:{hash(prompt)}"
    cached_response = await get_cached_response(cache_key)
    if cached_response:
        print("[CACHE] Using cached response for AI solution")
        return cached_response

    response = await client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=500
    )

    result = response.choices[0].message.content

    if not is_safe_response(result):
        return "Response cannot be provided due to ethical guidelines."

    await cache_response(cache_key, result)
    return result
