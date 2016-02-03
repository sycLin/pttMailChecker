# pttMailChecker
creates cron job to check PTT messages twice a day and sends email as notification.

- [x] 8:00 am & 8:00 pm

## Usage
Four steps, from nothing to everything! :+1:

### step 1
Clone the repository with: `$git clone https://github.com/sycLin/pttMailChecker.git`

### step 2
Configure PTT account.

Find the file `pttMailChecker.config`, and fill in your PTT account information.
```shell
USERNAME=<your_id>
PASSWORD=<your_password>
```

### step 3
Configure the address to which the notification emails will be sent.

Find the file `setup.sh`, and fill in your email address.
```shell
EXEC_CMD="cd ${ABSOLUTE_PATH_OF_DIR}; ...... sample@sample.com"
```
(replace the `sample@sample.com` with your email address.)

### step 4
Finally, use:
```shell
./setup.sh
```
It will create a cron job and check twice every day.

## Related Techniques
- [x] shell scripts
- [x] crontab / cron job knowledge
- [x] `mail` command
- [x] python scripts (`telnetlib` module)
- [x] PTT encodings

## To go further :fast_forward: :fast_forward:

### customize the time and frequency of checking
The checking is done by the Python script `pttMailChecker.py`, 
but the time and frequency settings are in `setup.sh` where the cron job is created.

To have your custom settings, revise something inside `setup.sh` if you're familiar with `crontab`.

If you know little about `crontab` command, read [this](http://linux.vbird.org/linux_basic/0430cron.php) for help.

### contribute to this repository/project
Everyone is welcomed to enhance pttMailChecker.

If you have any ideas of improving the structure, functionality, and implementation, contact me at once!
