#!/bin/bash
# Установка MIRAI как системного сервиса

echo "🔧 Установка MIRAI как системного сервиса..."
echo ""

# Копируем service файл
sudo cp /root/mirai/mirai-agent/mirai-autonomous.service /etc/systemd/system/

# Перезагружаем systemd
sudo systemctl daemon-reload

echo "✅ Сервис установлен!"
echo ""
echo "📋 Команды управления сервисом:"
echo ""
echo "   Запуск:           sudo systemctl start mirai-autonomous"
echo "   Остановка:        sudo systemctl stop mirai-autonomous"
echo "   Статус:           sudo systemctl status mirai-autonomous"
echo "   Автозапуск ВКЛ:   sudo systemctl enable mirai-autonomous"
echo "   Автозапуск ВЫКЛ:  sudo systemctl disable mirai-autonomous"
echo "   Логи:             sudo journalctl -u mirai-autonomous -f"
echo ""
echo "🎯 Для запуска при загрузке системы выполните:"
echo "   sudo systemctl enable mirai-autonomous"
echo "   sudo systemctl start mirai-autonomous"
