
# How to Reproduce the Project


## Prerequisites
- **Python**

    Ensure you have Python installed on your system.

- **Django**

     This project requires Django 5. Install it using pip if you haven’t done so.

- **Stripe Account**
     Create an account on Stripe by following this link: [Stripe Signup](https://dashboard.stripe.com/register).

## Setup Instructions

1. **Create a `.env` File**

   - Create a file named `.env` in your project root.
   - Add the necessary environment variables to this file. (Below I have addded a code snipet to show  specific variables needed.)

2. **Install Stripe CLI**:
   - Follow these steps to install the Stripe CLI:
     1. **Download the Latest Linux Tar.gz File**:
        - Go to the Stripe CLI GitHub releases page: [Stripe CLI Releases](https://github.com/stripe/stripe-cli/releases).
        - Download the latest version with "linux" in the filename (ending with ".tar.gz").
     2. **Unzip the File**:
        - Open a terminal and navigate to the download directory.
        - Run the command:
          ```bash
          tar -xvf stripe_X.X.X_linux_x86_64.tar.gz
          ```
          (Replace `X.X.X` with the actual version number.)
     3. **Move the Stripe Executable**:
        - Move the `stripe` executable to your execution path:
          ```bash
          sudo mv ./stripe /usr/local/bin/
          ```

3. **Create a Virtual Environment**:
   - Create a virtual environment using:
     ```bash
     python -m venv venv
     ```
   - Activate the virtual environment:
     - On Windows:
       ```bash
       venv\Scripts\activate
       ```
     - On macOS/Linux:
       ```bash
       source venv/bin/activate
       ```

4. **Install Requirements**:
   - Install the project dependencies:
     ```bash
     pip install -r requirements.txt
     ```

5. **Run Docker Compose**:
   - Start the application with Docker:
     ```bash
     docker-compose up
     ```

6. **Run Celery Worker**:
   - After everything is running, start the Celery worker:
     ```bash
     celery -A myshop worker -l info
     ```

7. **Run Django**:
   -    ```bash
         python manage.py makemigrations

         python manage.py migrate

         python manage.py runserver
         
     ```





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
