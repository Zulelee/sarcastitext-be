# SarcastiText-backend

# FastAPI Backend Project Setup Guide

This guide will walk you through setting up the FastAPI backend project of SuperChat.

## Prerequisites

Before you begin, ensure you have the following installed:

- Python
- pip (Python package manager)

## Setup Instructions

1. **Clone the Repository**:

   ```bash
   git clone <repository_url>
   cd <repository_name>
   ```

2. **Create a Virtual Environment**:

   ```bash
   python -m venv venv
   ```

3. **Activate the Virtual Environment**:

   - **Windows**:
     ```bash
     .\venv\Scripts\activate
     ```
   - **macOS/Linux**:
     ```bash
     source venv/bin/activate
     ```

4. **Install Requirements**:

   ```bash
   pip install -r requirements.txt
   ```

5. **Run the Server**:

   ```bash
   python -m uvicorn app.index:app --reload
   ```

6. **Access the API**:
   Once the server is running, you can access the API at http://localhost:8000.

7. **API Documentation**:
   The Swagger UI documentation is available at http://localhost:8000/docs.

## Additional Notes

- Make sure to replace `<repository_url>` and `<repository_name>` with the appropriate values based on the repository.
- Ensure that you have the correct permissions and dependencies installed to run the project.
- Modify the `requirements.txt` file as needed to include any additional dependencies required before pushing changes to this repository.
