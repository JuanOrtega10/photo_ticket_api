
# Photo Ticket API

## Description
Photo Ticket API is a system for managing tickets and optimized image uploads in Django. This project uses Poetry for dependency and environment management.

## Prerequisites
Ensure you have Python 3.10 and Poetry installed on your system to manage the project's dependencies.

## Initial Setup

### Environment Setup
Create a `.env` file in the project root directory and fill it with the necessary environment variables. Replace `<value>` with your actual configuration values:

```plaintext
SECRET_KEY=<value>
DEBUG=<value>
CELERY_BROKER_URL=<value>
CELERY_RESULT_BACKEND=<value>
CLOUDINARY_CLOUD_NAME=<value>
CLOUDINARY_API_KEY=<value>
CLOUDINARY_API_SECRET=<value>
CLOUDINARY_SECURE=<value>
DATABASE_ENGINE=<value>
DATABASE_NAME=<value>
DATABASE_USER=<value>
DATABASE_PASSWORD=<value>
DATABASE_HOST=<value>
DATABASE_PORT=<value>
```

### Install Dependencies
Use Poetry to install all required dependencies:

```bash
poetry install
```

### Running the Project
Activate the virtual environment managed by Poetry:

```bash
poetry shell
```

Run the Django migrations to set up your database schema:

```bash
python manage.py migrate
```

Start the Django development server:

```bash
python manage.py runserver
```

### Image Upload Optimization
The project optimizes image uploads by reducing their size using the following settings in the upload process:

```python
upload_result = upload(
    image_file, fetch_format="auto", quality="auto", resource_type="image"
)
```

These settings automatically adjust the format and quality of the images to optimize their size before uploading to Cloudinary.

## Additional Information
For more details on managing and configuring the project, refer to the official Django and Poetry documentation.
