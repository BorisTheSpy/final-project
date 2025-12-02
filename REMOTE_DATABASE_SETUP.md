# Remote Database Connection Guide

This guide will help you connect to a MySQL database that's running on another computer (remote database).

## Overview

You need to configure:
1. **Your PC (Client)**: Update the config to point to the remote database
2. **Other Person's PC (Server)**: Configure MySQL to allow remote connections

---

## Part 1: Configure Your PC (Client Side)

### Step 1: Update Configuration File

Edit `api/dependencies/config.py` to point to the remote database:

```python
class conf:
    db_host = "192.168.1.100"        # IP address of the other person's PC
    db_name = "sandwich_maker_api"    # Database name (should already exist)
    db_port = 3306                    # MySQL port (usually 3306)
    db_user = "your_username"         # MySQL username (get this from the other person)
    db_password = "your_password"     # MySQL password (get this from the other person)
    app_host = "localhost"
    app_port = 8000
```

**What you need from the other person:**
- IP address of their computer (or hostname if on same network)
- Database name
- MySQL username
- MySQL password
- MySQL port (usually 3306)

### Step 2: Find the Remote Computer's IP Address

**On the other person's computer**, they need to find their IP address:

**Windows:**
```cmd
ipconfig
```
Look for "IPv4 Address" (e.g., 192.168.1.100)

**macOS/Linux:**
```bash
ifconfig
# or
ip addr show
```
Look for the IP address (usually starts with 192.168.x.x or 10.x.x.x)

**If on the same local network:** Use the local IP address (192.168.x.x)
**If on different networks:** You'll need their public IP address and port forwarding (more complex)

### Step 3: Test the Connection

Run the test script to verify you can connect:

```bash
cd final-project/api
python test_db_connection.py
```

---

## Part 2: Configure the Other Person's PC (Server Side)

The person with the database needs to configure MySQL to allow remote connections.

### Step 1: Enable Remote Connections in MySQL

**On the other person's computer**, they need to:

