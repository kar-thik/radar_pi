#!/bin/bash

# This script sets up the Radar Pi to run as a startup service and a cronjob for refreshing.

echo "Setting up Radar Pi service..."

# Get the absolute path of the project directory
PROJECT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )/.." &> /dev/null && pwd )"
CURRENT_USER=$(whoami)
SERVICE_NAME="radarpi"
SERVICE_FILE="/etc/systemd/system/${SERVICE_NAME}.service"

# The main script to run
RUN_SCRIPT="${PROJECT_DIR}/run_radar.sh"

echo "Project directory: ${PROJECT_DIR}"
echo "Run script: ${RUN_SCRIPT}"
echo "Running as user: ${CURRENT_USER}"

# Create systemd service file
echo "Creating systemd service file at ${SERVICE_FILE}"
sudo bash -c "cat > ${SERVICE_FILE}" << EOL
[Unit]
Description=Radar Pi flight data fetcher and display
After=network-online.target
Wants=network-online.target

[Service]
Type=oneshot
User=${CURRENT_USER}
WorkingDirectory=${PROJECT_DIR}
ExecStart=/bin/bash ${RUN_SCRIPT}

[Install]
WantedBy=multi-user.target
EOL

# Reload systemd, enable and start the service
echo "Reloading systemd daemon..."
sudo systemctl daemon-reload

echo "Enabling the service to run on boot..."
sudo systemctl enable ${SERVICE_NAME}.service

echo "Starting the service immediately..."
sudo systemctl start ${SERVICE_NAME}.service

echo "Service setup is complete. It will now run on boot."
echo "You can check the service status with: sudo systemctl status ${SERVICE_NAME}.service"

# Set default refresh period in minutes, or use the first argument if provided
REFRESH_PERIOD=${1:-4}

# Setup cronjob for refreshing
echo "Setting up cronjob to refresh flight data every ${REFRESH_PERIOD} minutes..."
CRON_JOB="*/${REFRESH_PERIOD} * * * * /bin/bash ${RUN_SCRIPT}"
TEMP_CRON_FILE=$(mktemp)

# Safely add the cronjob, avoiding duplicates
crontab -l > "${TEMP_CRON_FILE}" 2>/dev/null
if ! grep -q "${RUN_SCRIPT}" "${TEMP_CRON_FILE}"; then
    echo "${CRON_JOB}" >> "${TEMP_CRON_FILE}"
    crontab "${TEMP_CRON_FILE}"
    echo "Cronjob added."
else
    echo "Cronjob already exists. No changes made."
fi
rm "${TEMP_CRON_FILE}"

echo "Cronjob setup is complete."
echo "You can view your cronjobs with: crontab -l" 