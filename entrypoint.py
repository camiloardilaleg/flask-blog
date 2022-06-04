import os
from app import create_app

settings_module = os.getenv('APP_SETTINGS_MODULE')
print(f'informacion->: {settings_module}')
app = create_app(settings_module)

"""
This file in on charge to boost the app.
"""