// ⚡ STRESS / SHOWCASE ФАЙЛ ДЛЯ ПРОВЕРКИ ЭКСТРЕМАЛЬНОГО РЕЖИМА AUTO ACCEPT
// Открой этот файл, начни печатать фразы из комментариев — смотри, как Copilot дописывает и как
// расширение автоматически ПРИНИМАЕТ подсказку (🔥 если включено).
// -----------------------------------------------------------------------------
// Подсказки сгруппированы по блокам. Иди сверху вниз и тестируй.
// РЕКОМЕНДАЦИЯ: включи strategy = "first" и smartGuards = false, чтобы увидеть максимум.

// 1. ПРОСТЫЕ ФУНКЦИИ -----------------------------------------------------------
// Начни набирать: function sum(a: number, b: number)
// Ожидаемо: Copilot подставит тело return a + b;
function sum(a: number, b: number) { return a + b; }

// Начни: const square = (n: number)
const square = (n: number) => n * n;

// Начни: function fibonacci(n: number)
function fibonacci(n: number): number {
  if (n <= 1) return n;
  return fibonacci(n - 1) + fibonacci(n - 2);
}

// 2. ОБРАБОТКА МАССИВОВ -------------------------------------------------------
// Начни: const nums = [
const nums = [1,2,3,4,5,6,7,8,9,10];
// Начни: const evens = nums.filter(
const evens = nums.filter(n => n % 2 === 0);
// Начни: const aggregated = nums.reduce(
const aggregated = nums.reduce((acc, v) => acc + v, 0);

// 3. КЛАССЫ И ОБЪЕКТЫ ---------------------------------------------------------
// Начни: class Account {
class Account {
  constructor(public id: string, public balance: number = 0) {}
  // Начни: deposit(amount: number)
  deposit(amount: number) { this.balance += amount; return this; }
  // Начни: withdraw(amount: number)
  withdraw(amount: number) { if (amount > this.balance) throw new Error('Insufficient'); this.balance -= amount; return this; }
  // Начни: toString()
  toString() { return `Account(${this.id}) balance=${this.balance}`; }
}

// 4. АСИНХРОННЫЙ КОД ----------------------------------------------------------
// Начни: async function delay(ms: number)
async function delay(ms: number) { return new Promise(r => setTimeout(r, ms)); }

// Начни: async function fetchJson(url: string)
async function fetchJson(url: string) {
  try {
    // В среде Node fetch может отсутствовать: делаем ленивый fallback
    let fetched: any;
    if (typeof (globalThis as any).fetch === 'function') {
      fetched = await (globalThis as any).fetch(url);
      if (!fetched.ok) throw new Error('Bad status ' + fetched.status);
      return await fetched.json();
    } else {
      // Простой fallback на https без полной типизации
      const https = await import('https');
      fetched = await new Promise<any>((resolve, reject) => {
        https.get(url, (resp: any) => {
          if (resp.statusCode && resp.statusCode >= 400) {
            reject(new Error('Bad status ' + resp.statusCode));
            return;
          }
          const chunks: Buffer[] = [];
            resp.on('data', (c: Buffer) => chunks.push(c));
            resp.on('end', () => {
              try {
                const raw = Buffer.concat(chunks).toString('utf8');
                resolve({ json: () => JSON.parse(raw) });
              } catch (e) { reject(e); }
            });
        }).on('error', reject);
      });
      return await fetched.json();
    }
  } catch (e) {
    console.error('fetchJson error', e);
    return null;
  }
}

// 5. ПАТТЕРНЫ С GUARDS --------------------------------------------------------
// Начни: function isNonEmptyString(value: any)
function isNonEmptyString(value: any): value is string {
  return typeof value === 'string' && value.trim().length > 0;
}

// Начни: function safeParseInt(str: string)
function safeParseInt(str: string) {
  const n = parseInt(str, 10);
  return Number.isNaN(n) ? null : n;
}

// 6. ОБОРАЧИВАНИЕ / ДЕКОРАТОРЫ (простой пример) -------------------------------
// Начни: function measure<T extends(...args:any[]) => any>(fn: T)
function measure<T extends (...args: any[]) => any>(fn: T): T {
  return ((...args: any[]) => {
    const start = performance.now();
    const result = fn(...args);
    const end = performance.now();
    console.log(`⏱️ ${fn.name} took ${(end - start).toFixed(2)}ms`);
    return result;
  }) as T;
}

// 7. РАБОТА С КАРТАМИ / НАБОРАМИ ---------------------------------------------
// Начни: const userSet = new Set<string>([
const userSet = new Set<string>(['alice','bob','carol']);
// Начни: const userMap = new Map<string, number>([
const userMap = new Map<string, number>([['alice',1],['bob',2]]);

// 8. ГЕНЕРАТОРЫ ----------------------------------------------------------------
// Начни: function *range(start: number, end: number)
function *range(start: number, end: number) {
  for (let i = start; i <= end; i++) yield i;
}

// 9. ERROR HANDLING С ПОВТОРОМ -------------------------------------------------
// Начни: async function withRetry<T>(fn: () => Promise<T>
async function withRetry<T>(fn: () => Promise<T>, attempts = 3): Promise<T> {
  let lastErr: any;
  for (let i = 0; i < attempts; i++) {
    try { return await fn(); } catch (e) { lastErr = e; await delay(50); }
  }
  throw lastErr;
}

// 10. ПРОСТАЯ ИМИТАЦИЯ DOMAIN МОДЕЛИ ------------------------------------------
// Начни: interface Order {
interface Order { id: string; items: string[]; total: number; createdAt: Date; }
// Начни: function createOrder(id: string)
function createOrder(id: string): Order { return { id, items: [], total: 0, createdAt: new Date() }; }
// Начни: function addItem(order: Order, name: string, price: number)
function addItem(order: Order, name: string, price: number) { order.items.push(name); order.total += price; }

// 11. ТЕСТОВЫЕ ВЫЗОВЫ ---------------------------------------------------------
async function demo() {
  const acc = new Account('demo').deposit(100).withdraw(40);
  console.log(acc.toString());
  console.log('fibonacci(8)=', fibonacci(8));
  console.log('sum=', sum(2,5), 'square=', square(9));
  console.log('evens=', evens, 'agg=', aggregated);
  console.log('range(3,7)=', [...range(3,7)]);
  console.log('isNonEmptyString("  hi ")=', isNonEmptyString('  hi '));
  console.log('safeParseInt("42")=', safeParseInt('42'));
  await withRetry(async () => { await delay(10); return true; });
  console.log('✅ demo complete');
}

// Запусти вручную в Node (либо просто оставь как есть). Для запуска:
// npx ts-node src/tests/auto-accept-stress.ts (если установлен ts-node)
// или предварительно tsc, затем node dist/tests/auto-accept-stress.js

if (require.main === module) {
  demo();
}

export {
    Account, addItem, aggregated, createOrder, delay, demo, evens, fetchJson, fibonacci, isNonEmptyString, measure, nums, range, safeParseInt, square, sum, userMap, userSet, withRetry
};

