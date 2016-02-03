
ABSOLUTE_PATH=`readlink -f run.sh`
ABSOLUTE_PATH_OF_DIR=`dirname ${ABSOLUTE_PATH}`

EXEC_CMD="cd ${ABSOLUTE_PATH_OF_DIR}; ./run.sh 2>>pttMailChecker.log | mail -s '[pttMailChecker] Notification' sample@sample.com"

# get current crontab
crontab -l > cron_jobs.tmp

# add the task
echo "00 08,20 * * * ${EXEC_CMD}" >> cron_jobs.tmp

# install cron jobs from file
crontab cron_jobs.tmp

# remove temporary files
rm -f cron_jobs.tmp

