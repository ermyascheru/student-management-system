# ============================================
# SCHOOL MANAGEMENT SYSTEM
# ============================================

from datetime import datetime
from typing import Optional

# --------------------------------------------
# BASE PERSON CLASS
# --------------------------------------------
class Person:
    """
    Base class for all people in the school system.
    
    This demonstrates INHERITANCE - Student and Teacher
    will inherit from this class to share common attributes.
    """
    
    def __init__(self, person_id: str, name: str, email: str, phone: str):
        # Protected attributes (single underscore convention)
        self._person_id = person_id
        self._name = name
        self._email = email
        self._phone = phone
        self._created_at = datetime.now()
    
    # ENCAPSULATION: Using properties to control access to attributes
    @property
    def person_id(self) -> str:
        return self._person_id
    
    @property
    def name(self) -> str:
        return self._name
    
    @name.setter
    def name(self, value: str):
        if not value.strip():
            raise ValueError("Name cannot be empty")
        self._name = value
    
    @property
    def email(self) -> str:
        return self._email
    
    @email.setter
    def email(self, value: str):
        if "@" not in value:
            raise ValueError("Invalid email format")
        self._email = value
    
    def get_info(self) -> dict:
        """Returns basic information about the person."""
        return {
            "id": self._person_id,
            "name": self._name,
            "email": self._email,
            "phone": self._phone
        }
    
    def __str__(self) -> str:
        return f"{self._name} (ID: {self._person_id})"


# --------------------------------------------
# STUDENT CLASS
# --------------------------------------------
class Student(Person):
    """
    Student class inheriting from Person.
    
    INHERITANCE: Reuses Person's attributes and methods.
    POLYMORPHISM: Overrides get_info() to include student-specific data.
    """
    
    def __init__(self, student_id: str, name: str, email: str, 
                 phone: str, grade_level: int, date_of_birth: str):
        # Call parent class constructor
        super().__init__(student_id, name, email, phone)
        
        self._grade_level = grade_level
        self._date_of_birth = date_of_birth
        self._enrolled_courses: list['Course'] = []  # Courses student is enrolled in
        self._grades: dict[str, float] = {}  # course_id -> grade
        self._attendance: dict[str, list[bool]] = {}  # course_id -> [present/absent]
    
    @property
    def grade_level(self) -> int:
        return self._grade_level
    
    @grade_level.setter
    def grade_level(self, value: int):
        if not 1 <= value <= 12:
            raise ValueError("Grade level must be between 1 and 12")
        self._grade_level = value
    
    def enroll_in_course(self, course: 'Course') -> bool:
        """Enroll student in a course."""
        if course in self._enrolled_courses:
            print(f"{self._name} is already enrolled in {course.name}")
            return False
        
        self._enrolled_courses.append(course)
        self._attendance[course.course_id] = []
        course.add_student(self)
        print(f"✓ {self._name} enrolled in {course.name}")
        return True
    
    def drop_course(self, course: 'Course') -> bool:
        """Remove student from a course."""
        if course not in self._enrolled_courses:
            print(f"{self._name} is not enrolled in {course.name}")
            return False
        
        self._enrolled_courses.remove(course)
        course.remove_student(self)
        print(f"✓ {self._name} dropped {course.name}")
        return True
    
    def record_attendance(self, course_id: str, present: bool):
        """Record attendance for a specific course."""
        if course_id in self._attendance:
            self._attendance[course_id].append(present)
    
    def get_attendance_rate(self, course_id: str) -> float:
        """Calculate attendance percentage for a course."""
        if course_id not in self._attendance or not self._attendance[course_id]:
            return 0.0
        
        records = self._attendance[course_id]
        return (sum(records) / len(records)) * 100
    
    def set_grade(self, course_id: str, grade: float):
        """Set grade for a course."""
        if not 0 <= grade <= 100:
            raise ValueError("Grade must be between 0 and 100")
        self._grades[course_id] = grade
    
    def get_grade(self, course_id: str) -> Optional[float]:
        """Get grade for a specific course."""
        return self._grades.get(course_id)
    
    def calculate_gpa(self) -> float:
        """
        Calculate GPA on a 4.0 scale.
        
        Grade to GPA conversion:
        90-100: 4.0, 80-89: 3.0, 70-79: 2.0, 60-69: 1.0, <60: 0.0
        """
        if not self._grades:
            return 0.0
        
        gpa_points = []
        for grade in self._grades.values():
            if grade >= 90:
                gpa_points.append(4.0)
            elif grade >= 80:
                gpa_points.append(3.0)
            elif grade >= 70:
                gpa_points.append(2.0)
            elif grade >= 60:
                gpa_points.append(1.0)
            else:
                gpa_points.append(0.0)
        
        return sum(gpa_points) / len(gpa_points)
    
    # POLYMORPHISM: Override parent's get_info method
    def get_info(self) -> dict:
        """Returns complete student information."""
        info = super().get_info()  # Get base info from parent
        info.update({
            "grade_level": self._grade_level,
            "date_of_birth": self._date_of_birth,
            "enrolled_courses": [c.name for c in self._enrolled_courses],
            "gpa": round(self.calculate_gpa(), 2)
        })
        return info
    
    def __repr__(self):
        return f"Student({self._name}, Grade {self._grade_level})"


