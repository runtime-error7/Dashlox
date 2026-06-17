import ollama
import json

def chat_to_modify_chart(user_instruction, columns, current_chart_state=None):
    """
    Talks to the local LLM to generate or update a Chart.js configuration.
    """
    
    # The System Prompt acts as the strict rules for the AI
    system_prompt = f"""
    You are Dashlox Engine AI, an expert offline data visualization script.
    Your ONLY task is to return a strict JSON configuration for Chart.js (v3/v4).
    Do not output any conversational text. Do not output markdown code blocks (like ```json).
    Return ONLY raw, valid JSON.
    
    The user has a dataset with the following exact column names:
    {columns}
    
    Use these column names for your labels and data mappings. Ensure the chart colors are visually appealing and contrast well with a dark-mode UI background (slate/indigo/emerald).
    """
    
    # If a chart already exists, we pass it back to the AI so it modifies it rather than starting over
    if current_chart_state:
        system_prompt += f"\n\nMODIFY THIS CURRENT CHART STATE based on the user request:\n{json.dumps(current_chart_state)}"
    else:
        system_prompt += "\n\nCREATE a new chart configuration from scratch based on the user request."

    try:
        # Call the local model via Ollama
        response = ollama.chat(
            model='qwen2.5:1.5b', # Ensure this matches the model downloaded in your setup script
            messages=[
                {'role': 'system', 'content': system_prompt},
                {'role': 'user', 'content': user_instruction}
            ],
            # 'format="json"' is the magic flag that hardware-locks the model to output valid JSON
            format='json' 
        )
        
        # Parse the AI's raw string response into a Python dictionary
        raw_output = response['message']['content']
        chart_config = json.loads(raw_output)
        
        return chart_config
        
    except json.JSONDecodeError:
        return {"error": "The AI failed to generate valid JSON format. Try your request again."}
    except Exception as e:
        return {"error": f"Local LLM communication failed. Is Ollama running? Details: {str(e)}"}
