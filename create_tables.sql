-- Use the newly created database
USE student_management;

-- Create the 'students' table with DATETIME for enrollment_date
CREATE TABLE students (
    student_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    date_of_birth DATE NOT NULL,
    enrollment_date DATETIME DEFAULT NOW()  -- Using NOW() as the default value
);

-- Create the 'courses' table
CREATE TABLE courses (
    course_id INT AUTO_INCREMENT PRIMARY KEY,
    course_name VARCHAR(100) NOT NULL,
    course_code VARCHAR(10) UNIQUE NOT NULL,
    credits INT NOT NULL CHECK (credits > 0)
);

-- Create the 'enrollments' table (junction table)
CREATE TABLE enrollments (
    enrollment_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT,
    course_id INT,
    grade CHAR(2),
    FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE,
    FOREIGN KEY (course_id) REFERENCES courses(course_id) ON DELETE CASCADE
);

-- Indexes (Optional)
CREATE INDEX idx_student_id ON enrollments(student_id);
CREATE INDEX idx_course_id ON enrollments(course_id);

