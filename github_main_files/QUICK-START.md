# 🔥 ЭКСТРЕМАЛЬНАЯ УСТАНОВКА И ЗАПУСК

## 📋 Быстрый старт

### 1. Установка расширения
```powershell
# Установка локального VSIX пакета
code --install-extension copilot-auto-accept-1.0.0.vsix
```

### 2. Активация экстремального режима
После установки расширения:
1. Перезапустите VS Code
2. Откройте любой TypeScript/JavaScript файл
3. Увидите предупреждение: "⚠️🔥 ЭКСТРЕМАЛЬНЫЙ РЕЖИМ: Copilot будет автоматически применять подсказки!"
4. В статус-баре появится индикатор: 🔥 Copilot Auto

### 3. Быстрые команды
- `Ctrl+Shift+P` → "Copilot Auto Accept: Toggle On/Off"
- `Ctrl+Shift+P` → "Copilot Auto Accept: Force Accept Now"

### 4. Запуск автокоммитов
```powershell
# Тестовый запуск (без реальных коммитов)
.\scripts\auto-commit.ps1 -DryRun -Verbose

# Одиночный коммит
.\scripts\auto-commit.ps1 -ConfigPath ".\scripts\auto-commit-config.json"

# Циклический режим (каждые 3 минуты)
.\scripts\auto-commit.ps1 -Verbose
```

## ⚙️ Настройки VS Code

Откройте Settings (`Ctrl+,`) и найдите "Copilot Auto Accept":

- **Enable**: Включить автоматизацию ✅
- **Idle Ms**: 800мс (задержка перед авто-принятием)
- **Strategy**: `stable` (рекомендуемо) или `first` (экстремально быстро)
- **Languages**: TypeScript, JavaScript, Python и др.
- **Smart Guards**: ✅ (защита от автоподстановки в незакрытых конструкциях)

## 🔧 Конфигурация автокоммитов

Отредактируйте `scripts/auto-commit-config.json`:
```json
{
  "intervalMinutes": 3,
  "commitPrefix": "🔥 auto:",
  "autoPush": false,
  "runOnce": false
}
```

## ⚠️ ВАЖНЫЕ ПРЕДУПРЕЖДЕНИЯ

1. **НЕ ИСПОЛЬЗУЙТЕ В ПРОДАКШЕНЕ** - только для экспериментов!
2. **Делайте резервные копии** перед включением
3. **Внимательно проверяйте** автоматически принятый код
4. **Готовьтесь к откату** через Git при проблемах

## 🚀 Экстремальные настройки

Если хочешь МАКСИМАЛЬНУЮ автоматизацию, скопируй настройки из `.vscode/settings.json` в свой глобальный settings.json VS Code:

1. `Ctrl+Shift+P` → "Preferences: Open Settings (JSON)"
2. Скопируй агрессивные настройки из проекта
3. Перезапусти VS Code

## 🛠️ Разработка

Для модификации расширения:
```powershell
# Режим watch (автоперекомпиляция)
npm run watch

# Запуск в Development Host
# Нажми F5 в VS Code
```

## 📁 Копирование в F:\extreme-copilot-auto

После тестирования скопируй всё содержимое `C:\extreme-copilot-auto-temp\` в `F:\extreme-copilot-auto\` через Проводник Windows (потребуются права администратора).

---

🔥 **ГОТОВ К ЭКСТРЕМАЛЬНЫМ ЭКСПЕРИМЕНТАМ С COPILOT!** 🔥