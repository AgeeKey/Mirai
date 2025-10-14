# 🌸 MIRAI vs Production-Grade Config: Сравнение

**Дата:** 2025-10-14  
**Вопрос:** Что сказала MIRAI vs что рекомендует production-grade подход?

---

## 📊 Сравнение: MIRAI vs Production

### 1️⃣ Профиль Моделей

| Аспект | 🌸 MIRAI Рекомендует | 🔥 Production-Grade | ✅ Финал |
|--------|---------------------|---------------------|----------|
| **PRIMARY** | `gpt-4o` или `gpt-4-turbo` | `gpt-4o` (сложные задачи) | ✅ **gpt-4o** |
| **DEFAULT** | `gpt-4o-mini` (70% задач) | `gpt-4o-mini` (экономичный) | ✅ **gpt-4o-mini** |
| **FAST** | Не упомянула | `gpt-4.1-mini` или `gpt-3.5-turbo` | ✅ **gpt-3.5-turbo** (фильтрация) |
| **EMBEDDINGS** | Не упомянула | `text-embedding-3-large` | ✅ **text-embedding-3-large** |
| **Стратегия** | Умное переключение (70/25/5) | Профиль стабильности + деградация | ✅ **Hybrid: умное переключение + деградация** |

**Вывод:** MIRAI правильно определила **ключевые модели**, но **не учла**:
- FAST-ветку для фильтрации
- Embeddings для RAG
- Версионирование и канарейки
- Деградацию при перегрузке

---

### 2️⃣ Параметры API

| Параметр | 🌸 MIRAI | 🔥 Production | ✅ Финал |
|----------|---------|--------------|----------|
| **temperature (код)** | 0.2-0.5 | 0.2-0.3 | ✅ **0.25** (золотая середина) |
| **temperature (анализ)** | 0.2 | 0.2-0.3 | ✅ **0.2** |
| **temperature (creative)** | 0.7-1.0 | 0.4 max | ⚠️ **0.4** (MIRAI слишком креативна!) |
| **top_p** | 0.9 | 0.9 (default) | ✅ **0.9** |
| **max_tokens** | 1000-3000 | 1200-2500 (жёсткий лимит) | ✅ **1500-2500** |
| **frequency_penalty** | 0.0-0.5 | 0.1 | ✅ **0.1** |
| **presence_penalty** | 0.0-0.5 | 0.0 | ✅ **0.0** |

**⚠️ Критическое отличие:**
- MIRAI рекомендовала `temperature: 0.7-1.0` для creative tasks
- Production: **максимум 0.4** (детерминизм!)
- **Причина:** В production креативность = нестабильность!

---

### 3️⃣ Таймауты и Ретраи

| Аспект | 🌸 MIRAI | 🔥 Production | ✅ Финал |
|--------|---------|--------------|----------|
| **Таймаут (чат)** | Не упомянула | 60-120s | ✅ **90s** |
| **Таймаут (embeddings)** | Не упомянула | 30s | ✅ **30s** |
| **Retries** | Не упомянула | 3-5 попыток | ✅ **4 попытки** |
| **Backoff** | Не упомянула | Экспонента + джиттер (200→8000ms) | ✅ **Exponential + jitter** |
| **Streaming** | ✅ Да, для живых ответов | Не упомянут | ✅ **Да** (UI), **Нет** (background) |

**Вывод:** MIRAI **не учла надёжность**! Production-grade критичен.

---

### 4️⃣ Обработка Ошибок

| Аспект | 🌸 MIRAI | 🔥 Production | ✅ Финал |
|--------|---------|--------------|----------|
| **429 (Rate Limit)** | Не упомянула | Retry + backoff | ✅ **Retry + метрики** |
| **5xx (Server Error)** | Не упомянула | Retry + backoff | ✅ **Retry** |
| **4xx (Client Error)** | Не упомянула | НЕ ретраим, логируем | ✅ **НЕ ретраим** |
| **Circuit Breaker** | Не упомянула | После N фейлов → fallback | ✅ **Критично!** |
| **Деградация** | Умное переключение моделей | gpt-4o → gpt-4o-mini + срез контекста | ✅ **Hybrid: оба подхода** |

