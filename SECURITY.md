# Security Policy for chestny-znak-flow-validator

## Supported Versions

We provide security fixes only for the latest minor release.

| Version   | Supported |
|----------|-----------|
| 1.2.x    | ✅        |
| 1.1.x    | ❌        |
| < 1.1.0  | ❌        |

If you use an unsupported version, please upgrade before reporting a vulnerability.

## Recent fixes

- Addressed code-scanning findings by upgrading to a safe `pypdf` release and hardening XML parsing with `defusedxml`.

## Reporting a Vulnerability

**Не создавайте публичных issue или pull request’ов с подробностями уязвимости.**

Для ответственного раскрытия используйте один из вариантов:

- Отправьте письмо на:  
- Или используйте GitHub → **Security → Report a vulnerability** (если включено private reporting).

В письме укажите: aleksandrranas@gmail.com

- краткое описание проблемы и возможное влияние;
- шаги для воспроизведения;
- версию библиотеки / бинарника и окружение.

Мы подтверждаем получение отчёта в течение **3 рабочих дней** и стараемся расследовать проблему в течение **7 рабочих дней**.

## Disclosure Policy

- Пока исправление не выпущено, детали уязвимости не публикуются.
- После выхода фикс-релиза мы можем опубликовать security advisory и, при необходимости, CVE.
- Если вы хотите быть указаны как discoverer, сообщите, под каким именем.
