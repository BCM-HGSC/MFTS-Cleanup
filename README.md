# MFTS-Cleanup

## Introduction

Managed File Transfer System (MFTS) has become cluttered with directories within our server.
This tool that has been created will serve to archive directories along with the ability to send warning emails to our collaborators during the life cycle of the cleanup process. Upon the 4 week completion date, folders will be archived to a new directory to be stored.


## Directory cleanup
- 1 week until clean up (3 weeks since rt creation)
- 48 hrs until cleanup (3 weeks and 4 days from rt creation)
- 24 hrs until cleanup (3 weeks and 6 days from rt creation)


## Registering a new share

Invocation would look something like:

`register-new-share PATH/TO/METADATA/ROOT SPONSOR_ID RT_NUMBER SHARE_DIRECTORY_PATH [EMAIL...]`


## Config file

A YAML file will contain the following:
Location: PATH/TO/METADATA/ROOT/config.yaml

```yaml
email:
  from_address: SENDER@bcm.edu
  host: SMTP.SERVER.DOMAIN
sponsors:  # Maps sponsor_id to sponsor_email for known sponsors
  - sponsor1: first_name.last_name1@bcm.edu
  - sponsor2: first_name.last_name2@bcm.edu
logging:
    level: INFO
    ...
```

## Emails leading to cleanup

- Directory used will be archived into a new directory.
  - will have a new naming convention:
    - rt{rt_number}_0000.yaml
        -  initial state
    - rt{rt_number}_0001.yaml
        -  1 week warning
    - rt{rt_number}_0002.yaml
        -  48 hr warning
    - rt{rt_number}_0003.yaml
        -  24 hr warning
    - rt{rt_number}_0004.yaml
        -  Data has now been deleted.


## CRON JOB
CRON will check every RT ticket status, its current state. Will also check if it has been 24 hours since the final email was sent to begin the deletion process.

Example cron command:

`auto-cleanup-shares CONFIG_FILE_PATH`

## Metadata Root Layout

Files will be organized by the following possible files:

- rt{rt_number}_0000.yaml
    - A new share has been recorded by creating this file along with its registration date.
- rt{rt_number}_0001.yaml
    - First email will be sent 3 weeks after the share has been registered along with the creation of this file.
- rt{rt_number}_0002.yaml
    - A second email will be sent 3 weeks and 4 days after registration date along with the creation of this file.
- rt{rt_number}_0003.yaml
    - A final email will be sent 3 weeks and 6 days after registration date along with the creation of this file.
- rt{rt_number}_0004.yaml
    - 4 weeks after registration, a cleanup file will be created followed by the cleaning up of the directory.


## Shares will be categorized by the two following directories:

- # active
    - rt5678_0000.yaml
    - rt5678_0001.yaml
    - ...
- # archive
    - rt1234_0000.yaml
    - rt1234_0001.yaml
    - rt1234_0002.yaml
    - rt1234_0003.yaml
    - rt1234_0004.yaml
    - ...
