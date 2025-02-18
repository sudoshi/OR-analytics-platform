#!/bin/bash

# Exit immediately on error and print each command (for debugging)
set -e
set -x

# Setup logging
LOG_FILE="./storage/logs/shutdown.log"
mkdir -p ./storage/logs
touch "$LOG_FILE"

log () {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# Ensure script is run as root
if [ "$EUID" -ne 0 ]; then
    log "Please run as root (sudo)"
    exit 1
fi

# Clear Laravel caches
log "Clearing Laravel caches..."
php artisan config:clear
php artisan cache:clear
php artisan route:clear
php artisan view:clear

# Kill any existing npm processes
log "Stopping npm processes..."
pkill -f npm || true

# Gracefully restart Apache (this ensures current requests are completed)
log "Gracefully restarting Apache..."
systemctl reload apache2

log "Shutdown script completed successfully"
echo "----------------------------------------"
echo "Shutdown completed"
echo "Logs available at: $LOG_FILE"
