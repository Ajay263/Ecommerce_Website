# Ecommerce_Website


## How to install stripe cli



1. Download the latest Linux tar.gz file:
   - Go to the Stripe CLI GitHub releases page: https://github.com/stripe/stripe-cli/releases
   - Look for the latest version with "linux" in the filename, ending with ".tar.gz"
   - Download this file to your computer

2. Unzip the file:
   - Open a terminal window
   - Navigate to the directory where you downloaded the file
   - Run the command: `tar -xvf stripe_X.X.X_linux_x86_64.tar.gz`
   - Replace X.X.X with the actual version number of the file you downloaded
   - This command extracts the contents of the tar.gz file

3. Move `./stripe` to your execution path:
   - After extraction, you'll have a `stripe` executable file
   - You need to move this file to a directory in your system's PATH
   - A common location is `/usr/local/bin`
   - Use this command: `sudo mv ./stripe /usr/local/bin/`