1. **Edit MySQL Configuration File**

   **Windows:**
   - Find `my.ini` in MySQL installation directory (usually `C:\ProgramData\MySQL\MySQL Server X.X\`)
   - Or use MySQL Workbench → Server → Options File

   **macOS (Homebrew):**
   ```bash
   # Edit the config file
   nano /opt/homebrew/etc/my.cnf
   # or
   nano /usr/local/etc/my.cnf
   ```

   **Linux:**
   ```bash
   sudo nano /etc/mysql/mysql.conf.d/mysqld.cnf
   # or
   sudo nano /etc/my.cnf
   ```

2. **Find and modify the `bind-address` setting:**

   Look for this line:
   ```
   bind-address = 127.0.0.1
   ```

   Change it to:
   ```
   bind-address = 0.0.0.0
   ```

   This allows MySQL to accept connections from any IP address.

   **OR** for better security, bind to a specific IP:
   ```
   bind-address = 192.168.1.100  # Their local IP address
   ```

3. **Restart MySQL Server**

   **Windows:**
   - Services → MySQL → Restart
   - Or: `net stop mysql` then `net start mysql`

   **macOS (Homebrew):**
   ```bash
   brew services restart mysql
   ```

   **Linux:**
   ```bash
   sudo systemctl restart mysql
   ```

### Step 2: Create/Configure MySQL User for Remote Access

**On the other person's computer**, connect to MySQL:

```bash
mysql -u root -p
```

Then create a user that can connect from your IP address:

```sql
-- Option 1: Allow connection from your specific IP
CREATE USER 'your_username'@'192.168.1.50' IDENTIFIED BY 'secure_password';
GRANT ALL PRIVILEGES ON sandwich_maker_api.* TO 'your_username'@'192.168.1.50';
FLUSH PRIVILEGES;

-- Option 2: Allow connection from any IP on local network (less secure)
CREATE USER 'your_username'@'192.168.1.%' IDENTIFIED BY 'secure_password';
GRANT ALL PRIVILEGES ON sandwich_maker_api.* TO 'your_username'@'192.168.1.%';
FLUSH PRIVILEGES;

-- Option 3: Allow connection from any IP (least secure, use only on trusted networks)
CREATE USER 'your_username'@'%' IDENTIFIED BY 'secure_password';
GRANT ALL PRIVILEGES ON sandwich_maker_api.* TO 'your_username'@'%';
FLUSH PRIVILEGES;
```

**Replace:**
- `your_username` - The username you want to use
- `192.168.1.50` - Your PC's IP address
- `secure_password` - A strong password
- `192.168.1.%` - Allows any IP starting with 192.168.1 (same subnet)

### Step 3: Configure Firewall

**On the other person's computer**, allow MySQL through the firewall:

**Windows:**
1. Open Windows Defender Firewall
2. Advanced Settings → Inbound Rules → New Rule
3. Port → TCP → 3306 → Allow connection
4. Apply to all profiles

**macOS:**
```bash
# If using built-in firewall
sudo /usr/libexec/ApplicationFirewall/socketfilterfw --add /usr/local/mysql/bin/mysqld
sudo /usr/libexec/ApplicationFirewall/socketfilterfw --unblockapp /usr/local/mysql/bin/mysqld
```

**Linux (UFW):**
```bash
sudo ufw allow 3306/tcp
sudo ufw reload
```

**Linux (firewalld):**
```bash
sudo firewall-cmd --permanent --add-port=3306/tcp
sudo firewall-cmd --reload
```

---

## Part 3: Testing the Connection

### From Your PC:

1. **Test basic connectivity:**
   ```bash
   # Test if you can reach the MySQL port
   telnet 192.168.1.100 3306
   # or
   nc -zv 192.168.1.100 3306
   ```

2. **Test MySQL connection:**
   ```bash
   mysql -h 192.168.1.100 -u your_username -p sandwich_maker_api
   ```

3. **Run the Python test script:**
   ```bash
   cd final-project/api
   python test_db_connection.py
   ```

---

## Troubleshooting

### Error: "Can't connect to MySQL server on '192.168.1.100'"

**Possible causes:**
1. MySQL not configured for remote access (`bind-address` still set to 127.0.0.1)
2. Firewall blocking port 3306
3. Wrong IP address
4. MySQL server not running on remote PC

**Solutions:**
- Verify MySQL is running on remote PC
- Check `bind-address` in MySQL config
- Verify firewall allows port 3306
- Ping the remote IP: `ping 192.168.1.100`

### Error: "Access denied for user"

**Possible causes:**
1. User doesn't have permission to connect from your IP
2. Wrong username or password
3. User was created for 'localhost' only

**Solutions:**
- Verify user was created with `@'your_ip'` or `@'%'`
- Check username and password in config.py
- Have the other person verify: `SELECT user, host FROM mysql.user;`

### Error: "Host 'xxx.xxx.xxx.xxx' is not allowed to connect"

**Solution:** The MySQL user needs to be created with your IP address or `%`:
```sql
-- On remote MySQL server
CREATE USER 'username'@'your_ip_address' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON sandwich_maker_api.* TO 'username'@'your_ip_address';
FLUSH PRIVILEGES;
```

### Connection works but tables don't exist

**Solution:** The database exists but tables haven't been created. Start your API server and it will create them automatically:
```bash
cd final-project/api
python -m uvicorn main:app --reload
```

---

## Security Best Practices

1. **Use specific IP addresses** instead of `%` when possible
2. **Use strong passwords** for database users
3. **Create dedicated users** with only necessary privileges
4. **Use VPN** if connecting over the internet (not just local network)
5. **Consider SSH tunneling** for additional security:
   ```bash
   ssh -L 3306:localhost:3306 user@remote-pc
   ```
   Then connect to `localhost:3306` from your application

---

## Quick Reference

**Your config.py should look like:**
```python
class conf:
    db_host = "192.168.1.100"        # Remote PC's IP
    db_name = "sandwich_maker_api"
    db_port = 3306
    db_user = "remote_user"          # Username created on remote MySQL
    db_password = "remote_password"  # Password for that user
    app_host = "localhost"
    app_port = 8000
```

**Remote MySQL user should be:**
```sql
CREATE USER 'remote_user'@'your_ip' IDENTIFIED BY 'remote_password';
GRANT ALL PRIVILEGES ON sandwich_maker_api.* TO 'remote_user'@'your_ip';
FLUSH PRIVILEGES;
```

