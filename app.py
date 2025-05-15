from flask import Flask
from config import Config
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Import blueprints
from routes.dashboard import dashboard_bp
from routes.sheets import sheet_bp
from routes.telegram import telegram_bp
from routes.template import template_bp
from routes.boss import boss_bp


def create_app():
    app = Flask(__name__)
    config = Config()

    # define the scope
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']

    creds_dict = {
        "type": "service_account",
        "project_id": config.project_id,
        "private_key_id": config.private_key_id,
        "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDDXaaHpduS8I5K\nMXUCZatlCUwgL6nXXtlGh3IK8/l2/s51q/wNK1pIxb2+6+cL6I331urZfk89/pp0\nTa0zYKyljH55UBpbF6MkbwFueR4uiYXNDBm4a658sbP7mutTG0QV3NSol6VsRo6a\nwxxhLYOuroT+UYxEA4FbVR4BpXkKmM5qHFmX/PdKz4Y+7qzXxDlRZs3dbI00q8w9\nWuVBxnC9VOs7T8d0LgXb6pMrdUbOeZ5EAjfhjLSgrOhBvoSy7vEtUItlEnLYnLE +\nr7louyBcqdF2VjMtiJ1OPhGu3K/Z6oXtczQpaPYOotD0/ktupov2rspjoGB18VGy\ntNr6EmcFAgMBAAECggEAD/URShkhAzKE3MiHXyfAxSLqReK+w6mqo5kiloRxBugv\nIutmTgkReco1AmgwWgenuOukCRnJDS5DnWZO1Fh8IZWFKxGA5ZnbqHksq8JW1cRD\n2oi3fRnGicbWBaIUwJgEiqib8h1Y1Kw6r6dqJQHbtKPqlv9ALrn+keA08Dt81IGc\nIDe3rqL3nDzFuHHCr35EZvlWzmRU907GrAHftSkdQTEOJNDqrrg2BYkW+tqewhRl\n8csMlqA08cNng1Ni6InC6gkfGverx9GRN+QHb8+9In4cQlEAi1+ps5M94sWHHJib\nqzx5eUpIdTaNAO0zHdoDfCmkxl15nOS7DdzG0zODrQKBgQDqFZi4o6sDKyzMmU9m\n/F7f/wi9d2eal+yI62PBQNmvI0IkIk1IjUf4HCkA6/8AoIdYoJU7uGZI3TIkfW3r\nsPDHgDjd8NRUPB6WHtmwVkFf7a1IF8XxbWi/Wtt4mjVdNCME/KO7T2ElZNBsQDZ6\nf0nOFzs/EEc+B2y75P38le5d7wKBgQDVqBHQL+zXtN/9Ql12GVRsoYcns5Uqrcjg\nYibJYEswJ87N5RIDucIaSny6eGQq4vOP5jxUga5ztCjIIbgf7AJ+PPG/JQJynTF9\nnoJUETlJuWNqyid7XCnDTTNfvU7OjX+QcWbAjPNPkEiaY6lyMaO+Y/brNinvAO //\n5VjpAlM+SwKBgQCXLQ1tqV3ndPnAxP5Pv4syVI37duL1J0q+fm71PwGXJ0ku9uw8\nf+nL5bvheYg9im7+oO7gG84LHrekc1ELF0HZRgjz5PXr1MvYHeJvDLW501DGr3vJ\n2OP+ORpmgAkYwXQgY10GulQ+BybH0oycfhpXPA+qQcQQ3lCt5EzX1KiWBwKBgQCD\neDsV1xevF/6ocZjfHfEEM1TeSjPkojE0WVEyow1BIY2wxl8SadCVqvYbLA+/EA39\noxfGjFHToq1hkNYi1nAmS8wZ6WUbL70PZmUd48dTpT8WrDQlRW3xXmTZaby/fvRa\n5lzq6RCjCc6TKfZPbVorwoli7N5a0kHcPb07DBI7BwKBgGZBnVaUnxqdQtcNWMoH\nYprWsuJz+sYz73ANb38NB5qyzGjdZ1xikTGCDDs5JK5p8uPnf/73uZkQG8u/1Xo6\nmxU5Ff5M55PYthuuL7bpKUeS9lE6rqS9f/rNMOncoEjPp6qrnzDEsfZ/ehzbDYDV\nUqxVQIpdMLsRLma9g/W8C7C /\n-----END PRIVATE KEY-----\n",
        "client_email": config.client_email,
        "client_id": config.client_id,
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": config.client_x509_cert_url,
        "universe_domain": "googleapis.com"
    }

    # add credentials to the account and authorize client
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    client = gspread.authorize(creds)

    # Register blueprints
    blueprints = [dashboard_bp, sheet_bp, telegram_bp, template_bp, boss_bp]
    for blueprint in blueprints:
        blueprint.client = client
        blueprint.config = config
        app.register_blueprint(blueprint)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=False)
