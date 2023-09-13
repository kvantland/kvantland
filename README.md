# Квантландия

## Требования

* PostgreSQL
* Python 3
* Библиотеки Python из `requirements.txt`
* Для версий Python без `tomllib` также требуется `tomli`

В зависимости от окружения, `psycopg` (из `requirements.txt`) может понадобится установить как `psycopg[binary,pool]`.

## Настройка

1. Скопировать `config.example.toml` в `config.toml`.
2. В `config.toml` указать в keys.cookie любую случайную строку вместо `any random string` (лучше ограничиться латиницей).
3. В нём же в db.url указать URL БД.
4. В БД по этому адресу выполнить `alter database <имя-базы> set search_path to "Квантландия", public;`
5. Запустить `db/reset.sh` с адресом БД в качестве аргумента.

## Запуск

Запускать `server.py`. Лучше из консоли.
