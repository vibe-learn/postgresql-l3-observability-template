        # postgresql — Observability: pg_stat_*, locks, autovacuum, bloat

        Homework-шаблон для урока **l3_observability** (Observability: pg_stat_*, locks, autovacuum, bloat) на платформе Vibe Learn.

        ## Что делать

        Дано: testcontainers PG + Prometheus + Grafana в docker-compose. Реализуй:
1) Скрипт-нагрузку: генерирует разные сценарии (нормальная нагрузка, long-running
   transaction, deadlock, write-heavy bloat, slow query).
2) Конфиг postgres_exporter с custom queries (pg_stat_user_tables.dead_tup_ratio,
   pg_blocking_pids count, long-running queries count).
3) Grafana dashboard JSON с базовыми панелями.
4) Prometheus alert rules для всех red flags.
Тесты в template проверят, что под нагрузкой алерты срабатывают корректно, что метрики
собираются, и что dashboard валидный JSON.

## Контекст (из transfer-задачи урока)

Тебя позвали в стартап спроектировать observability для PG. У них:
- Один primary + один async standby; 200 ГБ; 500 QPS пик.
- Stack: Prometheus + Grafana уже есть, postgres_exporter не настроен.
- Никакого мониторинга PG-специфики — следят только за CPU/RAM/disk через node_exporter.
- В последний месяц было два инцидента: один раз база зависла на 20 минут (никто не
  знал что), второй раз — резкое снижение throughput, поняли только когда клиенты
  пожаловались.

**Вопрос:** распиши обязательный минимум observability для этой системы. Что
мониторишь, какие алерты ставишь и с какими порогами. Какой первый дашборд в Grafana?
Что в логах? Опиши процесс реакции на типовой инцидент «база медленная».

## Recap из урока

- **pg_stat_activity — первая view в любом инциденте.** Покажет long-running queries, idle in transaction, wait events.
- **`idle in transaction` > 1 минуты — leaked transaction.** Держит snapshot, мешает VACUUM, ведёт к bloat. Лечится `idle_in_transaction_session_timeout`.
- **Cache hit ratio < 99% — флаг.** Либо мало shared_buffers, либо плохие планы. Считается через blks_hit/(blks_hit+blks_read).
- **Per-table autovacuum tuning** — главный инструмент против bloat на write-heavy таблицах. Дефолт 20% слишком слабый.
- **postgres_exporter + Grafana + alerts** — must-have. Не пиши свои дашборды с нуля, есть готовые наборы метрик.

        ## Как работать

        1. Платформа Vibe Learn создаёт копию этого репо в твоём GitHub-аккаунте по клику «Начать домашку» на странице урока (через GitHub `/generate`, codecrafters-pattern).
        2. Склонируй копию локально, реализуй TODO в `main.py`, прогони тесты, запушь.
        3. CI (`.github/workflows/ci.yml`) ставит зависимости и запускает `pytest` на каждый push. Платформа слушает результат через webhook от GitHub Actions и обновляет статус домашки на странице урока.

        ## Локальное окружение

        - Python 3.12+
        - Docker + docker-compose — `docker compose up -d` поднимает single-node PostgreSQL 16 на `localhost:5432` с healthcheck. DSN: `postgresql://postgres:postgres@localhost:5432/postgres`. Переопределяется через env `DATABASE_URL`.

        ## Запуск

        ```bash
        # Поднять локальный PostgreSQL
        docker compose up -d

        # Установить зависимости
        pip install -r requirements.txt

        # Прогнать тесты (интеграционный включается через PG_INTEGRATION=1)
        pytest
        PG_INTEGRATION=1 pytest

        # Запустить main (печатает marker; замени stub на реализацию)
        python main.py
        ```

        ## Заметка автора

        Это baseline-шаблон, сгенерированный платформой. Бизнес-сущность задачи (что конкретно реализовать в `main.py`, какие тесты сделать строгими) расширяется по ходу итераций — параллельно с углублением теории урока.
