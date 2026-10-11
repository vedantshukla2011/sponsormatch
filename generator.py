from groq import Groq

def generate_pitch(team_info, lead, api_key):
    client = Groq(api_key=api_key)
    
    # Extract lead details cleanly
    if isinstance(lead, dict):
        lead_name = lead.get("name", "Potential Sponsor")
        lead_address = lead.get("address", "N/A")
        lead_types = ", ".join(lead.get("types", [])) if isinstance(lead.get("types"), list) else "Business"
    else:
        lead_name = str(lead)
        lead_address = "N/A"
        lead_types = "Business"

    prompt = f"""
    You are an expert corporate sponsorship outreach coordinator. Write a compelling, professional sponsorship proposal email.

    Target Business: {lead_name}
    Address: {lead_address}
    Industry: {lead_types}

    Our Team & Goals:
    {team_info}

    Write a personalized pitch email requesting a sponsorship partnership or meeting. Keep it professional, concise, and persuasive. Include placeholders like [Your Name] and [Your Title] where appropriate.
    """

    models_to_try = ["llama-3.3-70b-versatile", "llama-3.1-8b-instant"]
    
    for model_name in models_to_try:
        try:
            completion = client.chat.completions.create(
                model=model_name,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=1000,
            )
            return completion.choices[0].message.content
        except Exception as e:
            if model_name == models_to_try[-1]:
                raise e