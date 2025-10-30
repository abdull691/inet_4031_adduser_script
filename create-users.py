#!/usr/bin/python3

# INET4031
# Author: Abdullahi
# Date Created: 30 oct
# Date Last Modified: 30 oct

"""
Automated user creation script.

This script reads user records from standard input (stdin). Each non-comment, non-empty
line should be colon-delimited with five fields:

    username:password:lastname:firstname:group1,group2

Behaviour:
- Lines beginning with '#' are treated as comments and skipped.
- Lines with fewer than 5 fields are skipped.
- The GECOS (user full name) is constructed from firstname and lastname.
- The groups field may be '-' to indicate "no supplemental groups".
- By default this version is safe: the os.system(...) calls that actually
  perform system changes are commented out so you can run a dry-run.
  To perform a real run, uncomment the os.system(...) lines (run as sudo).

Note: the instructor's original script uses interactive passwd. Many scripts use
chpasswd for non-interactive password setting; the original uses passwd via echo -ne.
"""

import os      # used to run system commands (os.system); commented out until real run
import re      # used to match comment lines beginning with '#'
import sys     # used to read lines from stdin (sys.stdin)

def main():
    # Read input line by line from stdin (input redirected from create-users.input)
    for line in sys.stdin:

        # Remove trailing newline characters but preserve other whitespace for tokenization
        line = line.rstrip('\n')

        # This regular expression checks if the line begins with '#' (a comment).
        # We treat such lines as comments and skip them so they don't create users.
        # This allows the input file to contain documentation or disabled entries.
        match = re.match(r"^#", line)

        # Split the line into fields using ':' as the delimiter.
        # The expected fields are:
        #  0: username
        #  1: password
        #  2: lastname
        #  3: firstname
        #  4: groups (comma-separated or '-' for none)
        fields = line.strip().split(':')

        # Guard clause: skip the line if it is a comment (match) OR if the number of
        # fields is not exactly 5. This prevents trying to create invalid or incomplete accounts.
        # The logic depends on the two previous operations: `match` (comment detection)
        # and `fields` (tokenization). If either indicates the line is not valid input,
        # we continue to the next line.
        if match or len(fields) != 5:
            continue

        # Extract the username and password fields. These correspond directly to the login name
        # and the plaintext password that will be set (the script later pipes this into passwd/chpasswd).
        username = fields[0]
        password = fields[1]

        # Construct the GECOS/Full Name field used by adduser. The instructor's format
        # places firstname in field index 3 and lastname in index 2, so we build "Firstname Lastname,,,"
        # which matches the expected --gecos format (GECOS fields separated by commas).
        gecos = "%s %s,,," % (fields[3], fields[2])

        # The groups field may contain multiple group names separated by commas.
        # We split that field into a Python list so we can iterate and add the user
        # to each supplemental group listed. A single '-' indicates no supplemental groups.
        groups = fields[4].split(',')

        # Informational message so operator can see progress.
        # This print is useful during both dry-runs (to show intent) and real runs.
        print("==> Creating account for %s..." % (username))

        # Build the adduser command. `--disabled-password` avoids an interactive password prompt;
        # the password will be set in a separate step. The GECOS string supplies the user's full name.
        cmd = "/usr/sbin/adduser --disabled-password --gecos '%s' %s" % (gecos, username)

        # In dry-run mode we print the command rather than executing it.
        # To perform a real run, uncomment the os.system(cmd) line below.
        print("    CMD:", cmd)
        # os.system(cmd)   # UNCOMMENT for real run (ensure you run the script with sudo)

        # Informational message about password setting.
        print("==> Setting the password for %s..." % (username))

        # The original instructor-provided method uses passwd with an echoed newline sequence.
        # This line constructs an echo that feeds the interactive passwd command. In many automated
        # scripts, chpasswd (echo "user:pass" | chpasswd) is preferred because it is more straightforward.
        # We keep the original command here but print it rather than running it so you can inspect it.
        cmd = "/bin/echo -ne '%s\n%s' | /usr/bin/sudo /usr/bin/passwd %s" % (password, password, username)
        print("    CMD:", cmd)
        # os.system(cmd)   # UNCOMMENT for real run (ensure you run the script with sudo)

        # For each group specified, if the group is not '-' (placeholder indicating no groups),
        # add the user to that group. The check `group != '-'` ensures placeholder entries are ignored.
        for group in groups:
            # Skip placeholder group markers and empty strings
            if group != '-' and group.strip() != '':
                print("==> Assigning %s to the %s group..." % (username, group))
                cmd = "/usr/sbin/adduser %s %s" % (username, group)
                print("    CMD:", cmd)
                # os.system(cmd)   # UNCOMMENT for real run (ensure you run the script with sudo)

if __name__ == '__main__':
    main()
