import * as vscode from 'vscode';

export class GuardChecker {
  
  /**
   * Проверяет, безопасно ли автоматически принимать подсказку в текущей позиции
   */
  public isSafeToAccept(document: vscode.TextDocument, position: vscode.Position): boolean {
    const line = document.lineAt(position.line);
    const lineText = line.text;
    const charIndex = position.character;

    // Проверка 1: Не принимать, если курсор внутри строки (не в конце)
    if (charIndex < lineText.length && lineText.substring(charIndex).trim() !== '') {
      return false;
    }

    // Проверка 2: Не принимать внутри незакрытых кавычек
    if (this.isInsideUnclosedQuotes(lineText, charIndex)) {
      return false;
    }

    // Проверка 3: Не принимать внутри незакрытых скобок
    if (this.isInsideUnclosedBrackets(lineText, charIndex)) {
      return false;
    }

    // Проверка 4: Не принимать в комментариях (опционально)
    if (this.isInsideComment(lineText, charIndex, document.languageId)) {
      return false;
    }

    // Проверка 5: Не принимать, если строка выглядит незавершённой
    if (this.looksIncomplete(lineText.substring(0, charIndex))) {
      return false;
    }

    return true;
  }

  private isInsideUnclosedQuotes(text: string, position: number): boolean {
    const beforeCursor = text.substring(0, position);
    
    // Проверяем одинарные кавычки
    const singleQuotes = (beforeCursor.match(/'/g) || []).length;
    if (singleQuotes % 2 !== 0) return true;

    // Проверяем двойные кавычки
    const doubleQuotes = (beforeCursor.match(/"/g) || []).length;
    if (doubleQuotes % 2 !== 0) return true;

    // Проверяем обратные кавычки (template literals)
    const backQuotes = (beforeCursor.match(/`/g) || []).length;
    if (backQuotes % 2 !== 0) return true;

    return false;
  }

  private isInsideUnclosedBrackets(text: string, position: number): boolean {
    const beforeCursor = text.substring(0, position);
    
    let roundBrackets = 0;
    let squareBrackets = 0;
    let curlyBrackets = 0;

    for (const char of beforeCursor) {
      switch (char) {
        case '(':
          roundBrackets++;
          break;
        case ')':
          roundBrackets--;
          break;
        case '[':
          squareBrackets++;
          break;
        case ']':
          squareBrackets--;
          break;
        case '{':
          curlyBrackets++;
          break;
        case '}':
          curlyBrackets--;
          break;
      }
    }

    return roundBrackets > 0 || squareBrackets > 0 || curlyBrackets > 0;
  }

  private isInsideComment(text: string, position: number, languageId: string): boolean {
    const beforeCursor = text.substring(0, position);

    // Для большинства языков
    if (beforeCursor.includes('//')) {
      const commentIndex = beforeCursor.lastIndexOf('//');
      if (commentIndex !== -1 && position > commentIndex) {
        return true;
      }
    }

    // Для Python, Shell
    if (['python', 'shellscript', 'powershell'].includes(languageId)) {
      if (beforeCursor.includes('#')) {
        const commentIndex = beforeCursor.lastIndexOf('#');
        if (commentIndex !== -1 && position > commentIndex) {
          return true;
        }
      }
    }

    return false;
  }

  private looksIncomplete(text: string): boolean {
    const trimmed = text.trim();
    
    // Пустая строка - ОК
    if (trimmed === '') return false;

    // Строка заканчивается на операторы - выглядит незавершённой
    const incompleteEndings = ['+', '-', '*', '/', '=', '==', '!=', '<', '>', '&&', '||', '&', '|', '^'];
    if (incompleteEndings.some(op => trimmed.endsWith(op))) {
      return true;
    }

    // Строка заканчивается на ключевые слова
    const incompleteKeywords = ['if', 'else', 'for', 'while', 'function', 'def', 'class', 'import', 'from'];
    const lastWord = trimmed.split(/\s+/).pop() || '';
    if (incompleteKeywords.includes(lastWord)) {
      return true;
    }

    return false;
  }
}