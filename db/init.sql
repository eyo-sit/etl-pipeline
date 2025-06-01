
   CREATE TABLE launch_origins (
  city_name VARCHAR(50),
  country VARCHAR(50),
  latitude Decimal(8,6),
  longitudes Decimal(9,6),
  altitude Decimal(10,2),
  population INTEGER
);
    

    CREATE TABLE target_locations (
	city_name VARCHAR(50),
	state VARCHAR(50),
	latitude Decimal(8,6),
	longitude Decimal(9,6),
	altitude Decimal(10,2),
	population INTEGER
);
    

    CREATE TABLE sensor_data (
    sensor_id SERIAL,
    latitude Decimal,
    longitude Decimal,
    altitude Decimal,
    measurement_sampling_rate INTEGER,
    positional_measurement_error DECIMAL,
    radiometric_measurement_error DECIMAL,
    maximum_measurement_range DECIMAL
    );
    

    CREATE TABLE missile_tracks_sensor_1(
    unix_timestamp INTEGER,
    track_id INTEGER,
    sensor_id INTEGER,
    latitude Decimal,
    longitude Decimal,
    laltitude Decimal,
    altitude Decimal,
    radiometric_intensity Decimal
    );

    

    CREATE TABLE missile_tracks_sensor_2(
    unix_timestamp INTEGER,
    track_id INTEGER,
    sensor_id INTEGER,
    latitude Decimal,
    longitude Decimal,
    laltitude Decimal,
    altitude Decimal,
    radiometric_intensity Decimal
    );

    

    CREATE TABLE missile_tracks_sensor_3(
    unix_timestamp INTEGER,
    track_id INTEGER,
    sensor_id INTEGER,
    latitude Decimal,
    longitude Decimal,
    laltitude Decimal,
    altitude Decimal,
    radiometric_intensity Decimal
    );

    

    CREATE TABLE missile_tracks_sensor_4(
    unix_timestamp INTEGER,
    track_id INTEGER,
    sensor_id INTEGER,
    latitude Decimal,
    longitude Decimal,
    laltitude Decimal,
    altitude Decimal,
    radiometric_intensity Decimal
    );

    

    CREATE TABLE missile_tracks_sensor_5(
    unix_timestamp INTEGER,
    track_id INTEGER,
    sensor_id INTEGER,
    latitude Decimal,
    longitude Decimal,
    altitude Decimal,
    radiometric_intensity Decimal
    );

    
