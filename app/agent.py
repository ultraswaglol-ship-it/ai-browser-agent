import json
import asyncio
from app.services.llm import LLMService
from app.services.browser import BrowserService
from app.tools.prompt import SYSTEM_PROMPT

class Agent:
    def __init__(self):
        self.llm = LLMService()
        self.browser = BrowserService()
        self.history = []

    async def run(self, task: str):
        await self.browser.start()
        self.history.append({"role": "user", "content": f"TASK: {task}"})

        step = 0
        max_steps = 25

        try:
            while step < max_steps:
                print(f"\n--- Step {step + 1} ---")
                
                dom_state = await self.browser.get_dom_snapshot()
                
                messages = [{"role": "system", "content": SYSTEM_PROMPT}]
                messages.extend(self.history)
                messages.append({"role": "user", "content": f"CURRENT PAGE STATE:\n{dom_state}"})

                decision = None
                for attempt in range(3):
                    try:
                        decision = await self.llm.get_decision(messages)
                        if decision: break
                    except Exception as e:
                        print(f"LLM Parse Error (Attempt {attempt+1}): {e}")
                        messages.append({"role": "user", "content": "Error: Your last response was not a valid JSON. Please reply with a single JSON object."})

                if not decision:
                    print("Critical: LLM failed to provide valid action.")
                    break

                print(f"Thought: {decision.get('thought')}")
                print(f"Action: {decision.get('action')} {decision.get('params')}")

                self.history.append({"role": "assistant", "content": json.dumps(decision, ensure_ascii=False)})

                action = decision.get("action")
                params = decision.get("params", {})

                if action == "done":
                    print(" Mission accomplished.")
                    break
                if action == "fail":
                    print(" Agent failed to complete the task.")
                    break

                try:
                    if action == "goto":
                        await self.browser.navigate(params.get("url"))
                    elif action == "scroll":
                        await self.browser.interact("scroll", {})
                    elif action in ["click", "type"]:
                        await self.browser.interact(action, params)
                except Exception as e:
                    error_msg = f"Action failed: {str(e)}"
                    print(f" {error_msg}")
                    self.history.append({"role": "user", "content": error_msg})

                step += 1
        finally:
            await self.browser.close()