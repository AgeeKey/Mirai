import * as vscode from 'vscode';

export class Config {
  private config!: vscode.WorkspaceConfiguration;

  constructor() {
    this.reload();
  }

  public reload(): void {
    this.config = vscode.workspace.getConfiguration('copilotAutoAccept');
  }

  public isEnabled(): boolean {
    return this.config.get<boolean>('enable', true);
  }

  public getIdleMs(): number {
    return this.config.get<number>('idleMs', 800);
  }

  public getMaxFileSizeKB(): number {
    return this.config.get<number>('maxFileSizeKB', 500);
  }

  public getStrategy(): 'first' | 'stable' {
    return this.config.get<'first' | 'stable'>('strategy', 'stable');
  }

  public getSupportedLanguages(): string[] {
    return this.config.get<string[]>('languages', [
      'typescript', 'javascript', 'python', 'go', 'rust', 'java', 'csharp'
    ]);
  }

  public getExcludePatterns(): string[] {
    return this.config.get<string[]>('excludePatterns', ['*.md', '*.txt', '*.json']);
  }

  public isSmartGuardsEnabled(): boolean {
    return this.config.get<boolean>('smartGuards', true);
  }

  public isLanguageSupported(languageId: string): boolean {
    const supported = this.getSupportedLanguages();
    return supported.length === 0 || supported.includes(languageId);
  }

  public isFileExcluded(fileName: string): boolean {
    const patterns = this.getExcludePatterns();
    return patterns.some(pattern => this.matchesPattern(fileName, pattern));
  }

  private matchesPattern(fileName: string, pattern: string): boolean {
    // Simple glob-like matching
    const regex = pattern
      .replace(/\./g, '\\.')
      .replace(/\*/g, '.*')
      .replace(/\?/g, '.');
    
    return new RegExp(regex + '$', 'i').test(fileName);
  }
}