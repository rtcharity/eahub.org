# Data Protection Policy

The production database access is granted only to the people who require it.

The eahub.org website administrators who are able to approve or delete profiles are granted only profiles data accesses, which doesn't include user passwords or their hashes.

### Production Database Access Management

Administrators credentials which grant direct access to the production database must follow the following guidelines: 
- Passwords must be generated out of random characters and be 64+ symbols long.
- Passwords must be stored in a separate password manager database, which is decrypted only when the production database access is required.
- SSH access to the running production server must use a separate EA Hub ssh key that can be decrypted only by a password that satisfies the aforementioned criteria.
- Two-Factor Authentication must be enabled when it is possible.
- Passwords must be renewed every 12 months, which is managed through an assigned ticket with a due date.

Access sharing guidelines:
- Passwords sharing request must be initiated only though a video call.
- Passwords must be transferred only as a text document in an encrypted archive, using a end-to-end encrypted communication channel. The password to the archive must be shared through a different communication channel.

### Backups Management

The hosting provider is creating a backup each morning (04:00 GMT) and stores up to 7 backups at a time.

An export of the database and media files is done by the end of each month. That backup is encrypted with a secure password and uploaded to a private google folder. By the end of each backup the security of the resulting file is confirmed by at least two lead developers.

The monthly backups are stored for 6 months only.
