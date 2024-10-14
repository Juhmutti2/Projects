import os
import os.path
import sqlite3

# poistaa tietokannan alussa (kätevä moduulin testailussa)
if os.path.exists("courses.db"):
    os.remove("courses.db")

db = sqlite3.connect("courses.db")
db.isolation_level = None

# luo tietokantaan tarvittavat taulut
def create_tables():
    db.execute("""
        CREATE TABLE Teachers (
            id INTEGER PRIMARY KEY,
            name TEXT
        )
    """)

    db.execute("""
        CREATE TABLE Courses (
            id INTEGER PRIMARY KEY,
            name TEXT,
            credits INTEGER
        )
    """)

    db.execute("""
        CREATE TABLE CourseTeachers (
            course_id INTEGER,
            teacher_id INTEGER,
            FOREIGN KEY (course_id) REFERENCES Courses(id),
            FOREIGN KEY (teacher_id) REFERENCES Teachers(id)
        )
    """)

    db.execute("""
        CREATE TABLE Students (
            id INTEGER PRIMARY KEY,
            name TEXT
        )
    """)

    db.execute("""
        CREATE TABLE Credits (
            id INTEGER PRIMARY KEY,
            student_id INTEGER,
            course_id INTEGER,
            date TEXT,
            grade INTEGER,
            FOREIGN KEY (student_id) REFERENCES Students(id),
            FOREIGN KEY (course_id) REFERENCES Courses(id)
        )
    """)

    db.execute("""
        CREATE TABLE Groups (
            id INTEGER PRIMARY KEY,
            name TEXT
        )
    """)

    db.execute("""
        CREATE TABLE GroupTeachers (
            group_id INTEGER,
            teacher_id INTEGER,
            FOREIGN KEY (group_id) REFERENCES Groups(id),
            FOREIGN KEY (teacher_id) REFERENCES Teachers(id)
        )
    """)

    db.execute("""
        CREATE TABLE GroupStudents (
            group_id INTEGER,
            student_id INTEGER,
            FOREIGN KEY (group_id) REFERENCES Groups(id),
            FOREIGN KEY (student_id) REFERENCES Students(id)
        )
    """)

# lisää opettajan tietokantaan
def create_teacher(name):
    cursor = db.cursor()
    cursor.execute("INSERT INTO Teachers (name) VALUES (?)", (name,))
    return cursor.lastrowid

# lisää kurssin tietokantaan
def create_course(name, credits, teacher_ids):
    cursor = db.cursor()
    cursor.execute("INSERT INTO Courses (name, credits) VALUES (?, ?)", (name, credits))
    course_id = cursor.lastrowid

    for teacher_id in teacher_ids:
        cursor.execute("INSERT INTO CourseTeachers (course_id, teacher_id) VALUES (?, ?)", (course_id, teacher_id))

    return course_id

# lisää opiskelijan tietokantaan
def create_student(name):
    cursor = db.cursor()
    cursor.execute("INSERT INTO Students (name) VALUES (?)", (name,))
    return cursor.lastrowid

# antaa opiskelijalle suorituksen kurssista
def add_credits(student_id, course_id, date, grade):
    cursor = db.cursor()
    cursor.execute("INSERT INTO Credits (student_id, course_id, date, grade) VALUES (?, ?, ?, ?)", (student_id, course_id, date, grade))
    return cursor.lastrowid

# lisää ryhmän tietokantaan
def create_group(name, teacher_ids, student_ids):
    cursor = db.cursor()
    cursor.execute("INSERT INTO Groups (name) VALUES (?)", (name,))
    group_id = cursor.lastrowid

    for teacher_id in teacher_ids:
        cursor.execute("INSERT INTO GroupTeachers (group_id, teacher_id) VALUES (?, ?)", (group_id, teacher_id))

    for student_id in student_ids:
        cursor.execute("INSERT INTO GroupStudents (group_id, student_id) VALUES (?, ?)", (group_id, student_id))

    return group_id

# hakee kurssit, joissa opettaja opettaa (aakkosjärjestyksessä)
def courses_by_teacher(teacher_name):
    cursor = db.cursor()
    cursor.execute("""
        SELECT c.name
        FROM Courses c
        JOIN CourseTeachers ct ON c.id = ct.course_id
        JOIN Teachers t ON t.id = ct.teacher_id
        WHERE t.name = ?
        ORDER BY c.name ASC
    """, (teacher_name,))
    return [row[0] for row in cursor.fetchall()]

# hakee opettajan antamien opintopisteiden määrän
def credits_by_teacher(teacher_name):
    cursor = db.cursor()
    cursor.execute("""
        SELECT SUM(c.credits)
        FROM Courses c
        JOIN CourseTeachers ct ON c.id = ct.course_id
        JOIN Teachers t ON t.id = ct.teacher_id
        JOIN Credits cr ON c.id = cr.course_id
        WHERE t.name = ?
    """, (teacher_name,))
    result = cursor.fetchone()
    return result[0] if result else 0
# hakee opiskelijan suorittamat kurssit arvosanoineen (aakkosjärjestyksessä)
def courses_by_student(student_name):
    cursor = db.cursor()
    cursor.execute("""
        SELECT c.name, cr.grade
        FROM Courses c
        JOIN Credits cr ON c.id = cr.course_id
        JOIN Students s ON s.id = cr.student_id
        WHERE s.name = ?
        ORDER BY c.name ASC
    """, (student_name,))
    return cursor.fetchall()

