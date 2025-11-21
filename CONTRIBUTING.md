# Contributing

## Workflow
1. Разрабатывайте по TDD: сначала тесты, затем код.
2. Перед PR запускайте `./scripts/lint.sh`, `./scripts/dev_run_all_tests.sh`, `./scripts/security_scan.sh`.
3. PR должен пройти Codex Code Review. Добавьте комментарий `@codex review` или настройте авто-проверку в Codex Cloud.
4. Исправьте замечания Codex перед merge.

## Настройка Codex Code Review
1. Настройте Codex Cloud и привяжите репозиторий `chestny-znak-flow-validator` в настройках.
2. Включите фичу **Code review** для репозитория.
3. В PR можно вызывать ревью вручную:
   - `@codex review`
   - `@codex review for security regressions`
4. Любой комментарий с `@codex` без `review` запустит облачный таск по контексту PR.
5. Все запросы через GitHub считаются usage в разделе Code Review. Лимиты Copilot не изменяются.

## Кодстайл
- Python 3.11+, избегайте try/except вокруг импортов.
- Используйте типы и простую структуру модулей (io_import, core, ai, cli, webapp).

Спасибо за вклад!
