# Data Protection Policy

## Access roles  
Access to the user database is given to team members based on what is minimally required for them to fulfil their roles.
Roles and data access
* Profile Reviewers - responsible for approval or rejection of user profiles
  * Emails
  * Private users’ profiles
* Website Administrators - responsible for eahub.org management
  * All of the above
  * Profile update logs
* Technical Administrators
  * All of the above
  * Passwords (hashed with pbkdf2_sha256)
  * IP addresses

## Production Database Access Management
Technical Administrators’ credentials which grant direct access to the production database must follow the following guidelines:
  * Passwords must have 130+ bits of entropy.
  * Passwords must be stored in a password manager database.
  * SSH access to the running production server must use a separate EA Hub ssh key that can be decrypted only by a password that satisfies the aforementioned criteria.
  * Two-Factor Authentication must be enabled when it is possible.
  * Passwords must be renewed every 12 months, which is managed through an assigned ticket with a due date.
Access sharing guidelines:
* Passwords sharing requests must be confirmed via a video call.
* Passwords must be transferred only as a text document in an encrypted archive, using an end-to-end encrypted communication channel. The password to the archive must be shared through a different communication channel.

## Backups Management
* The hosting provider is creating a backup each morning (04:00 GMT) and stores up to 7 backups at a time.
* An export of the database and media files is done by the end of each month. That backup is encrypted with a secure password and uploaded to a secure hosting platform. By the end of each backup the security of the resulting file is confirmed by at least two lead developers.
* The monthly backups are stored for 6 months only.