# --------------------------------------------
# TEACHER CLASS
# --------------------------------------------
class Teacher(Person):
    """
    Teacher class inheriting from Person.
    
    Manages course assignments and student grading.
    """
    
    def __init__(self, teacher_id: str, name: str, email: str,
                 phone: str, department: str, salary: float):
        super().__init__(teacher_id, name, email, phone)
        
        self._department = department
        self._salary = salary
        self._assigned_courses: list['Course'] = []
        self._hire_date = datetime.now()
    
    @property
    def department(self) -> str:
        return self._department
    
    @property
    def salary(self) -> float:
        return self._salary
    
    @salary.setter
    def salary(self, value: float):
        if value < 0:
            raise ValueError("Salary cannot be negative")
        self._salary = value
    
    def assign_course(self, course: 'Course'):
        """Assign teacher to a course."""
        if course not in self._assigned_courses:
            self._assigned_courses.append(course)
            course.assign_teacher(self)
            print(f"✓ {self._name} assigned to teach {course.name}")
    
    def grade_student(self, student: Student, course: 'Course', grade: float):
        """Grade a student in one of the teacher's courses."""
        if course not in self._assigned_courses:
            print(f"Error: {self._name} doesn't teach {course.name}")
            return False
        
        student.set_grade(course.course_id, grade)
        print(f"✓ {student.name} received {grade}% in {course.name}")
        return True
    
    def take_attendance(self, course: 'Course', attendance_dict: dict[str, bool]):
        """
        Record attendance for all students in a course.
        
        attendance_dict: {student_id: True/False}
        """
        if course not in self._assigned_courses:
            print(f"Error: {self._name} doesn't teach {course.name}")
            return
        
        for student in course.students:
            if student.person_id in attendance_dict:
                student.record_attendance(
                    course.course_id, 
                    attendance_dict[student.person_id]
                )
        print(f"✓ Attendance recorded for {course.name}")
    
    def get_info(self) -> dict:
        info = super().get_info()
        info.update({
            "department": self._department,
            "courses_teaching": [c.name for c in self._assigned_courses],
            "hire_date": self._hire_date.strftime("%Y-%m-%d")
        })
        return info
    
    def __repr__(self):
        return f"Teacher({self._name}, {self._department})"


