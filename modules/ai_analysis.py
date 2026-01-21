import os
import aiohttp
import json
from colorama import Fore, Style

class AIAnalyst:
    def __init__(self):
        self.openai_key = os.getenv("OPENAI_API_KEY")
        # Default to local Ollama instance if no key provided
        self.ollama_url = "http://localhost:11434/api/generate"
        
        self.system_prompt = """
        You are a Senior Intelligence Analyst. 
        Your job is to analyze raw OSINT (Open Source Intelligence) data and produce a comprehensive "Target Dossier".
        
        Guidance:
        1. Analyze the social media handles, emails, and phone data provided.
        2. Identify patterns (e.g., username reuse, specific interests, potential location).
        3. Assess potential security risks or exposed information (breaches, leaked passwords).
        4. Be professional, concise, and objective. Use "Target" to refer to the subject.
        5. If data is scarce, state "Insufficient Intelligence" for that section.
        6. Conclude with a "Threat/Privacy Score" (1-10, where 10 is completely exposed).
        """

    async def generate_dossier(self, target_data):
        """
        Takes a dictionary of collected OSINT data and generates a report.
        """
        print(f"\n{Fore.MAGENTA}[🧠] AI Analyst: Initializing dossier generation...{Style.RESET_ALL}")
        
        prompt = f"TARGET DATA:\n{json.dumps(target_data, indent=2)}\n\n"
        prompt += "Based on the above data, write a detailed Intelligence Report."

        if self.openai_key:
            return await self._call_openai(prompt)
        else:
            return await self._call_ollama(prompt)

    async def _call_openai(self, user_prompt):
        print(f"{Fore.CYAN}[*] Using OpenAI API (Cloud)...{Style.RESET_ALL}")
        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.openai_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "gpt-4-turbo-preview",
            "messages": [
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": user_prompt}
            ]
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, headers=headers, json=payload) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        return data['choices'][0]['message']['content']
                    else:
                        return f"{Fore.RED}[!] OpenAI Error: {resp.status} - {await resp.text()}{Style.RESET_ALL}"
        except Exception as e:
            return f"{Fore.RED}[!] Request Error: {e}{Style.RESET_ALL}"

    async def _call_ollama(self, user_prompt):
        print(f"{Fore.CYAN}[*] Using Ollama (Local - Privacy Mode)...{Style.RESET_ALL}")
        # Simplistic Ollama call - assumes 'llama3' or 'mistral' is installed
        payload = {
            "model": "llama3", # User might need to pull this
            "prompt": f"{self.system_prompt}\n\n{user_prompt}",
            "stream": False
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                # Short timeout check to see if service is up
                try:
                    async with session.post(self.ollama_url, json=payload, timeout=60) as resp:
                        if resp.status == 200:
                            data = await resp.json()
                            return data['response']
                        else:
                            return f"{Fore.YELLOW}[!] Ollama Error: {resp.status}. Is it running?{Style.RESET_ALL}"
                except aiohttp.ClientConnectorError:
                     return (
                         f"{Fore.RED}[!] Could not connect to Ollama on {self.ollama_url}.{Style.RESET_ALL}\n"
                         f"{Fore.YELLOW}Tip: Run 'ollama serve' and 'ollama pull llama3' to use local AI.{Style.RESET_ALL}\n"
                         f"Or set 'OPENAI_API_KEY' env var for cloud AI."
                     )
        except Exception as e:
             return f"{Fore.RED}[!] Unknown Error: {e}{Style.RESET_ALL}"