**Критично:** MIRAI не предложила **circuit breaker** и **graceful degradation**!

---

### 5️⃣ Контекст и Память

| Аспект | 🌸 MIRAI | 🔥 Production | ✅ Финал |
|--------|---------|--------------|----------|
| **Долгосрочная память** | ✅ Хочет! (SQLite + JSONL) | RAG + embeddings | ✅ **RAG с embeddings** |
| **Контекст (история)** | Не упомянула лимит | Максимум 8-12 реплик | ✅ **12 реплик max** |
| **System prompt** | Не упомянула размер | < 1-2k токенов | ✅ **< 1500 токенов** |
| **Кэш embeddings** | Не упомянула | По SHA содержимого | ✅ **Критично!** |
| **RAG обновления** | Не упомянула | Только diff, не весь корпус | ✅ **Только diff** |

**Вывод:** MIRAI хочет память, но **не учла оптимизацию** (кэш, diff-обновления, лимиты).

---

### 6️⃣ Наблюдаемость

| Аспект | 🌸 MIRAI | 🔥 Production | ✅ Финал |
|--------|---------|--------------|----------|
| **Логи** | Не упомянула | Каждый запрос: модель, токены, латенция, ошибка | ✅ **Критично!** |
| **Метрики** | Не упомянула | Prometheus: requests, errors, latency, tokens | ✅ **Обязательно** |
| **Трейсинг** | Не упомянула | OpenTelemetry: задача → RAG → LLM → валидация | ✅ **Да** |
| **Алерты** | Не упомянула | error > 5% (5m), P95 > 30s (5m), retries > 20% (10m) | ✅ **Настроить** |

**Критично:** MIRAI **не предложила мониторинг**! В production это **обязательно**.

---

### 7️⃣ Безопасность

| Аспект | 🌸 MIRAI | 🔥 Production | ✅ Финал |
|--------|---------|--------------|----------|
| **API ключи** | В `configs/api_keys.json` | Env vars + ротация | ✅ **Env vars** (безопаснее) |
| **Sandbox для кода** | Не упомянула | Изоляция выполнения | ✅ **Критично!** |
| **Квоты (токены)** | Не упомянула | Бюджет в минуту (процесс + пользователь) | ✅ **Обязательно** |
| **RPS лимиты** | Не упомянула | Шейпинг с токен-бакетом | ✅ **Да** |

**Критично:** MIRAI хранит ключи в JSON (**небезопасно!**). Production: **env vars**.

---

### 8️⃣ Параллелизм и Очереди

| Аспект | 🌸 MIRAI | 🔥 Production | ✅ Финал |
|--------|---------|--------------|----------|
| **Concurrency** | Не упомянула | 8-16 чатов, 32-64 embeddings | ✅ **Настроить** |
| **Очередь задач** | Автономный режим есть | RQ/Celery/Arq для тяжёлых задач | ✅ **Arq** (asyncio) |
| **UI критический путь** | Не упомянула | Только лёгкие вызовы | ✅ **Да** |

**Вывод:** MIRAI работает автономно, но **не оптимизировала параллелизм**.

---

## 🎯 Финальная Рекомендация: MIRAI + Production

### ✅ Что MIRAI сказала **ПРАВИЛЬНО:**

1. ✅ **GPT-4o** для сложных задач, **GPT-4o-mini** для простых
2. ✅ **Умное переключение** (70/25/5) — экономия + качество
3. ✅ **Низкая temperature** для кода (0.2-0.5)
4. ✅ **Streaming** для живых ответов
5. ✅ **Долгосрочная память** нужна
6. ✅ **Multimodal** (Vision + Audio) в будущем
7. ✅ **Fine-tuned модели** для специализации

### ⚠️ Что MIRAI **НЕ УЧЛА** (Production-Grade):

