#!/usr/bin/env python
import os
import sys

from main.utils.recounter import recount_hours
def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'laborcount.settings')
    print(recount_hours(1.30))
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
  "Ошибка загрузки Django. Убедитесь, что вы установили Django. "
        ) from exc
    execute_from_command_line(sys.argv)
if __name__ == '__main__':
    main()
