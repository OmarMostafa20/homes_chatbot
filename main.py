# main.py

import logging
from app import create_app
from flask import jsonify

app = create_app()


@app.errorhandler(Exception)
def handle_exception(e):
    # Log the full error details for debugging
    logging.error("An error occurred", exc_info=True)

    # Check if it's an HTTPException (Flask's built-in error class)
    if hasattr(e, 'code'):
        # Return the error message and the status code
        return jsonify(error=str(e)), e.code
    else:
        # Handle non-HTTP exceptions (unexpected errors)
        return jsonify(error="An unexpected error occurred."), 500

# The main entry point for running the Flask application
if __name__ == "__main__":
    app.run(debug=True)