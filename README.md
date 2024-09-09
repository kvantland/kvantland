# Квантландия

## Требования

* Git
* PostgreSQL
* Python 3
* Node.js
* Nuxt 2, установить командой `npm install nuxt` после установки Node.js из папки `client`
* Библиотеки Python из `requirements.txt`, устанавливать с помошью `python3 -m pip install <python_module>`
* Для версий Python без `tomllib` также требуется `tomli`

В зависимости от окружения, `psycopg` (из `requirements.txt`) может понадобится установить как `psycopg[binary,pool]`.

## Настройка

1. Запросить `config.toml` и `.env` файлы у одного из действующих разроботчиков 
2. В `config.toml` db.url указать URL БД (составляется по принципу `postgres://postgres:<password>@127.0.0.1:<port>/kvantland`)
3. Запустить `db/res.sh`

## Запуск

1. Запускать `server.py`. Лучше из консоли.
2. Запустить приложение из папки `client` с помощью команды `npm run dev`

## Для пользователей Windows

* Потребуется Cygwin для запуска .sh скриптов
* Для Cygwin нужны следующие пакеты:
```
* libpq
* gcc
* python3
* psql
```
* Для удобства рекомендуется добавить путь к Cygwin терминалу в PATH
* Библиотеки Python надо будет устанавливать как в Cygwin терминале, так и в обычном
* Если при попытке запуска .sh скрипта возникает ошибка, воспользуйтесь командой `sed -i 's/\r$//'reset.sh`

## Очень рекомендуется к использованию

* pgAdmin 4 для работы с бд
