# MFTS-Cleanup

## Introduction

Managed File Transfer System (MFTS) has become cluttered with directories within our server. 
This tool that has been created will serve to archive directories along with the ability to send warning emails to our collaborators during the life cycle of the cleanup process. Upon the 4 week completion date, folders will be archived to a new directory to be stored. 

## Emails leading to cleanup


## Directory cleanup
- 1 week until clean up (3 weeks since rt creation)
- 48 hrs until cleanup (3 weeks and 4 days from rt creation)
- 24 hrs until cleanup (3 weeks and 6 days from rt creation)


## Registering a new share 

Invocation would look something like:

`register-new-share CONFIG_FILE_PATH RT_NUMBER SHARE_DIRECTORY_PATH EMAIL [EMAIL]...`


## Config file

A YAML file will contain the following:

```yaml
metadata_root: PATH/TO/METADATA/ROOT
email:
    from_address: SENDER@bcm.edu
    host: SMTP.SERVER.DOMAIN
logging:
    level: INFO
    ...
```
where will memory occur? --> specify using a command
- Directory used will be archived into a new directory. 
  - will have a new naming convention
  - RT#____first_email.yaml 
      -  1 week warning
  - RT#____second_email.yaml 
      -  48 hr warning
  - RT#____24hr_final_email.yaml
      -  24 hr warning
  - RT#_____deleted_email.yaml
      -  Email has now been deleted.
  

## CRON JOB
CRON will check every RT ticket status, its current state. Will also check if it has been 24 hours since the final email was sent to begin the deletion process. 

Example cron command:

`auto-cleanup-shares CONFIG_FILE_PATH`

## Metadata Root Layout

- active
    - 5678_initial.yaml
    - 5678_first_email.yaml
    - ...
- archive
    - 1234_initial.yaml
    - 1234_first_email.yaml
    - 1234_second_email.yaml
    - 1234_final_email.yaml
    - 1234_cleanup.yaml
    - ...
