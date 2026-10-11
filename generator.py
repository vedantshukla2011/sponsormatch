from groq import Groq

def generate_pitch(team_info, lead_info, api_key):
    """
    Generates a tailored sponsorship pitch email using Groq's Llama 3 model.
    """
    client = Groq(api_key=api_key)

    prompt = f"""
    You are an outreach lead for a high school robotics team seeking corporate sponsorship.
    Write a concise, high-impact sponsorship pitch email tailored to a prospective sponsor.

    Team Information:
    - Competition League: {team_info.get('league')}
    - Key Highlight: {team_info.get('highlight')}
    - Funding Request: {team_info.get('request')}
    - Team Location Zip Code: {team_info.get('zip_code')}

    Prospective Sponsor Information:
    - Company Name: {lead_info.get('Name')}
    - Address: {lead_info.get('Address')}
    - Industry/Category: {lead_info.get('Category')}

    Formatting & Style Requirements:
    1. Professional, passionate, and concise (150-200 words max).
    2. Directly connect the company's industry to the team's technical goals (e.g., engineering, manufacturing, workforce development).
    3. Include placeholders like [Your Name], [Your Team Number], and [Contact Phone/Email].
    4. Do not include a subject line in the body text (subject is handled separately).
    """

    response = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "You are an expert STEM fundraising advisor specializing in tech and engineering team sponsorships."
            },
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="openai/gpt-oss-120b",
        temperature=0.7,
        max_tokens=500
    )

    return response.choices[0].message.content