from flask import Flask, render_template, request, redirect, url_for, flash, session, send_file, send_from_directory, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
import datetime
import uuid
from functools import wraps

app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

def nl2br(string):
    return string.replace('\n', '<br>\n')

app.jinja_env.filters['nl2br'] = nl2br

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Database Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    
    # Relationships
    orders = db.relationship('Order', backref='user', lazy=True)

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    file_path = db.Column(db.String(255), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    tech_stack = db.Column(db.String(200), nullable=False)
    branch = db.Column(db.String(100), nullable=False)
    uploaded_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    preview_image = db.Column(db.String(255))
    
    # Relationships
    orders = db.relationship('Order', backref='project', lazy=True)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    payment_status = db.Column(db.String(50), default='pending')
    amount = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    transaction_id = db.Column(db.String(100))

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    subject = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

class Inquiry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20))
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    message = db.Column(db.Text)
    status = db.Column(db.String(50), default='new')  # new, contacted, closed
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    
    # Relationship
    project = db.relationship('Project', backref='inquiries')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('Access denied. Admin privileges required.', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Routes
@app.route('/')
def home():
    featured_projects = Project.query.limit(6).all()
    return render_template('home.html', featured_projects=featured_projects)

@app.route('/projects')
def projects():
    category = request.args.get('category')
    tech_stack = request.args.get('tech_stack')
    branch = request.args.get('branch')
    min_price = request.args.get('min_price')
    max_price = request.args.get('max_price')
    
    query = Project.query
    
    if category:
        query = query.filter(Project.category == category)
    if tech_stack:
        query = query.filter(Project.tech_stack.contains(tech_stack))
    if branch:
        query = query.filter(Project.branch == branch)
    if min_price:
        query = query.filter(Project.price >= float(min_price))
    if max_price:
        query = query.filter(Project.price <= float(max_price))
    
    projects = query.all()
    
    # Get unique values for filters
    categories = db.session.query(Project.category).distinct().all()
    tech_stacks = db.session.query(Project.tech_stack).distinct().all()
    branches = db.session.query(Project.branch).distinct().all()
    
    return render_template('projects.html', projects=projects, 
                         categories=categories, tech_stacks=tech_stacks, branches=branches)

@app.route('/project/<int:project_id>')
def project_detail(project_id):
    project = Project.query.get_or_404(project_id)
    
    # Get related projects (same category or branch, excluding current project)
    related_projects = Project.query.filter(
        Project.id != project_id,
        db.or_(
            Project.category == project.category,
            Project.branch == project.branch
        )
    ).limit(3).all()
    
    return render_template('project_detail.html', project=project, related_projects=related_projects)

@app.route('/inquiry/<int:project_id>', methods=['GET', 'POST'])
def project_inquiry(project_id):
    project = Project.query.get_or_404(project_id)
    
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form.get('phone', '')
        message = request.form.get('message', '')
        
        inquiry = Inquiry(
            name=name,
            email=email,
            phone=phone,
            project_id=project_id,
            message=message
        )
        db.session.add(inquiry)
        db.session.commit()
        
        flash('Thank you for your interest! Our team will contact you soon.', 'success')
        return redirect(url_for('project_detail', project_id=project_id))
    
    return render_template('inquiry.html', project=project)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        subject = request.form['subject']
        message = request.form['message']
        
        contact = Contact(name=name, email=email, subject=subject, message=message)
        db.session.add(contact)
        db.session.commit()
        
        flash('Message sent successfully! We will get back to you soon.', 'success')
        return redirect(url_for('contact'))
    
    return render_template('contact.html')

@app.route('/admin')
@admin_required
def admin_dashboard():
    total_projects = Project.query.count()
    total_inquiries = Inquiry.query.count()
    total_contacts = Contact.query.count()
    recent_inquiries = Inquiry.query.order_by(Inquiry.created_at.desc()).limit(5).all()
    
    return render_template('admin/dashboard.html', 
                         total_projects=total_projects,
                         total_inquiries=total_inquiries,
                         total_contacts=total_contacts,
                         recent_inquiries=recent_inquiries)

@app.route('/admin/projects')
@admin_required
def admin_projects():
    projects = Project.query.all()
    return render_template('admin/projects.html', projects=projects)

@app.route('/admin/projects/add', methods=['GET', 'POST'])
@admin_required
def admin_add_project():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        price = float(request.form['price'])
        category = request.form['category']
        tech_stack = request.form['tech_stack']
        branch = request.form['branch']
        
        # Handle file upload
        if 'project_file' not in request.files:
            flash('No file selected', 'error')
            return render_template('admin/add_project.html')
        
        file = request.files['project_file']
        if file.filename == '':
            flash('No file selected', 'error')
            return render_template('admin/add_project.html')
        
        if file:
            filename = secure_filename(f"{uuid.uuid4()}_{file.filename}")
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
        
        # Handle preview image
        preview_image = None
        if 'preview_image' in request.files:
            preview_file = request.files['preview_image']
            if preview_file.filename != '':
                preview_filename = secure_filename(f"preview_{uuid.uuid4()}_{preview_file.filename}")
                preview_path = os.path.join(app.config['UPLOAD_FOLDER'], preview_filename)
                preview_file.save(preview_path)
                preview_image = preview_filename
        
        project = Project(
            title=title,
            description=description,
            price=price,
            file_path=filename,
            category=category,
            tech_stack=tech_stack,
            branch=branch,
            preview_image=preview_image
        )
        
        db.session.add(project)
        db.session.commit()
        
        flash('Project added successfully!', 'success')
        return redirect(url_for('admin_projects'))
    
    return render_template('admin/add_project.html')

@app.route('/admin/projects/edit/<int:project_id>', methods=['GET', 'POST'])
@admin_required
def admin_edit_project(project_id):
    project = Project.query.get_or_404(project_id)
    
    if request.method == 'POST':
        project.title = request.form['title']
        project.description = request.form['description']
        project.price = float(request.form['price'])
        project.category = request.form['category']
        project.tech_stack = request.form['tech_stack']
        project.branch = request.form['branch']
        
        # Handle new file upload
        if 'project_file' in request.files and request.files['project_file'].filename != '':
            file = request.files['project_file']
            filename = secure_filename(f"{uuid.uuid4()}_{file.filename}")
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            
            # Delete old file
            if project.file_path:
                old_file_path = os.path.join(app.config['UPLOAD_FOLDER'], project.file_path)
                if os.path.exists(old_file_path):
                    os.remove(old_file_path)
            
            project.file_path = filename
        
        # Handle new preview image
        if 'preview_image' in request.files and request.files['preview_image'].filename != '':
            preview_file = request.files['preview_image']
            preview_filename = secure_filename(f"preview_{uuid.uuid4()}_{preview_file.filename}")
            preview_path = os.path.join(app.config['UPLOAD_FOLDER'], preview_filename)
            preview_file.save(preview_path)
            
            # Delete old preview image
            if project.preview_image:
                old_preview_path = os.path.join(app.config['UPLOAD_FOLDER'], project.preview_image)
                if os.path.exists(old_preview_path):
                    os.remove(old_preview_path)
            
            project.preview_image = preview_filename
        
        db.session.commit()
        flash('Project updated successfully!', 'success')
        return redirect(url_for('admin_projects'))
    
    return render_template('admin/edit_project.html', project=project)

@app.route('/admin/projects/delete/<int:project_id>')
@admin_required
def admin_delete_project(project_id):
    project = Project.query.get_or_404(project_id)
    
    # Delete associated files
    if project.file_path:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], project.file_path)
        if os.path.exists(file_path):
            os.remove(file_path)
    
    if project.preview_image:
        preview_path = os.path.join(app.config['UPLOAD_FOLDER'], project.preview_image)
        if os.path.exists(preview_path):
            os.remove(preview_path)
    
    db.session.delete(project)
    db.session.commit()
    
    flash('Project deleted successfully!', 'success')
    return redirect(url_for('admin_projects'))

