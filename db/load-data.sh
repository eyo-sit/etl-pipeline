#!/bin/bash
set -e

echo "Loading csv data into tables..."

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
  COPY launch_origins(city_name, country, latitude, longitudes, altitude, population)
  FROM '/csv/launch_origin_locations.csv' 
  DELIMITER ','
  CSV HEADER;

  COPY target_locations(city_name, state, latitude, longitude, altitude, population)
  FROM '/csv/target_locations.csv' 
  DELIMITER ','
  CSV HEADER;

  COPY sensor_data(sensor_id, latitude, longitude, altitude, measurement_sampling_rate, positional_measurement_error, radiometric_measurement_error, maximum_measurement_range)
  FROM '/csv/sensor_data.csv'
  DELIMITER ','
  CSV HEADER;

  COPY missile_tracks_sensor_1(unix_timestamp, track_id, sensor_id, latitude, longitude, altitude, radiometric_intensity)
  FROM '/csv/missile_tracks_sensor_1.csv' 
  DELIMITER ','
  CSV HEADER;

  COPY missile_tracks_sensor_2(unix_timestamp, track_id, sensor_id, latitude, longitude, altitude, radiometric_intensity)
  FROM '/csv/missile_tracks_sensor_2.csv' 
  DELIMITER ','
  CSV HEADER;

  COPY missile_tracks_sensor_3(unix_timestamp, track_id, sensor_id, latitude, longitude, altitude, radiometric_intensity)
  FROM '/csv/missile_tracks_sensor_3.csv' 
  DELIMITER ','
  CSV HEADER;

  COPY missile_tracks_sensor_4(unix_timestamp, track_id, sensor_id, latitude, longitude, altitude, radiometric_intensity)
  FROM '/csv/missile_tracks_sensor_4.csv' 
  DELIMITER ','
  CSV HEADER;

  COPY missile_tracks_sensor_5(unix_timestamp, track_id, sensor_id, latitude, longitude, altitude, radiometric_intensity)
  FROM '/csv/missile_tracks_sensor_5.csv' 
  DELIMITER ','
  CSV HEADER;
EOSQL
