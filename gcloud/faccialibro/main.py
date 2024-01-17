# SERVE AL FINE DI IMPLEMENTARE UN TEST PER LE GCLOUD FUNCTIONS;
# E' UNA COSA IN PIU'; NON E' RICHIESTA DALLA TRACCIA!!!!
import json
import requests


def hello_firestore(data, context):
    """Triggered by a change to a Firestore document.
    Args:
        data (dict): The event payload.
        context (google.cloud.functions.Context): Metadata for the event.
    """
    trigger_resource = context.resource

    print("Function triggered by change to: %s" % trigger_resource)

    print("\nOld value:")
    print(json.dumps(data["oldValue"]))

    print("\nupdateMask:")
    print(json.dumps(data["updateMask"]))

    print("\nNew value:")
    print(json.dumps(data["value"]["fields"]["message"]["stringValue"]))
    message = json.dumps(data["value"]["fields"]["message"]["stringValue"])
    requests.post(
        'https://api.telegram.org/botxxxx:yyyyy/sendMessage?chat_id=zzzzz&text='+message
    )

