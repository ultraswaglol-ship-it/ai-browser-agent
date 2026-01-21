import asyncio
import os
from playwright.async_api import async_playwright
from app.tools.dom_script import DOM_JS_SCRIPT
from app.config import HEADLESS, SLOW_MO, VIEWPORT

class BrowserService:
    def __init__(self):
        self.playwright = None
        self.browser = None
        self.page = None

    async def start(self):
        self.playwright = await async_playwright().start()
        
        launch_args = [
            "--disable-blink-features=AutomationControlled",
            "--no-sandbox",
            "--disable-infobars",
            "--no-proxy-server"
        ]

        self.browser = await self.playwright.chromium.launch(
            headless=HEADLESS, 
            slow_mo=SLOW_MO,
            args=launch_args,
            proxy=None
        )
        
        context_args = {
            "viewport": VIEWPORT,
            "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "ignore_https_errors": True
        }

        if os.path.exists("auth.json"):
            context_args["storage_state"] = "auth.json"

        context = await self.browser.new_context(**context_args)
        self.page = await context.new_page()

    async def get_dom_snapshot(self):
        try:
            return await self.page.evaluate(DOM_JS_SCRIPT)
        except Exception as e:
            return str(e)

    async def navigate(self, url):
        try:
            await self.page.goto(url, wait_until="domcontentloaded", timeout=60000)
            await self.page.wait_for_timeout(3000)
        except Exception as e:
            print(f"Navigation error: {e}")

    async def interact(self, action: str, params: dict):
        if action == "scroll":
            await self.page.evaluate("window.scrollBy(0, 700)")
            await self.page.wait_for_timeout(1000)
            return

        element_id = params.get("id")
        if not element_id:
            raise Exception(f"Action '{action}' requires an 'id'")

        selector = f'[data-agent-id="{element_id}"]'
        
        if await self.page.locator(selector).count() == 0:
            await self.page.evaluate(DOM_JS_SCRIPT)
            await asyncio.sleep(0.5)
        
        locator = self.page.locator(selector)
        if await locator.count() == 0:
            raise Exception(f"Element {element_id} not found")

        if action == "click":
            try:
                await locator.evaluate("el => el.style.border = '3px solid red'")
            except: pass

            try:
                await locator.click(timeout=3000)
            except:
                try:
                    await locator.click(force=True, timeout=2000)
                except:
                    await locator.evaluate("el => el.click()")
            
        elif action == "type":
            try:
                await locator.click(timeout=2000)
                await locator.focus()
            except:
                await locator.evaluate("el => { el.focus(); el.click(); }")
            
            await locator.fill("")
            await self.page.fill(selector, params.get("text", ""))
            await asyncio.sleep(0.5)
            await self.page.keyboard.press("Enter")

        await self.page.wait_for_timeout(2000)

    async def close(self):
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()