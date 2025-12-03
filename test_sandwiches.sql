-- SQL script to add 3 sample sandwiches to the sandwiches table
-- This matches the ACTUAL table structure (id, sandwich_name, price)

USE sandwich_maker_api;

-- Insert 3 sample sandwiches
INSERT INTO sandwiches (sandwich_name, price)
VALUES 
-- Sandwich 1: Classic BLT
(
    'Classic BLT', 
    8.99
),
-- Sandwich 2: Turkey Club
(
    'Turkey Club', 
    9.99
),
-- Sandwich 3: Veggie Delight
(
    'Veggie Delight', 
    7.99
);

-- Verify the sandwiches were inserted
SELECT 
    id,
    sandwich_name,
    price
FROM sandwiches
ORDER BY id;

