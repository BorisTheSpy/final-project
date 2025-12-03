# Database Setup Guide

This guide will help you connect your application to a MySQL database.

## Prerequisites

1. **MySQL Server** - Make sure MySQL is installed and running on your system
   - macOS: `brew install mysql` or download from [MySQL website](https://dev.mysql.com/downloads/mysql/)
   - Windows: Download MySQL Installer from [MySQL website](https://dev.mysql.com/downloads/installer/)
   - Linux: `sudo apt-get install mysql-server` (Ubuntu/Debian) or `sudo yum install mysql-server` (CentOS/RHEL)

2. **Python Dependencies** - Install required packages:
   ```bash
   cd final-project/api
   pip install -r requirements.txt
   ```

## Step 1: Create the Database

1. **Start MySQL Server** (if not already running):
   ```bash
   # macOS (if installed via Homebrew)
   brew services start mysql
   
   # Linux
   sudo systemctl start mysql
   
   # Windows - Start MySQL from Services or MySQL Workbench
   ```

2. **Connect to MySQL**:
   ```bash
   mysql -u root -p
   ```
   (Enter your MySQL root password when prompted)

3. **Create the Database**:
   ```sql
   CREATE DATABASE sandwich_maker_api;
   ```

4. **Verify the database was created**:
   ```sql
   SHOW DATABASES;
   ```
   You should see `sandwich_maker_api` in the list.

5. **Exit MySQL**:
   ```sql
   EXIT;
   ```

## Step 2: Configure Database Connection

Edit the configuration file: `api/dependencies/config.py`

```python
class conf:
    db_host = "localhost"          # MySQL server host
    db_name = "sandwich_maker_api"  # Database name
    db_port = 3306                  # MySQL port (default is 3306)
    db_user = "root"                # MySQL username
    db_password = ""                 # MySQL password (set your password here)
    app_host = "localhost"
    app_port = 8000
```

**Important**: Update `db_password` with your MySQL root password (or create a dedicated MySQL user).

### Optional: Create a Dedicated MySQL User

For better security, create a dedicated MySQL user instead of using root:

```sql
-- Connect to MySQL as root
mysql -u root -p

-- Create a new user
CREATE USER 'sandwich_user'@'localhost' IDENTIFIED BY 'your_secure_password';

-- Grant privileges on the database
GRANT ALL PRIVILEGES ON sandwich_maker_api.* TO 'sandwich_user'@'localhost';

-- Apply changes
FLUSH PRIVILEGES;

-- Exit
EXIT;
```

Then update `config.py`:
```python
db_user = "sandwich_user"
db_password = "your_secure_password"
```

## Step 3: Start the Application

The application will automatically create all database tables when it starts.

1. **Navigate to the API directory**:
   ```bash
   cd final-project/api
   ```

2. **Start the FastAPI server**:
   ```bash
   python -m uvicorn main:app --reload
   ```
   
   Or if you have a startup script:
   ```bash
   python main.py
   ```

3. **Check the console output** - You should see:
   ```
   Database tables initialized successfully
   ```

   If you see an error, check:
   - MySQL server is running
   - Database name is correct
   - Username and password are correct
   - Database exists

## Step 4: Verify Database Connection

1. **Check that tables were created**:
   ```bash
   mysql -u root -p
   ```
   ```sql
   USE sandwich_maker_api;
   SHOW TABLES;
   ```

   You should see tables like:
   - `users`
   - `orders`
   - `order_details`
   - `sandwiches`
   - `resources`
   - `recipes`
   - `payments`
   - `reviews`
   - `promos`

2. **Test the API**:
   - Open your browser to: `http://localhost:8000/docs`
   - This will show the FastAPI interactive documentation (Swagger UI)
   - You can test endpoints from there

## Troubleshooting

### Error: "Can't connect to MySQL server"
- **Solution**: Make sure MySQL server is running
  ```bash
  # Check MySQL status (macOS/Linux)
  brew services list | grep mysql
  # or
  sudo systemctl status mysql
  ```

### Error: "Access denied for user"
- **Solution**: Check your username and password in `config.py`
- Verify the user has privileges: `SHOW GRANTS FOR 'your_user'@'localhost';`

### Error: "Unknown database 'sandwich_maker_api'"
- **Solution**: Create the database (see Step 1)

### Error: "Table already exists"
- **Solution**: This is normal if tables were already created. The application will continue to work.

### Tables not being created
- **Solution**: 
  1. Check the application logs for errors
  2. Verify all model files are properly imported in `model_loader.py`
  3. Make sure you have write permissions on the database

## Database Structure

The application uses SQLAlchemy ORM with the following main models:
- **User**: Customer and admin accounts
- **Order**: Customer orders
- **OrderDetail**: Items in each order
- **Sandwich**: Available sandwich types
- **Resource**: Inventory items
- **Recipe**: Recipes for sandwiches
- **Payment**: Payment information
- **Review**: Customer reviews
- **Promo**: Promotional codes

All models are defined in `api/models/` and tables are automatically created on application startup.

## Next Steps

Once your database is connected:
1. The API will be available at `http://localhost:8000`
2. API documentation at `http://localhost:8000/docs`
3. Your frontend (HTML files) can connect to the API endpoints

