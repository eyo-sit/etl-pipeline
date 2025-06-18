
def unpackage(message):
    fields = message.strip().split(b',')
    return {
        "unix_timestamp": fields[0].decode(),
        "track_id": fields[1].decode(),
        "sensor_id": fields[2].decode(),
        "latitude": fields[3].decode(),
        "longitude": fields[4].decode(),
        "altitude": fields[5].decode(),
        "radiometric_intensity": fields[6].decode()
    }

