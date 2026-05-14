# Deployment & Production Guide

## Production Checklist

- [ ] Update environment variables
- [ ] Configure database for production
- [ ] Set up HTTPS/SSL
- [ ] Configure CORS for production domain
- [ ] Set up logging and monitoring
- [ ] Configure backups
- [ ] Load testing completed
- [ ] Security audit passed
- [ ] Documentation updated

---

## Deployment Options

### Option 1: Local Network Deployment

**Setup:**
```bash
# On server machine
cd backend
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate
pip install -r requirements.txt
python run.py

# On frontend (same or different machine)
cd frontend
npm install
npm run build
npm install -g serve
serve -s build -l 3000
```

**Network Access:**
- Get server IP: `ipconfig` (Windows) or `ifconfig` (Linux/Mac)
- Access from other machines: `http://<SERVER_IP>:3000`

---

### Option 2: Docker Deployment

**Build and Run:**
```bash
# Build images
docker-compose build

# Start containers
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

**Docker Benefits:**
- ✅ Consistent environment
- ✅ Easy scaling
- ✅ Simple deployment
- ✅ Isolated dependencies

---

### Option 3: Cloud Deployment (AWS)

#### Deploy Backend (Lambda + RDS)

```bash
# Install AWS CLI
pip install awscli

# Configure AWS
aws configure

# Create Lambda function
aws lambda create-function \
  --function-name finance-insights-backend \
  --runtime python3.10 \
  --role arn:aws:iam::YOUR_ACCOUNT:role/lambda-role \
  --handler run.app

# Set up RDS database
aws rds create-db-instance \
  --db-instance-identifier finance-insights-db \
  --db-instance-class db.t3.micro \
  --engine mysql
```

#### Deploy Frontend (S3 + CloudFront)

```bash
# Build frontend
cd frontend && npm run build

# Upload to S3
aws s3 sync build/ s3://finance-insights-frontend/

# Create CloudFront distribution
aws cloudfront create-distribution \
  --origin-domain-name finance-insights-frontend.s3.amazonaws.com
```

---

### Option 4: Heroku Deployment

#### Backend

```bash
# Install Heroku CLI
npm install -g heroku

# Login to Heroku
heroku login

# Create app
heroku create finance-insights-backend

# Add PostgreSQL addon
heroku addons:create heroku-postgresql:hobby-dev

# Deploy
git push heroku main
```

#### Frontend

```bash
# Create frontend app
heroku create finance-insights-frontend

# Deploy (frontend uses buildpack)
git subtree push --prefix frontend heroku main
```

---

### Option 5: On-Premises Server

#### Linux (Ubuntu/Debian)

```bash
# Update system
sudo apt-get update && sudo apt-get upgrade

# Install Python 3.10
sudo apt-get install python3.10 python3.10-venv python3-pip

# Install Node.js
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install nodejs

# Clone project
git clone <repo-url>
cd finance-insights

# Setup backend
cd backend
python3.10 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Setup frontend
cd ../frontend
npm install
npm run build

# Setup systemd service (for auto-start)
sudo nano /etc/systemd/system/finance-insights.service
```

**Systemd Service File:**
```ini
[Unit]
Description=Finance Insights Backend
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/home/www-data/finance-insights/backend
ExecStart=/home/www-data/finance-insights/backend/venv/bin/python run.py
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
# Enable and start service
sudo systemctl daemon-reload
sudo systemctl enable finance-insights
sudo systemctl start finance-insights
```

---

### Option 6: Windows Server

```batch
# Install Python 3.10 (from python.org)
# Install Node.js (from nodejs.org)

# Create backend service
cd backend
python -m venv venv
call venv\Scripts\activate.bat
pip install -r requirements.txt

# Create batch file: start_backend.bat
@echo off
cd backend
call venv\Scripts\activate.bat
python run.py
```

**Install as Windows Service:**
```bash
# Using NSSM (Non-Sucking Service Manager)
nssm install FinanceInsightsBackend "C:\path\to\start_backend.bat"
nssm start FinanceInsightsBackend
```

---

## Production Configuration

### Backend (run.py) - Production Setup

```python
import os
from app import create_app

if __name__ == '__main__':
    app = create_app()
    
    # Production settings
    if os.getenv('FLASK_ENV') == 'production':
        # Use production server (gunicorn, waitress, etc)
        from waitress import serve
        serve(app, host='0.0.0.0', port=5000)
    else:
        # Development server
        app.run(debug=False, host='0.0.0.0', port=5000)
