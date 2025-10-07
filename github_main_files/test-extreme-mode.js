"use strict";
// 🔥 ТЕСТ ЭКСТРЕМАЛЬНОГО РЕЖИМА COPILOT AUTO ACCEPT
// Попробуй набрать код ниже - Copilot должен автоматически подставлять и принимать!
Object.defineProperty(exports, "__esModule", { value: true });
exports.doubled = exports.evenNumbers = exports.User = void 0;
exports.factorial = factorial;
exports.fetchUserData = fetchUserData;
// Функция для вычисления факториала
function factorial(n) {
    // Начни набирать: if (n <= 1) return 1;
    // Затем Copilot должен продолжить рекурсию
    return n <= 1 ? 1 : n * factorial(n - 1); // <-- можно изменить, тест автоподстановки
}
// Класс для работы с пользователями
class User {
    constructor(name, email, age) {
        this.name = name;
        this.email = email;
        this.age = age;
    }
    // Метод для проверки совершеннолетия - начни набирать
    isAdult() {
        // Начни набирать: return this.age >= 18
        return this.age >= 18;
    }
    // Метод для получения краткой информации - начни набирать
    getInfo() {
        // Начни набирать шаблонную строку
        return `${this.name} <${this.email}> (${this.age})`;
    }
}
exports.User = User;
// Асинхронная функция для получения данных
async function fetchUserData(userId) {
    // Начни набирать: try {
    try {
        // Имитируем задержку
        await new Promise(r => setTimeout(r, 50));
        return new User("Test", `${userId}@mail.local`, 25);
    }
    catch (e) {
        console.error("Fetch error", e);
        return null;
    }
}
// Массив чисел для обработки
const numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
// Фильтрация четных чисел - начни набирать
const evenNumbers = numbers.filter(n => n % 2 === 0);
exports.evenNumbers = evenNumbers;
// Умножение на 2 - начни набирать  
const doubled = numbers.map(n => n * 2);
exports.doubled = doubled;
console.log("🔥 Экстремальный режим активен! Попробуй набрать код выше.");
//# sourceMappingURL=test-extreme-mode.js.map