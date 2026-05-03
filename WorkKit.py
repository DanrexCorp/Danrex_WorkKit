# main.py - Danrex WorkKit v2.0 - Beautiful Edition
# Fixes: white theme text colors, language switching, all disks, speed test, animations

import customtkinter as ctk
from tkinter import messagebox, filedialog
import tkinter as tk
import os
import sys
import json
import datetime
import threading
import time
import subprocess
import psutil
import socket

try:
    import winsound
    WINDOWS = True
except ImportError:
    WINDOWS = False

try:
    import pyperclip
    HAS_CLIPBOARD = True
except:
    HAS_CLIPBOARD = False

try:
    from plyer import notification
    HAS_NOTIFY = True
except:
    HAS_NOTIFY = False

try:
    import keyboard
    HAS_KEYBOARD = True
except:
    HAS_KEYBOARD = False

try:
    import winreg
    HAS_WINREG = True
except:
    HAS_WINREG = False

try:
    import requests
    HAS_REQUESTS = True
except:
    HAS_REQUESTS = False

# ── Colour Palette ──────────────────────────────────────────────────────────
DARK = {
    "bg":          "#0d0f14",
    "surface":     "#141720",
    "surface2":    "#1c2030",
    "card":        "#1e2235",
    "border":      "#2a3050",
    "accent":      "#4f8ef7",
    "accent2":     "#7c5cbf",
    "accent3":     "#22d3a8",
    "danger":      "#f05a5a",
    "warning":     "#f5a623",
    "text":        "#e8eaf6",
    "text2":       "#8b93b5",
    "text3":       "#5a6285",
    "nav_active":  "#252d48",
    "hover":       "#2a3358",
}

LIGHT = {
    "bg":          "#f0f4ff",
    "surface":     "#ffffff",
    "surface2":    "#f5f7ff",
    "card":        "#ffffff",
    "border":      "#d0d8f0",
    "accent":      "#3d6ef5",
    "accent2":     "#6b44b5",
    "accent3":     "#12b896",
    "danger":      "#e04444",
    "warning":     "#e59515",
    "text":        "#1a1f3c",
    "text2":       "#4a5280",
    "text3":       "#8a94b8",
    "nav_active":  "#e8eeff",
    "hover":       "#dde5ff",
}

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

TRANSLATIONS = {
    "ru": {
        "app_name": "Danrex WorkKit",
        "ready": "Готов к работе",
        "cpu": "CPU",
        "ram": "RAM",
        "disk": "Диски",
        "gb_free": "ГБ своб.",
        "gb_total": "ГБ всего",
        "quick_actions": "Быстрые действия",
        "pomodoro": "🍅 Pomodoro",
        "notes": "📝 Заметки",
        "cleaner": "🧹 Очистка",
        "screenshot": "📸 Скриншот",
        "work_min": "Работа (мин):",
        "break_min": "Отдых (мин):",
        "start": "▶  Старт",
        "pause": "⏸  Пауза",
        "reset": "↺  Сброс",
        "today_sessions": "Сегодня",
        "total_sessions": "Всего",
        "new_note": "+  Новая заметка",
        "search": "Поиск...",
        "save": "Сохранить",
        "delete": "Удалить",
        "clipboard_history": "История буфера обмена",
        "clear_history": "Очистить историю",
        "copy": "Копировать",
        "reminder": "🔔 Напоминания",
        "reminder_text": "Текст напоминания",
        "datetime_format": "ГГГГ-ММ-ДД ЧЧ:ММ",
        "add": "Добавить",
        "open": "Открыть",
        "shorten_url": "🔗 Сокращение ссылок",
        "enter_url": "Введите URL...",
        "shorten": "Сократить и скопировать",
        "short_url": "Короткая ссылка",
        "speed_test": "⚡ Скорость сети",
        "start_test": "Начать тест",
        "testing": "Тестирование...",
        "whois": "🔍 Whois",
        "domain": "Введите домен (example.com)",
        "get_info": "Получить",
        "ip_info": "🌐 IP информация",
        "get_ip": "Получить IP",
        "external_ip": "Внешний IP:",
        "local_ip": "Локальный IP:",
        "host": "Хост:",
        "port_check": "🔒 Проверка портов",
        "host_label": "Хост",
        "port_label": "Порт",
        "check_port": "Проверить",
        "port_open": "ОТКРЫТ ✅",
        "port_closed": "ЗАКРЫТ ❌",
        "ping_trace": "📊 Пинг / Трассировка",
        "ping": "Ping",
        "tracert": "Трассировка",
        "installed_programs": "📦 Программы",
        "search_programs": "Поиск программ...",
        "find": "Найти",
        "uninstall": "Удалить",
        "big_files": "🔍 Большие файлы",
        "select_folder": "Выберите папку...",
        "browse": "Обзор",
        "start_search": "Начать поиск",
        "wipe": "🗑️ Безвозвратное удаление",
        "warning_wipe": "⚠️  Удалённые файлы НЕЛЬЗЯ восстановить!",
        "wipe_button": "Безвозвратно удалить",
        "associations": "🛡️ Ассоциации файлов",
        "restore_assoc": "Восстановить",
        "windows_theme": "🌙 Тема Windows",
        "dark_theme": "🌙  Тёмная тема",
        "light_theme": "☀️  Светлая тема",
        "system_clean": "🧹 Очистка системы",
        "home": "🏠 Главная",
        "network": "🌐 Сеть",
        "startup": "⚡ Автозагрузка",
        "monitor": "📊 Монитор",
        "programs": "📦 Программы",
        "big_files_nav": "🔍 Большие файлы",
        "wipe_nav": "🗑️ Удаление",
        "assoc_nav": "🛡️ Ассоциации",
        "win_theme": "🌙 Тема Windows",
        "screenshots": "📸 Скриншоты",
        "buffer": "📋 Буфер",
        "settings": "⚙️  Настройки",
        "theme": "🌓  Тема",
        "greeting_morning": "Доброе утро",
        "greeting_day": "Добрый день",
        "greeting_evening": "Добрый вечер",
        "system_overview": "Обзор системы",
        "work_stage": "Работа",
        "break_stage": "Отдых",
        "clean_start": "Начать очистку",
        "autostart_label": "Запускать при старте Windows",
        "disable": "Отключить",
        "confirm_delete": "Удалить файл без возможности восстановления?",
        "confirm_uninstall": "Запустить удаление программы?",
        "confirm_clean": "Очистить все временные файлы?",
        "success": "Успех",
        "error": "Ошибка",
        "note_saved": "Заметка сохранена",
        "note_deleted": "Заметка удалена",
        "confirm_note_delete": "Удалить заметку?",
        "confirm_clear_clipboard": "Очистить всю историю?",
        "reminder_added": "Напоминание добавлено",
        "bad_date_format": "Неверный формат даты (ГГГГ-ММ-ДД ЧЧ:ММ)",
        "new_note_title": "Новая заметка",
        "hint_screenshot": "Нажмите Win+Shift+S для создания скриншота",
        "hint_hotkeys": "Ctrl+Shift+N — быстрая заметка",
        "no_screenshots": "Нет скриншотов",
        "files_deleted": "файлов удалено",
        "deleted": "Файл удалён",
        "added_to_autostart": "Добавлено в автозагрузку",
        "removed_from_autostart": "Удалено из автозагрузки",
        "language_label": "Язык / Language",
        "app_theme_label": "Тема приложения",
        "autostart_settings": "Автозагрузка",
        "save_settings": "Сохранить",
        "settings_saved": "Настройки сохранены. Перезапустите раздел.",
        "mbps_down": "Загрузка",
        "mbps_up": "Отдача",
        "ms_ping": "Пинг",
        "speed_error": "Не удалось провести тест. Установите: pip install speedtest-cli",
        "url_shortened": "Ссылка скопирована",
        "url_error": "Ошибка сокращения",
    },
    "en": {
        "app_name": "Danrex WorkKit",
        "ready": "Ready to work",
        "cpu": "CPU",
        "ram": "RAM",
        "disk": "Drives",
        "gb_free": "GB free",
        "gb_total": "GB total",
        "quick_actions": "Quick Actions",
        "pomodoro": "🍅 Pomodoro",
        "notes": "📝 Notes",
        "cleaner": "🧹 Cleaner",
        "screenshot": "📸 Screenshot",
        "work_min": "Work (min):",
        "break_min": "Break (min):",
        "start": "▶  Start",
        "pause": "⏸  Pause",
        "reset": "↺  Reset",
        "today_sessions": "Today",
        "total_sessions": "Total",
        "new_note": "+  New Note",
        "search": "Search...",
        "save": "Save",
        "delete": "Delete",
        "clipboard_history": "Clipboard History",
        "clear_history": "Clear History",
        "copy": "Copy",
        "reminder": "🔔 Reminders",
        "reminder_text": "Reminder text",
        "datetime_format": "YYYY-MM-DD HH:MM",
        "add": "Add",
        "open": "Open",
        "shorten_url": "🔗 URL Shortener",
        "enter_url": "Enter URL...",
        "shorten": "Shorten & Copy",
        "short_url": "Short URL",
        "speed_test": "⚡ Network Speed",
        "start_test": "Start Test",
        "testing": "Testing...",
        "whois": "🔍 Whois",
        "domain": "Enter domain (example.com)",
        "get_info": "Get Info",
        "ip_info": "🌐 IP Information",
        "get_ip": "Get IP",
        "external_ip": "External IP:",
        "local_ip": "Local IP:",
        "host": "Host:",
        "port_check": "🔒 Port Check",
        "host_label": "Host",
        "port_label": "Port",
        "check_port": "Check",
        "port_open": "OPEN ✅",
        "port_closed": "CLOSED ❌",
        "ping_trace": "📊 Ping / Traceroute",
        "ping": "Ping",
        "tracert": "Traceroute",
        "installed_programs": "📦 Programs",
        "search_programs": "Search programs...",
        "find": "Find",
        "uninstall": "Uninstall",
        "big_files": "🔍 Large Files",
        "select_folder": "Select folder...",
        "browse": "Browse",
        "start_search": "Start Search",
        "wipe": "🗑️ Secure Delete",
        "warning_wipe": "⚠️  Deleted files CANNOT be recovered!",
        "wipe_button": "Secure Delete",
        "associations": "🛡️ File Associations",
        "restore_assoc": "Restore",
        "windows_theme": "🌙 Windows Theme",
        "dark_theme": "🌙  Dark Theme",
        "light_theme": "☀️  Light Theme",
        "system_clean": "🧹 System Cleaner",
        "home": "🏠 Home",
        "network": "🌐 Network",
        "startup": "⚡ Startup",
        "monitor": "📊 Monitor",
        "programs": "📦 Programs",
        "big_files_nav": "🔍 Large Files",
        "wipe_nav": "🗑️ Secure Delete",
        "assoc_nav": "🛡️ Associations",
        "win_theme": "🌙 Win Theme",
        "screenshots": "📸 Screenshots",
        "buffer": "📋 Clipboard",
        "settings": "⚙️  Settings",
        "theme": "🌓  Theme",
        "greeting_morning": "Good morning",
        "greeting_day": "Good afternoon",
        "greeting_evening": "Good evening",
        "system_overview": "System Overview",
        "work_stage": "Work",
        "break_stage": "Break",
        "clean_start": "Start Cleaning",
        "autostart_label": "Launch on Windows startup",
        "disable": "Disable",
        "confirm_delete": "Delete file permanently?",
        "confirm_uninstall": "Launch uninstaller?",
        "confirm_clean": "Clean all temp files?",
        "success": "Success",
        "error": "Error",
        "note_saved": "Note saved",
        "note_deleted": "Note deleted",
        "confirm_note_delete": "Delete this note?",
        "confirm_clear_clipboard": "Clear all clipboard history?",
        "reminder_added": "Reminder added",
        "bad_date_format": "Invalid date format (YYYY-MM-DD HH:MM)",
        "new_note_title": "New Note",
        "hint_screenshot": "Press Win+Shift+S to take a screenshot",
        "hint_hotkeys": "Ctrl+Shift+N — quick note",
        "no_screenshots": "No screenshots",
        "files_deleted": "files deleted",
        "deleted": "File deleted",
        "added_to_autostart": "Added to startup",
        "removed_from_autostart": "Removed from startup",
        "language_label": "Language / Язык",
        "app_theme_label": "App Theme",
        "autostart_settings": "Autostart",
        "save_settings": "Save",
        "settings_saved": "Settings saved. Reload section.",
        "mbps_down": "Download",
        "mbps_up": "Upload",
        "ms_ping": "Ping",
        "speed_error": "Test failed. Install: pip install speedtest-cli",
        "url_shortened": "Link copied",
        "url_error": "Shortening failed",
    },
}