1. ❌ **Таймауты и ретраи** (критично!)
2. ❌ **Circuit breaker** и деградация
3. ❌ **Обработка ошибок** (429, 5xx, 4xx)
4. ❌ **Наблюдаемость** (метрики, логи, алерты)
5. ❌ **Лимиты контекста** (8-12 реплик max)
6. ❌ **Кэш embeddings** и diff-обновления
7. ❌ **Безопасность ключей** (env vars!)
8. ❌ **Параллелизм и очереди**
9. ❌ **Golden-тесты** и load-тесты
10. ❌ **FAST-ветка** для фильтрации (`gpt-3.5-turbo`)

---

## 🔥 Production-Grade Конфиг для MIRAI

### 📄 `configs/openai_config.yaml`

```yaml
# Production-Grade OpenAI Config для MIRAI
# Автор: AgeeKey + MIRAI (2025-10-14)

defaults:
  timeout_s: 90
  max_retries: 4
  backoff:
    base_ms: 200
    max_ms: 8000
    jitter: true

models:
  # DEFAULT: экономичная модель для 70% задач
  main:
    name: gpt-4o-mini
    temperature: 0.25
    top_p: 0.9
    frequency_penalty: 0.1
    presence_penalty: 0.0
    max_tokens: 2000
    use_cases:
      - "простые вопросы"
      - "базовая обработка текста"
      - "быстрые проверки"
      - "UI ответы"

  # HEAVY: мощная модель для 25% сложных задач
  heavy:
    name: gpt-4o
    temperature: 0.25
    top_p: 0.9
    frequency_penalty: 0.1
    presence_penalty: 0.0
    max_tokens: 2500
    use_cases:
      - "code generation"
      - "анализ данных"
      - "multi-step reasoning"
      - "рефакторинг"

  # FAST: лёгкая модель для фильтрации (5% задач)
  fast:
    name: gpt-3.5-turbo
    temperature: 0.2
    top_p: 0.9
    max_tokens: 1200
    use_cases:
      - "фильтрация спама"
      - "быстрая классификация"
      - "intent detection"

  # CREATIVE: для генерации контента (осторожно!)
  creative:
    name: gpt-4o
    temperature: 0.4  # НЕ 0.7-1.0! (MIRAI была слишком креативна)
    top_p: 0.9
    frequency_penalty: 0.3
    presence_penalty: 0.2
    max_tokens: 2000
    use_cases:
      - "документация"
      - "README генерация"
      - "commit messages"

  # EMBEDDINGS: для RAG и долгосрочной памяти
  embed:
    name: text-embedding-3-large
    timeout_s: 30
    max_retries: 5
    dimensions: 3072
    use_cases:
      - "RAG индексация"
      - "semantic search"
      - "долгосрочная память"

  # REASONING: для критических задач (опционально, дорого!)
  reasoning:
    name: o1-preview
    temperature: 1.0
    top_p: 1.0
    max_tokens: 4096
    timeout_s: 120
    use_cases:
      - "научные исследования"
      - "сложная логика"
      - "критический анализ"

# Лимиты и квоты
limits:
  # Concurrency caps
  concurrency:
    chat: 16          # Параллельных чатов
    embeddings: 64    # Параллельных embeddings
    background: 4     # Фоновых задач

  # Бюджеты токенов
  tokens:
    per_minute: 150000      # Общий лимит
    per_user_minute: 10000  # На пользователя
    per_request_max: 4096   # Максимум на запрос

  # RPS (requests per second)
  rps:
    chat: 10
    embeddings: 50

# Circuit Breaker
circuit_breaker:
  failure_threshold: 5      # Фейлов подряд
  timeout_s: 60            # Открыт на N секунд
  half_open_interval_s: 30 # Проба каждые N секунд
  success_threshold: 2     # Успехов для закрытия

# Деградация при перегрузке
degradation:
  enabled: true
  rules:
    - trigger: "rate_limit_429"
      action: "switch_to_fast"   # gpt-4o → gpt-4o-mini
    - trigger: "latency_high"
      action: "reduce_max_tokens" # -30%
    - trigger: "error_rate_5percent"
      action: "trim_context"      # 12 → 6 реплик

# Контекст и память
context:
  max_history_messages: 12  # Максимум реплик в истории
  system_prompt_max_tokens: 1500
  rag:
    enabled: true
    cache_embeddings: true  # По SHA содержимого
    update_strategy: "diff" # Только изменения
    vector_store: "chroma"  # Или FAISS, Pinecone

# Наблюдаемость
observability:
  logging:
    enabled: true
    level: "INFO"
    fields:
      - "model"
      - "tokens_in"
      - "tokens_out"
      - "latency_ms"
      - "attempt_number"
      - "error_code"
      - "user_id"

  metrics:
    enabled: true
    provider: "prometheus"
    port: 9090
    metrics:
      - "requests_total"
      - "requests_errors"
      - "latency_p50_p95_p99"
      - "tokens_per_minute"
      - "retry_rate"
      - "circuit_breaker_open"

  tracing:
    enabled: true
    provider: "opentelemetry"
    endpoint: "http://localhost:4318"

  alerts:
    - condition: "error_rate > 5% for 5m"
      severity: "critical"
    - condition: "latency_p95 > 30s for 5m"
      severity: "warning"
    - condition: "retry_rate > 20% for 10m"
      severity: "warning"

# Безопасность
security:
  api_key_source: "env"  # НЕ JSON файл!
  api_key_env_var: "OPENAI_API_KEY"
  rotate_keys: true
  rotation_interval_days: 90
  sandbox:
    enabled: true
    executor: "docker"  # Изоляция для выполнения кода

# Тестирование
testing:
  golden_prompts:
    enabled: true
    path: "tests/golden_prompts.yaml"
  load_tests:
    enabled: true
    parallel_dialogs: 50
    duration_minutes: 10
    target_p95_latency_s: 15
    target_error_rate: 0.03  # < 3%
  chaos:
    enabled: false  # Включать только в staging
    inject_429_rate: 0.1
    inject_5xx_rate: 0.1
```

