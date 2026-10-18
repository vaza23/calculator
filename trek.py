import flet as ft

async def main(page: ft.Page):
    page.title = "Habit Tracker"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    prefs = ft.SharedPreferences()

    # -----------------------------
    # ЗАГРУЗКА ДАННЫХ
    # -----------------------------
    saved_days = await prefs.get("habit_tracker.days")
    if saved_days is None or not isinstance(saved_days, int):
        saved_days = 0

    saved_name = await prefs.get("habit_tracker.name")
    if saved_name is None:
        saved_name = ""

    state = {
        "days": saved_days,
        "goal": 31,
    }

    habit_input = ft.TextField(
        label="Название привычки",
        value=saved_name,
        width=320,
    )

    days_text = ft.Text(
        f'{state["days"]} / {state["goal"]}',
        size=42,
        weight=ft.FontWeight.BOLD,
    )

    counter_circle = ft.Container(
        width=320,
        height=320,
        content=days_text,
        alignment=ft.Alignment.CENTER,
        border_radius=70,
        border=ft.Border.all(width=4),
        # Цвет будет установлен сразу при запуске
    )

    def get_color_by_progress(days: int, goal: int) -> str:
        """Вычисляет цвет круга по прогрессу."""
        if goal == 0:
            return "#e0e0e0"
        progress = days / goal
        if progress == 0:
            return "#FF0000"          # Красный: ещё не начал
        elif progress < 0.5:
            return "#ffeb3b"          # Жёлтый: середина пути
        elif progress < 1:
            return "#4caf50"          # Зелёный: почти цель
        else:
            return "#f706c3"          # Синий: цель достигнута (исправленный HEX)

    def update_display():
        """Обновляет текст и цвет круга."""
        days_text.value = f'{state["days"]} / {state["goal"]}'
        counter_circle.bgcolor = get_color_by_progress(state["days"], state["goal"])
        page.update()

    # Сразу устанавливаем цвет при старте (на случай, если days уже был сохранён)
    update_display()

    async def save_name(e):
        name = (habit_input.value or "").strip()
        if not name:
            return
        await prefs.set("habit_tracker.name", name)

    habit_input.on_blur = save_name

    async def add_day(e):
        if state["days"] < state["goal"]:
            state["days"] += 1
            await prefs.set("habit_tracker.days", state["days"])
            update_display()

    async def add_dayz(e):
            if state["days"] < state["goal"]:
                state["days"] -=1
                await prefs.set("habit_tracker.days", state["days"])
                update_display()

    async def reset_days(e):
        state["days"] = 0
        await prefs.set("habit_tracker.days", 0)
        update_display()

    page.add(
        ft.Column(
            controls=[
                habit_input,
                ft.Container(height=30),
                counter_circle,
                ft.Container(height=30),
                ft.Row(
                    controls=[
                        ft.Button(content="+1 день", on_click=add_day),
                        ft.Button(content="Сбросить", on_click=reset_days),
                        ft.Button(content="-1 дней", on_click=add_dayz)
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20,
        )
    )

ft.run(main)
