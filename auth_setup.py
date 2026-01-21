import asyncio
from playwright.async_api import async_playwright

async def save_auth():
    print(" Запускаю браузер для авторизации...")
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=False,
            args=["--disable-blink-features=AutomationControlled"]
        )
        context = await browser.new_context(
            viewport={"width": 1280, "height": 800}
        )
        page = await context.new_page()

        print(" Перехожу на hh.ru/login...")
        try:
            await page.goto("https://hh.ru/account/login", timeout=60000)
        except:
            print(" Не удалось загрузить страницу, но браузер открыт.")

        print("\n" + "="*50)
        print(" ЗАДАЧА: Авторизуйся вручную прямо сейчас.")
        print("Введи логин/пароль или войди через почту/код.")
        print("Когда увидишь свой профиль (главную страницу) - вернись сюда.")
        print("="*50 + "\n")

        input(" Нажми ENTER в этом терминале ПОСЛЕ того, как успешно войдешь в аккаунт...")

        await context.storage_state(path="auth.json")
        print("\n Успешно! Файл auth.json создан.")
        print("Теперь агент будет использовать твой аккаунт.")
        
        await browser.close()

if __name__ == "__main__":
    asyncio.run(save_auth())