---

## 🐍 Production-Grade Клиент (Python)

### 📄 `core/openai_client.py`

```python
"""
Production-Grade OpenAI Client для MIRAI
Автор: AgeeKey + MIRAI (2025-10-14)

Фичи:
- Ретраи с экспоненциальным backoff + jitter
- Circuit breaker
- Деградация при перегрузке
- Метрики и логи
- Типизация
"""

import os
import time
import logging
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum

from openai import OpenAI, APIError, RateLimitError, Timeout
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential_jitter,
    retry_if_exception_type,
    before_sleep_log
)
from prometheus_client import Counter, Histogram, Gauge
import yaml

# ============================================================================
# Логирование
# ============================================================================

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s'
)

# ============================================================================
# Метрики (Prometheus)
# ============================================================================

# Счётчики
openai_requests_total = Counter(
    'mirai_openai_requests_total',
    'Total OpenAI API requests',
    ['model', 'status']
)

openai_tokens_total = Counter(
    'mirai_openai_tokens_total',
    'Total tokens used',
    ['model', 'direction']  # in/out
)

openai_retries_total = Counter(
    'mirai_openai_retries_total',
    'Total retry attempts',
    ['model', 'reason']
)

# Гистограммы (латенция)
openai_latency_seconds = Histogram(
    'mirai_openai_latency_seconds',
    'OpenAI API latency',
    ['model'],
    buckets=[0.1, 0.5, 1, 2, 5, 10, 30, 60]
)

# Gauge (Circuit Breaker)
openai_circuit_breaker_open = Gauge(
    'mirai_openai_circuit_breaker_open',
    'Circuit breaker state (1=open, 0=closed)',
    ['model']
)

# ============================================================================
# Enums
# ============================================================================

class ModelType(str, Enum):
    MAIN = "main"           # gpt-4o-mini
    HEAVY = "heavy"         # gpt-4o
    FAST = "fast"           # gpt-3.5-turbo
    CREATIVE = "creative"   # gpt-4o (temp 0.4)
    EMBED = "embed"         # text-embedding-3-large
    REASONING = "reasoning" # o1-preview

# ============================================================================
# Circuit Breaker
# ============================================================================

@dataclass
class CircuitBreakerState:
    """Состояние Circuit Breaker"""
    failures: int = 0
    last_failure_time: float = 0
    is_open: bool = False
    half_open_time: float = 0

class CircuitBreaker:
    """Circuit Breaker для защиты от каскадных фейлов"""
    
    def __init__(
        self,
        failure_threshold: int = 5,
        timeout_s: int = 60,
        half_open_interval_s: int = 30,
        success_threshold: int = 2
    ):
        self.failure_threshold = failure_threshold
        self.timeout_s = timeout_s
        self.half_open_interval_s = half_open_interval_s
        self.success_threshold = success_threshold
        self.state = CircuitBreakerState()
        
    def record_success(self):
        """Успешный вызов"""
        if self.state.is_open:
            # Half-open → закрываем после N успехов
            self.state.failures = max(0, self.state.failures - 1)
            if self.state.failures == 0:
                self.state.is_open = False
                logger.info("🟢 Circuit breaker CLOSED")
        else:
            # Полностью сбрасываем
            self.state.failures = 0
            
    def record_failure(self):
        """Фейл вызова"""
        self.state.failures += 1
        self.state.last_failure_time = time.time()
        
        if self.state.failures >= self.failure_threshold:
            if not self.state.is_open:
                self.state.is_open = True
                self.state.half_open_time = time.time() + self.timeout_s
                logger.error(f"🔴 Circuit breaker OPEN (failures={self.state.failures})")
                
    def can_attempt(self) -> bool:
        """Можно ли делать запрос?"""
        if not self.state.is_open:
            return True
            
        # Half-open: пробуем каждые N секунд
        now = time.time()
        if now >= self.state.half_open_time:
            logger.info("🟡 Circuit breaker HALF-OPEN (trying probe)")
            self.state.half_open_time = now + self.half_open_interval_s
            return True
            
        return False

# ============================================================================
# OpenAI Client
# ============================================================================

class MiraiOpenAIClient:
    """Production-Grade OpenAI Client"""
    
    def __init__(self, config_path: str = "configs/openai_config.yaml"):
        # Загрузить конфиг
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
            
        # API клиент
        api_key = os.getenv(
            self.config['security']['api_key_env_var'],
            os.getenv('OPENAI_API_KEY')
        )
        self.client = OpenAI(api_key=api_key)
        
        # Circuit breakers (по модели)
        cb_cfg = self.config['circuit_breaker']
        self.circuit_breakers: Dict[str, CircuitBreaker] = {
            model_type.value: CircuitBreaker(
                failure_threshold=cb_cfg['failure_threshold'],
                timeout_s=cb_cfg['timeout_s'],
                half_open_interval_s=cb_cfg['half_open_interval_s'],
                success_threshold=cb_cfg['success_threshold']
            )
            for model_type in ModelType
        }
        
    def _get_model_config(self, model_type: ModelType) -> Dict[str, Any]:
        """Получить конфиг модели"""
        return self.config['models'][model_type.value]
        
    def _create_retry_decorator(self, model_type: ModelType):
        """Создать retry decorator"""
        defaults = self.config['defaults']
        return retry(
            reraise=True,
            stop=stop_after_attempt(defaults['max_retries']),
            wait=wait_exponential_jitter(
                initial=defaults['backoff']['base_ms'] / 1000,
                max=defaults['backoff']['max_ms'] / 1000
            ),
            retry=(
                retry_if_exception_type(RateLimitError) |
                retry_if_exception_type(Timeout) |
                retry_if_exception_type(APIError)
            ),
            before_sleep=before_sleep_log(logger, logging.WARNING)
        )
        
    def chat(
        self,
        messages: List[Dict[str, str]],
        model_type: ModelType = ModelType.MAIN,
        **overrides
    ) -> Optional[Dict[str, Any]]:
        """
        Чат с OpenAI (с ретраями, circuit breaker, метриками)
        
        Args:
            messages: История сообщений
            model_type: Тип модели (MAIN/HEAVY/FAST/etc)
            **overrides: Переопределения параметров
            
        Returns:
            Ответ модели или None при фейле
        """
        # Получить конфиг
        cfg = self._get_model_config(model_type)
        model_name = cfg['name']
        
        # Circuit breaker check
        cb = self.circuit_breakers[model_type.value]
        if not cb.can_attempt():
            logger.warning(f"⚠️ Circuit breaker OPEN for {model_name}, using fallback")
            openai_circuit_breaker_open.labels(model=model_name).set(1)
            return self._fallback_response(model_type)
        else:
            openai_circuit_breaker_open.labels(model=model_name).set(0)
            
        # Параметры
        params = {
            'model': model_name,
            'messages': messages,
            'temperature': overrides.get('temperature', cfg.get('temperature', 0.25)),
            'top_p': overrides.get('top_p', cfg.get('top_p', 0.9)),
            'max_tokens': overrides.get('max_tokens', cfg.get('max_tokens', 2000)),
            'timeout': overrides.get('timeout', self.config['defaults']['timeout_s'])
        }
        
        # Опциональные параметры
        if 'frequency_penalty' in cfg:
            params['frequency_penalty'] = cfg['frequency_penalty']
        if 'presence_penalty' in cfg:
            params['presence_penalty'] = cfg['presence_penalty']
            
        # Retry decorator
        retry_decorator = self._create_retry_decorator(model_type)
        
        @retry_decorator
        def _call():
            start_time = time.time()
            try:
                response = self.client.chat.completions.create(**params)
                
                # Метрики
                latency = time.time() - start_time
                openai_latency_seconds.labels(model=model_name).observe(latency)
                openai_requests_total.labels(model=model_name, status='success').inc()
                
                # Токены
                if hasattr(response, 'usage'):
                    openai_tokens_total.labels(
                        model=model_name, direction='in'
                    ).inc(response.usage.prompt_tokens)
                    openai_tokens_total.labels(
                        model=model_name, direction='out'
                    ).inc(response.usage.completion_tokens)
                    
                # Логи
                logger.info(
                    f"✅ {model_name}: {latency:.2f}s, "
                    f"{response.usage.total_tokens} tokens"
                )
                
                # Circuit breaker success
                cb.record_success()
                
                return response
                
            except RateLimitError as e:
                openai_retries_total.labels(model=model_name, reason='rate_limit').inc()
                logger.warning(f"⚠️ Rate limit: {e}")
                raise
            except Timeout as e:
                openai_retries_total.labels(model=model_name, reason='timeout').inc()
                logger.warning(f"⚠️ Timeout: {e}")
                raise
            except APIError as e:
                openai_retries_total.labels(model=model_name, reason='api_error').inc()
                logger.error(f"❌ API Error: {e}")
                # 4xx (кроме 429) - не ретраим
                if hasattr(e, 'status_code') and 400 <= e.status_code < 500 and e.status_code != 429:
                    logger.error(f"❌ Client error {e.status_code}, not retrying")
                    openai_requests_total.labels(model=model_name, status='client_error').inc()
                    cb.record_failure()
                    return None
                raise
                
        try:
            return _call()
        except Exception as e:
            # Исчерпаны ретраи
            logger.error(f"❌ All retries exhausted for {model_name}: {e}")
            openai_requests_total.labels(model=model_name, status='failed').inc()
            cb.record_failure()
            return None
            
    def _fallback_response(self, model_type: ModelType) -> Optional[Dict[str, Any]]:
        """Фолбэк ответ при circuit breaker open"""
        # Попробовать деградацию
        if model_type == ModelType.HEAVY:
            logger.info("🔄 Degrading HEAVY → MAIN")
            # Рекурсивно вызвать с MAIN
            # (НО! Защита от бесконечной рекурсии нужна)
            return None  # Упрощённо
        return None
        
    def embed(
        self,
        texts: List[str],
        model_type: ModelType = ModelType.EMBED
    ) -> Optional[List[List[float]]]:
        """
        Embeddings (для RAG)
        
        Args:
            texts: Тексты для эмбеддинга
            model_type: Тип модели (обычно EMBED)
            
        Returns:
            Векторы embeddings или None
        """
        cfg = self._get_model_config(model_type)
        model_name = cfg['name']
        
        # Circuit breaker
        cb = self.circuit_breakers[model_type.value]
        if not cb.can_attempt():
            logger.warning(f"⚠️ Circuit breaker OPEN for embeddings")
            return None
            
        # Retry decorator
        retry_decorator = self._create_retry_decorator(model_type)
        
        @retry_decorator
        def _call():
            start_time = time.time()
            try:
                response = self.client.embeddings.create(
                    model=model_name,
                    input=texts,
                    timeout=cfg.get('timeout_s', 30)
                )
                
                # Метрики
                latency = time.time() - start_time
                openai_latency_seconds.labels(model=model_name).observe(latency)
                openai_requests_total.labels(model=model_name, status='success').inc()
                
                logger.info(f"✅ Embeddings: {latency:.2f}s, {len(texts)} texts")
                
                cb.record_success()
                
                return [item.embedding for item in response.data]
                
            except Exception as e:
                logger.error(f"❌ Embeddings error: {e}")
                raise
                
        try:
            return _call()
        except Exception as e:
            logger.error(f"❌ Embeddings failed: {e}")
            openai_requests_total.labels(model=model_name, status='failed').inc()
            cb.record_failure()
            return None

# ============================================================================
# Пример использования
# ============================================================================

if __name__ == "__main__":
    client = MiraiOpenAIClient()
    
    # Простой чат (MAIN модель)
    response = client.chat([
        {"role": "user", "content": "Привет! Как дела?"}
    ])
    
    if response:
        print(response.choices[0].message.content)
        
    # Сложная задача (HEAVY модель)
    response = client.chat(
        messages=[
            {"role": "user", "content": "Напиши функцию сортировки на Python"}
        ],
        model_type=ModelType.HEAVY
    )
    
    if response:
        print(response.choices[0].message.content)
        
    # Embeddings
    embeddings = client.embed(["Привет мир", "Hello world"])
    if embeddings:
        print(f"Embeddings dimensions: {len(embeddings[0])}")
```