```

### Production Requirements

```bash
# Add to requirements.txt for production
gunicorn==20.1.0  # or waitress==2.1.0
python-dotenv==0.21.0  # for environment variables
```

### Environment Variables (Production)

```bash
# .env (production)
FLASK_ENV=production
FLASK_DEBUG=False
DATABASE_URL=postgresql://user:pass@prod-db:5432/finance_insights
CORS_ORIGINS=https://yourdomain.com
SECRET_KEY=your-secret-key-here
LOG_LEVEL=INFO
```

---

## Database Setup for Production

### PostgreSQL (Recommended for Production)

```bash
# Install PostgreSQL
sudo apt-get install postgresql postgresql-contrib  # Linux
# or download from postgresql.org (Windows/Mac)

# Create database
createdb finance_insights

# Create user
createuser finance_user
psql -c "ALTER USER finance_user WITH PASSWORD 'secure_password';"

# Grant permissions
psql -c "GRANT ALL PRIVILEGES ON DATABASE finance_insights TO finance_user;"

# Update connection string
DATABASE_URL=postgresql://finance_user:secure_password@localhost/finance_insights
```

### MySQL/MariaDB

```bash
# Install MySQL
sudo apt-get install mysql-server  # Linux

# Create database
mysql -u root -p -e "CREATE DATABASE finance_insights;"

# Create user
mysql -u root -p -e "CREATE USER 'finance_user'@'localhost' IDENTIFIED BY 'password';"

# Grant permissions
mysql -u root -p -e "GRANT ALL PRIVILEGES ON finance_insights.* TO 'finance_user'@'localhost';"

# Update connection string
DATABASE_URL=mysql+pymysql://finance_user:password@localhost/finance_insights
```

---

## SSL/HTTPS Setup

### Using Let's Encrypt (Free)

```bash
# Install Certbot
sudo apt-get install certbot python3-certbot-nginx

# Get certificate
sudo certbot certonly --nginx -d yourdomain.com

# Auto-renew
sudo certbot renew --dry-run
```

### Nginx Configuration

```nginx
server {
    listen 443 ssl;
    server_name yourdomain.com;

    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;

    location /api/ {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location / {
        proxy_pass http://localhost:3000;
    }
}
```

---

## Monitoring & Logging

### Application Monitoring

```python
# backend/app/__init__.py - Add logging

import logging
from logging.handlers import RotatingFileHandler

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        RotatingFileHandler('app.log', maxBytes=1024*1024, backupCount=10),
        logging.StreamHandler()
    ]
)
```

### Performance Monitoring

```python
# Add to routes for timing
import time

@app.before_request
def before_request():
    g.start = time.time()

@app.after_request
def after_request(response):
    elapsed = time.time() - g.start
    logger.info(f"Request took {elapsed:.2f}s - {request.path}")
    return response
```

### Database Backups

```bash
# PostgreSQL backup
pg_dump finance_insights > backup_$(date +%Y%m%d).sql

# Schedule daily backup (cron)
0 2 * * * pg_dump finance_insights > /backups/backup_$(date +\%Y\%m\%d).sql
```

---

## Performance Optimization

### Backend Optimization

```python
# Enable query result caching
from flask_caching import Cache

cache = Cache(app, config={'CACHE_TYPE': 'simple'})

@app.route('/api/dashboard/stats')
@cache.cached(timeout=300)  # Cache for 5 minutes
def get_dashboard_stats():
    ...
```

### Database Optimization

```sql
-- Add indexes for common queries
CREATE INDEX idx_payment_customer_id ON payments(customer_id);
CREATE INDEX idx_payment_status ON payments(status);
CREATE INDEX idx_payment_due_date ON payments(due_date);
CREATE INDEX idx_customer_risk ON customers(risk_score);
```

### Frontend Optimization

```bash
# Build optimized frontend
cd frontend
npm run build

# Gzip compression (in Nginx)
gzip on;
gzip_types text/plain text/css text/javascript application/json;
```

---

## Scaling Strategy

### Horizontal Scaling

```bash
# Run multiple backend instances with load balancer
# Load Balancer (Nginx) → API 1, API 2, API 3
# ↓
# Database (PostgreSQL)
```

### Vertical Scaling

- Increase server resources (CPU, RAM)
- Optimize database queries
- Add caching layer (Redis)
- Use CDN for static files

### High Availability

```yaml
# Docker Swarm / Kubernetes
version: '3.9'
services:
  backend:
    image: finance-insights-backend
    deploy:
      replicas: 3
      placement:
        constraints: [node.role == worker]
