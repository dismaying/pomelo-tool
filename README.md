# Pomelo Tool

This script checks a list of usernames for Discord's pomelo update. It handles rate limits and supports using a proxy for anonymous requests.

## Features

- **Handle Rate Limits**: Manages server rate limits for continuous checking.
- **Proxy Support**: Enables anonymous requests using proxies.

## Prerequisites

- **Python 3.10**: Download and install [Python 3.10](https://www.python.org/downloads/release/python-31011/).
- It's highly recommended to use a Python environment:
  - **Linux**: `python -m venv .env` then `source .env/bin/activate`
  - **Windows**: `python -m venv .env` then `.\.env\Scripts\activate`

## Setup

1. `git clone https://github.com/subpoen-a/pomelo-tool`
2. `pip install -r requirements.txt`
3. Change the `.env.example` to `.env` after modifying the variables.

## Usage

1. Add the usernames to check in `words.txt`, one per line.
2. Run the script `python main.py`.
3. The script will check the usernames and display the results.

## Configuration

- **Discord Token**: Get a Discord token and set it in the `.env` file.
- **Proxy**: If needed, set your proxy details in the `.env` file.

## Download Python

- **Mac**: [Link](https://www.python.org/ftp/python/3.10.11/python-3.10.11-macos11.pkg)
- **Linux**: [Link](https://www.python.org/ftp/python/3.10.11/Python-3.10.11.tar.xz)
- **Windows**: [Link](https://www.python.org/ftp/python/3.10.11/python-3.10.11-amd64.exe)

## License

This project is licensed under the [EPL License](LICENSE).

## Contributing

Contributions are welcome! Fork the repository, create a new branch, make changes, and submit a pull request.

## Note

Please use this responsibly and follow Discord's terms and API usage policies.