@app.route('/admin/users')
@admin_required
def admin_users():
    users = User.query.all()
    return render_template('admin/users.html', users=users)

@app.route('/admin/orders')
@admin_required
def admin_orders():
    orders = Order.query.order_by(Order.timestamp.desc()).all()
    return render_template('admin/orders.html', orders=orders)

@app.route('/admin/contacts')
@admin_required
def admin_contacts():
    contacts = Contact.query.order_by(Contact.created_at.desc()).all()
    return render_template('admin/contacts.html', contacts=contacts)

@app.route('/admin/inquiries')
@admin_required
def admin_inquiries():
    inquiries = Inquiry.query.order_by(Inquiry.created_at.desc()).all()
    return render_template('admin/inquiries.html', inquiries=inquiries)
@app.route('/login', methods=['GET', 'POST'])
def login():
    print("Login route accessed")  # Add this line
    if current_user.is_authenticated:
        if current_user.is_admin:
            return redirect(url_for('admin_dashboard'))
        return redirect(url_for('home'))
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            if user.is_admin:
                return redirect(url_for('admin_dashboard'))
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Invalid email or password', 'error')
    return render_template('admin/login.html')
    
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        
        if User.query.filter_by(email=email).first():
            flash('Email already registered', 'error')
            return render_template('register.html')
        
        user = User(
            name=name,
            email=email,
            password_hash=generate_password_hash(password)
        )
        db.session.add(user)
        db.session.commit()
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    # Redirect to the register route
    return redirect(url_for('register'))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('home'))

