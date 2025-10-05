def query_llm(
    prompt,
    system_prompt=None,
    provider="OpenAI",
    model=None,
    api_key=None,
    temperature=0.0,
):
    """Simple LLM query function with optional system prompt"""

    if provider == "OpenAI":
        import openai

        client = openai.OpenAI(api_key=api_key)
        model = model or "gpt-4o-mini"
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        response = client.chat.completions.create(
            model=model, messages=messages, temperature=temperature
        )
        return response.choices[0].message.content

    elif provider == "Mistral":
        import mistralai

        client = mistralai.Mistral(api_key=api_key)
        model = model or "mistral-small-latest"
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        response = client.chat.complete(
            model=model, messages=messages, temperature=temperature
        )
        return response.choices[0].message.content

    elif provider == "Anthropic":
        import anthropic

        client = anthropic.Anthropic(api_key=api_key)
        model = model or "claude-3-5-haiku-latest"

        response = client.messages.create(
            model=model,
            system=system_prompt or "",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=4096,
            temperature=temperature,
        )
        return response.content[0].text

    else:
        raise ValueError(f"Unsupported provider: {provider}")


def natural_language_to_cypher(
    question,
    system_prompt,
    provider="OpenAI",
    model=None,
    api_key=None,
    temperature=0.0,
):
    """Convert natural language question to Cypher query"""
    cypher_query = query_llm(
        prompt=question,
        system_prompt=system_prompt,
        provider=provider,
        model=model,
        api_key=api_key,
        temperature=temperature,
    )

    return cypher_query.strip()
