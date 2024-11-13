from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
import numpy as np
import pandas as pd
from db import get_db_connection
from traumas import load_trauma_data

language = "ru"  # Default language


# Main Menu
main_menu_kb = ReplyKeyboardBuilder()
main_menu_kb.button(text="🚨", request_location=True)
main_menu_kb.button(text="⚙️")
main_menu_kb.button(text="📚")
# =

# Settings
settings_kb = ReplyKeyboardBuilder()
settings_kb.button(text="Близкие друзья")
settings_kb.button(text="Выйти")
# =

# Emergency
traumas = load_trauma_data()
emergency_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text=trauma_data["title"], callback_data=trauma_file)]
        for trauma_file, trauma_data in traumas.items()
    ]
)
# =

# Load the CSV file into a DataFrame
hospitals_df = pd.read_csv("assets/saqbol-hospitals.csv")
polices_df = pd.read_csv("assets/saqbol-polices.csv")


def get_keyboard_of_hospitals(lat, long):
    temp_hospitals_df = hospitals_df

    # Calculate the distance using the Pythagorean theorem approximation
    temp_hospitals_df["coordinate_distance"] = np.sqrt(
        (temp_hospitals_df["latitude"] - lat) ** 2
        + (temp_hospitals_df["longitude"] - long) ** 2
    )

    # Sort by distance in ascending order
    temp_hospitals_df = temp_hospitals_df.sort_values(by="coordinate_distance")

    ###

    temp_polices_df = polices_df

    # Calculate the distance using the Pythagorean theorem approximation
    temp_polices_df["coordinate_distance"] = np.sqrt(
        (temp_polices_df["latitude"] - lat) ** 2
        + (temp_polices_df["longitude"] - long) ** 2
    )

    # Sort by distance in ascending order
    temp_polices_df = temp_polices_df.sort_values(by="coordinate_distance")

    inline_keyboard_buttons = []

    for index, row in temp_hospitals_df.head(5).iterrows():
        inline_keyboard_buttons.append(
            [
                InlineKeyboardButton(
                    text=row["name_ru"],
                    url=f"https://www.google.com/maps/search/?api=1&query={row['latitude']},{row['longitude']}",
                )
            ]
        )

    for index, row in temp_polices_df.head(2).iterrows():
        inline_keyboard_buttons.append(
            [
                InlineKeyboardButton(
                    text=row["name_ru"],
                    url=f"https://www.google.com/maps/search/?api=1&query={row['latitude']},{row['longitude']}",
                )
            ]
        )

    # Create an inline keyboard with buttons for the first 5 hospitals
    keyboard = InlineKeyboardMarkup(inline_keyboard=inline_keyboard_buttons)

    return keyboard


"""

def get_keyboard_of_hospitals(lat, long):
    temp_df = hospitals_df

    # Calculate the distance using the Pythagorean theorem approximation
    temp_df["coordinate_distance"] = np.sqrt(
        (temp_df["latitude"] - lat) ** 2 + (temp_df["longitude"] - long) ** 2
    )

    # Sort by distance in ascending order
    temp_df = temp_df.sort_values(by="coordinate_distance")

    # Create an inline keyboard with buttons for the first 5 hospitals
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=row["name_ru"],
                    url=f"https://www.google.com/maps/search/?api=1&query={row['latitude']},{row['longitude']}",
                )
            ]
            for index, row in temp_df.head(5).iterrows()
        ]
    )

    return keyboard
"""

languages_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="English", callback_data="lang_en")],
        [InlineKeyboardButton(text="Русский", callback_data="lang_ru")],
        [InlineKeyboardButton(text="Қазақша", callback_data="lang_kz")],
    ]
)


keyboard_friend = ReplyKeyboardBuilder()
keyboard_friend.button(text="Добавить друга")
keyboard_friend.button(text="Удалить друга")
keyboard_friend.button(text="Показать список друзей")
keyboard_friend.button(text="Выйти")


keyboard_back = ReplyKeyboardBuilder()
keyboard_back.button(text="Назад")


def create_friends_keyboard(user_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT username, user_id FROM friends WHERE user_id = ?", (user_id,)
    )
    friends = cursor.fetchall()
    conn.close()

    keyboard = ReplyKeyboardBuilder()
    for username, friend_id in friends:
        keyboard.button(text=username, callback_data=f"friend_{username[1:]}")
    return keyboard.as_markup()