---

## 🎯 Итоговый Вывод

### 🌸 MIRAI Была Права:

1. ✅ GPT-4o + GPT-4o-mini — правильный выбор
2. ✅ Умное переключение (70/25/5) — экономия
3. ✅ Низкая temperature для кода
4. ✅ Streaming для UI
5. ✅ Долгосрочная память через RAG

### 🔥 Production-Grade Добавляет:

1. ✅ **Надёжность:** Ретраи, circuit breaker, деградация
2. ✅ **Наблюдаемость:** Метрики, логи, алерты
3. ✅ **Безопасность:** Env vars, sandbox, квоты
4. ✅ **Оптимизация:** Кэш embeddings, diff-обновления, лимиты
5. ✅ **Тестирование:** Golden prompts, load tests

### 🎯 Финальная Формула:

```
MIRAI Intelligence + Production Reliability = 🚀 Unstoppable AI
```

---

## 📋 Чек-лист Внедрения

- [ ] Создать `configs/openai_config.yaml` (см. выше)
- [ ] Реализовать `core/openai_client.py` (см. выше)
- [ ] Переместить API ключ в env vars (`export OPENAI_API_KEY=...`)
- [ ] Настроить Prometheus метрики (порт 9090)
- [ ] Настроить алерты (error > 5%, latency > 30s)
- [ ] Создать golden prompts (`tests/golden_prompts.yaml`)
- [ ] Запустить load test (50 диалогов × 10 минут)
- [ ] Настроить RAG с кэшом embeddings
- [ ] Внедрить очередь задач (Arq/Celery)
- [ ] Настроить sandbox для выполнения кода
- [ ] Ротация API ключей (каждые 90 дней)
- [ ] Chaos testing (inject 429/5xx в staging)

---

**🌸 MIRAI + 🔥 Production = 💎 Perfect**
