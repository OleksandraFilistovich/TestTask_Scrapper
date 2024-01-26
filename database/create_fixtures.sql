CREATE TABLE IF NOT EXISTS cars (
    id SERIAL PRIMARY KEY,
    url VARCHAR(400) NOT NULL UNIQUE,
    title VARCHAR(200),
    price_usd INT,
    odometer INT,
    username VARCHAR(100),
    phone_number VARCHAR(15),
    image_url VARCHAR(400),
    images_count INT,
    car_number VARCHAR(12),
    car_vin VARCHAR(17),
    datetime_found TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);