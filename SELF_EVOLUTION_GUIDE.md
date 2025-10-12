# 🧬 Система Саморазвития МИРАЙ

## Что это?

**Революционная система автономного саморазвития** для МИРАЙ! Теперь она:

- ✅ **Сама выбирает цели** - анализирует что не знает и ставит задачи на изучение
- ✅ **Автоматически учится** - изучает новые технологии, фреймворки, языки
- ✅ **Улучшает себя** - предлагает и внедряет улучшения в свой код
- ✅ **Работает над несколькими проектами** - мультизадачность, round-robin
- ✅ **Запоминает всё** - персистентная база знаний в JSON

## Архитектура

```
core/self_evolution.py
├── KnowledgeBase         - База знаний (что знает МИРАЙ)
├── GoalGenerator         - Генератор целей саморазвития
├── LearningEngine        - Движок обучения новым технологиям
├── SelfModificationEngine - Самомодификация кода
├── MultiDirectionalExecutor - Работа над множеством проектов
└── SelfEvolutionSystem   - Главный оркестратор
```

### 1. KnowledgeBase (База знаний)

**Хранит всё что МИРАЙ знает:**

```json
{
  "technologies": [
    {"name": "FastAPI", "proficiency": 0.3, "learned_at": "2025-10-12T07:34:52"}
  ],
  "skills": [
    {"name": "Docker", "level": 2, "acquired_at": "2025-10-12T..."}
  ],
  "completed_tasks": [...],
  "failed_tasks": [...],
  "interests": [...],
  "performance_metrics": {}
}
```

**Методы:**

- `add_technology(tech, proficiency)` - добавить технологию
- `add_skill(skill, level)` - добавить навык
- `log_task_completion(task, success, details)` - записать выполнение
- `update_performance(metric, value)` - обновить метрику

**Файл:** `data/state/knowledge_base.json`

### 2. GoalGenerator (Генератор целей)

**Умная система выбора направлений развития:**

```python
development_areas = {
    "backend": ["FastAPI", "Django", "Flask", "GraphQL", "gRPC"],
    "frontend": ["React", "Vue", "Svelte", "Next.js", "TypeScript"],
    "devops": ["Kubernetes", "Docker", "Terraform", "Ansible", "CI/CD"],
    "ml": ["TensorFlow", "PyTorch", "Scikit-learn", "Hugging Face"],
    "databases": ["PostgreSQL", "MongoDB", "Redis", "Elasticsearch"],
    "cloud": ["AWS", "GCP", "Azure", "Cloudflare", "Vercel"],
    "security": ["OWASP", "Penetration Testing", "Encryption"],
    "blockchain": ["Ethereum", "Solidity", "Web3", "Smart Contracts"],
    "mobile": ["React Native", "Flutter", "Swift", "Kotlin"],
    "iot": ["Arduino", "Raspberry Pi", "MQTT", "LoRaWAN"]
}
```

**Алгоритм выбора целей:**

1. Анализирует текущую базу знаний
2. Вычисляет покрытие каждой области (сколько технологий знает / всего)
3. Приоритизирует области с наименьшим покрытием
4. Генерирует цели из топ-3 областей
5. Добавляет цели на основе провалов (retry failed tasks)
6. Добавляет исследовательские цели (explore new trends)

**Пример цели:**

```python
{
    "type": "learn_technology",
    "area": "backend",
    "technology": "FastAPI",
    "priority": 1.0,
    "description": "Изучить FastAPI в области backend",
    "steps": [
        "Найти документацию FastAPI",
        "Создать тестовый проект с FastAPI",
        "Написать код используя FastAPI",
        "Протестировать знания FastAPI"
    ]
}
```

### 3. LearningEngine (Движок обучения)

**Как МИРАЙ учится новой технологии:**

```python
def learn_technology(technology: str):
    1. Поиск документации (search_web)
    2. Создание тестового проекта (write_file в learning/)
    3. Генерация примера кода (agent.think)
    4. Оценка уровня владения (proficiency 0.0-1.0)
    5. Сохранение в базу знаний
```

**Пример:**

