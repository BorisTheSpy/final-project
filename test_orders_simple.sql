-- Simple SQL script to add 3 test orders
-- This matches the ACTUAL table structure (id, customer_name, order_date, description)

USE sandwich_maker_api;

-- Insert 3 test orders
INSERT INTO orders (customer_name, description, order_date)
VALUES 
-- Order 1: Recent order
(
    'John Doe', 
    'Turkey Club Sandwich with extra mayo',
    NOW()
),
-- Order 2: Order from 1 hour ago
(
    'Jane Smith', 
    'Veggie Delight Sandwich, no onions',
    DATE_SUB(NOW(), INTERVAL 1 HOUR)
),
-- Order 3: Order from 2 hours ago
(
    'Bob Johnson', 
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

