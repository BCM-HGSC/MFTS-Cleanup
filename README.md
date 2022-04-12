# minimal_hello_world

## Introduction

Managed File Transfer System (MFTS) has become cluttered with directories within our server. 
This tool that has been created will serve to archive directories along with the ability to send warning emails to our collaborators during the life cycle of the cleanup process. Upon the 4 week completion date, folders will be archived to a new directory to be stored. 

## Emails leading to cleanup


## Directory cleanup


## Registering a new share 

Invocation would look something like: 
[register new share, RT #, list email directory, start = now, config email]


## config file
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
  

## CHRON JOB
CHRON will check every RT ticket status, its current state. Will also check if it has been 24 hours since the final email was sent to begin the deletion process. 

This tool will not completley delete a directory but instead be a redirection mechanism for the directory to an external directory which will serve as an archive folder for storage. 



