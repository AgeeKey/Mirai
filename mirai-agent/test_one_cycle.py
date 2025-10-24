"""
Тестовый скрипт - выполняет ОДИН цикл умного агента V2
"""

import asyncio
from autonomous_desktop_v2 import IntelligentMiraiAgent


async def test_one_cycle():
    print('🧪 Создаю умного агента V2...')
    agent = IntelligentMiraiAgent()
    
    print('🔄 Выполняю ОДИН тестовый цикл...')
    print('=' * 70)
    
    await agent.intelligent_cycle()
    
    print('=' * 70)
    print('\n✅ ТЕСТ ЗАВЕРШЁН!')
    print('\n📊 Статистика:')
    print(f'   Всего действий: {agent.context.total_actions}')
    print(f'   Успешных: {agent.context.successful_actions}')
    print(f'   Провальных: {agent.context.failed_actions}')
    print(f'   Успешность: {agent.context.get_context_summary()["success_rate"]}')
    
    if agent.context.action_history:
        print('\n📝 Последние действия:')
        for action in agent.context.get_recent_actions(5):
            status_emoji = "✅" if action.status.value == "success" else "❌"
            print(f'   {status_emoji} {action.action_type}: {action.description[:60]}')
    
    print('\n💾 Контекст сохранён в:', agent.context.context_file)
    print('📁 Логи:', 'autonomous_desktop_v2.log')


if __name__ == "__main__":
    asyncio.run(test_one_cycle())
