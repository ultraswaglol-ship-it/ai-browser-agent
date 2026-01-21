import json
import os
import re
from openai import AsyncOpenAI
from app.config import MODEL_NAME, OPENROUTER_API_KEY

class LLMService:
    def __init__(self):
        self.client = AsyncOpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=OPENROUTER_API_KEY,
        )
        self.model = MODEL_NAME

    def _clean_json(self, text: str):
        """Очищает ответ от LLM, вытаскивая первый валидный JSON"""
        text = text.strip()
        
        if "```" in text:
            match = re.search(r"```(?:json)?(.*?)```", text, re.DOTALL)
            if match:
                text = match.group(1).strip()

        try:
            return json.loads(text)
        except json.JSONDecodeError:
            pass

        try:
            start = text.find('{')
            if start != -1:
                brace_count = 0
                for i, char in enumerate(text[start:], start=start):
                    if char == '{':
                        brace_count += 1
                    elif char == '}':
                        brace_count -= 1
                        if brace_count == 0:
                            first_json = text[start:i+1]
                            return json.loads(first_json)
        except:
            pass
            
        return None

    async def get_decision(self, messages: list) -> dict:
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                response_format={"type": "json_object"},
                temperature=0.1
            )
            content = response.choices[0].message.content
            
            decision = self._clean_json(content)
            
            if not decision:
                print(f"❌ LLM Error: Raw content cannot be parsed -> {content}")
                return None
                
            return decision

        except Exception as e:
            print(f"API Error: {e}")
            return None