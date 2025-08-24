from .types import localization
from env import env
from typing import TypedDict

class Language(TypedDict):
    always_hide_id_name: str
    always_hide_id_description: str
    always_set_alias_name: str
    always_set_alias_description: str

    producer: str
    producer_placeholder: str

    create_level_description: str
    alias_name: str
    alias_description: str
    hide_id_name: str
    hide_id_description: str

    usc_file: str
    img_file: str
    better_square: str
    bgm_file: str

    visibility: str
    visibility_public: str
    visibility_unlisted: str

    search_by_user_handle: str
    sort_by_most_liked: str

strings = { # I aint gon lie, chatgpt fixed my text. At least it's readable now
    'en': {
        'always_hide_id_name': 'Always Hide My ID',
        'always_hide_id_description': \
f"""NOTE: This setting does not affect actions on the website.

Replaces your Sonolus ID with your {env.PROJECT_NAME} ID when uploading new levels and replays.
Existing levels and replays will not be changed. Your displayed name will stay the same — you can change it using the "Alias" option.

You can change this and the "Alias" option here for all new uploads, or enable it per level in the "Create" menu.
""",
        'always_set_alias_name': 'Always Set Alias',
        'always_set_alias_description': \
"""NOTE: This setting does not affect actions on the website.

Replaces your nickname with this text when uploading new levels and replays.
Existing levels and replays will not be changed. Your Sonolus ID will still be visible (and by knowing it, anyone can find your actual nickname). You can hide it by enabling the "Hide My ID" option.

You can change this and the "Hide My ID" option here for all new uploads, or enable it per level in the "Create" menu.

If left empty, your actual nickname will be used.
""",
        'producer': 'Producer',
        'producer_placeholder': 'Enter producer...',
        'create_level_description': \
f"It’s probably more convenient to upload and manage your levels from the website: {env.FINAL_HOST_LINKS[0]} (you can also upload private levels without a cover there)",
        'alias_name': 'Alias',
        'alias_description': \
"""Replaces your nickname with this text. Your Sonolus ID will still be visible (and by knowing it, anyone can find your actual nickname). You can hide it by enabling the "Hide My ID" option.

You can change this and the "Hide My ID" option here for only this level, or enable it globally for all new level and replay uploads in the server options.

If left empty, your actual nickname will be used.
""",
        'hide_id_name': 'Hide My ID',
        'hide_id_description': \
f"""Replaces your Sonolus ID with your {env.PROJECT_NAME} ID. Your displayed name will stay the same — you can change it using the "Alias" option.

You can change this and the "Alias" option here for only this level, or enable it globally for all new level and replay uploads in the server options.
""",
        'usc_file': 'File in USC format',
        'bgm_file': 'Music in MP3/OGG/WAV format',
        'img_file': 'Image in PNG/JPG/BMP/TIFF/ICO/WEBP format',
        'better_square': 'The image will be automatically padded to a square. If you want, you can crop it yourself to have full control over the positioning.',
        'visibility': 'Visibility',
        'visibility_public': 'Public',
        'visibility_unlisted': 'Unlisted',
        'search_by_user_handle': 'User ID',
        'sort_by_most_liked': 'Most liked'
    },
    'ru': {
        'always_hide_id_name': 'Всегда скрывать ID',
        'always_hide_id_description': \
f"""ПРИМЕЧАНИЕ: эта настройка не влияет на действия, совершённые на сайте.

Заменит твой Sonolus ID на {env.PROJECT_NAME} ID при загрузке новых уровней и реплеев.
Старые уровни и реплеи не будут изменены. Отображаемое имя останется тем же — его можно изменить настройкой «Псевдоним».

Эту и настройку «Псевдоним» можно изменить здесь для всех новых загрузок, либо включить для конкретного уровня в меню «Создать».
""",
        'always_set_alias_name': 'Всегда использовать псевдоним',
        'always_set_alias_description': \
"""ПРИМЕЧАНИЕ: эта настройка не влияет на действия, совершённые на сайте.

Заменит твой никнейм на указанный текст при загрузке новых уровней и реплеев.
Старые уровни и реплеи не будут изменены. Твой Sonolus ID всё ещё будет виден (и зная его, можно узнать твой настоящий никнейм). Ты можешь скрыть его, включив настройку «Скрывать ID».

Эту и настройку «Скрывать ID» можно изменить здесь для всех новых загрузок, либо включить для конкретного уровня в меню «Создать».

Если оставить поле пустым, будет использован твой настоящий никнейм.
""",
        'producer': 'Продюсер',
        'producer_placeholder': 'Введите продюсера...',
        'create_level_description': \
f"Вероятнее всего, будет удобнее управлять уровнями и загружать новые с сайта: {env.FINAL_HOST_LINKS[0]} (там также можно загружать приватные уровни без обложки).",
        'alias_name': 'Псевдоним',
        'alias_description': \
"""Заменит твой никнейм на указанный текст. Твой Sonolus ID всё ещё будет виден (и зная его, можно узнать твой настоящий никнейм). Ты можешь скрыть его, включив настройку «Скрывать ID».

Эту и настройку «Скрывать ID» можно изменить здесь только для этого уровня или включить глобально для всех новых загрузок уровней и реплеев в настройках сервера.

Если оставить поле пустым, будет использован твой настоящий никнейм.
""",
        'hide_id_name': 'Скрывать ID',
        'hide_id_description': \
f"""Заменит твой Sonolus ID на {env.PROJECT_NAME} ID. Отображаемое имя останется тем же — его можно изменить настройкой «Псевдоним».

Эту и настройку «Псевдоним» можно изменить здесь только для этого уровня или включить глобально для всех новых загрузок уровней и реплеев в настройках сервера.
""",
        'usc_file': 'Файл в формате USC',
        'bgm_file': 'Музыка в формате MP3/OGG/WAV',
        'img_file': 'Изображение в формате PNG/JPG/BMP/TIFF/ICO/WEBP',
        'better_square': 'К изображению будут автоматически добавлены рамки чтобы получился квадрат. Если хочешь, можешь обрезать его самостоятельно, чтобы сохранить полный контроль над позицией.',
        'visibility': 'Видимость',
        'visibility_public': 'Общий доступ',
        'visibility_unlisted': 'Доступ по ссылке',
        'sort_by_most_liked': 'Самые залайканные',
        'search_by_user_handle': 'По ID пользователя'
    }
}



def get_language(localization: localization) -> Language:
    return strings.get(localization, strings['en'])