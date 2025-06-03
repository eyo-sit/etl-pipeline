
def unpackage(message):
    fields = message.strip().split(b',')
    return {
        "unix_timestamp": fields[0],
        "track_id": fields[1],
        "sensor_id": fields[2],
        "latitude": fields[3],
        "longitude": fields[4],
        "altitude": fields[5],
        "radiometric_intensity": fields[6]
    }

