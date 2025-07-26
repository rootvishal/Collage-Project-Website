-- College Projects Store Database Schema
-- Create database
CREATE DATABASE IF NOT EXISTS college_projects;
USE college_projects;

-- Users table
CREATE TABLE user (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    is_admin BOOLEAN DEFAULT FALSE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Projects table
CREATE TABLE project (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    description TEXT NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    file_path VARCHAR(255) NOT NULL,
    category VARCHAR(100) NOT NULL,
    tech_stack VARCHAR(200) NOT NULL,
    branch VARCHAR(100) NOT NULL,
    uploaded_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    preview_image VARCHAR(255)
);

-- Orders table
CREATE TABLE `order` (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    project_id INT NOT NULL,
    payment_status VARCHAR(50) DEFAULT 'pending',
    amount DECIMAL(10,2) NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    transaction_id VARCHAR(100),
    FOREIGN KEY (user_id) REFERENCES user(id) ON DELETE CASCADE,
    FOREIGN KEY (project_id) REFERENCES project(id) ON DELETE CASCADE
);

-- Contact messages table
CREATE TABLE contact (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(120) NOT NULL,
    subject VARCHAR(200) NOT NULL,
    message TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Insert sample data
INSERT INTO user (name, email, password_hash, is_admin) VALUES
('Admin', 'admin@collegeprojects.com', 'pbkdf2:sha256:600000$your_hash_here', TRUE);

-- Insert sample projects
INSERT INTO project (title, description, price, file_path, category, tech_stack, branch, preview_image) VALUES
('Student Management System', 'A comprehensive web-based student management system with features like student registration, course management, attendance tracking, and grade management. Built with modern web technologies.', 299.00, 'sample_project_1.zip', 'Web Development', 'HTML, CSS, JavaScript, PHP, MySQL', 'Computer Science', 'sample_preview_1.jpg'),
('E-Commerce Platform', 'A full-featured e-commerce platform with user authentication, product catalog, shopping cart, payment integration, and admin panel. Perfect for learning modern web development.', 399.00, 'sample_project_2.zip', 'Web Development', 'React.js, Node.js, Express.js, MongoDB', 'Computer Science', 'sample_preview_2.jpg'),
('Inventory Management System', 'An efficient inventory management system with barcode scanning, stock tracking, supplier management, and detailed reporting. Ideal for business applications.', 249.00, 'sample_project_3.zip', 'Desktop Application', 'Java, Swing, MySQL', 'Information Technology', 'sample_preview_3.jpg');

-- Create indexes for better performance
CREATE INDEX idx_user_email ON user(email);
CREATE INDEX idx_project_category ON project(category);
CREATE INDEX idx_project_branch ON project(branch);
CREATE INDEX idx_order_user ON `order`(user_id);
CREATE INDEX idx_order_project ON `order`(project_id);
CREATE INDEX idx_order_status ON `order`(payment_status);
CREATE INDEX idx_contact_email ON contact(email);
CREATE INDEX idx_contact_created ON contact(created_at); 