# hakee tiettynä vuonna saatujen opintopisteiden määrän
def credits_by_year(year):
    cursor = db.cursor()
    cursor.execute("""
        SELECT SUM(c.credits)
        FROM Courses c
        JOIN Credits cr ON c.id = cr.course_id
        WHERE cr.date LIKE ?
    """, (f"{year}%",))
    result = cursor.fetchone()
    return result[0] if result else 0

# hakee kurssin arvosanojen jakauman (järjestyksessä arvosanat 1-5)
# hakee kurssin arvosanojen jakauman (järjestyksessä arvosanat 1-5)
def grade_distribution(course_name):
    cursor = db.cursor()
    cursor.execute("""
        SELECT cr.grade, COUNT(cr.id)
        FROM Courses c
        JOIN Credits cr ON c.id = cr.course_id
        WHERE c.name = ?
        GROUP BY cr.grade
        ORDER BY cr.grade ASC
    """, (course_name,))
    grades = cursor.fetchall()
    
    # Alustetaan jakauma kaikille arvosanoille 1-5
    distribution = {i: 0 for i in range(1, 6)}
    
    # Päivitetään jakauma saaduilla arvosanoilla
    for grade, count in grades:
        distribution[grade] = count

    return distribution


# hakee listan kursseista (nimi, opettajien määrä, suorittajien määrä) (aakkosjärjestyksessä)
def course_list():
    cursor = db.cursor()
    cursor.execute("""
        SELECT c.name, COUNT(DISTINCT ct.teacher_id), COUNT(DISTINCT cr.student_id)
        FROM Courses c
        LEFT JOIN CourseTeachers ct ON c.id = ct.course_id
        LEFT JOIN Credits cr ON c.id = cr.course_id
        GROUP BY c.id
        ORDER BY c.name ASC
    """)
    return cursor.fetchall()

# hakee listan opettajista kursseineen (aakkosjärjestyksessä opettajat ja kurssit)
def teacher_list():
    cursor = db.cursor()
    cursor.execute("""
        SELECT t.name, GROUP_CONCAT(c.name, ',')
        FROM Teachers t
        LEFT JOIN CourseTeachers ct ON t.id = ct.teacher_id
        LEFT JOIN Courses c ON c.id = ct.course_id
        GROUP BY t.id
        ORDER BY t.name ASC
    """)
    teachers = cursor.fetchall()
    
    # Ryhmitellään opettajat ja heidän opettamansa kurssit
    teacher_course_list = []
    for teacher, courses in teachers:
        if courses:
            course_list = courses.split(',')
        else:
            course_list = []
        teacher_course_list.append((teacher, course_list))

    return teacher_course_list
    
    # Ryhmitellään opettajat ja heidän opettamansa kurssit
    teacher_course_dict = {}
    for teacher, course in teachers:
        if teacher not in teacher_course_dict:
            teacher_course_dict[teacher] = []
        if course:
            teacher_course_dict[teacher].append(course)

    # Muodostetaan lopullinen lista opettajista ja heidän kursseistaan
    teacher_course_list = [(teacher, courses) for teacher, courses in teacher_course_dict.items()]

    return teacher_course_list


# hakee ryhmän jäsenet (opettajat ja opiskelijat nimien mukaan)
# hakee ryhmän jäsenet (opettajat ja opiskelijat nimien mukaan)
def group_people(group_name):
    cursor = db.cursor()
    cursor.execute("""
        SELECT g.id
        FROM Groups g
        WHERE g.name = ?
    """, (group_name,))
    group_id = cursor.fetchone()
    
    if not group_id:
        return None
    group_id = group_id[0]

    cursor.execute("""
        SELECT t.name
        FROM Teachers t
        JOIN GroupTeachers gt ON t.id = gt.teacher_id
        WHERE gt.group_id = ?
        ORDER BY t.name ASC
    """, (group_id,))
    teachers = [row[0] for row in cursor.fetchall()]

    cursor.execute("""
        SELECT s.name
        FROM Students s
        JOIN GroupStudents gs ON s.id = gs.student_id
        WHERE gs.group_id = ?
        ORDER BY s.name ASC
    """, (group_id,))
    students = [row[0] for row in cursor.fetchall()]

    # Yhdistetään opettajat ja opiskelijat yhdeksi listaksi ja lajitellaan aakkosjärjestykseen
    members = teachers + students
    members.sort()

    return members


# hakee ryhmien opintopisteet
# hakee ryhmien opintopisteet
def credits_in_groups():
    cursor = db.cursor()
    cursor.execute("""
        SELECT g.name, COALESCE(SUM(c.credits), 0) AS total_credits
        FROM Groups g
        LEFT JOIN GroupStudents gs ON g.id = gs.group_id
        LEFT JOIN Credits cr ON gs.student_id = cr.student_id
        LEFT JOIN Courses c ON cr.course_id = c.id
        GROUP BY g.id
        ORDER BY g.name ASC
    """)
    return cursor.fetchall()


# hakee yhteiset ryhmät opettajalle ja opiskelijalle
def common_groups(teacher_name, student_name):
    cursor = db.cursor()
    cursor.execute("""
        SELECT g.name
        FROM Groups g
        JOIN GroupTeachers gt ON g.id = gt.group_id
        JOIN Teachers t ON t.id = gt.teacher_id
        JOIN GroupStudents gs ON g.id = gs.group_id
        JOIN Students s ON s.id = gs.student_id
        WHERE t.name = ? AND s.name = ?
        ORDER BY g.name ASC
    """, (teacher_name, student_name))
    return [row[0] for row in cursor.fetchall()]