```

---

## Rollback Strategy

```bash
# Keep previous versions
git tag release-v1.0
git tag release-v1.1

# Rollback to previous version
git checkout release-v1.0
docker-compose up --build

# Database migration rollback
alembic downgrade -1
```

---

## Disaster Recovery

### Backup Strategy
- Daily database backups
- Weekly full system backups
- Off-site backup storage
- Regular restore tests

### Recovery Plan
- RTO (Recovery Time Objective): < 1 hour
- RPO (Recovery Point Objective): < 24 hours
- Document recovery procedures
- Test recovery regularly

### Disaster Recovery Site
- Standby environment
- Regular synchronization
- Failover procedures
- Communication plan

---

## Security Hardening

### Backend Security

```python
# Enable security headers
@app.after_request
def set_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    return response
```

### Database Security
- Use strong passwords
- Implement row-level security
- Encrypt sensitive data
- Regular security updates

### File Upload Security
```python
# Validate file types and sizes
ALLOWED_EXTENSIONS = {'xlsx', 'xls'}
MAX_FILE_SIZE = 16 * 1024 * 1024  # 16MB

def validate_upload(file):
    if file.size > MAX_FILE_SIZE:
        raise ValueError("File too large")
    if not file.filename.endswith(('.xlsx', '.xls')):
        raise ValueError("Invalid file type")
```

---

## Maintenance Schedule

### Daily
- Monitor logs
- Check disk space
- Verify backups completed

### Weekly
- Review performance metrics
- Check for security updates
- Test backup restoration

### Monthly
- Update dependencies
- Review and archive logs
- Disaster recovery drills
- Security audit

### Quarterly
- Full system audit
- Performance optimization
- Capacity planning
- Compliance review

---

## Troubleshooting Production Issues

### High CPU Usage
```bash
# Identify process
top -p $(pgrep -f "python run.py")

# Check database queries
SELECT * FROM pg_stat_statements ORDER BY mean_time DESC LIMIT 10;
```

### Database Connection Issues
```bash
# Test connection
psql -h localhost -U finance_user -d finance_insights

# Check active connections
SELECT count(*) FROM pg_stat_activity;
```

### Disk Space Issues
```bash
# Check disk usage
df -h

# Clean old backups
rm /backups/backup_*.sql -mtime +30

# Archive old logs
tar -czf logs_archive_$(date +%Y%m).tar.gz *.log
```

---

## Migration from Development to Production

```bash
# 1. Export data from development
pg_dump dev_finance_insights > migration.sql

# 2. Create production database
createdb finance_insights_prod

# 3. Import data
psql finance_insights_prod < migration.sql

# 4. Update connection strings
# Update DATABASE_URL in .env

# 5. Verify
curl http://production-server:5000/api/analysis/summary

# 6. Update frontend API URL
# REACT_APP_API_URL=https://api.yourdomain.com

# 7. Test thoroughly
```

---

## Post-Deployment Checklist

- [ ] All API endpoints tested and working
- [ ] Database backed up
- [ ] SSL certificate valid
- [ ] Monitoring and logging active
- [ ] Email notifications configured
- [ ] Support documentation updated
- [ ] Incident response plan ready
- [ ] Team trained on procedures
- [ ] Performance baseline established
- [ ] Security audit completed

---

## Support & Incident Response

### Incident Severity Levels

| Level | Response Time | Example |
|-------|---|---------|
| Critical | 15 minutes | Database down |
| High | 1 hour | API errors |
| Medium | 4 hours | UI issues |
| Low | 1 day | Documentation |

### Escalation Path
1. Application Team
2. Database Administrator
3. Infrastructure Team
4. Vendor Support

---

## References

- [Gunicorn Documentation](https://gunicorn.org/)
- [Flask Production Deployment](https://flask.palletsprojects.com/en/2.3.x/deploying/)
- [PostgreSQL Administration](https://www.postgresql.org/docs/current/admin.html)
- [Nginx Documentation](https://nginx.org/en/docs/)
- [Let's Encrypt](https://letsencrypt.org/)
- [Docker Documentation](https://docs.docker.com/)

---

**Ready for production? Follow this guide carefully! 🚀**
