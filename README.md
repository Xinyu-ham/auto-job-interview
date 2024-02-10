# auto-job-interview
## Installation
If you are using MacOS, switch to the `macos` branch
```bash
pip install -r requirements.txt
```
## Usage
0. Ensure you have your OpenAI API key stored in environment variable as `OPENAI_API_KEY`
    ```bash
    export OPENAI_API_KEY = <your api key here>
    ```
1. Create a file named `job_description.txt` in the `tmp` directory of the project.
2. Run the following command:

    Windows:
    ```bash
    python -m main
    ```
    MacOS
    ```bash
    python3 -m main
    ```
    (Optional) You can also configure interview with arguments
    ```bash
    python -m main --voice shimmer --rounds 3
    ```