# --------------------------------------------
# COURSE CLASS
# --------------------------------------------
class Course:
    """
    Represents a course in the school.
    
    COMPOSITION: Contains references to Teacher and Students.
    """
    
    def __init__(self, course_id: str, name: str, description: str,
                 credits: int, max_students: int = 30):
        self._course_id = course_id
        self._name = name
        self._description = description
        self._credits = credits
        self._max_students = max_students
        self._teacher: Optional[Teacher] = None
        self._students: list[Student] = []
        self._schedule: dict = {}  # day -> time
    
    @property
    def course_id(self) -> str:
        return self._course_id
    
    @property
    def name(self) -> str:
        return self._name
    
    @property
    def students(self) -> list[Student]:
        return self._students.copy()  # Return copy to prevent direct modification
    
    @property
    def teacher(self) -> Optional[Teacher]:
        return self._teacher
    
    def assign_teacher(self, teacher: Teacher):
        """Assign a teacher to this course."""
        self._teacher = teacher
    
    def add_student(self, student: Student) -> bool:
        """Add a student to the course."""
        if len(self._students) >= self._max_students:
            print(f"Error: {self._name} is full")
            return False
        
        if student not in self._students:
            self._students.append(student)
            return True
        return False
    
    def remove_student(self, student: Student) -> bool:
        """Remove a student from the course."""
        if student in self._students:
            self._students.remove(student)
            return True
        return False
    
    def set_schedule(self, schedule: dict):
        """
        Set course schedule.
        Example: {"Monday": "09:00-10:30", "Wednesday": "09:00-10:30"}
        """
        self._schedule = schedule
    
    def get_class_average(self) -> float:
        """Calculate the average grade for this course."""
        grades = []
        for student in self._students:
            grade = student.get_grade(self._course_id)
            if grade is not None:
                grades.append(grade)
        
        return sum(grades) / len(grades) if grades else 0.0
    
    def get_info(self) -> dict:
        return {
            "course_id": self._course_id,
            "name": self._name,
            "description": self._description,
            "credits": self._credits,
            "teacher": self._teacher.name if self._teacher else "Unassigned",
            "enrolled": len(self._students),
            "max_students": self._max_students,
            "schedule": self._schedule,
            "class_average": round(self.get_class_average(), 2)
        }
    
    def __str__(self):
        return f"{self._name} ({self._course_id})"
    
    def __repr__(self):
        return f"Course({self._name}, {len(self._students)} students)"


