# PUSON (Posyandu Untuk Stunting Online)

PUSON is an online system for managing and monitoring stunting cases through Posyandu. This project aims to assist Posyandu staff and the public in managing health check data and stunting reports. The application includes features for user management, health check data management, stunting data management, and an integrated helpdesk with a chatbot for support.

## Tech Stack

- **Frontend**: Nuxt 3 (Typescript)
- **Backend**: Flask (Python)
- **CSS**: TailwindCSS
- **Database**: MySQL and Supabase
- **Testing**: Postman, Katalon

## Features

### 1. Authentication (Login/Register)
- Users can register and login to the system.
- Role-based access control (RBAC) with different user levels.

### 2. User Management
- **Super Admin** can manage all users in the system.
- **Admin Puskesmas** can manage Posyandu Admins (Kader).
- **Admin Posyandu (Kader)** can manage parents and children associated with the Posyandu.
- **Parents** (Users) are associated with their children's health data and can access related features.

### 3. Health Check Data Management
- Admins can manage health check data reports related to stunting cases.
- Health data can be logged, updated, and tracked over time.

### 4. Stunting Data Management
- Track and manage stunting reports for children.
- Generate health reports and analyze stunting cases.

### 5. Helpdesk (Chatbot Integration)
- Integrated chatbot using **Gemini** for helpdesk support.
- Users can interact with the chatbot for assistance.

## User Roles and Permissions

### 1. Super Admin
- The owner of the application or the development team.
- Can manage everything in the system, including all users and settings.

### 2. Admin Puskesmas
- Puskesmas staff responsible for managing related Posyandu.
- Can manage **Admin Posyandu** (Kader) and view reports.

### 3. Admin Posyandu (Kader)
- The Posyandu personnel or volunteers (Kader).
- Can manage **Parents and Children** within their assigned Posyandu.
- Can input health check and stunting data.

### 4. User (Parents and Children)
- **Parents**: Can view their children's health and stunting reports.
- **Children**: Managed by their respective parents.

## Project Setup

### Frontend (Nuxt 3)

```bash
# install dependencies
npm install

# serve with hot reload at localhost:3000
npm run dev

# build for production
npm run build
```

### Backend (Flask)
```bash
# create virtual environment
python -m venv venv

# activate virtual environment
.venv/Scripts/activate

# install dependencies
pip install -r requirements.txt

# run the Flask app
python run.py
```

## Database Setup
#### MySQL is used for core data storage.
#### Supabase is used for handling file storage and real-time updates.

## Testing
- Postman: For API endpoint testing.
- Katalon: For UI testing and automation.


## Dokumentasi API
 - (Dokumentasi)[https://documenter.getpostman.com/view/32065108/2sAYBRFDs6]

## Contributing
- Fork the repository.
- Create a new branch (git checkout -b feature/your-feature).
- Commit your changes (git commit -m 'Add your feature').
- Push to the branch (git push origin feature/your-feature).
- Open a pull request.
- License
- This project is licensed under the MIT License. See the LICENSE file for more information.
