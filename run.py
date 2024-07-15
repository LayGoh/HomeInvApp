# Import the Flask app instance
from app import app

# Run the app on the home network
#if __name__ == "__main__":
#    app.run(debug=True, host='0.0.0.0', port=1000)

# Uncomment the following lines to run the app on the work network
if __name__ == "__main__":
    app.run(debug=True, host='127.0.0.1', port=5000)