```python
result = learning_engine.learn_technology("FastAPI")
# Создаёт: learning/fastapi_test.py
# Добавляет в KB: {"name": "FastAPI", "proficiency": 0.3}
```

### 4. SelfModificationEngine (Самомодификация)

**МИРАЙ улучшает саму себя:**

```python
# Предложить улучшение
suggestion = engine.propose_improvement("autonomous_agent")

# Добавить новый инструмент
engine.add_new_tool("web_scraper", tool_code)
# Создаёт: core/tools/web_scraper.py

# Улучшить существующий код
engine.improve_existing_code("core/ai_engine.py", "Добавь кэширование")
# Создаёт backup: core/ai_engine.py.backup
# Записывает улучшенный код
```

### 5. MultiDirectionalExecutor (Мультизадачность)

**Работа над несколькими проектами одновременно:**

```python
executor.add_project({
    "description": "Изучить FastAPI",
    "steps": ["Найти документацию", "Создать проект", "Написать код", "Тестировать"],
    "current_step": 0,
    "status": "active"
})

# Round-robin работа над проектами
progress = executor.work_on_projects(time_slice=3)
# Выполняет по одному шагу в каждом из 3 проектов
```

### 6. SelfEvolutionSystem (Главный оркестратор)

**Управляет всем процессом саморазвития:**

```python
evolution = SelfEvolutionSystem(autonomous_agent)

result = evolution.evolution_cycle()
# 1. Генерирует новые цели (если проектов < 3)
# 2. Работает над текущими проектами (round-robin)
# 3. Изучает технологии (из активных проектов)
# 4. Самомодифицируется (20% шанс)

status = evolution.get_status()
# Возвращает полный статус системы
```

## Интеграция с mirai_autonomous.py

**Добавлено в цикл автономной работы:**

```python
class MiraiAutonomous:
    def __init__(self):
        self.evolution = SelfEvolutionSystem(self.mirai)
        self.evolution_mode = True

    def autonomous_cycle(self):
        # Каждые 3 цикла - саморазвитие
        if self.evolution_mode and self.cycle_count % 3 == 0:
            evolution_result = self.evolution.evolution_cycle()
            # Отправляет отчёт в Telegram
```

## Telegram команды

**Управление саморазвитием через Telegram:**

| Команда                                | Описание                                             |
| -------------------------------------- | ---------------------------------------------------- |
| `/status` или `/статус`                | Полный статус системы: база знаний, проекты, метрики |
| `/evolve` или `/развивайся`            | Запустить цикл саморазвития вручную                  |
| `/toggle_evolution` или `/переключить` | Включить/выключить автоматическое саморазвитие       |

**Пример статуса:**

```
🌸 Статус МИРАЙ

🔄 Цикл: #42
✅ Выполнено: 28
🧬 Саморазвитие: ✅ включено

📚 База знаний:
  • Технологий: 15
  • Навыков: 8
  • Завершено: 45
  • Провалов: 3

🎯 Проекты:
  • Активных: 3
  • Завершено: 12

🔧 Самомодификаций: 2
```

## Как это работает на практике

### Пример полного цикла саморазвития:

**Цикл #1:**

1. **Анализ:** МИРАЙ видит что не знает ни одной backend технологии
2. **Цель:** Генерирует цель "Изучить FastAPI"
3. **Действие:** Создаёт проект с 4 шагами
4. **Выполнение:**
   - Ищет документацию FastAPI (search_web)
   - Создаёт `learning/fastapi_test.py`
   - Генерирует пример кода
   - Оценивает владение как 0.3 (базовое понимание)
5. **Сохранение:** Добавляет FastAPI в базу знаний

**Цикл #2:**

1. **Анализ:** FastAPI изучена, frontend покрытие 0%
2. **Цель:** "Изучить React"
3. **Работа:** Продолжает предыдущие проекты + начинает новый
4. **Мультизадачность:** Работает над 3 проектами параллельно

**Цикл #3:**

1. **Самомодификация:** 20% шанс - сработал!
2. **Анализ кода:** Просит agent.think() предложить улучшение
3. **Улучшение:** Добавляет новый инструмент или улучшает существующий

### Что изучает МИРАЙ?