@app.route('/buy/<int:project_id>', methods=['POST'])
@login_required
def buy_project(project_id):
    project = Project.query.get_or_404(project_id)
    
    # For demo, assume instant payment completion
    order = Order(
        user_id=current_user.id,
        project_id=project_id,
        amount=project.price,
        payment_status='completed',
        transaction_id=str(uuid.uuid4())
    )
    db.session.add(order)
    db.session.commit()
    
    flash(f'Project "{project.title}" purchased successfully! You can download it now.', 'success')
    return redirect(url_for('project_detail', project_id=project_id))

@app.route('/download/<int:order_id>')
@login_required
def download_project(order_id):
    order = Order.query.filter_by(id=order_id, user_id=current_user.id, payment_status='completed').first_or_404()
    
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], order.project.file_path)
    if not os.path.exists(file_path):
        flash('File not found.', 'error')
        return redirect(url_for('home'))
    
    return send_file(file_path, as_attachment=True, download_name=order.project.title + '.zip')







@app.route('/uploads/<filename>')
def uploaded_file(filename):
    """Serve uploaded files"""
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        
        # Create admin user if not exists
        admin = User.query.filter_by(email='admin@collegeprojects.com').first()
        if not admin:
            admin = User(
                name='Admin',
                email='admin@collegeprojects.com',
                password_hash=generate_password_hash('admin123'),
                is_admin=True
            )
            db.session.add(admin)
            db.session.commit()
        
        # Add sample projects if none exist (without preview images for now)
        if Project.query.count() == 0:
            sample_projects = [
                {
                    'title': 'Student Management System',
                    'description': 'A comprehensive web-based student management system with features like student registration, course management, attendance tracking, and grade management. Built with modern web technologies.',
                    'price': 299.0,
                    'file_path': 'sample_project_1.zip',
                    'category': 'Web Development',
                    'tech_stack': 'HTML, CSS, JavaScript, PHP, MySQL',
                    'branch': 'Computer Science',
                    'preview_image': None
                },
                {
                    'title': 'E-Commerce Platform',
                    'description': 'A full-featured e-commerce platform with user authentication, product catalog, shopping cart, payment integration, and admin panel. Perfect for learning modern web development.',
                    'price': 399.0,
                    'file_path': 'sample_project_2.zip',
                    'category': 'Web Development',
                    'tech_stack': 'React.js, Node.js, Express.js, MongoDB',
                    'branch': 'Computer Science',
                    'preview_image': None
                },
                {
                    'title': 'Inventory Management System',
                    'description': 'An efficient inventory management system with barcode scanning, stock tracking, supplier management, and detailed reporting. Ideal for business applications.',
                    'price': 249.0,
                    'file_path': 'sample_project_3.zip',
                    'category': 'Desktop Application',
                    'tech_stack': 'Java, Swing, MySQL',
                    'branch': 'Information Technology',
                    'preview_image': None
                }
            ]
            
            for project_data in sample_projects:
                project = Project(**project_data)
                db.session.add(project)
            
            db.session.commit()
    
    app.run(debug=True) 