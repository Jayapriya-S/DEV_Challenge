# Development Goals Tracker

A Flask application to help developers track their learning goals, built with GitHub Copilot assistance.

## Features

- Set development goals with deadlines
- Track completion status
- Delete completed goals
- Validate inputs
- Error handling

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/Jayapriya-S/DEV_Challenge.git
    cd DEV_Challenge
    ```

2. Create a virtual environment:
    ```bash
    python -m venv venv
    ```

3. Activate the virtual environment:
    - On Windows:
        ```bash
        venv\Scripts\activate
        ```
    - On macOS/Linux:
        ```bash
        source venv/bin/activate
        ```

4. Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Configuration

The application uses environment variables for configuration. You can set these variables in your environment or create a `.env` file in the root directory of your project.

Here are the environment variables you can set:

- [SECRET_KEY](http://_vscodecontentref_/1): Secret key for the Flask application.
- [FLASK_APP](http://_vscodecontentref_/2): The entry point of the Flask application (default is [app.py](http://_vscodecontentref_/3)).
- `DATABASE_URL`: The database URL for the production environment.
- `DEV_DATABASE_URL`: The database URL for the development environment.
- `TEST_SECRET_KEY`: Secret key for the test environment.
- `PROD_SECRET_KEY`: Secret key for the production environment.

## Running the Application

1. Set the [FLASK_APP](http://_vscodecontentref_/4) environment variable:
    ```bash
    export FLASK_APP=app.py
    ```

2. Run the Flask application:
    ```bash
    flask run
    ```

The application will be available at `http://127.0.0.1:5000`.

## Running Tests

To run the tests, use the following command:
```bash
pytest