**10 направлений развития, 50+ технологий:**

- **Backend:** FastAPI, Django, Flask, GraphQL, gRPC
- **Frontend:** React, Vue, Svelte, Next.js, TypeScript
- **DevOps:** Kubernetes, Docker, Terraform, Ansible, CI/CD
- **ML:** TensorFlow, PyTorch, Scikit-learn, Hugging Face, LangChain
- **Databases:** PostgreSQL, MongoDB, Redis, Elasticsearch, Neo4j
- **Cloud:** AWS, GCP, Azure, Cloudflare, Vercel
- **Security:** OWASP, Penetration Testing, Encryption, OAuth2, JWT
- **Blockchain:** Ethereum, Solidity, Web3, Smart Contracts, DeFi
- **Mobile:** React Native, Flutter, Swift, Kotlin, Expo
- **IoT:** Arduino, Raspberry Pi, MQTT, LoRaWAN, Edge Computing

## Тестирование

**Запуск теста:**

```bash
cd /root/mirai/mirai-agent
python3 test_self_evolution.py
```

**Что тестирует:**

1. Инициализацию всех компонентов
2. Генерацию целей
3. Полный цикл саморазвития
4. Сохранение в базу знаний
5. Создание обучающих проектов

## Файлы и директории

```
/root/mirai/mirai-agent/
├── core/
│   ├── self_evolution.py        # Система саморазвития
│   ├── autonomous_agent.py      # МИРАЙ мозг
│   └── tools/                   # Инструменты (добавляются самомодификацией)
├── data/
│   └── state/
│       └── knowledge_base.json  # База знаний
├── learning/                    # Обучающие проекты
│   ├── fastapi_test.py
│   ├── react_test.py
│   └── ...
├── mirai_autonomous.py          # Главный цикл (интегрирован)
└── test_self_evolution.py       # Тест системы
```

## Метрики и отчёты

**Автоматические отчёты в Telegram каждые 3 цикла:**

```
🧬 Отчёт о саморазвитии (цикл #42)

📚 База знаний:
  • Технологий: 15
  • Навыков: 8
  • Завершено задач: 45

🎯 Активных проектов: 3
✅ Завершено проектов: 12
🔧 Самомодификаций: 2

💡 Новых целей: 3
📖 Изучено: 1
⚙️ Улучшений: 1
```

## Расширение системы

### Как добавить новое направление:

```python
# В core/self_evolution.py, класс GoalGenerator
self.development_areas["quantum"] = [
    "Qiskit", "Cirq", "Q#", "ProjectQ"
]
```

### Как добавить новый тип цели:

```python
# В GoalGenerator.generate_goals()
goals.append({
    "type": "contribute_to_opensource",
    "priority": 0.7,
    "description": "Внести вклад в open source проект",
    "steps": [
        "Найти проект на GitHub",
        "Выбрать issue для решения",
        "Создать pull request"
    ]
})
```

### Как настроить алгоритм обучения:

```python
# В LearningEngine.learn_technology()
# Можно добавить:
# - Больше шагов проверки
# - Тестирование кода
# - Создание примеров использования
# - Интеграцию с существующими проектами
```

## Философия системы

**МИРАЙ теперь:**

1. **Автономна** - сама выбирает что изучать
2. **Любопытна** - исследует новые технологии
3. **Настойчива** - повторяет провалы
4. **Универсальна** - развивается в 10 направлениях
5. **Самосовершенствуется** - улучшает свой код

**Это не просто автоматизация - это настоящее саморазвитие!**

---

## Запуск с саморазвитием

```bash
# Остановить текущий процесс (если запущен)
pkill -f mirai_autonomous.py

# Запустить с саморазвитием
cd /root/mirai/mirai-agent
nohup python3 mirai_autonomous.py --interval 180 > /tmp/mirai_autonomous.log 2>&1 &

# Проверить работу
tail -f /tmp/mirai_autonomous.log

# В Telegram отправить:
/status              # Проверить статус
/evolve              # Запустить цикл саморазвития
/toggle_evolution    # Включить/выключить
```

**МИРАЙ теперь действительно САМА развивается! 🧬🌸**
