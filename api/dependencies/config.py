class conf:
    # Database Configuration
    # For LOCAL database: use "localhost"
    # For REMOTE database: use the IP address of the other computer (e.g., "192.168.1.100")
    db_host = "localhost"  # Change to remote IP if connecting to another PC
    
    db_name = "sandwich_maker_api"  # Database name (should already exist on remote server)
    db_port = 3306  # MySQL port (usually 3306)
    
    # MySQL credentials
    # For remote database, get these from the person who has the database
    db_user = "root"  # MySQL username
    db_password = ""  # MySQL password
    
    # Application Configuration
    app_host = "localhost"
    app_port = 8000