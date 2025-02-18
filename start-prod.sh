#!/usr/bin/env bash
set -euo pipefail

##
# 1. Basic Setup
##
LOG_FILE=./storage/logs/startup.log
mkdir -p "$(dirname "$LOG_FILE")"
touch "$LOG_FILE"

# Helper function to log to both console and file
log() {
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" | tee -a "$LOG_FILE"
}

handle_error() {
  log "ERROR: An error occurred on line $1"
  exit 1
}

trap 'handle_error $LINENO' ERR


##
# 2. (Optional) Trust “dubious ownership” if using Git in /var/www/Zephyrus
#    - This allows Git-based composer or other commands to run without warning.
##
if [ -d .git ]; then
  log "Configuring Git safe.directory to avoid dubious ownership warnings..."
  sudo -u www-data git config --global --add safe.directory /var/www/Zephyrus \
    || log "Warning: Could not set safe.directory. Proceeding anyway..."
fi

##
# 3. Ensure no stray npm processes are running
##
log "Checking for existing npm processes..."
pkill -f npm || true


##
# 4. Install/Update Composer Dependencies
##
log "Installing/updating composer dependencies..."
composer install --no-dev --optimize-autoloader


##
# 5. Install NPM Packages & Build Production Assets with Vite
##
log "Installing npm dependencies..."
npm install

log "Building Vite assets..."
npm run build


##
# 6. Correct File Permissions
##




##
# 8. Run Migrations (Forcing in Production)
##
log "Running database migrations..."
php artisan migrate --force


##
# 9. Database Seeding
#    - Seeding is not needed in production as all data is managed separately
#    - This section is intentionally skipped
##
# Examples of seeding commands (not used):
#   php artisan db:seed --class=TestUsersSeeder --force
#   php artisan db:seed --force
#   php artisan db:seed --class=ProductionSeeder --force


##
# 10. Apache2 Checks & Restart
##
log "Checking Apache2 configuration..."
apache2ctl configtest

log "Restarting Apache2..."
systemctl restart apache2
systemctl status apache2 --no-pager | grep Active: || true


##
# 11. Clear & Rebuild Caches for Production Optimization
##
log "Clearing Laravel caches..."
php artisan config:clear
php artisan cache:clear
php artisan route:clear
php artisan view:clear

log "Optimizing Laravel..."
php artisan optimize

log "Rebuilding Laravel caches for production..."
php artisan config:cache
php artisan route:cache
php artisan view:cache


##
# 12. Final Status
##
log "Checking final status..."
# Example test: an HTTP request to confirm the site is responsive
curl -s https://demo.zephyrus.care > /dev/null || log "Warning: Could not reach site homepage."

echo "----------------------------------------"
echo "Status Summary:"
echo "----------------------------------------"
systemctl status apache2 --no-pager | grep Active:

log "Startup script completed successfully"
echo "----------------------------------------"
echo "Logs available at: $LOG_FILE"
