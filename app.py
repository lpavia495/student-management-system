from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_mysqldb import MySQL
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

mysql = MySQL(app)

# Home route
@app.route('/')
def home():
    return render_template('index.html')

# CRUD for Students with Search
@app.route('/view_students')
def view_students_page():
    search_query = request.args.get('search', '')
    cursor = mysql.connection.cursor()

    if search_query:
        cursor.execute("SELECT * FROM students WHERE first_name LIKE %s OR last_name LIKE %s", 
                       ('%' + search_query + '%', '%' + search_query + '%'))
    else:
        cursor.execute("SELECT * FROM students")

    students = cursor.fetchall()
    cursor.close()
    return render_template('students.html', students=students)

@app.route('/add_student', methods=['POST'])
def add_student():
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    email = request.form['email']
    date_of_birth = request.form['date_of_birth']
    cursor = mysql.connection.cursor()
    cursor.execute(
        "INSERT INTO students (first_name, last_name, email, date_of_birth) VALUES (%s, %s, %s, %s)",
        (first_name, last_name, email, date_of_birth)
    )
    mysql.connection.commit()
    cursor.close()
    return redirect(url_for('view_students_page'))

@app.route('/update_student/<int:student_id>', methods=['GET', 'POST'])
def update_student_page(student_id):
    cursor = mysql.connection.cursor()
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        date_of_birth = request.form['date_of_birth']
        cursor.execute(
            "UPDATE students SET first_name=%s, last_name=%s, email=%s, date_of_birth=%s WHERE student_id=%s",
            (first_name, last_name, email, date_of_birth, student_id)
        )
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('view_students_page'))
    else:
        cursor.execute("SELECT * FROM students WHERE student_id = %s", (student_id,))
        student = cursor.fetchone()
        cursor.close()
        return render_template('update_student.html', student=student)

@app.route('/delete_student/<int:student_id>', methods=['POST'])
def delete_student(student_id):
    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM students WHERE student_id = %s", (student_id,))
    mysql.connection.commit()
    cursor.close()
    return redirect(url_for('view_students_page'))

# CRUD for Courses with Search
@app.route('/view_courses')
def view_courses_page():
    search_query = request.args.get('search', '')
    cursor = mysql.connection.cursor()

    if search_query:
        cursor.execute("SELECT * FROM courses WHERE course_name LIKE %s OR course_code LIKE %s", 
                       ('%' + search_query + '%', '%' + search_query + '%'))
    else:
        cursor.execute("SELECT * FROM courses")

    courses = cursor.fetchall()
    cursor.close()
    return render_template('courses.html', courses=courses)

@app.route('/add_course', methods=['POST'])
def add_course():
    course_name = request.form['course_name']
    course_code = request.form['course_code']
    credits = request.form['credits']
    cursor = mysql.connection.cursor()
    cursor.execute(
        "INSERT INTO courses (course_name, course_code, credits) VALUES (%s, %s, %s)",
        (course_name, course_code, credits)
    )
    mysql.connection.commit()
    cursor.close()
    return redirect(url_for('view_courses_page'))

@app.route('/update_course/<int:course_id>', methods=['GET', 'POST'])
def update_course_page(course_id):
    cursor = mysql.connection.cursor()
    if request.method == 'POST':
        course_name = request.form['course_name']
        course_code = request.form['course_code']
        credits = request.form['credits']
        cursor.execute(
            "UPDATE courses SET course_name=%s, course_code=%s, credits=%s WHERE course_id=%s",
            (course_name, course_code, credits, course_id)
        )
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('view_courses_page'))
    else:
        cursor.execute("SELECT * FROM courses WHERE course_id = %s", (course_id,))
        course = cursor.fetchone()
        cursor.close()
        return render_template('update_course.html', course=course)

@app.route('/delete_course/<int:course_id>', methods=['POST'])
def delete_course(course_id):
    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM courses WHERE course_id = %s", (course_id,))
    mysql.connection.commit()
    cursor.close()
    return redirect(url_for('view_courses_page'))

# CRUD for Enrollments with Search
@app.route('/view_enrollments')
def view_enrollments_page():
    search_query = request.args.get('search', '')
    cursor = mysql.connection.cursor()

    if search_query:
        cursor.execute("""
            SELECT enrollments.enrollment_id, students.first_name AS student_name, courses.course_name, enrollments.grade
            FROM enrollments
            JOIN students ON enrollments.student_id = students.student_id
            JOIN courses ON enrollments.course_id = courses.course_id
            WHERE students.first_name LIKE %s OR students.last_name LIKE %s OR courses.course_name LIKE %s
        """, ('%' + search_query + '%', '%' + search_query + '%', '%' + search_query + '%'))
    else:
        cursor.execute("""
            SELECT enrollments.enrollment_id, students.first_name AS student_name, courses.course_name, enrollments.grade
            FROM enrollments
            JOIN students ON enrollments.student_id = students.student_id
            JOIN courses ON enrollments.course_id = courses.course_id
        """)

    enrollments = cursor.fetchall()
    cursor.close()
    return render_template('enrollments.html', enrollments=enrollments)

@app.route('/enroll_student', methods=['POST'])
def enroll_student():
    student_id = request.form['student_id']
    course_id = request.form['course_id']
    grade = request.form['grade']
    cursor = mysql.connection.cursor()
    cursor.execute(
        "INSERT INTO enrollments (student_id, course_id, grade) VALUES (%s, %s, %s)",
        (student_id, course_id, grade)
    )
    mysql.connection.commit()
    cursor.close()
    return redirect(url_for('view_enrollments_page'))

@app.route('/update_enrollment/<int:enrollment_id>', methods=['GET', 'POST'])
def update_enrollment_page(enrollment_id):
    cursor = mysql.connection.cursor()
    if request.method == 'POST':
        grade = request.form['grade']
        cursor.execute(
            "UPDATE enrollments SET grade=%s WHERE enrollment_id=%s",
            (grade, enrollment_id)
        )
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('view_enrollments_page'))
    else:
        cursor.execute("SELECT * FROM enrollments WHERE enrollment_id = %s", (enrollment_id,))
        enrollment = cursor.fetchone()
        cursor.close()
        return render_template('update_enrollment.html', enrollment=enrollment)

@app.route('/delete_enrollment/<int:enrollment_id>', methods=['POST'])
def delete_enrollment(enrollment_id):
    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM enrollments WHERE enrollment_id = %s", (enrollment_id,))
    mysql.connection.commit()
    cursor.close()
    return redirect(url_for('view_enrollments_page'))

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
