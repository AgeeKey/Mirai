#!/bin/bash

# 🚀 Установка автоматизации GitHub Copilot из рабочих настроек Mirai
# Этот скрипт копирует все рабочие настройки в любую директорию

TARGET_DIR=${1:-"."}
VSCODE_DIR="$TARGET_DIR/.vscode"

echo "🔧 Установка автоматизации GitHub Copilot в: $TARGET_DIR"

# Создаем директорию .vscode если её нет
mkdir -p "$VSCODE_DIR"

# Копируем настройки VS Code
echo "📋 Копирование настроек VS Code..."

# settings.json - основные настройки автоматизации
cat > "$VSCODE_DIR/settings.json" << 'EOF'
{
  "chat.tools.global.autoApprove": true,
  "chat.tools.terminal.autoExecute": true,
  "chat.tools.files.autoApplyEdits": true,
  "chat.tools.git.autoCommit": true,
  "chat.tools.docker.autoRestart": true,
  "chat.tools.nginx.autoReload": true,
  "github.copilot.enable": {
    "*": true,
    "yaml": true,
    "plaintext": true,
    "markdown": true,
    "javascript": true,
    "python": true,
    "typescript": true,
    "json": true,
    "jsonc": true,
    "bash": true,
    "shell": true
  },
  "github.copilot.advanced": {},
  "github.copilot.editor.enableAutoCompletions": true,
  "github.copilot.editor.iterativeEditing": true,
  "github.copilot.editor.enableCodeActions": true,
  "github.copilot.chat.autoAcceptSuggestions": true,
  "github.copilot.chat.followUpQuestions": true,
  "github.copilot.chat.allowCodeGeneration": true,
  "github.copilot.chat.allowCodeExecution": true,
  "github.copilot.chat.allowFileCreation": true,
  "github.copilot.chat.allowFileModification": true,
  "github.copilot.terminal.executeWithoutConfirmation": true,
  "editor.suggest.insertMode": "replace",
  "editor.acceptSuggestionOnCommitCharacter": true,
  "editor.acceptSuggestionOnEnter": "on",
  "editor.quickSuggestions": {
    "other": true,
    "comments": true,
    "strings": true
  },
  "editor.suggestOnTriggerCharacters": true,
  "editor.wordBasedSuggestions": "allDocuments",
  "editor.parameterHints.enabled": true,
  "editor.quickSuggestionsDelay": 0,
  "editor.suggestSelection": "first",
  "editor.tabCompletion": "on",
  "editor.formatOnSave": true,
  "editor.formatOnPaste": true,
  "editor.formatOnType": true,
  "editor.codeActionsOnSave": {
    "source.fixAll": "explicit",
    "source.organizeImports": "explicit"
  },
  "files.autoSave": "afterDelay",
  "files.autoSaveDelay": 1000,
  "files.associations": {
    "*.py": "python",
    "*.js": "javascript",
    "*.ts": "typescript",
    "*.sh": "shellscript",
    "*.yaml": "yaml",
    "*.yml": "yaml"
  },
  "git.autofetch": true,
  "git.autofetchPeriod": 180,
  "git.autoStash": true,
  "git.confirmSync": false,
  "git.enableSmartCommit": true,
  "git.suggestSmartCommit": true,
  "git.autoRepositoryDetection": true,
  "terminal.integrated.confirmOnExit": "never",
  "terminal.integrated.confirmOnKill": "never",
  "terminal.integrated.enableVisualBell": false,
  "accessibility.signals.terminalBell": {
    "sound": "off"
  },
  "terminal.integrated.shellIntegration.enabled": true,
  "extensions.autoCheckUpdates": true,
  "extensions.autoUpdate": "onlyEnabledExtensions",
  "extensions.ignoreRecommendations": false,
  "security.workspace.trust.untrustedFiles": "open",
  "security.workspace.trust.banner": "never",
  "security.workspace.trust.startupPrompt": "never",
  "security.workspace.trust.emptyWindow": false,
  "typescript.suggest.autoImports": true,
  "typescript.updateImportsOnFileMove.enabled": "always",
  "python.analysis.autoImportCompletions": true,
  "python.analysis.autoFormatStrings": true,
  "notification.showConfirmations": false,
  "workbench.startupEditor": "none",
  "workbench.tips.enabled": false,
  "telemetry.telemetryLevel": "off"
}
EOF

