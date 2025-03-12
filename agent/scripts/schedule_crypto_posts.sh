#!/bin/bash

# Set up environment
cd /home/edwardtay/SA/superior-agents/agent
source /home/edwardtay/SA/superior-agents/agent-venv/bin/activate

# Log file
LOG_FILE="/tmp/crypto_marketing_posts.log"

# Function to post and log
post_and_log() {
    echo "$(date): Running crypto marketing post script..." >> $LOG_FILE
    python scripts/crypto_marketing_post.py >> $LOG_FILE 2>&1
    echo "$(date): Finished posting." >> $LOG_FILE
    echo "----------------------------------------" >> $LOG_FILE
}

# Create log file if it doesn't exist
touch $LOG_FILE

# Post immediately
post_and_log

# Schedule future posts (uncomment to enable)
# while true; do
#     # Wait for 3 hours before posting again
#     sleep 10800
#     post_and_log
# done

echo "Posted to X. To schedule regular posts, edit this script and uncomment the scheduling loop." 