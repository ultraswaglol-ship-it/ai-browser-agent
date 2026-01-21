import asyncio
import sys

sys.path.append(".")

from app.agent import Agent

async def main():
    print(" Browser AI Agent ")
    print("--------------------------------")
 
    task = input(" Введите задачу для агента: ")
    
    if not task:
        print("Задача не может быть пустой.")
        return

    agent = Agent()
    
    try:
        await agent.run(task)
    except KeyboardInterrupt:
        print("\n Принудительная остановка пользователем.")
    except Exception as e:
        print(f"\n Критическая ошибка: {e}")

if __name__ == "__main__":
    asyncio.run(main())