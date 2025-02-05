import sqlite3
import sys
import random
from faker import Faker


def main():
    qt_students_generated = 10
    SUBJECTS = (
        (1, "Matemática"),
        (2, "Geografia"),
        (3, "Língua Portuguesa"),
        (4, "Biologia"),
        (5, "Física"),
        (6, "Química"),
        (7, "História")
    )

    if len(sys.argv) > 1:
        try:
            qt_students_generated = int(sys.argv[1])
        except:
            raise TypeError(f"Cannot convert '{sys.argv[1]}' into an integer.")

    fake = Faker("pt_BR")
    student_rows = []

    for n in range(qt_students_generated):
        full_name = fake.first_name() + " " + fake.last_name()

        for subject_id, _ in SUBJECTS:
            grade = round(random.uniform(0, 10), 1)
            student_rows.append([full_name, subject_id, grade])

    with sqlite3.connect("students.db") as conn:
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS subjects(
                id INTEGER,
                name VARCHAR(300) NOT NULL UNIQUE,
                PRIMARY KEY (id)
            );
        """)
        cursor.executemany("INSERT INTO subjects VALUES(?, ?) ON CONFLICT (id) DO NOTHING", SUBJECTS)
        conn.commit()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS students(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                full_name VARCHAR(300) NOT NULL,
                subject INTEGER NOT NULL,
                grade DECIMAL(2,1) NOT NULL,

                FOREIGN KEY(subject) REFERENCES subjects(id)
            );
        """)
        cursor.executemany("INSERT INTO students(full_name, subject, grade) VALUES(?, ?, ?)", student_rows)
        conn.commit()


if __name__ == '__main__':
    main()