# --------------------------------------------
# SCHOOL MANAGEMENT SYSTEM (MAIN CONTROLLER)
# --------------------------------------------
class SchoolManagementSystem:
    """
    Main controller class that manages the entire school system.
    
    FACADE PATTERN: Provides a simplified interface to the complex
    subsystem of students, teachers, and courses.
    """
    
    def __init__(self, school_name: str):
        self._school_name = school_name
        self._students: dict[str, Student] = {}
        self._teachers: dict[str, Teacher] = {}
        self._courses: dict[str, Course] = {}
        
        # Auto-increment IDs
        self._next_student_id = 1
        self._next_teacher_id = 1
        self._next_course_id = 1
    
    def _generate_student_id(self) -> str:
        id_str = f"STU{self._next_student_id:04d}"
        self._next_student_id += 1
        return id_str
    
    def _generate_teacher_id(self) -> str:
        id_str = f"TCH{self._next_teacher_id:04d}"
        self._next_teacher_id += 1
        return id_str
    
    def _generate_course_id(self) -> str:
        id_str = f"CRS{self._next_course_id:04d}"
        self._next_course_id += 1
        return id_str
    
    # ========== STUDENT MANAGEMENT ==========
    
    def add_student(self, name: str, email: str, phone: str,
                    grade_level: int, date_of_birth: str) -> Student:
        """Register a new student in the school."""
        student_id = self._generate_student_id()
        student = Student(student_id, name, email, phone, grade_level, date_of_birth)
        self._students[student_id] = student
        print(f"✓ Student registered: {student}")
        return student
    
    def get_student(self, student_id: str) -> Optional[Student]:
        """Find a student by ID."""
        return self._students.get(student_id)
    
    def remove_student(self, student_id: str) -> bool:
        """Remove a student from the school."""
        if student_id in self._students:
            student = self._students.pop(student_id)
            print(f"✓ Student removed: {student.name}")
            return True
        print(f"Error: Student {student_id} not found")
        return False
    
    def list_students(self, grade_level: Optional[int] = None) -> list[Student]:
        """List all students, optionally filtered by grade level."""
        students = list(self._students.values())
        if grade_level is not None:
            students = [s for s in students if s.grade_level == grade_level]
        return students
    
    # ========== TEACHER MANAGEMENT ==========
    
    def hire_teacher(self, name: str, email: str, phone: str,
                     department: str, salary: float) -> Teacher:
        """Hire a new teacher."""
        teacher_id = self._generate_teacher_id()
        teacher = Teacher(teacher_id, name, email, phone, department, salary)
        self._teachers[teacher_id] = teacher
        print(f"✓ Teacher hired: {teacher}")
        return teacher
    
    def get_teacher(self, teacher_id: str) -> Optional[Teacher]:
        """Find a teacher by ID."""
        return self._teachers.get(teacher_id)
    
    def remove_teacher(self, teacher_id: str) -> bool:
        """Remove a teacher from the school."""
        if teacher_id in self._teachers:
            teacher = self._teachers.pop(teacher_id)
            print(f"✓ Teacher removed: {teacher.name}")
            return True
        print(f"Error: Teacher {teacher_id} not found")
        return False
    
    def list_teachers(self, department: Optional[str] = None) -> list[Teacher]:
        """List all teachers, optionally filtered by department."""
        teachers = list(self._teachers.values())
        if department is not None:
            teachers = [t for t in teachers if t.department == department]
        return teachers
    
    # ========== COURSE MANAGEMENT ==========
    
    def create_course(self, name: str, description: str,
                      credits: int, max_students: int = 30) -> Course:
        """Create a new course."""
        course_id = self._generate_course_id()
        course = Course(course_id, name, description, credits, max_students)
        self._courses[course_id] = course
        print(f"✓ Course created: {course}")
        return course
    
    def get_course(self, course_id: str) -> Optional[Course]:
        """Find a course by ID."""
        return self._courses.get(course_id)
    
    def remove_course(self, course_id: str) -> bool:
        """Remove a course from the school."""
        if course_id in self._courses:
            course = self._courses.pop(course_id)
            print(f"✓ Course removed: {course.name}")
            return True
        print(f"Error: Course {course_id} not found")
        return False
    
    def list_courses(self) -> list[Course]:
        """List all courses."""
        return list(self._courses.values())
    
    # ========== REPORTS ==========
    
    def generate_student_report(self, student_id: str) -> dict:
        """Generate a comprehensive report for a student."""
        student = self.get_student(student_id)
        if not student:
            return {"error": "Student not found"}
        
        report = student.get_info()
        report["grades"] = {}
        
        for course in student._enrolled_courses:
            grade = student.get_grade(course.course_id)
            attendance = student.get_attendance_rate(course.course_id)
            report["grades"][course.name] = {
                "grade": grade if grade else "Not graded",
                "attendance_rate": f"{attendance:.1f}%"
            }
        
        return report
    
    def generate_course_report(self, course_id: str) -> dict:
        """Generate a comprehensive report for a course."""
        course = self.get_course(course_id)
        if not course:
            return {"error": "Course not found"}
        
        report = course.get_info()
        report["student_grades"] = {}
        
        for student in course.students:
            grade = student.get_grade(course_id)
            report["student_grades"][student.name] = grade if grade else "Not graded"
        
        return report
    
    def get_school_statistics(self) -> dict:
        """Get overall school statistics."""
        total_students = len(self._students)
        total_teachers = len(self._teachers)
        total_courses = len(self._courses)
        
        # Calculate overall GPA
        gpas = [s.calculate_gpa() for s in self._students.values()]
        avg_gpa = sum(gpas) / len(gpas) if gpas else 0.0
        
        # Students per grade level
        grade_distribution = {}
        for student in self._students.values():
            level = student.grade_level
            grade_distribution[level] = grade_distribution.get(level, 0) + 1
        
        return {
            "school_name": self._school_name,
            "total_students": total_students,
            "total_teachers": total_teachers,
            "total_courses": total_courses,
            "average_gpa": round(avg_gpa, 2),
            "grade_distribution": grade_distribution
        }


