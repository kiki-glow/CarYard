# Caryard

**Caryard** is a web application for vintage car enthusiasts to browse, buy, and sell vintage cars. The platform includes a main marketplace for users, as well as an admin dashboard where admins can add, edit, or delete car listings.

## Table of Contents
1. [Features](#features)
2. [Tech Stack](#tech-stack)
3. [Project Structure](#project-structure)
4. [Setup and Installation](#setup-and-installation)
5. [Usage](#usage)
6. [Contributing](#contributing)
7. [License](#license)

## Features
- **Browse Listings**: View details of vintage cars available for sale.
- **Admin Dashboard**: Admin login and dashboard for managing car listings.
- **Car Details**: Each car has detailed information including make, model, description, and price.
- **Quotation Request**: Users can request quotations for specific cars (basic placeholder).

## Tech Stack
- **Frontend**: HTML, CSS, JavaScript
- **Backend**: Python, Flask
- **Database**: MongoDB
- **Additional Libraries**: `Flask-Bcrypt` for password hashing, `python-dotenv` for environment management

## Project Structure
```
caryard_project/
│
├── app.py                   # Main Flask application
├── requirements.txt         # Python dependencies
├── .env                     # Environment variables (e.g., secret keys, database URI)
│
├── templates/               # HTML templates
│   ├── index.html           # Homepage template
│   ├── admin_register.html  # Admin registration page
│   ├── admin_login.html     # Admin login page
│   ├── admin_dashboard.html # Admin dashboard for managing cars
│   ├── edit_car.html        # Edit car page for updating car details
│   └── quotation.html       # Quotation request page for individual car
│
├── static/                  # Static assets like CSS, images, JavaScript
│   ├── css/
│   │   └── style.css        # Main stylesheet for the web app
│   │
│   ├── images/
│   │   ├── favicon.ico      # Favicon image
│   │   └── default_car.jpg  # Placeholder car image (optional)
│   │
│   └── js/                  # JavaScript files (optional)
│       └── main.js          # Main JavaScript file for interactivity (optional)
│
└── README.md                # Project documentation
```

## Setup and Installation

### Prerequisites
- **Python 3.x** installed on your machine.
- **MongoDB** server or MongoDB Atlas account.

### Installation Steps

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/caryard.git
   cd caryard
   ```

2. **Set Up a Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up Environment Variables**:
   Create a `.env` file in the project root with the following content:
   ```plaintext
   SECRET_KEY="your_secret_key"
   MONGO_URI="mongodb://<username>:<password>@<host>:<port>/<database_name>"
   ```

5. **Run the Application**:
   ```bash
   python app.py
   ```
   Open your browser and go to `http://127.0.0.1:5000`.

## Usage

### Main Features
- **Homepage**: View cars available for sale.
- **Admin Dashboard**: Accessible via `/admin/login` for registered admins. Admins can add, edit, or delete cars from this dashboard.

### Admin Functions
1. **Register Admin**: Visit `/admin/register` to create a new admin account.
2. **Login**: Admins can log in via `/admin/login` to access the dashboard.
3. **Add, Edit, Delete Cars**: Once logged in, admins can manage car listings.

## Contributing
Contributions are welcome! Please follow these steps to contribute:
1. Fork the repository.
2. Create a feature branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -m 'Add new feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Open a pull request.

## License
This project is licensed under the MIT License.