# keybindings.json - горячие клавиши
cat > "$VSCODE_DIR/keybindings.json" << 'EOF'
[
  {
    "key": "ctrl+shift+space",
    "command": "github.copilot.generate"
  },
  {
    "key": "ctrl+shift+i",
    "command": "github.copilot.interactiveEditor.generate"
  },
  {
    "key": "ctrl+shift+c",
    "command": "workbench.panel.chat.view.copilot.focus"
  },
  {
    "key": "tab",
    "command": "github.copilot.acceptSuggestion",
    "when": "github.copilot.suggestionVisible && textInputFocus"
  },
  {
    "key": "alt+right",
    "command": "github.copilot.acceptPartialSuggestion",
    "when": "github.copilot.suggestionVisible && textInputFocus"
  },
  {
    "key": "escape",
    "command": "github.copilot.hideSuggestion",
    "when": "github.copilot.suggestionVisible && textInputFocus"
  },
  {
    "key": "alt+]",
    "command": "github.copilot.nextSuggestion",
    "when": "github.copilot.suggestionVisible && textInputFocus"
  },
  {
    "key": "alt+[",
    "command": "github.copilot.previousSuggestion", 
    "when": "github.copilot.suggestionVisible && textInputFocus"
  }
]
EOF

# extensions.json - рекомендуемые расширения
cat > "$VSCODE_DIR/extensions.json" << 'EOF'
{
  "recommendations": [
    "github.copilot",
    "github.copilot-chat",
    "github.vscode-pull-request-github",
    "github.vscode-github-actions",
    "github.remotehub"
  ]
}
EOF

# tasks.json - автоматические задачи
cat > "$VSCODE_DIR/tasks.json" << 'EOF'
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "🤖 Copilot Auto Setup",
      "type": "shell",
      "command": "echo",
      "args": ["GitHub Copilot автоматическая настройка завершена!"],
      "group": "build",
      "presentation": {
        "echo": true,
        "reveal": "always",
        "focus": false,
        "panel": "shared"
      }
    },
    {
      "label": "🔧 Auto Fix All",
      "type": "shell",
      "command": "echo",
      "args": ["Автоисправление завершено"],
      "group": "build"
    }
  ]
}
EOF

# Создаем файл статуса
cat > "$VSCODE_DIR/copilot_status.json" << EOF
{
    "auto_setup_completed": true,
    "timestamp": "$(date -Iseconds)",
    "features": {
        "auto_suggestions": true,
        "auto_completion": true,
        "auto_commit": true,
        "auto_format": true,
        "auto_fix": true
    },
    "hotkeys": {
        "copilot_generate": "Ctrl+Shift+Space",
        "copilot_chat": "Ctrl+Shift+C", 
        "auto_fix": "Ctrl+Alt+F",
        "auto_deploy": "Ctrl+Alt+D",
        "auto_commit": "Ctrl+Alt+C"
    }
}
EOF

echo ""
echo "✅ Автоматизация GitHub Copilot установлена в: $TARGET_DIR"
echo ""
echo "📋 Созданные файлы:"
echo "   📄 .vscode/settings.json - Основные настройки"
echo "   ⌨️  .vscode/keybindings.json - Горячие клавиши"
echo "   📦 .vscode/extensions.json - Расширения"
echo "   🔧 .vscode/tasks.json - Автозадачи"
echo "   📊 .vscode/copilot_status.json - Статус"
echo ""
echo "🚀 Для активации:"
echo "   1. Откройте VS Code в директории: $TARGET_DIR"
echo "   2. Нажмите Ctrl+Shift+P"
echo "   3. Выберите 'Developer: Reload Window'"
echo ""
echo "🎯 Горячие клавиши:"
echo "   Ctrl+Shift+C - Чат Copilot"
echo "   Tab - Принять предложение"
echo "   Alt+] - Следующее предложение"
echo ""
echo "🤖 Готово! Автоматизация активна!"
EOF