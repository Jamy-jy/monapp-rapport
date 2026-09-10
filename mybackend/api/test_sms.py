import messagebird
from django.conf import settings

client = messagebird.Client(settings.MESSAGEBIRD_API_KEY)
try:
    response = client.message_create(
        originator=settings.MESSAGEBIRD_ORIGINATOR,
        recipients=['+261349189391'],
        body='Test SDK legacy'
    )
    print("OK:", response.id, response.recipients)

    print("API KEY:", settings.MESSAGEBIRD_API_KEY)
except messagebird.client.ErrorException as e:
    print("ERREUR:", e.errors[0].description if e.errors else str(e))