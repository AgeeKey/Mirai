import * as vscode from 'vscode';
import { Config } from './config';
import { GuardChecker } from './guard';

export class CopilotAutoAccept {
  private disposables: vscode.Disposable[] = [];
  private timer: NodeJS.Timeout | undefined;
  private config: Config;
  private guard: GuardChecker;
  private isEnabled = true;
  private statusBarItem: vscode.StatusBarItem;

  constructor(context: vscode.ExtensionContext) {
    this.config = new Config();
    this.guard = new GuardChecker();
    
    // Status bar indicator
    this.statusBarItem = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Right, 100);
    this.statusBarItem.command = 'copilotAutoAccept.toggle';
    this.updateStatusBar();
    this.statusBarItem.show();
    
    this.registerCommands(context);
    this.registerEventListeners();
    
    // Log startup
    console.log('🔥 Copilot Auto Accept: EXTREME MODE ACTIVATED');
    vscode.window.showInformationMessage('⚡ Copilot Auto Accept активирован! ЭКСТРЕМАЛЬНЫЙ РЕЖИМ');
  }

  private registerCommands(context: vscode.ExtensionContext) {
    // Toggle command
    const toggleCmd = vscode.commands.registerCommand('copilotAutoAccept.toggle', () => {
      this.isEnabled = !this.isEnabled;
      this.updateStatusBar();
      const status = this.isEnabled ? 'ВКЛЮЧЕН' : 'ВЫКЛЮЧЕН';
      vscode.window.showInformationMessage(`🔥 Copilot Auto Accept: ${status}`);
    });

    // Force accept command
    const forceCmd = vscode.commands.registerCommand('copilotAutoAccept.forceAccept', async () => {
      await this.tryAcceptSuggestion(true);
    });

    context.subscriptions.push(toggleCmd, forceCmd);
  }

  private registerEventListeners() {
    // Listen to text document changes
    const onDidChangeText = vscode.workspace.onDidChangeTextDocument((e) => {
      if (!this.isEnabled || !this.config.isEnabled()) return;
      
      const document = e.document;
      if (!this.shouldProcessDocument(document)) return;

      // Clear existing timer
      if (this.timer) {
        clearTimeout(this.timer);
        this.timer = undefined;
      }

      // Strategy handling
      const strategy = this.config.getStrategy();
      const delay = strategy === 'first' ? 50 : this.config.getIdleMs();

      this.timer = setTimeout(async () => {
        await this.tryAcceptSuggestion();
      }, delay);
    });

    // Listen to selection changes (cursor movement)
    const onDidChangeSelection = vscode.window.onDidChangeTextEditorSelection((e) => {
      if (!this.isEnabled || !this.config.isEnabled()) return;
      
      // Cancel auto-accept if user moves cursor manually
      if (this.timer) {
        clearTimeout(this.timer);
        this.timer = undefined;
      }
    });

    // Listen to config changes
    const onDidChangeConfig = vscode.workspace.onDidChangeConfiguration((e) => {
      if (e.affectsConfiguration('copilotAutoAccept')) {
        this.config.reload();
        this.updateStatusBar();
      }
    });

    this.disposables.push(onDidChangeText, onDidChangeSelection, onDidChangeConfig);
  }

  private shouldProcessDocument(document: vscode.TextDocument): boolean {
    // Check file size
    const sizeKB = Buffer.byteLength(document.getText(), 'utf8') / 1024;
    if (sizeKB > this.config.getMaxFileSizeKB()) {
      return false;
    }

    // Check language
    if (!this.config.isLanguageSupported(document.languageId)) {
      return false;
    }

    // Check exclude patterns
    if (this.config.isFileExcluded(document.fileName)) {
      return false;
    }

    return true;
  }

  private async tryAcceptSuggestion(force = false): Promise<void> {
    try {
      const editor = vscode.window.activeTextEditor;
      if (!editor) return;

      // Smart guards check (if enabled and not forced)
      if (!force && this.config.isSmartGuardsEnabled()) {
        const position = editor.selection.active;
        if (!this.guard.isSafeToAccept(editor.document, position)) {
          console.log('🛡️ Smart guard prevented auto-accept');
          return;
        }
      }

      // Try to accept inline suggestion
      await vscode.commands.executeCommand('editor.action.inlineSuggest.commit');
      
      if (force) {
        vscode.window.showInformationMessage('🔥 Принудительно принята подсказка Copilot!');
      }
    } catch (error) {
      // Silent fail - suggestion might not be available
      if (force) {
        vscode.window.showWarningMessage('⚠️ Нет доступных подсказок Copilot');
      }
    }
  }

  private updateStatusBar() {
    if (this.isEnabled && this.config.isEnabled()) {
      this.statusBarItem.text = '🔥 Copilot Auto';
      this.statusBarItem.tooltip = 'Copilot Auto Accept: АКТИВЕН (клик для переключения)';
      this.statusBarItem.backgroundColor = undefined;
    } else {
      this.statusBarItem.text = '💤 Copilot Auto';
      this.statusBarItem.tooltip = 'Copilot Auto Accept: ВЫКЛЮЧЕН (клик для включения)';
      this.statusBarItem.backgroundColor = new vscode.ThemeColor('statusBarItem.warningBackground');
    }
  }

  public dispose() {
    if (this.timer) {
      clearTimeout(this.timer);
    }
    this.statusBarItem.dispose();
    this.disposables.forEach(d => d.dispose());
  }
}