# rainbowtables

For Python 2.7.x

* Edit (or leave defaults) config.txt to configure rainbow tables
* Run generateTables.py to generate the rainbow tables
* Run crack.py for crack instructions, or with flags:
    * -test to run through prebuilt array of passwords
    * -password password_to_be_cracked to hash that password and search for it in the tables
    * -hash md5_hash_of_password_to_be_cracked to search for that hash's plaintext