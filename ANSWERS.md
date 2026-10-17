# Домашнее задание 31-32: Параметризация, маркировка и отчётность

## Часть F. Ответы на вопросы

### 1. Команды запуска и итоговые строки вывода

**Весь проект:**
```bash
pytest -v
Вывод: 30 passed, 1 skipped, 1 xfailed (числа могут незначительно отличаться в зависимости от версии pytest, но skipped и xfailed должны быть по 1).
Только smoke:
bash
1
Вывод: 11 passed, 20 deselected. (deselected, потому что тесты без маркера smoke или с другими маркерами игнорируются).
Regression, но без permissions:
bash
1
Вывод: 18 passed, 1 skipped, 12 deselected.
Только permissions с выводом причин xfail:
bash
1
Вывод: 12 passed, 1 xfailed, 24 deselected. Флаг -r x добавляет блок XFAIL tests/booking/test_permissions.py::test_permissions_matrix[guest-list_bookings-bug] с указанием причины из reason.
2. Объяснение чисел selected/deselected и skipped
deselected: тесты, которые не попали в выборку из-за фильтра -m.
skipped: тест test_pay_booking_when_enabled, потому что FEATURES["online_payment"] == False. Условие skipif сработало на этапе сбора тестов.
xfailed: тест guest-list_bookings-bug, потому что мы явно пометили его xfail(strict=True) из-за известного бага в коде.
3. Сколько кейсов дал тест из шага 5 и почему?
Тест test_create_booking_all_rooms_and_hours дал 9 кейсов.
Почему: используется стек из двух декораторов @pytest.mark.parametrize. Первый даёт 3 значения (small, medium, large), второй даёт 3 значения (1, 4, 8). Pytest перемножает их (декартово произведение): 3 × 3 = 9 комбинаций.
4. Команда запуска по node id
bash
1
Вывод: 1 passed. Node id берётся в кавычки, так как содержит квадратные скобки.
5. Команда с -k для кейсов про количество людей
bash
1
Вывод: Запустятся только те тесты из test_booking_boundary_cases, в имени которых (в id) есть слово people (например, people-zero, people-one). Остальные будут deselected.
6. Команда генерации HTML-отчёта
bash
1
7. Баг-репорт BUG-1
Шаги: Создать клиент с ролью guest. Вызвать метод list_bookings().
Ожидаемый результат (по таблице прав): Статус 403 Forbidden.
Фактический результат: Статус 200 OK и пустой список, так как в коде list_bookings проверяется только if self.role == "user", а роль guest пропускается дальше.
8. Эксперимент со strict=True
Если временно исправить баг в app/booking.py (добавить if self.role in ("guest", "user"):), тест guest-list_bookings-bug начнёт проходить (возвращать 403).
При запуске pytest выдаст: 1 xpassed, 1 warning. Прогон станет красным (ошибка), потому что strict=True означает: "если тест, помеченный как xfail, вдруг прошёл (XPASS), считай это ошибкой".
Что делать: удалить маркер xfail из этого кейса, так как баг исправлен.
9. Эксперимент с опечаткой в маркере
Если добавить @pytest.mark.smok (без e), при запуске с --strict-markers pytest выдаст ошибку:
PytestUnknownMarkWarning: Unknown pytest.mark.smok.
Без --strict-markers: pytest просто вывел бы предупреждение (warning), но продолжил бы выполнение тестов, что опасно, так как можно случайно опечататься и потерять покрытие.
10. Как в HTML-отчёте показаны xfailed и skipped?
В таблице результатов тесты со статусом Skipped и XFailed выделены серым и жёлтым цветами соответственно. При разворачивании строки теста (нажав на стрелочку) в блоке Setup или Call виден текст причины (например, reason: BUG-1: list_bookings не проверяет роль guest... или skipif: Онлайн-оплата выключена).
12345678910
(Должно быть ~30 passed, 1 skipped, 1 xfailed. Ни одного FAILED или ERROR!)