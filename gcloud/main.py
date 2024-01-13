import json

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

