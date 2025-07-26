# College Projects Store

A full-stack dynamic website for selling college projects to students. Built with Flask, MySQL, and Bootstrap.

## 🚀 Features

### Core Features
- **Home Page** with banner, intro text, and featured projects
- **Project Listing** with advanced filtering (category, tech stack, branch, price)
- **Project Details** with comprehensive information and preview images
- **User Authentication** (login/signup) for students
- **Admin Panel** for project management (upload/edit/delete)
- **Payment Integration** (Razorpay for India, Stripe globally)
- **Download Protection** - access only after payment
- **Contact Form** for custom project requests

### Admin Features
- Dashboard with statistics and overview
- Project management (CRUD operations)
- User management
- Order tracking
- Contact message management
- File upload system for projects

### User Features
- Browse projects with filters
- Purchase projects securely
- Download purchased projects
- View order history
- Contact support

## 🛠 Tech Stack

- **Frontend**: HTML, CSS, JavaScript, Bootstrap 5
- **Backend**: Python with Flask
- **Database**: MySQL
- **Authentication**: Flask-Login
- **Payment**: Razorpay (India) / Stripe (Global)
- **File Upload**: Werkzeug

## 📁 Project Structure

```
college-projects-store/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── database_schema.sql    # MySQL database schema
├── README.md             # Project documentation
├── templates/            # HTML templates
│   ├── base.html         # Base template
│   ├── home.html         # Home page
│   ├── projects.html     # Project listing
│   ├── project_detail.html # Project details
│   ├── login.html        # Login page
│   ├── signup.html       # Signup page
│   ├── contact.html      # Contact page
│   ├── purchase.html     # Purchase page
│   └── admin/            # Admin templates
│       ├── dashboard.html
│       ├── projects.html
│       ├── add_project.html
│       ├── edit_project.html
│       ├── orders.html
│       ├── users.html
│       └── contacts.html
├── static/               # Static files (CSS, JS, images)
└── uploads/              # Uploaded project files
```

## 🗄 Database Schema

### Tables
1. **users** - User accounts and authentication
2. **projects** - Project information and files
3. **orders** - Purchase transactions
4. **contacts** - Contact form submissions

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8+
- MySQL 8.0+
- pip (Python package manager)

### Step 1: Clone the Repository
```bash
git clone <repository-url>
cd college-projects-store
```

### Step 2: Set Up Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Set Up MySQL Database
1. Create MySQL database:
```sql
CREATE DATABASE college_projects;
```

2. Import the schema:
```bash
mysql -u root -p college_projects < database_schema.sql
```

### Step 5: Configure Environment Variables
Create a `.env` file in the root directory:
```env
SECRET_KEY=your-secret-key-here
DATABASE_URL=mysql://username:password@localhost/college_projects
RAZORPAY_KEY_ID=your-razorpay-key
RAZORPAY_KEY_SECRET=your-razorpay-secret
```

### Step 6: Run the Application
```bash
python app.py
```

The application will be available at `http://localhost:5000`

## 👤 Default Admin Account

- **Email**: admin@collegeprojects.com
- **Password**: admin123

## 🔧 Configuration

### Database Configuration
Update the database connection in `app.py`:
```python
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://username:password@localhost/college_projects'
```

### Payment Gateway Configuration
For Razorpay integration:
1. Sign up at [Razorpay](https://razorpay.com)
2. Get your API keys
3. Update the configuration in the purchase template

### File Upload Configuration
- Maximum file size: 16MB
- Supported formats: ZIP, PDF
- Upload directory: `uploads/`

## 📱 Features in Detail

### Project Management
- Upload project files (ZIP/PDF)
- Add preview images
- Set pricing and categories
- Manage project details

### User Management
- User registration and authentication
- Role-based access (admin/user)
- User profile management

### Payment System
- Secure payment processing
- Multiple payment methods
- Order tracking
- Download protection

### Admin Panel
- Dashboard with statistics
- Project CRUD operations
- User management
- Order management
- Contact message handling

## 🔒 Security Features

- Password hashing with Werkzeug
- Session management with Flask-Login
- File upload validation
- SQL injection protection
- XSS protection
- CSRF protection

## 🎨 UI/UX Features

- Responsive design with Bootstrap 5
- Modern and clean interface
- Interactive filters and search
- User-friendly navigation
- Mobile-optimized layout

## 🚀 Deployment

### Production Deployment
1. Set up a production server (AWS, DigitalOcean, etc.)
2. Install required software (Python, MySQL, Nginx)
3. Configure environment variables
4. Set up SSL certificate
5. Configure Nginx as reverse proxy
6. Use Gunicorn as WSGI server

### Environment Variables for Production
```env
FLASK_ENV=production
SECRET_KEY=your-production-secret-key
DATABASE_URL=mysql://username:password@localhost/college_projects
RAZORPAY_KEY_ID=your-production-razorpay-key
RAZORPAY_KEY_SECRET=your-production-razorpay-secret
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📞 Support

For support and questions:
- Email: info@collegeprojects.com
- Phone: +91 98765 43210

## 🔄 Updates and Maintenance

- Regular security updates
- Feature enhancements
- Bug fixes
- Performance optimizations

## 📊 Sample Data

The application comes with 3 sample projects:
1. Student Management System (Web Development)
2. E-Commerce Platform (Web Development)
3. Inventory Management System (Desktop Application)

## 🎯 Future Enhancements

- Advanced search functionality
- Project reviews and ratings
- Bulk project upload
- Email notifications
- API endpoints
- Mobile app
- Multi-language support
- Advanced analytics 