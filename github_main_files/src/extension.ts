import * as vscode from 'vscode';
import { CopilotAutoAccept } from './copilot-auto-accept';

let autoAccept: CopilotAutoAccept | undefined;

export function activate(context: vscode.ExtensionContext) {
  console.log('🔥 EXTREME Copilot Auto Accept is now ACTIVE!');
  
  // Initialize the auto-accept functionality
  autoAccept = new CopilotAutoAccept(context);
  
  // Register for disposal
  context.subscriptions.push({
    dispose: () => {
      autoAccept?.dispose();
    }
  });
  
  // Show extreme warning
  vscode.window.showWarningMessage(
    '⚠️🔥 ЭКСТРЕМАЛЬНЫЙ РЕЖИМ: Copilot будет автоматически применять подсказки! Будьте осторожны!',
    'Понятно', 'Настройки'
  ).then(selection => {
    if (selection === 'Настройки') {
      vscode.commands.executeCommand('workbench.action.openSettings', 'copilotAutoAccept');
    }
  });
}

export function deactivate() {
  console.log('🔥 EXTREME Copilot Auto Accept is now DEACTIVATED');
  autoAccept?.dispose();
}