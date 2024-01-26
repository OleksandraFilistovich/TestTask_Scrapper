CREATE TABLE IF NOT EXISTS cars (
    id SERIAL PRIMARY KEY,
    url VARCHAR(300) NOT NULL UNIQUE,
    title VARCHAR(150),
    price_usd INT,
    odometer INT,
    username VARCHAR(100),
    phone_number VARCHAR(15),
    image_url VARCHAR(300),
    images_count INT,
    car_number VARCHAR(10),
    car_vin VARCHAR(17),
    datetime_found TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);