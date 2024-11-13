rescuer_bot/
├── bot.py # Main entry point for the bot
├── config.py # Configuration file for bot token, API keys, and settings
├── requirements.txt # Python dependencies
├── data/
│ ├── db.py # Database connection and schema
│ └── translations/ # Translation files for multiple languages
├── handlers/
│ ├── **init**.py # Initialize handlers package
│ ├── emergency.py # Emergency handling logic
│ ├── settings.py # User settings (emergency contacts, language)
│ └── resources.py # Resource section (first aid tips, exercises)
├── keyboards/
│ ├── **init**.py # Initialize keyboards package
│ ├── main_menu.py # Main menu buttons
│ ├── emergency_menu.py # Buttons for emergency types
│ └── settings_menu.py # Buttons for settings options
├── localization/
│ ├── en.json # English translations
│ ├── ru.json # Russian translations
│ └── kz.json # Kazakh translations
├── services/
│ ├── **init**.py # Initialize services package
│ ├── map_service.py # Functions to handle map and routing logic
│ └── notification_service.py # Service to send notifications to contacts
└── utils/
├── **init**.py # Initialize utils package
├── i18n.py # Utility for handling translations
└── location_utils.py # Geolocation and mapping helpers
