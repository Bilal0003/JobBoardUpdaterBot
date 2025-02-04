
# JobBoardUpdaterBot

This project automates navigation to the APEC website using Selenium. It loads environment variables from a 

.env

 file and configures Chromium in headless mode for cloud environments.

## Prerequisites

- **Python 3.x**  
- **Google Chrome** installed (or a compatible Chromium-based browser).
- **pip** for package management.

## Installation

1. **Clone the repository** (if not already done).
2. **Create and activate a virtual environment**:

   ```sh
   python -m venv venv
   # Activate on Linux/macOS:
   source venv/bin/activate
   # Activate on Windows:
   venv\Scripts\activate
   ```

3. **Install the dependencies**:

   ```sh
   pip install -r requirements.txt
   ```

## Configuration

- Place your environment variables (for example, email and password) in a 

.env

 file located at the root of the project.  
- The project uses [python-dotenv](https://pypi.org/project/python-dotenv/) to load these variables automatically.  
- Example 

.env

 layout:

  ```env
  EMAIL=your_email@example.com
  PASSWORD=your_secret_password
  ```

## Usage

- The main code is in 

main.py

. The primary function `NavigateFunction` sets up the Chrome driver with cloud-friendly options, navigates to "https://www.apec.fr", waits for certain elements to be visible/invisible, and interacts with the page.
- To run the project, execute:

  ```sh
  python main.py
  ```


- For automation on Linux/Mac environments, run :
   ``crontab -e`` and add the following line, to execute at 8h45 everyday:
   ```sh
   45 08 * * * /home/bilal0003/Projects/JobBoardUpdaterBot/automate.sh >> /home/bilal0003/Projects/JobBoardUpdaterBot/logfile.log 2>&1
   ```
   the ouput is logged to ``logfile.log``


   

## Project Structure

```
.env
.gitignore
automate.sh
logfile.log
main.py
requirements.txt
steps.md
venv/
├── bin/
├── include/
├── lib/
│   └── python3.10/
│       └── site-packages/
└── lib64
```

- **main.py**: Contains the automation logic and Selenium configuration.
- **requirements.txt**: Lists all necessary Python packages (including Selenium and python-dotenv).
- **steps.md**: Contains additional documentation or step-by-step instructions.
- **automate.sh**: Shell script that can be used to run or deploy the project.

## Additional Information

- The project is structured for ease of deployment in cloud environments as it configures Chrome to run in headless mode and includes settings such as `--no-sandbox` and `--disable-dev-shm-usage`.
- Refer to the inline comments in 

main.py

 (specifically around `NavigateFunction`) for details on how the site's navigation and element handling are implemented.

---