# ============================================
# DEMONSTRATION / USAGE EXAMPLE
# ============================================

def main():
    """Demonstrate the School Management System."""
    
    print("=" * 60)
    print("SCHOOL MANAGEMENT SYSTEM DEMO")
    print("=" * 60)
    
    # Initialize the school
    school = SchoolManagementSystem("Sunrise High School")
    
    # ----- Add Teachers -----
    print("\n📚 HIRING TEACHERS...")
    teacher1 = school.hire_teacher(
        "Dr. Sarah Johnson", "sarah.j@school.edu", "555-0101",
        "Mathematics", 65000
    )
    teacher2 = school.hire_teacher(
        "Mr. James Wilson", "james.w@school.edu", "555-0102",
        "Science", 62000
    )
    
    # ----- Create Courses -----
    print("\n📖 CREATING COURSES...")
    math_course = school.create_course(
        "Algebra II", "Advanced algebraic concepts", 4, 25
    )
    science_course = school.create_course(
        "Physics 101", "Introduction to physics", 4, 25
    )
    
    # ----- Assign Teachers to Courses -----
    print("\n👨‍🏫 ASSIGNING TEACHERS...")
    teacher1.assign_course(math_course)
    teacher2.assign_course(science_course)
    
    # ----- Set Course Schedules -----
    math_course.set_schedule({
        "Monday": "09:00-10:30",
        "Wednesday": "09:00-10:30",
        "Friday": "09:00-10:30"
    })
    
    # ----- Add Students -----
    print("\n🎓 REGISTERING STUDENTS...")
    student1 = school.add_student(
        "Alice Chen", "alice.c@student.edu", "555-1001",
        10, "2008-05-15"
    )
    student2 = school.add_student(
        "Bob Martinez", "bob.m@student.edu", "555-1002",
        10, "2008-08-22"
    )
    student3 = school.add_student(
        "Carol Davis", "carol.d@student.edu", "555-1003",
        10, "2008-03-10"
    )
    
    # ----- Enroll Students in Courses -----
    print("\n📝 ENROLLING STUDENTS...")
    student1.enroll_in_course(math_course)
    student1.enroll_in_course(science_course)
    student2.enroll_in_course(math_course)
    student2.enroll_in_course(science_course)
    student3.enroll_in_course(math_course)
    
    # ----- Record Attendance -----
    print("\n📋 RECORDING ATTENDANCE...")
    attendance_day1 = {
        student1.person_id: True,
        student2.person_id: True,
        student3.person_id: False
    }
    teacher1.take_attendance(math_course, attendance_day1)
    
    # ----- Grade Students -----
    print("\n✏️ GRADING STUDENTS...")
    teacher1.grade_student(student1, math_course, 95)
    teacher1.grade_student(student2, math_course, 87)
    teacher1.grade_student(student3, math_course, 78)
    teacher2.grade_student(student1, science_course, 92)
    teacher2.grade_student(student2, science_course, 85)
    
    # ----- Generate Reports -----
    print("\n" + "=" * 60)
    print("📊 REPORTS")
    print("=" * 60)
    
    # Student Report
    print("\n--- Student Report: Alice Chen ---")
    report = school.generate_student_report(student1.person_id)
    for key, value in report.items():
        print(f"  {key}: {value}")
    
    # Course Report
    print("\n--- Course Report: Algebra II ---")
    report = school.generate_course_report(math_course.course_id)
    for key, value in report.items():
        print(f"  {key}: {value}")
    
    # School Statistics
    print("\n--- School Statistics ---")
    stats = school.get_school_statistics()
    for key, value in stats.items():
        print(f"  {key}: {value}")


if __name__ == "__main__":
    main()
