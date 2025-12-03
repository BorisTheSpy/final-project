-- SQL script to add 3 test orders to the orders table
-- This matches the ACTUAL table structure (id, customer_name, order_date, description)

USE sandwich_maker_api;

-- Insert 3 test orders
-- Order 1: Recent order
INSERT INTO orders (customer_name, description, order_date)
VALUES 
(
    'Test Customer 1', 
    'Turkey Club Sandwich with extra mayo',
    NOW()
);

-- Order 2: Order from 1 hour ago
INSERT INTO orders (customer_name, description, order_date)
VALUES 
(
    'Test Customer 2', 
    'Veggie Delight Sandwich, no onions',
    DATE_SUB(NOW(), INTERVAL 1 HOUR)
);

-- Order 3: Order from 2 hours ago
INSERT INTO orders (customer_name, description, order_date)
VALUES 
(
    'Test Customer 3', 
    'Classic BLT Sandwich with avocado',
    DATE_SUB(NOW(), INTERVAL 2 HOUR)
);

-- Verify the orders were inserted
SELECT 
    id,
    customer_name,
    description,
    order_date
FROM orders
ORDER BY order_date DESC
LIMIT 3;

