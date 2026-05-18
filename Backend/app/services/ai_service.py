import os
import json
import time

from openai import OpenAI, OpenAIError

from app.utils.logger import get_logger

logger = get_logger(__name__)

FALLBACK = {
    "error": "Unable to generate AI suggestions right now. Please try again later."
}


def _get_client():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise OpenAIError("OPENAI_API_KEY não configurada no .env")
    return OpenAI(api_key=api_key, timeout=20.0)


def get_suggestions(title: str, discipline: str, summary: str) -> tuple[dict, bool]:
    """
    Retorna (resultado, sucesso).
    sucesso=False indica que deve ser retornado status 503 ao cliente.
    """
    prompt = f"""Você é um assistente pedagógico especialista em planejamento de aulas.

Com base nas informações abaixo, sugira conteúdos complementares para enriquecer o plano de aula.

Título: {title}
Disciplina: {discipline}
Resumo: {summary}

Responda APENAS com um JSON válido, sem texto adicional, no seguinte formato:
{{
  "contents": ["tópico 1", "tópico 2", "tópico 3"],
  "recommended_tags": ["tag1", "tag2", "tag3"],
  "support_resources": ["recurso 1", "recurso 2"]
}}"""

    start = time.time()

    try:
        client = _get_client()

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=500,
        )

        latency = round(time.time() - start, 2)
        usage = response.usage.total_tokens if response.usage else "?"

        logger.info(
            "AI suggestion generated: Title=%r, Discipline=%r, TokenUsage=%s, Latency=%ss",
            title, discipline, usage, latency,
        )

        raw = response.choices[0].message.content.strip()
        result = json.loads(raw)

        return {
            "contents": result.get("contents", []),
            "recommended_tags": result.get("recommended_tags", []),
            "support_resources": result.get("support_resources", []),
        }, True

    except json.JSONDecodeError:
        logger.warning("AI returned response in unexpected format (not valid JSON)")
        return FALLBACK, False

    except OpenAIError as e:
        logger.error("OpenAI request failed: %s", str(e))
        return FALLBACK, False

    except Exception as e:
        logger.error("Unexpected error in AI service: %s", str(e))
        return FALLBACK, False
