"""Homework scaffold — postgresql lesson `l3_observability` (Vibe Learn).

Задача: нагрузочные сценарии, custom-метрики postgres_exporter, Grafana JSON и Prometheus alerts.

Реализуй функции ниже — сигнатуры и тестовая поверхность фиксированы;
CI (.github/workflows/ci.yml) ставит зависимости и гоняет `pytest`.
Подробности и критерии приёмки — в README.md.

Драйвер: psycopg (v3). DSN берётся из env DATABASE_URL.
"""

import os

import psycopg


def database_url() -> str:
    """DSN PostgreSQL из env. Дефолт совпадает с docker-compose.yml."""
    return os.environ.get(
        "DATABASE_URL",
        "postgresql://postgres:postgres@localhost:5432/postgres",
    )


def connect() -> "psycopg.Connection":
    """Открыть соединение psycopg из DATABASE_URL."""
    return psycopg.connect(database_url())


# ----- TODO #1: dead_tup_ratio -----
def dead_tup_ratio(conn) -> list[dict]:
    """SELECT relname, n_dead_tup, n_live_tup из pg_stat_user_tables → ratio мёртвых строк"""
    raise NotImplementedError("dead_tup_ratio: реализуй меня")


# ----- TODO #2: blocking_pids -----
def blocking_pids(conn) -> int:
    """SELECT count(*) FROM pg_stat_activity WHERE cardinality(pg_blocking_pids(pid)) > 0"""
    raise NotImplementedError("blocking_pids: реализуй меня")


# ----- TODO #3: validate_dashboard -----
def validate_dashboard(path: str) -> bool:
    """чистая функция: прочитать Grafana dashboard JSON и проверить, что это валидный JSON с panels"""
    raise NotImplementedError("validate_dashboard: реализуй меня")



def main() -> None:
    """Точка входа: подключиться и напомнить, что реализовать.

    Замени тело на демонстрацию реализованных функций.
    """
    print("Vibe Learn — postgresql lesson scaffold up")
    print(f"DATABASE_URL: {database_url()}")
    print("Реализуй TODO-функции, затем `pytest`. README.md содержит задачу.")


if __name__ == "__main__":
    main()
