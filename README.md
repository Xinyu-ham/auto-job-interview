![pip installation](svg/python3_ver.svg)
<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://www.notion.so/workmate/Recommendation-system-19a5c980e65f4b879dcb9fdf5dfe1f81">
    <img src="https://static.thenounproject.com/png/1237093-200.png" alt="Logo" width="120" height="120">
  </a>

  <h3 align="center">Automated job interview simulation</h3>

  <p align="center">
    Practice doing job interview with AI
    <br />
    <a href="#infra-overview"><strong>Explore the docs »</strong></a>
    <br />
    <br />
  </p>
</div>

## Installation
```bash
python -m install
```

*Note: Installer should automatically detect your OS, if not:*
```bash
pip install -r requirements/<your OS>.txt
```
If windows, your OS should be `windows` else `macos`
## Usage
0. Ensure you have your OpenAI API key stored in environment variable as `OPENAI_API_KEY`
    ```bash
    export OPENAI_API_KEY="<your api key here>"
    ```
1. Create a file named `job_description.txt` in the `tmp` directory of the project.
2. Run the following command:
    
    > NOTE: `--input-ui` can be either `text` or `voice`, voice is currently WIP and not available

    Windows:
    ```bash
    python -m main --input-ui text
    ```
    MacOS
    ```bash
    python3 -m main --input-ui text
    ```
    (Optional) You can also configure interview with arguments
    ```bash
    python -m main --input-ui text --voice shimmer --rounds 3
    ```

