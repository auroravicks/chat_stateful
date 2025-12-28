# Stateful Chat Application

A Django-based chat application that maintains conversation state, built on top of [tomitokko/django-chatbot](https://github.com/tomitokko/django-chatbot). This project extends the original implementation with stateful chat capabilities and a modified database schema to support conversation history and context.


## Setup Instructions

### Prerequisites
- Python 3.8+
- pip (Python package manager)
- Virtual environment (recommended)

### Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd chat_stateful
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up the database:
   ```bash
   python manage.py migrate
   ```

5. Create a superuser (optional):
   ```bash
   python manage.py createsuperuser
   ```

6. Run the development server:
   ```bash
   python manage.py runserver
   ```

7. Access the application at `http://127.0.0.1:8000/`

## Project Notes

This project was built on top of [tomitokko/django-chatbot](https://github.com/tomitokko/django-chatbot) and includes significant modifications:
- Added stateful chat functionality
- Modified database schema for better conversation handling
- Enhanced user experience with improved conversation flow

The original project and its accompanying video tutorial provided an excellent introduction to Django and chat application development.