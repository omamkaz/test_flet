#!/usr/bin/python3
# -*- coding: utf-8 -*-

import flet as ft
from typing import Callable, Sequence
from ...constant import THEME_COLORS, ThemeController


class ThemeColorButtonGroup(ft.Row):
    def __init__(self,
                 value: str,
                 colors: Sequence[str],
                 on_change: Callable):
        super().__init__()

        self.scroll = ft.ScrollMode.HIDDEN
        self.alignment = ft.MainAxisAlignment.CENTER

        self.on_change = on_change
        self.controls = [
            ft.Container(
                key=color,
                width=38,
                height=38,
                bgcolor=color,
                on_click=self._on_click,
                shape=ft.BoxShape.CIRCLE,
                border=None if color != value else ft.border.all(3, value + "100")
            )
            for color in colors
        ]

    def select_color(self, color: str) -> None:
        for i, c in enumerate(self.controls):
            if i <= len(self.controls) - 1:
                c.border = None if c.key != color else ft.border.all(3, c.bgcolor + "100")
            else:
                c.border = ft.border.all(3, ft.colors.BLACK12)
        self.update()

    def _on_click(self, e: ft.ControlEvent) -> None:
        self.select_color(e.control.key)
        self.on_change(e.control.key)


class ThemeModeButtonGroup(ft.Row):
    def __init__(self,
                 value: str,
                 on_change: Callable):
        super().__init__()

        self.on_change = on_change
        self.alignment = ft.MainAxisAlignment.SPACE_AROUND
        self.vertical_alignment = ft.CrossAxisAlignment.CENTER

        self.controls = [
            ft.Container(
                key=name,
                padding=5,
                tooltip=tooltip,
                border_radius=18,
                on_click=self._on_click,
                alignment=ft.alignment.center,
                border=None if name != value else ft.border.all(2),
                content=ft.Column(
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Icon(
                            name=icon,
                            size=64
                        ),
                        ft.Text(
                            value=tooltip,
                            text_align="center",
                            size=12,
                            rtl=True,
                            weight=ft.FontWeight.BOLD
                        )
                    ]
                )
            )
            for icon, name, tooltip in zip(
                [ft.icons.BRIGHTNESS_MEDIUM, ft.icons.DARK_MODE, ft.icons.LIGHT_MODE], 
                ["system", "dark", "light"], 
                ["الوضع الافتراضي", "الوضع الليلي", "الوضع النهاري"])
        ]

    def select_mode(self, mode: str) -> None:
        for c in self.controls:
            c.border = None if c.key != mode else ft.border.all(2)
        self.update()

    def _on_click(self, e: ft.ControlEvent) -> None:
        self.select_mode(e.control.key)
        self.on_change(e.control.key)


class ThemeDialog(ft.BottomSheet):
    def __init__(self, page: ft.Page):
        super().__init__(ft.Control)
        
        self.page = page
        self.enable_drag = True
        self.show_drag_handle = True

        self.content = ft.SafeArea(
            expand=True,
            minimum_padding=ft.padding.only(left=5, right=5),
            content=ft.Column(
                alignment=ft.MainAxisAlignment.SPACE_AROUND,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ThemeModeButtonGroup(
                        value=ThemeController.get_theme_mode(self.page),
                        on_change=lambda mode: ThemeController.toggle_theme_mode(mode, self.page)
                    ),
                    ft.Container(
                        margin=ft.margin.only(left=25, right=25),
                        content=ThemeColorButtonGroup(
                            value=ThemeController.get_theme_color(self.page),
                            colors=THEME_COLORS,
                            on_change=lambda color: ThemeController.set_theme_color(color, self.page)
                        )
                    )
                ]
            )
        )