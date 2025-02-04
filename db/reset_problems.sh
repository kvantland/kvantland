#!/bin/bash

# Функция для вывода справки
usage() {
    echo "Использование: $0 [--users | -u] <user1,user2,...> [--problems | -p] <problem1,problem2,...>"
    echo "Пример: $0 --users user1 user2 user3 --problems problem1 problem2"
    echo "Или: $0 -u user1 user2 -p problem1 problem2 problem3"
    exit 1
}

# Получаем путь к директории, где находится скрипт
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Парсинг аргументов
users=()
problems=()
current_arg=""

while [[ $# -gt 0 ]]; do
    case "$1" in
        --users | -u)
            current_arg="users"
            shift
            ;;
        --problems | -p)
            current_arg="problems"
            shift
            ;;
        --help | -h)
            usage
            ;;
        *)
            if [ "$current_arg" == "users" ]; then
                users+=("$1")
            elif [ "$current_arg" == "problems" ]; then
                problems+=("$1")
            else
                echo "Ошибка: неизвестный параметр или аргумент: $1"
                usage
            fi
            shift
            ;;
    esac
done

# Проверка, что оба параметра переданы
if [ ${#users[@]} -eq 0 ] || [ ${#problems[@]} -eq 0 ]; then
    echo "Ошибка: не указаны обязательные параметры."
    usage
fi

# Преобразование массивов в строки с разделителем ","
users_str=$(IFS=,; echo "${users[*]}")
problems_str=$(IFS=,; echo "${problems[*]}")

# Вызов Python-скрипта с передачей аргументов и захватом возвращаемого кода
python3 - <<END
import sys
import os

# Добавляем директорию скрипта в sys.path
script_dir = os.path.dirname(os.path.abspath(__file__))
base_dir = os.path.dirname(script_dir)
sys.path.append(script_dir)
sys.path.append(base_dir)

from config import config
from reset_problems import resetProblemsForUsers

# Преобразование строк в списки
users_list = "$users_str".split(',')
problems_list = "$problems_str".split(',')
db = config['db']['url']

# Вызов функции с переданными аргументами
result = resetProblemsForUsers(users_list, problems_list, db)

# Возвращаем результат в Bash
sys.exit(result)
END