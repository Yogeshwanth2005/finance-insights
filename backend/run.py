import os
from app import create_app

if __name__ == '__main__':
    app = create_app()
    
    # Create uploads directory
    os.makedirs(os.path.join(os.path.dirname(__file__), 'uploads'), exist_ok=True)
    
    # Run the app
    app.run(debug=True, host='localhost', port=5000)
