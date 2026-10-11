import flet as ft


def main(page: ft.Page):
    page.title = 'Первое приложение'
    page.add(ft.Text('Привет, мобильная разработка!', size=28))

    
ft.run(main)