def get_all_disks():
    """Get all disk partitions with usage info."""
    disks = []
    for p in psutil.disk_partitions(all=False):
        try:
            usage = psutil.disk_usage(p.mountpoint)
            disks.append({
                "device": p.device,
                "mountpoint": p.mountpoint,
                "fstype": p.fstype,
                "total": usage.total,
                "used": usage.used,
                "free": usage.free,
                "percent": usage.percent,
            })
        except (PermissionError, OSError):
            pass
    return disks


class DanrexWorkKit:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Danrex WorkKit")
        self.root.geometry("1380x820")
        self.root.minsize(1100, 640)

        self.config_data = self._load_json("config.json", {"theme": "dark", "language": "ru"})
        self.theme = self.config_data.get("theme", "dark")
        self.language = self.config_data.get("language", "ru")
        self.C = DARK if self.theme == "dark" else LIGHT
        self.current_section = None
        self.running = True

        self.cpu_pct = 0.0
        self.ram_pct = 0.0

        self.notes = self._load_json("notes.json", [])
        self.reminders = self._load_json("reminders.json", [])
        self.clipboard_history = self._load_json("clipboard.json", [])
        self.pomodoro_stats = self._load_json("pomodoro.json", {"today": 0, "total": 0})

        self.pomodoro_time = 25 * 60
        self.pomodoro_running = False
        self.pomodoro_stage = "work"
        self.pomodoro_last_tick = 0.0
        self.speed_test_running = False

        self._build_ui()
        self._setup_hotkeys()
        self._start_bg()

    # ── Translations ─────────────────────────────────────────────────────────
    def t(self, key: str) -> str:
        return TRANSLATIONS[self.language].get(key, key)

    # ── JSON helpers ─────────────────────────────────────────────────────────
    def _load_json(self, path, default):
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return default

    def _save_json(self, path, data):
        try:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception:
            pass

    def _save_all(self):
        self._save_json("config.json", self.config_data)
        self._save_json("notes.json", self.notes)
        self._save_json("reminders.json", self.reminders)
        self._save_json("clipboard.json", self.clipboard_history[:100])
        self._save_json("pomodoro.json", self.pomodoro_stats)

    # ── UI Build ─────────────────────────────────────────────────────────────
    def _build_ui(self):
        self.root.configure(fg_color=self.C["bg"])

        self._nav = ctk.CTkFrame(self.root, width=230, fg_color=self.C["surface"],
                                 corner_radius=0)
        self._nav.pack(side="left", fill="y")
        self._nav.pack_propagate(False)

        self._content_outer = ctk.CTkFrame(self.root, fg_color=self.C["bg"], corner_radius=0)
        self._content_outer.pack(side="left", fill="both", expand=True)

        # Status bar
        self._status_bar = ctk.CTkFrame(self._content_outer, height=32,
                                        fg_color=self.C["surface"], corner_radius=0)
        self._status_bar.pack(side="bottom", fill="x")
        self._status_lbl = ctk.CTkLabel(self._status_bar, text=self.t("ready"),
                                        font=("Segoe UI", 11), text_color=self.C["text2"])
        self._status_lbl.pack(side="left", padx=16)
        self._clock_lbl = ctk.CTkLabel(self._status_bar, text="",
                                       font=("Segoe UI", 11), text_color=self.C["text2"])
        self._clock_lbl.pack(side="right", padx=16)

        # Scrollable content
        self._scroll = ctk.CTkScrollableFrame(self._content_outer, fg_color=self.C["bg"],
                                              scrollbar_button_color=self.C["border"],
                                              scrollbar_button_hover_color=self.C["accent"])
        self._scroll.pack(fill="both", expand=True, padx=0, pady=0)
        self._content = ctk.CTkFrame(self._scroll, fg_color="transparent")
        self._content.pack(fill="both", expand=True, padx=28, pady=24)

        self._build_nav()
        self._update_clock()
        self.switch_section("home")

    def _build_nav(self):
        # Logo
        logo_frame = ctk.CTkFrame(self._nav, fg_color="transparent", height=72)
        logo_frame.pack(fill="x", pady=(4, 0))
        logo_frame.pack_propagate(False)

        logo_dot = ctk.CTkFrame(logo_frame, width=8, height=8,
                                fg_color=self.C["accent"], corner_radius=4)
        logo_dot.place(x=20, y=32)

        ctk.CTkLabel(logo_frame, text="Danrex WorkKit",
                     font=("Segoe UI", 15, "bold"),
                     text_color=self.C["text"]).place(x=36, y=26)

        sep = ctk.CTkFrame(self._nav, height=1, fg_color=self.C["border"])
        sep.pack(fill="x", padx=16, pady=(0, 8))

        nav_scroll = ctk.CTkScrollableFrame(self._nav, fg_color="transparent",
                                            scrollbar_button_color=self.C["border"])
        nav_scroll.pack(fill="both", expand=True, padx=8)

        self._nav_btns = {}
        sections = [
            ("home",         self.t("home")),
            ("pomodoro",     self.t("pomodoro")),
            ("notes",        self.t("notes")),
            ("clipboard",    self.t("buffer")),
            ("reminders",    self.t("reminder")),
            ("screenshots",  self.t("screenshots")),
            ("cleaner",      self.t("cleaner")),
            ("startup",      self.t("startup")),
            ("monitor",      self.t("monitor")),
            ("programs",     self.t("programs")),
            ("bigfiles",     self.t("big_files_nav")),
            ("wipe",         self.t("wipe_nav")),
            ("associations", self.t("assoc_nav")),
            ("wintheme",     self.t("win_theme")),
            ("network",      self.t("network")),
        ]
        for key, label in sections:
            btn = ctk.CTkButton(
                nav_scroll, text=label, anchor="w",
                height=40, corner_radius=10,
                fg_color="transparent",
                hover_color=self.C["hover"],
                text_color=self.C["text2"],
                font=("Segoe UI", 12),
                command=lambda k=key: self.switch_section(k),
            )
            btn.pack(fill="x", pady=2)
            self._nav_btns[key] = btn

        sep2 = ctk.CTkFrame(self._nav, height=1, fg_color=self.C["border"])
        sep2.pack(fill="x", padx=16, pady=8)

        bottom = ctk.CTkFrame(self._nav, fg_color="transparent")
        bottom.pack(side="bottom", fill="x", padx=8, pady=12)

        ctk.CTkButton(bottom, text=self.t("theme"), anchor="w",
                      height=38, corner_radius=10,
                      fg_color="transparent", hover_color=self.C["hover"],
                      text_color=self.C["text2"], font=("Segoe UI", 12),
                      command=self._toggle_theme).pack(fill="x", pady=2)

        ctk.CTkButton(bottom, text=self.t("settings"), anchor="w",
                      height=38, corner_radius=10,
                      fg_color="transparent", hover_color=self.C["hover"],
                      text_color=self.C["text2"], font=("Segoe UI", 12),
                      command=self._open_settings).pack(fill="x", pady=2)

    # ── Navigation ────────────────────────────────────────────────────────────
    def switch_section(self, key: str):
        self.current_section = key

        for k, btn in self._nav_btns.items():
            if k == key:
                btn.configure(fg_color=self.C["nav_active"],
                              text_color=self.C["accent"])
            else:
                btn.configure(fg_color="transparent",
                              text_color=self.C["text2"])

        for w in self._content.winfo_children():
            w.destroy()

        dispatch = {
            "home":         self._sec_home,
            "pomodoro":     self._sec_pomodoro,
            "notes":        self._sec_notes,
            "clipboard":    self._sec_clipboard,
            "reminders":    self._sec_reminders,
            "screenshots":  self._sec_screenshots,
            "cleaner":      self._sec_cleaner,
            "startup":      self._sec_startup,
            "monitor":      self._sec_monitor,
            "programs":     self._sec_programs,
            "bigfiles":     self._sec_bigfiles,
            "wipe":         self._sec_wipe,
            "associations": self._sec_associations,
            "wintheme":     self._sec_wintheme,
            "network":      self._sec_network,
        }
        if key in dispatch:
            dispatch[key]()

    # ── Widgets helpers ───────────────────────────────────────────────────────
    def _title(self, parent, text, pady=(0, 20)):
        ctk.CTkLabel(parent, text=text, font=("Segoe UI", 26, "bold"),
                     text_color=self.C["text"]).pack(anchor="w", pady=pady)

    def _card(self, parent, **kwargs):
        defaults = dict(corner_radius=14, fg_color=self.C["card"],
                        border_width=1, border_color=self.C["border"])
        defaults.update(kwargs)
        return ctk.CTkFrame(parent, **defaults)

    def _label(self, parent, text, size=13, color=None, bold=False, **kwargs):
        font = ("Segoe UI", size, "bold") if bold else ("Segoe UI", size)
        return ctk.CTkLabel(parent, text=text, font=font,
                            text_color=color or self.C["text"], **kwargs)

    def _button(self, parent, text, command, color=None, width=140, **kwargs):
        return ctk.CTkButton(
            parent, text=text, command=command,
            width=width, height=38, corner_radius=10,
            fg_color=color or self.C["accent"],
            hover_color=self.C["accent2"],
            font=("Segoe UI", 12),
            **kwargs,
        )

    def _entry(self, parent, placeholder="", width=300, **kwargs):
        return ctk.CTkEntry(
            parent, placeholder_text=placeholder, width=width,
            corner_radius=10, border_color=self.C["border"],
            fg_color=self.C["surface2"], text_color=self.C["text"],
            placeholder_text_color=self.C["text3"],
            font=("Segoe UI", 12), **kwargs,
        )

    def _textbox(self, parent, height=200, **kwargs):
        return ctk.CTkTextbox(
            parent, height=height, corner_radius=10,
            fg_color=self.C["surface2"], text_color=self.C["text"],
            font=("Segoe UI", 12), **kwargs,
        )

    def _progress(self, parent, width=400):
        return ctk.CTkProgressBar(parent, width=width, height=8,
                                  corner_radius=4,
                                  fg_color=self.C["surface2"],
                                  progress_color=self.C["accent"])

    # ── Clock ─────────────────────────────────────────────────────────────────
    def _update_clock(self):
        if self.running:
            self._clock_lbl.configure(
                text=datetime.datetime.now().strftime("%d.%m.%Y  %H:%M:%S"))
            self.root.after(1000, self._update_clock)

    # ── Theme ─────────────────────────────────────────────────────────────────
    def _toggle_theme(self):
        self.theme = "light" if self.theme == "dark" else "dark"
        self._apply_theme()

    def _apply_theme(self):
        self.C = DARK if self.theme == "dark" else LIGHT
        ctk.set_appearance_mode(self.theme)
        self.config_data["theme"] = self.theme
        self._save_json("config.json", self.config_data)
        # Rebuild UI
        for w in self.root.winfo_children():
            w.destroy()
        self._build_ui()

    # ── Settings ──────────────────────────────────────────────────────────────
    def _open_settings(self):
        win = ctk.CTkToplevel(self.root)
        win.title(self.t("settings"))
        win.geometry("440x340")
        win.configure(fg_color=self.C["surface"])
        win.grab_set()

        pad = ctk.CTkFrame(win, fg_color="transparent")
        pad.pack(fill="both", expand=True, padx=28, pady=24)

        self._label(pad, self.t("language_label"), size=15, bold=True).pack(anchor="w", pady=(0, 10))
        lf = ctk.CTkFrame(pad, fg_color="transparent")
        lf.pack(fill="x", pady=(0, 20))

        for code, label in [("ru", "🇷🇺  Русский"), ("en", "🇬🇧  English")]:
            self._button(lf, label, lambda c=code: self._set_lang(c, win), width=170).pack(side="left", padx=5)

        self._label(pad, self.t("app_theme_label"), size=15, bold=True).pack(anchor="w", pady=(0, 10))
        tf = ctk.CTkFrame(pad, fg_color="transparent")
        tf.pack(fill="x", pady=(0, 20))
        self._button(tf, self.t("dark_theme"), lambda: self._set_theme("dark", win), width=170).pack(side="left", padx=5)
        self._button(tf, self.t("light_theme"), lambda: self._set_theme("light", win), width=170).pack(side="left", padx=5)

        if WINDOWS:
            self._label(pad, self.t("autostart_settings"), size=15, bold=True).pack(anchor="w", pady=(0, 10))
            v = ctk.BooleanVar(value=self._check_autostart())
            ctk.CTkCheckBox(pad, text=self.t("autostart_label"), variable=v,
                            text_color=self.C["text"],
                            command=lambda: self._toggle_autostart(v)).pack(anchor="w")

    def _set_lang(self, code, win):
        self.language = code
        self.config_data["language"] = code
        self._save_json("config.json", self.config_data)
        win.destroy()
        for w in self.root.winfo_children():
            w.destroy()
        self._build_ui()

    def _set_theme(self, theme, win):
        self.theme = theme
        win.destroy()
        self._apply_theme()

    # ── Autostart ─────────────────────────────────────────────────────────────
    def _check_autostart(self):
        p = self._startup_shortcut_path()
        return os.path.exists(p)

    def _startup_shortcut_path(self):
        return os.path.join(
            os.environ.get("APPDATA", ""),
            "Microsoft", "Windows", "Start Menu", "Programs", "Startup",
            "Danrex WorkKit.lnk",
        )

    def _toggle_autostart(self, var):
        path = self._startup_shortcut_path()
        if var.get():
            try:
                import pythoncom
                from win32com.client import Dispatch
                pythoncom.CoInitialize()
                shell = Dispatch("WScript.Shell")
                sc = shell.CreateShortCut(path)
                sc.Targetpath = os.path.abspath(sys.argv[0])
                sc.WorkingDirectory = os.path.dirname(os.path.abspath(sys.argv[0]))
                sc.save()
                pythoncom.CoUninitialize()
                messagebox.showinfo(self.t("success"), self.t("added_to_autostart"))
            except Exception as e:
                messagebox.showerror(self.t("error"), str(e))
        else:
            if os.path.exists(path):
                os.remove(path)
                messagebox.showinfo(self.t("success"), self.t("removed_from_autostart"))

    # ── Background tasks ──────────────────────────────────────────────────────
    def _setup_hotkeys(self):
        if HAS_KEYBOARD:
            try:
                keyboard.add_hotkey("ctrl+shift+n", self._quick_note_popup)
            except Exception:
                pass

    def _start_bg(self):
        threading.Thread(target=self._bg_clipboard, daemon=True).start()
        threading.Thread(target=self._bg_reminders, daemon=True).start()
        threading.Thread(target=self._bg_sysmon, daemon=True).start()

    def _bg_clipboard(self):
        last = ""
        while self.running:
            if HAS_CLIPBOARD:
                try:
                    cur = pyperclip.paste()
                    if cur and cur != last and len(cur) < 500:
                        self.clipboard_history.insert(0, {
                            "content": cur[:200],
                            "time": datetime.datetime.now().isoformat(),
                        })
                        self._save_json("clipboard.json", self.clipboard_history[:100])
                        last = cur
                except Exception:
                    pass
            time.sleep(1)

    def _bg_reminders(self):
        while self.running:
            now = datetime.datetime.now()
            changed = False
            for r in self.reminders:
                if not r.get("completed"):
                    try:
                        dt = datetime.datetime.fromisoformat(r["datetime"])
                        if now >= dt:
                            if HAS_NOTIFY:
                                try:
                                    notification.notify(title="Reminder", message=r["text"], timeout=10)
                                except Exception:
                                    pass
                            r["completed"] = True
                            changed = True
                    except Exception:
                        pass
            if changed:
                self._save_json("reminders.json", self.reminders)
            time.sleep(30)

    def _bg_sysmon(self):
        while self.running:
            self.cpu_pct = min(psutil.cpu_percent(interval=1), 100)
            self.ram_pct = psutil.virtual_memory().percent
            time.sleep(1)

    # ═══════════════════════════════════════════════════════════════════════════
    # SECTIONS
    # ═══════════════════════════════════════════════════════════════════════════

    # ── Home ──────────────────────────────────────────────────────────────────
    def _sec_home(self):
        f = self._content
        hour = datetime.datetime.now().hour
        greet_key = "greeting_morning" if hour < 12 else ("greeting_day" if hour < 18 else "greeting_evening")
        try:
            name = os.getlogin()
        except Exception:
            name = "User"

        self._label(f, f"{self.t(greet_key)}, {name}!", size=30, bold=True).pack(anchor="w", pady=(0, 6))
        self._label(f, datetime.datetime.now().strftime("%A, %d %B %Y"),
                    color=self.C["text2"]).pack(anchor="w", pady=(0, 28))

        # ── System cards row ───────────────────────────────────────────────
        self._label(f, self.t("system_overview"), size=16, bold=True).pack(anchor="w", pady=(0, 12))

        row = ctk.CTkFrame(f, fg_color="transparent")
        row.pack(fill="x", pady=(0, 28))

        # CPU card
        cpu_card = self._card(row)
        cpu_card.pack(side="left", expand=True, fill="both", padx=(0, 10))
        self._label(cpu_card, self.t("cpu"), size=12, color=self.C["text2"]).pack(pady=(16, 4))
        self.cpu_home_val = self._label(cpu_card, "0%", size=36, bold=True, color=self.C["accent"])
        self.cpu_home_val.pack()
        self.cpu_home_bar = self._progress(cpu_card, width=160)
        self.cpu_home_bar.pack(pady=(6, 16))
        self.cpu_home_bar.set(0)

        # RAM card
        ram_card = self._card(row)
        ram_card.pack(side="left", expand=True, fill="both", padx=5)
        self._label(ram_card, self.t("ram"), size=12, color=self.C["text2"]).pack(pady=(16, 4))
        self.ram_home_val = self._label(ram_card, "0%", size=36, bold=True, color=self.C["accent2"])
        self.ram_home_val.pack()
        self.ram_home_bar = self._progress(ram_card, width=160)
        self.ram_home_bar.pack(pady=(6, 16))
        self.ram_home_bar.set(0)

        # Disks
        disks = get_all_disks()
        for disk in disks[:4]:
            dc = self._card(row)
            dc.pack(side="left", expand=True, fill="both", padx=(5, 0))
            dev_name = disk["mountpoint"]
            self._label(dc, dev_name, size=12, color=self.C["text2"]).pack(pady=(16, 4))
            free_gb = disk["free"] // (1024 ** 3)
            total_gb = disk["total"] // (1024 ** 3)
            self._label(dc, f"{free_gb}", size=36, bold=True, color=self.C["accent3"]).pack()
            self._label(dc, f"{self.t('gb_free')} / {total_gb} {self.t('gb_total')}",
                        size=11, color=self.C["text2"]).pack(pady=(2, 6))
            dp = self._progress(dc, width=160)
            dp.pack(pady=(2, 16))
            dp.set(disk["percent"] / 100)

        self._update_home_stats()

        # ── Quick actions ──────────────────────────────────────────────────
        self._label(f, self.t("quick_actions"), size=16, bold=True).pack(anchor="w", pady=(0, 12))
        qa = ctk.CTkFrame(f, fg_color="transparent")
        qa.pack(fill="x")

        actions = [
            (self.t("pomodoro"), "pomodoro", self.C["accent"]),
            (self.t("notes"), "notes", self.C["accent2"]),
            (self.t("cleaner"), "cleaner", self.C["accent3"]),
            (self.t("monitor"), "monitor", self.C["warning"]),
            (self.t("network"), "network", "#e05cb8"),
        ]
        for label, sec, col in actions:
            btn = ctk.CTkButton(
                qa, text=label, width=160, height=76,
                corner_radius=14, fg_color=self.C["surface2"],
                hover_color=self.C["hover"],
                text_color=col, border_width=1, border_color=col,
                font=("Segoe UI", 13, "bold"),
                command=lambda s=sec: self.switch_section(s),
            )
            btn.pack(side="left", padx=(0, 12))

    def _update_home_stats(self):
        if self.running and hasattr(self, "cpu_home_val"):
            try:
                self.cpu_home_val.configure(text=f"{self.cpu_pct:.0f}%")
                self.cpu_home_bar.set(self.cpu_pct / 100)
                self.ram_home_val.configure(text=f"{self.ram_pct:.0f}%")
                self.ram_home_bar.set(self.ram_pct / 100)
                self.root.after(2000, self._update_home_stats)
            except Exception:
                pass

    # ── Pomodoro ──────────────────────────────────────────────────────────────
    def _sec_pomodoro(self):
        f = self._content
        self._title(f, self.t("pomodoro"))

        center = self._card(f)
        center.pack(fill="x", pady=(0, 20))

        # Timer display
        inner = ctk.CTkFrame(center, fg_color="transparent")
        inner.pack(expand=True, pady=30)

        self._pom_stage_lbl = self._label(inner, self.t("work_stage"),
                                          size=14, color=self.C["text2"])
        self._pom_stage_lbl.pack()

        self._pom_display = ctk.CTkLabel(inner, text="25:00",
                                         font=("Courier New", 72, "bold"),
                                         text_color=self.C["accent"])
        self._pom_display.pack(pady=(6, 6))

        ctrl = ctk.CTkFrame(inner, fg_color="transparent")
        ctrl.pack(pady=10)
        self._button(ctrl, self.t("start"), self._pom_start, width=110).pack(side="left", padx=8)
        self._button(ctrl, self.t("pause"), self._pom_pause, color=self.C["text3"], width=110).pack(side="left", padx=8)
        self._button(ctrl, self.t("reset"), self._pom_reset, color=self.C["surface2"], width=110).pack(side="left", padx=8)

        # Settings
        sett = ctk.CTkFrame(center, fg_color="transparent")
        sett.pack(pady=(0, 20))
        self._label(sett, self.t("work_min"), color=self.C["text2"]).grid(row=0, column=0, padx=8, pady=4, sticky="w")
        self._work_entry = self._entry(sett, "25", width=80)
        self._work_entry.grid(row=0, column=1, padx=8)
        self._label(sett, self.t("break_min"), color=self.C["text2"]).grid(row=1, column=0, padx=8, pady=4, sticky="w")
        self._break_entry = self._entry(sett, "5", width=80)
        self._break_entry.grid(row=1, column=1, padx=8)

        # Stats row
        stats_row = ctk.CTkFrame(f, fg_color="transparent")
        stats_row.pack(fill="x", pady=10)
        for label, val in [(self.t("today_sessions"), self.pomodoro_stats["today"]),
                           (self.t("total_sessions"), self.pomodoro_stats["total"])]:
            sc = self._card(stats_row)
            sc.pack(side="left", expand=True, fill="both", padx=6)
            self._label(sc, label, size=12, color=self.C["text2"]).pack(pady=(14, 4))
            self._label(sc, str(val), size=34, bold=True, color=self.C["accent3"]).pack(pady=(0, 14))

        self._pom_update_display()

    def _pom_start(self):
        if not self.pomodoro_running:
            self.pomodoro_running = True
            self.pomodoro_last_tick = time.time()
            self._pom_tick()

    def _pom_pause(self):
        self.pomodoro_running = False

    def _pom_reset(self):
        self.pomodoro_running = False
        try:
            w = int(self._work_entry.get())
        except Exception:
            w = 25
        self.pomodoro_time = w * 60
        self.pomodoro_stage = "work"
        if hasattr(self, "_pom_stage_lbl"):
            self._pom_stage_lbl.configure(text=self.t("work_stage"))
        self._pom_update_display()

    def _pom_tick(self):
        if not self.pomodoro_running:
            return
        now = time.time()
        elapsed = int(now - self.pomodoro_last_tick)
        if elapsed >= 1:
            self.pomodoro_time -= elapsed
            self.pomodoro_last_tick = now
            self._pom_update_display()
        if self.pomodoro_time <= 0:
            self._pom_complete()
        else:
            self.root.after(400, self._pom_tick)

    def _pom_complete(self):
        if WINDOWS:
            try:
                winsound.Beep(880, 600)
            except Exception:
                pass
        if self.pomodoro_stage == "work":
            self.pomodoro_stats["today"] += 1
            self.pomodoro_stats["total"] += 1
            self._save_json("pomodoro.json", self.pomodoro_stats)
            try:
                b = int(self._break_entry.get())
            except Exception:
                b = 5
            self.pomodoro_time = b * 60
            self.pomodoro_stage = "break"
            if hasattr(self, "_pom_stage_lbl"):
                self._pom_stage_lbl.configure(text=self.t("break_stage"))
        else:
            try:
                w = int(self._work_entry.get())
            except Exception:
                w = 25
            self.pomodoro_time = w * 60
            self.pomodoro_stage = "work"
            if hasattr(self, "_pom_stage_lbl"):
                self._pom_stage_lbl.configure(text=self.t("work_stage"))
        self._pom_update_display()
        self.pomodoro_last_tick = time.time()
        self._pom_tick()

    def _pom_update_display(self):
        if hasattr(self, "_pom_display"):
            m = max(0, self.pomodoro_time) // 60
            s = max(0, self.pomodoro_time) % 60
            self._pom_display.configure(text=f"{m:02d}:{s:02d}")

    # ── Notes ─────────────────────────────────────────────────────────────────
    def _sec_notes(self):
        f = self._content
        self._title(f, self.t("notes"))

        main = ctk.CTkFrame(f, fg_color="transparent")
        main.pack(fill="both", expand=True)

        # Left panel
        left = self._card(main, width=270)
        left.pack(side="left", fill="y", padx=(0, 16))
        left.pack_propagate(False)

        self._button(left, self.t("new_note"), self._note_new,
                     width=230).pack(padx=16, pady=(16, 10))

        srch = self._entry(left, self.t("search"), width=230)
        srch.pack(padx=16, pady=(0, 10))
        srch.bind("<KeyRelease>", lambda e: self._notes_search(srch.get()))

        # Native listbox styled
        bg = self.C["surface2"]
        fg = self.C["text"]
        sel_bg = self.C["accent"]

        self._notes_lb = tk.Listbox(
            left, bg=bg, fg=fg, selectbackground=sel_bg,
            selectforeground="white", font=("Segoe UI", 11),
            relief="flat", bd=0, highlightthickness=0,
            activestyle="none",
        )
        self._notes_lb.pack(padx=16, pady=(0, 16), fill="both", expand=True)
        self._notes_lb.bind("<<ListboxSelect>>", self._note_load)
        self._notes_refresh()

        # Right panel
        right = self._card(main)
        right.pack(side="left", fill="both", expand=True)

        self._note_title_e = self._entry(right, "Title / Заголовок", width=0)
        self._note_title_e.pack(fill="x", padx=16, pady=(16, 8))

        self._note_body = self._textbox(right, height=0)
        self._note_body.pack(padx=16, pady=(0, 10), fill="both", expand=True)

        btn_row = ctk.CTkFrame(right, fg_color="transparent")
        btn_row.pack(pady=12)
        self._button(btn_row, self.t("save"), self._note_save, width=120).pack(side="left", padx=8)
        self._button(btn_row, self.t("delete"), self._note_delete,
                     color=self.C["danger"], width=120).pack(side="left", padx=8)

        self._current_note_id = None

    def _notes_search(self, q):
        self._notes_lb.delete(0, "end")
        q = q.lower()
        for note in self.notes:
            if q in note["title"].lower() or q in note["content"].lower():
                self._notes_lb.insert("end", note["title"])

    def _notes_refresh(self):
        self._notes_lb.delete(0, "end")
        for note in self.notes:
            self._notes_lb.insert("end", note["title"])

    def _note_new(self):
        note = {
            "id": str(time.time()),
            "title": self.t("new_note_title"),
            "content": "",
            "created": datetime.datetime.now().isoformat(),
        }
        self.notes.append(note)
        self._save_json("notes.json", self.notes)
        self._notes_refresh()
        self._current_note_id = note["id"]
        self._note_title_e.delete(0, "end")
        self._note_title_e.insert(0, note["title"])
        self._note_body.delete("1.0", "end")

    def _note_load(self, _=None):
        sel = self._notes_lb.curselection()
        if not sel:
            return
        note = self.notes[sel[0]]
        self._current_note_id = note["id"]
        self._note_title_e.delete(0, "end")
        self._note_title_e.insert(0, note["title"])
        self._note_body.delete("1.0", "end")
        self._note_body.insert("1.0", note["content"])

    def _note_save(self):
        if not self._current_note_id:
            return
        for note in self.notes:
            if note["id"] == self._current_note_id:
                note["title"] = self._note_title_e.get()
                note["content"] = self._note_body.get("1.0", "end-1c")
        self._save_json("notes.json", self.notes)
        self._notes_refresh()
        self._status_lbl.configure(text=self.t("note_saved"))

    def _note_delete(self):
        if self._current_note_id and messagebox.askyesno(
                self.t("delete"), self.t("confirm_note_delete")):
            self.notes = [n for n in self.notes if n["id"] != self._current_note_id]
            self._save_json("notes.json", self.notes)
            self._notes_refresh()
            self._note_title_e.delete(0, "end")
            self._note_body.delete("1.0", "end")
            self._current_note_id = None

    def _quick_note_popup(self):
        win = ctk.CTkToplevel(self.root)
        win.title(self.t("new_note_title"))
        win.geometry("420x320")
        win.configure(fg_color=self.C["surface"])
        win.attributes("-topmost", True)
        tb = self._textbox(win, height=200)
        tb.pack(fill="both", expand=True, padx=12, pady=12)

        def _save():
            txt = tb.get("1.0", "end-1c")
            if txt:
                self.notes.append({
                    "id": str(time.time()),
                    "title": f"Note {datetime.datetime.now().strftime('%H:%M:%S')}",
                    "content": txt,
                    "created": datetime.datetime.now().isoformat(),
                })
                self._save_json("notes.json", self.notes)
            win.destroy()

        self._button(win, self.t("save"), _save, width=140).pack(pady=8)

    # ── Clipboard ─────────────────────────────────────────────────────────────
    def _sec_clipboard(self):
        f = self._content
        self._title(f, self.t("clipboard_history"))

        hdr = ctk.CTkFrame(f, fg_color="transparent")
        hdr.pack(fill="x", pady=(0, 12))
        self._button(hdr, self.t("clear_history"), self._clipboard_clear,
                     color=self.C["danger"], width=160).pack(side="right")

        self._clip_scroll = ctk.CTkScrollableFrame(f, fg_color="transparent",
                                                   scrollbar_button_color=self.C["border"])
        self._clip_scroll.pack(fill="both", expand=True)
        self._clipboard_refresh()

    def _clipboard_refresh(self):
        for w in self._clip_scroll.winfo_children():
            w.destroy()
        for item in self.clipboard_history[:50]:
            card = self._card(self._clip_scroll)
            card.pack(fill="x", padx=4, pady=4)
            self._label(card, item["content"][:100], color=self.C["text"]).pack(
                side="left", padx=12, fill="x", expand=True)
            ts = datetime.datetime.fromisoformat(item["time"]).strftime("%H:%M")
            self._label(card, ts, size=11, color=self.C["text3"]).pack(side="right", padx=8)
            if HAS_CLIPBOARD:
                self._button(card, self.t("copy"), lambda c=item["content"]: pyperclip.copy(c),
                             width=90).pack(side="right", padx=8, pady=8)

    def _clipboard_clear(self):
        if messagebox.askyesno(self.t("delete"), self.t("confirm_clear_clipboard")):
            self.clipboard_history = []
            self._save_json("clipboard.json", [])
            self._clipboard_refresh()

    # ── Reminders ─────────────────────────────────────────────────────────────
    def _sec_reminders(self):
        f = self._content
        self._title(f, self.t("reminder"))

        add_card = self._card(f)
        add_card.pack(fill="x", pady=(0, 16))

        row = ctk.CTkFrame(add_card, fg_color="transparent")
        row.pack(fill="x", padx=16, pady=16)

        self._rem_text = self._entry(row, self.t("reminder_text"), width=340)
        self._rem_text.pack(side="left", padx=(0, 10))
        self._rem_time = self._entry(row, self.t("datetime_format"), width=190)
        self._rem_time.pack(side="left", padx=(0, 10))
        self._button(row, self.t("add"), self._rem_add, width=100).pack(side="left")

        self._rem_scroll = ctk.CTkScrollableFrame(f, fg_color="transparent",
                                                  scrollbar_button_color=self.C["border"])
        self._rem_scroll.pack(fill="both", expand=True)
        self._rem_refresh()

    def _rem_add(self):
        txt = self._rem_text.get().strip()
        ts = self._rem_time.get().strip()
        if txt and ts:
            try:
                dt = datetime.datetime.strptime(ts, "%Y-%m-%d %H:%M")
                self.reminders.append({
                    "id": str(time.time()),
                    "text": txt,
                    "datetime": dt.isoformat(),
                    "completed": False,
                })
                self._save_json("reminders.json", self.reminders)
                self._rem_refresh()
                self._rem_text.delete(0, "end")
                self._rem_time.delete(0, "end")
                self._status_lbl.configure(text=self.t("reminder_added"))
            except ValueError:
                messagebox.showerror(self.t("error"), self.t("bad_date_format"))

    def _rem_refresh(self):
        for w in self._rem_scroll.winfo_children():
            w.destroy()
        for r in self.reminders:
            if not r.get("completed"):
                card = self._card(self._rem_scroll)
                card.pack(fill="x", padx=4, pady=4)
                self._label(card, r["text"], color=self.C["text"]).pack(
                    side="left", padx=12, fill="x", expand=True)
                dt = datetime.datetime.fromisoformat(r["datetime"])
                self._label(card, dt.strftime("%d.%m.%Y %H:%M"),
                            size=11, color=self.C["text2"]).pack(side="right", padx=8)
                self._button(card, "✅", lambda rem=r: (rem.update({"completed": True}),
                                                        self._save_json("reminders.json", self.reminders),
                                                        self._rem_refresh()), width=44).pack(side="right", padx=4, pady=8)
                self._button(card, "🗑", lambda rem=r: (self.reminders.remove(rem),
                                                        self._save_json("reminders.json", self.reminders),
                                                        self._rem_refresh()),
                             color=self.C["danger"], width=44).pack(side="right", padx=4, pady=8)

    # ── Screenshots ───────────────────────────────────────────────────────────
    def _sec_screenshots(self):
        f = self._content
        self._title(f, self.t("screenshot"))
        self._label(f, self.t("hint_screenshot"), color=self.C["text2"]).pack(anchor="w", pady=(0, 4))
        self._label(f, self.t("hint_hotkeys"), color=self.C["text3"], size=12).pack(anchor="w", pady=(0, 16))

        self._button(f, self.t("screenshot"), self._quick_screenshot, width=200).pack(anchor="w", pady=(0, 20))

        scr_scroll = ctk.CTkScrollableFrame(f, fg_color="transparent",
                                            scrollbar_button_color=self.C["border"])
        scr_scroll.pack(fill="both", expand=True)
        dir_path = os.path.join(os.path.expanduser("~"), "Pictures", "Danrex")
        files = []
        if os.path.exists(dir_path):
            files = sorted(
                [os.path.join(dir_path, x) for x in os.listdir(dir_path) if x.endswith(".png")],
                key=os.path.getmtime, reverse=True,
            )
        for fp in files[:30]:
            card = self._card(scr_scroll)
            card.pack(fill="x", padx=4, pady=4)
            self._label(card, os.path.basename(fp), color=self.C["text"]).pack(
                side="left", padx=12, fill="x", expand=True)
            self._button(card, self.t("open"), lambda p=fp: os.startfile(p), width=90).pack(
                side="right", padx=8, pady=8)

    def _quick_screenshot(self):
        def _cap():
            try:
                import pyautogui
                d = os.path.join(os.path.expanduser("~"), "Pictures", "Danrex")
                os.makedirs(d, exist_ok=True)
                img = pyautogui.screenshot()
                name = f"screenshot_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                path = os.path.join(d, name)
                img.save(path)
                self.root.after(0, lambda: messagebox.showinfo(self.t("success"), name))
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror(self.t("error"), str(e)))
        threading.Thread(target=_cap, daemon=True).start()

    # ── Cleaner ───────────────────────────────────────────────────────────────
    def _sec_cleaner(self):
        f = self._content
        self._title(f, self.t("system_clean"))

        card = self._card(f)
        card.pack(fill="x", pady=(0, 20))

        self._clean_info = self._label(card, "Temp folder: " + os.environ.get("TEMP", "N/A"),
                                       color=self.C["text2"])
        self._clean_info.pack(padx=16, pady=(16, 8))

        self._clean_bar = self._progress(card, width=500)
        self._clean_bar.pack(pady=(4, 16))
        self._clean_bar.set(0)

        self._button(f, self.t("clean_start"), self._clean_run,
                     color=self.C["danger"], width=200).pack(pady=8)

    def _clean_run(self):
        def _do():
            cleaned = 0
            tmp = os.environ.get("TEMP", "")
            if os.path.exists(tmp):
                files = os.listdir(tmp)
                total = max(len(files), 1)
                for i, fn in enumerate(files):
                    try:
                        os.remove(os.path.join(tmp, fn))
                        cleaned += 1
                    except Exception:
                        pass
                    self.root.after(0, lambda v=i / total: self._clean_bar.set(v))
            self.root.after(0, lambda: messagebox.showinfo(
                self.t("success"), f"{cleaned} {self.t('files_deleted')}"))
            self.root.after(0, lambda: self._clean_bar.set(0))
        threading.Thread(target=_do, daemon=True).start()

    # ── Startup ───────────────────────────────────────────────────────────────
    def _sec_startup(self):
        f = self._content
        self._title(f, self.t("startup"))

        scroll = ctk.CTkScrollableFrame(f, fg_color="transparent",
                                        scrollbar_button_color=self.C["border"])
        scroll.pack(fill="both", expand=True)

        startup_path = os.path.join(
            os.environ.get("APPDATA", ""),
            "Microsoft", "Windows", "Start Menu", "Programs", "Startup",
        )

        def _load():
            if os.path.exists(startup_path):
                for fn in os.listdir(startup_path):
                    self.root.after(0, lambda n=fn, p=os.path.join(startup_path, fn):
                                    self._startup_item(scroll, n, p))
        threading.Thread(target=_load, daemon=True).start()

    def _startup_item(self, parent, name, path):
        card = self._card(parent)
        card.pack(fill="x", padx=4, pady=4)
        self._label(card, name, color=self.C["text"]).pack(side="left", padx=12, fill="x", expand=True)
        self._button(card, self.t("disable"),
                     lambda p=path: self._startup_disable(p),
                     color=self.C["danger"], width=100).pack(side="right", padx=12, pady=8)

    def _startup_disable(self, path):
        try:
            os.remove(path)
            messagebox.showinfo(self.t("success"), self.t("removed_from_autostart"))
            self.switch_section("startup")
        except Exception as e:
            messagebox.showerror(self.t("error"), str(e))

    # ── Monitor ───────────────────────────────────────────────────────────────
    def _sec_monitor(self):
        f = self._content
        self._title(f, self.t("monitor"))

        for attr, label, color in [
            ("_mon_cpu", self.t("cpu"), self.C["accent"]),
            ("_mon_ram", self.t("ram"), self.C["accent2"]),
        ]:
            card = self._card(f)
            card.pack(fill="x", pady=(0, 14))
            row = ctk.CTkFrame(card, fg_color="transparent")
            row.pack(fill="x", padx=16, pady=14)
            self._label(row, label, size=14, bold=True, color=color).pack(side="left")
            lbl = self._label(row, "0%", size=14, color=self.C["text"])
            lbl.pack(side="right")
            bar = self._progress(card, width=0)
            bar.pack(fill="x", padx=16, pady=(0, 14))
            bar.set(0)
            setattr(self, attr + "_lbl", lbl)
            setattr(self, attr + "_bar", bar)

        # Disk cards
        disk_title = self._card(f)
        disk_title.pack(fill="x", pady=(0, 14))
        row2 = ctk.CTkFrame(disk_title, fg_color="transparent")
        row2.pack(fill="x", padx=16, pady=8)
        self._label(row2, self.t("disk"), size=14, bold=True, color=self.C["accent3"]).pack(side="left")
        disks = get_all_disks()
        for disk in disks:
            dr = ctk.CTkFrame(disk_title, fg_color="transparent")
            dr.pack(fill="x", padx=24, pady=2)
            pct = disk["percent"]
            free_gb = disk["free"] // (1024 ** 3)
            total_gb = disk["total"] // (1024 ** 3)
            self._label(dr, f"{disk['mountpoint']}  {free_gb}/{total_gb} GB  ({pct:.0f}%)",
                        color=self.C["text2"], size=12).pack(side="left")
            bp = self._progress(dr, width=200)
            bp.pack(side="right", pady=4)
            bp.set(pct / 100)

        self._mon_update()

    def _mon_update(self):
        if self.running and hasattr(self, "_mon_cpu_lbl"):
            try:
                self._mon_cpu_lbl.configure(text=f"{self.cpu_pct:.0f}%")
                self._mon_cpu_bar.set(self.cpu_pct / 100)
                self._mon_ram_lbl.configure(text=f"{self.ram_pct:.0f}%")
                self._mon_ram_bar.set(self.ram_pct / 100)
                self.root.after(1500, self._mon_update)
            except Exception:
                pass

    # ── Programs ──────────────────────────────────────────────────────────────
    def _sec_programs(self):
        f = self._content
        self._title(f, self.t("installed_programs"))

        sr = ctk.CTkFrame(f, fg_color="transparent")
        sr.pack(fill="x", pady=(0, 12))
        self._prog_search_e = self._entry(sr, self.t("search_programs"), width=320)
        self._prog_search_e.pack(side="left", padx=(0, 10))
        self._button(sr, self.t("find"), self._prog_search, width=100).pack(side="left")

        self._prog_scroll = ctk.CTkScrollableFrame(f, fg_color="transparent",
                                                   scrollbar_button_color=self.C["border"])
        self._prog_scroll.pack(fill="both", expand=True)

        self._all_programs = []
        threading.Thread(target=self._prog_load, daemon=True).start()

    def _prog_load(self):
        progs = []
        if not HAS_WINREG:
            return
        keys = [
            r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
            r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall",
        ]
        for kp in keys:
            try:
                key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, kp)
                for i in range(winreg.QueryInfoKey(key)[0]):
                    try:
                        sk = winreg.OpenKey(key, winreg.EnumKey(key, i))
                        name = winreg.QueryValueEx(sk, "DisplayName")[0]
                        if name and name.strip():
                            try:
                                un = winreg.QueryValueEx(sk, "UninstallString")[0]
                            except Exception:
                                un = None
                            progs.append({"name": name.strip(), "uninstall": un})
                    except Exception:
                        pass
            except Exception:
                pass
        self._all_programs = sorted(progs, key=lambda x: x["name"].lower())
        self.root.after(0, lambda: self._prog_display())

    def _prog_display(self, q=""):
        for w in self._prog_scroll.winfo_children():
            w.destroy()
        shown = 0
        for p in self._all_programs:
            if shown >= 100:
                break
            if q.lower() in p["name"].lower():
                card = self._card(self._prog_scroll)
                card.pack(fill="x", padx=4, pady=3)
                self._label(card, p["name"], color=self.C["text"]).pack(
                    side="left", padx=12, fill="x", expand=True)
                if p["uninstall"]:
                    self._button(card, self.t("uninstall"),
                                 lambda u=p["uninstall"]: self._prog_uninstall(u),
                                 color=self.C["danger"], width=100).pack(side="right", padx=10, pady=8)
                shown += 1

    def _prog_search(self):
        self._prog_display(self._prog_search_e.get())

    def _prog_uninstall(self, cmd):
        if messagebox.askyesno(self.t("uninstall"), self.t("confirm_uninstall")):
            try:
                subprocess.run(cmd, shell=True)
            except Exception as e:
                messagebox.showerror(self.t("error"), str(e))

    # ── Big Files ─────────────────────────────────────────────────────────────
    def _sec_bigfiles(self):
        f = self._content
        self._title(f, self.t("big_files"))

        row = ctk.CTkFrame(f, fg_color="transparent")
        row.pack(fill="x", pady=(0, 12))
        self._scan_path_e = self._entry(row, self.t("select_folder"), width=400)
        self._scan_path_e.pack(side="left", padx=(0, 8))
        self._button(row, self.t("browse"), self._bigfiles_browse, width=100).pack(side="left", padx=(0, 8))
        self._button(row, self.t("start_search"), self._bigfiles_scan, width=140).pack(side="left")

        self._bigfiles_scroll = ctk.CTkScrollableFrame(f, fg_color="transparent",
                                                       scrollbar_button_color=self.C["border"])
        self._bigfiles_scroll.pack(fill="both", expand=True)

    def _bigfiles_browse(self):
        folder = filedialog.askdirectory()
        if folder:
            self._scan_path_e.delete(0, "end")
            self._scan_path_e.insert(0, folder)

    def _bigfiles_scan(self):
        for w in self._bigfiles_scroll.winfo_children():
            w.destroy()
        path = self._scan_path_e.get()
        if not path:
            return

        def _scan():
            for root_dir, _dirs, files in os.walk(path):
                for fn in files:
                    try:
                        fp = os.path.join(root_dir, fn)
                        size_mb = os.path.getsize(fp) / (1024 * 1024)
                        if size_mb > 50:
                            self.root.after(0, lambda fp=fp, s=size_mb: self._bigfiles_add(fp, s))
                    except Exception:
                        pass
        threading.Thread(target=_scan, daemon=True).start()

    def _bigfiles_add(self, path, size_mb):
        card = self._card(self._bigfiles_scroll)
        card.pack(fill="x", padx=4, pady=3)
        self._label(card, f"{os.path.basename(path)}  ({size_mb:.1f} MB)",
                    color=self.C["text"]).pack(side="left", padx=12, fill="x", expand=True)
        self._button(card, self.t("open"), lambda p=path: os.startfile(p), width=80).pack(side="right", padx=4, pady=8)
        self._button(card, self.t("delete"), lambda p=path: self._bigfiles_delete(p),
                     color=self.C["danger"], width=80).pack(side="right", padx=4, pady=8)

    def _bigfiles_delete(self, path):
        if messagebox.askyesno(self.t("delete"), self.t("confirm_delete")):
            try:
                os.remove(path)
                self._bigfiles_scan()
            except Exception as e:
                messagebox.showerror(self.t("error"), str(e))

    # ── Wipe ─────────────────────────────────────────────────────────────────
    def _sec_wipe(self):
        f = self._content
        self._title(f, self.t("wipe"))

        warn = self._card(f, fg_color=self.C["danger"] + "22",
                          border_color=self.C["danger"] + "88")
        warn.pack(fill="x", pady=(0, 20))
        self._label(warn, self.t("warning_wipe"), color=self.C["danger"],
                    size=13, bold=True).pack(padx=16, pady=12)

        row = ctk.CTkFrame(f, fg_color="transparent")
        row.pack(fill="x", pady=(0, 12))
        self._wipe_path_e = self._entry(row, "", width=400)
        self._wipe_path_e.pack(side="left", padx=(0, 8))
        self._button(row, self.t("browse"), self._wipe_browse, width=100).pack(side="left")

        self._wipe_bar = self._progress(f, width=500)
        self._wipe_bar.pack(pady=10)
        self._wipe_bar.set(0)

        self._button(f, self.t("wipe_button"), self._wipe_run,
                     color=self.C["danger"], width=200).pack(pady=10)

    def _wipe_browse(self):
        path = filedialog.askopenfilename()
        if path:
            self._wipe_path_e.delete(0, "end")
            self._wipe_path_e.insert(0, path)

    def _wipe_run(self):
        path = self._wipe_path_e.get()
        if path and messagebox.askyesno(self.t("wipe"), self.t("confirm_delete")):
            try:
                size = os.path.getsize(path)
                chunk = 1024 * 1024
                with open(path, "wb") as fh:
                    for i in range(0, size, chunk):
                        fh.write(b"\x00" * min(chunk, size - i))
                        self._wipe_bar.set(min(1.0, (i + chunk) / size))
                os.remove(path)
                messagebox.showinfo(self.t("success"), self.t("deleted"))
                self._wipe_path_e.delete(0, "end")
                self._wipe_bar.set(0)
            except Exception as e:
                messagebox.showerror(self.t("error"), str(e))

    # ── Associations ──────────────────────────────────────────────────────────
    def _sec_associations(self):
        f = self._content
        self._title(f, self.t("associations"))

        exts = [".txt", ".pdf", ".jpg", ".png", ".mp3", ".mp4", ".docx", ".xlsx"]
        self._assoc_vars = {}
        for ext in exts:
            v = ctk.BooleanVar(value=True)
            self._assoc_vars[ext] = v
            ctk.CTkCheckBox(f, text=ext, variable=v,
                            text_color=self.C["text"],
                            font=("Segoe UI", 12)).pack(anchor="w", pady=4)

        self._button(f, self.t("restore_assoc"), self._assoc_restore, width=200).pack(pady=20)

    def _assoc_restore(self):
        try:
            for ext, var in self._assoc_vars.items():
                if var.get():
                    subprocess.run(f"assoc {ext}", shell=True, capture_output=True)
            messagebox.showinfo(self.t("success"), self.t("restore_assoc"))
        except Exception as e:
            messagebox.showerror(self.t("error"), str(e))

    # ── Windows Theme ─────────────────────────────────────────────────────────
    def _sec_wintheme(self):
        f = self._content
        self._title(f, self.t("windows_theme"))

        card = self._card(f)
        card.pack(fill="x", pady=(0, 20))

        row = ctk.CTkFrame(card, fg_color="transparent")
        row.pack(padx=24, pady=24)
        self._button(row, self.t("dark_theme"),
                     lambda: self._win_theme("dark"), width=180).pack(side="left", padx=10)
        self._button(row, self.t("light_theme"),
                     lambda: self._win_theme("light"), width=180).pack(side="left", padx=10)

    def _win_theme(self, t):
        if not HAS_WINREG:
            messagebox.showerror(self.t("error"), "winreg not available")
            return
        try:
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r"SOFTWARE\Microsoft\Windows\CurrentVersion\Themes\Personalize",
                0, winreg.KEY_SET_VALUE,
            )
            val = 0 if t == "dark" else 1
            winreg.SetValueEx(key, "AppsUseLightTheme", 0, winreg.REG_DWORD, val)
            winreg.SetValueEx(key, "SystemUsesLightTheme", 0, winreg.REG_DWORD, val)
            winreg.CloseKey(key)
            messagebox.showinfo(self.t("success"), f"Windows theme → {t}")
        except Exception as e:
            messagebox.showerror(self.t("error"), str(e))

    # ── Network ───────────────────────────────────────────────────────────────
    def _sec_network(self):
        f = self._content
        self._title(f, self.t("network"))

        nb = ctk.CTkTabview(f, fg_color=self.C["card"],
                            segmented_button_fg_color=self.C["surface2"],
                            segmented_button_selected_color=self.C["accent"],
                            segmented_button_selected_hover_color=self.C["accent2"],
                            text_color=self.C["text"],
                            text_color_disabled=self.C["text3"])
        nb.pack(fill="both", expand=True)

        # ── URL Shortener
        t1 = nb.add(self.t("shorten_url"))
        url_e = self._entry(t1, self.t("enter_url"), width=460)
        url_e.pack(pady=(24, 10))
        result_e = self._entry(t1, self.t("short_url"), width=460)
        result_e.pack(pady=(0, 10))

        def _shorten():
            url = url_e.get().strip()
            if not url:
                return
            if not HAS_REQUESTS:
                messagebox.showerror(self.t("error"), "pip install requests")
                return
            try:
                r = requests.post("https://clck.ru/--", data={"url": url}, timeout=10)
                short = r.text.strip()
                result_e.delete(0, "end")
                result_e.insert(0, short)
                if HAS_CLIPBOARD:
                    pyperclip.copy(short)
                messagebox.showinfo(self.t("success"), self.t("url_shortened"))
            except Exception as e:
                messagebox.showerror(self.t("error"), str(e))

        self._button(t1, self.t("shorten"), _shorten, width=220).pack(pady=8)

        # ── Speed Test
        t2 = nb.add(self.t("speed_test"))
        speed_lbl = self._label(t2, "", size=13, color=self.C["text2"])
        speed_lbl.pack(pady=(24, 8))

        # Live counters
        details_frame = ctk.CTkFrame(t2, fg_color="transparent")
        details_frame.pack(pady=8)
        dl_lbl = self._label(details_frame, f"{self.t('mbps_down')}: —", size=14, color=self.C["accent"])
        dl_lbl.grid(row=0, column=0, padx=30, pady=4)
        ul_lbl = self._label(details_frame, f"{self.t('mbps_up')}: —", size=14, color=self.C["accent2"])
        ul_lbl.grid(row=0, column=1, padx=30, pady=4)
        ping_lbl = self._label(details_frame, f"{self.t('ms_ping')}: —", size=14, color=self.C["accent3"])
        ping_lbl.grid(row=0, column=2, padx=30, pady=4)

        speed_bar = self._progress(t2, width=440)
        speed_bar.pack(pady=8)
        speed_bar.set(0)

        def _speed():
            if self.speed_test_running:
                return
            self.speed_test_running = True
            speed_lbl.configure(text=self.t("testing"))
            speed_bar.set(0)
            dl_lbl.configure(text=f"{self.t('mbps_down')}: —")
            ul_lbl.configure(text=f"{self.t('mbps_up')}: —")
            ping_lbl.configure(text=f"{self.t('ms_ping')}: —")

            def _run():
                try:
                    import speedtest as st_lib
                    st = st_lib.Speedtest()
                    speed_lbl.configure(text="Finding best server...")
                    st.get_best_server()
                    speed_bar.set(0.1)

                    speed_lbl.configure(text="Testing download...")
                    dl = st.download() / 1_000_000
                    speed_bar.set(0.5)
                    dl_lbl.configure(text=f"{self.t('mbps_down')}: {dl:.1f} Mbps")

                    speed_lbl.configure(text="Testing upload...")
                    ul = st.upload() / 1_000_000
                    speed_bar.set(0.9)
                    ul_lbl.configure(text=f"{self.t('mbps_up')}: {ul:.1f} Mbps")

                    ping = st.results.ping
                    ping_lbl.configure(text=f"{self.t('ms_ping')}: {ping:.0f} ms")
                    speed_bar.set(1.0)
                    speed_lbl.configure(text="✅  Done")
                except ImportError:
                    speed_lbl.configure(text=self.t("speed_error"))
                except Exception as e:
                    speed_lbl.configure(text=f"Error: {str(e)[:60]}")
                finally:
                    self.speed_test_running = False
            threading.Thread(target=_run, daemon=True).start()

        self._button(t2, self.t("start_test"), _speed, width=200).pack(pady=12)

        # ── Whois
        t3 = nb.add(self.t("whois"))
        dom_e = self._entry(t3, self.t("domain"), width=360)
        dom_e.pack(pady=(24, 10))
        whois_tb = self._textbox(t3, height=240)
        whois_tb.pack(fill="both", expand=True, padx=0, pady=8)

        def _whois():
            d = dom_e.get().strip()
            if not d:
                return
            try:
                import whois
                w = whois.whois(d)
                info = (f"Domain: {w.domain_name}\n"
                        f"Registrar: {w.registrar}\n"
                        f"Created: {w.creation_date}\n"
                        f"Expires: {w.expiration_date}\n"
                        f"Name servers: {w.name_servers}")
                whois_tb.delete("1.0", "end")
                whois_tb.insert("1.0", info)
            except ImportError:
                whois_tb.delete("1.0", "end")
                whois_tb.insert("1.0", "pip install python-whois")
            except Exception as e:
                whois_tb.delete("1.0", "end")
                whois_tb.insert("1.0", str(e))

        self._button(t3, self.t("get_info"), _whois, width=160).pack(pady=6)

        # ── IP Info
        t4 = nb.add(self.t("ip_info"))
        ip_lbl = self._label(t4, "", size=13, color=self.C["text"])
        ip_lbl.pack(pady=(24, 12))

        def _ip():
            try:
                if HAS_REQUESTS:
                    ext = requests.get("https://api.ipify.org?format=json", timeout=8).json()["ip"]
                else:
                    ext = "N/A (install requests)"
                hostname = socket.gethostname()
                local = socket.gethostbyname(hostname)
                ip_lbl.configure(text=f"{self.t('external_ip')} {ext}\n"
                                      f"{self.t('local_ip')} {local}\n"
                                      f"{self.t('host')} {hostname}")
            except Exception as e:
                ip_lbl.configure(text=str(e))

        self._button(t4, self.t("get_ip"), _ip, width=160).pack(pady=8)

        # ── Port Check
        t5 = nb.add(self.t("port_check"))
        pr = ctk.CTkFrame(t5, fg_color="transparent")
        pr.pack(pady=(24, 10))
        host_e = self._entry(pr, self.t("host_label"), width=220)
        host_e.pack(side="left", padx=(0, 8))
        port_e = self._entry(pr, self.t("port_label"), width=100)
        port_e.pack(side="left", padx=(0, 8))
        port_res = self._label(t5, "", size=14, bold=True)
        port_res.pack(pady=10)

        def _port():
            h = host_e.get().strip()
            p = port_e.get().strip()
            if h and p:
                try:
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.settimeout(3)
                    r = s.connect_ex((h, int(p)))
                    s.close()
                    if r == 0:
                        port_res.configure(text=self.t("port_open"), text_color=self.C["accent3"])
                    else:
                        port_res.configure(text=self.t("port_closed"), text_color=self.C["danger"])
                except Exception as e:
                    port_res.configure(text=str(e), text_color=self.C["warning"])

        self._button(t5, self.t("check_port"), _port, width=160).pack(pady=8)

        # ── Ping
        t6 = nb.add(self.t("ping_trace"))
        ph = ctk.CTkFrame(t6, fg_color="transparent")
        ph.pack(pady=(24, 10))
        ping_e = self._entry(ph, "google.com", width=280)
        ping_e.pack(side="left", padx=(0, 8))
        ping_tb = self._textbox(t6, height=220)
        ping_tb.pack(fill="both", expand=True, padx=0, pady=8)

        cmd_prefix = "ping -n 4" if WINDOWS else "ping -c 4"

        def _ping():
            host = ping_e.get().strip()
            if host:
                def _run():
                    try:
                        r = subprocess.run(f"{cmd_prefix} {host}", capture_output=True,
                                           text=True, shell=True, timeout=15)
                        ping_tb.delete("1.0", "end")
                        ping_tb.insert("1.0", r.stdout[:600] or r.stderr[:300])
                    except Exception as e:
                        ping_tb.delete("1.0", "end")
                        ping_tb.insert("1.0", str(e))
                threading.Thread(target=_run, daemon=True).start()

        btn_row6 = ctk.CTkFrame(t6, fg_color="transparent")
        btn_row6.pack(pady=6)
        self._button(btn_row6, self.t("ping"), _ping, width=120).pack(side="left", padx=6)

        if WINDOWS:
            def _trace():
                host = ping_e.get().strip()
                if host:
                    def _run():
                        try:
                            r = subprocess.run(f"tracert {host}", capture_output=True,
                                               text=True, shell=True, timeout=30)
                            ping_tb.delete("1.0", "end")
                            ping_tb.insert("1.0", r.stdout[:1000])
                        except Exception as e:
                            ping_tb.delete("1.0", "end")
                            ping_tb.insert("1.0", str(e))
                    threading.Thread(target=_run, daemon=True).start()
            self._button(btn_row6, self.t("tracert"), _trace, width=140,
                         color=self.C["accent2"]).pack(side="left", padx=6)

    # ── Run ───────────────────────────────────────────────────────────────────
    def run(self):
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)
        self.root.mainloop()

    def _on_close(self):
        self.running = False
        self._save_all()
        self.root.destroy()


if __name__ == "__main__":
    app = DanrexWorkKit()
    app.run()
