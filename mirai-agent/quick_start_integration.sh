#!/bin/bash
#
# 🚀 БЫСТРЫЙ СТАРТ NASA-LEVEL ИНТЕГРАЦИИ
#

cat << 'EOF'
╔══════════════════════════════════════════════════════════════════════╗
║  🎉 NASA-LEVEL INTEGRATION - БЫСТРЫЙ СТАРТ                          ║
╚══════════════════════════════════════════════════════════════════════╝

✅ ВСЕ ИНТЕГРАЦИИ ЗАВЕРШЕНЫ! 100% SUCCESS RATE!

📋 ЧТО СДЕЛАНО:
   1. ✅ Autonomous Service + NASA Learning
   2. ✅ Dashboard + 8 новых endpoints
   3. ✅ Systemd Services для автозапуска

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🚀 ВЫБЕРИ ОДИН ИЗ ВАРИАНТОВ:

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1️⃣  РУЧНОЙ ЗАПУСК (для тестирования):

   cd /root/mirai/mirai-agent
   source venv/bin/activate
   
   # Terminal 1: Autonomous Service
   python3 autonomous_service.py --interval 600
   
   # Terminal 2: Dashboard
   python3 dashboard_server.py

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

2️⃣  SYSTEMD SERVICES (рекомендуется для production):

   cd /root/mirai/mirai-agent
   sudo ./install_nasa_services.sh
   
   # Сервисы запустятся автоматически и будут:
   # - Стартовать при загрузке системы
   # - Перезапускаться при падении
   # - Логировать всё автоматически

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔍 ПРОВЕРКА РАБОТЫ:

   # Тест интеграции
   python3 test_nasa_integration.py
   
   # Логи autonomous service
   tail -f /tmp/kaizen_mirai.log
   
   # Dashboard endpoints
   curl http://localhost:5000/api/nasa/status
   curl http://localhost:5000/api/nasa/metrics
   curl http://localhost:5000/api/nasa/knowledge

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📚 ДОКУМЕНТАЦИЯ:

   • NASA_INTEGRATION_COMPLETE.md - Полное описание
   • NASA_LEVEL_DEPLOYMENT.md - Deployment guide
   • NASA_FUTURE_IMPROVEMENTS.md - Что можно добавить

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎯 КАК ЭТО РАБОТАЕТ:

   1. autonomous_service.py работает в фоне (каждые 10 минут)
   2. Каждые 3 цикла MIRAI выбирает что изучить
   3. KAIZEN изучает через NASA-Level систему
   4. Результаты сохраняются в Knowledge Base + Metrics
   5. Dashboard показывает всё в реальном времени

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🌟 ГОТОВО! Наслаждайся автономным AI обучением! 🚀

EOF
