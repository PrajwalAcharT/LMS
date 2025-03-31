from flask import Blueprint, render_template, redirect, url_for, flash, request
from app import db
from app.models import Course, User, Enrollment, Section, Lesson
from flask_login import login_required, current_user

main = Blueprint('main', __name__)

@main.route('/')
def index():
    courses = Course.query.all()
    return render_template('index.html', courses=courses)

@main.route('/course/<int:course_id>')
def course(course_id):
    course = Course.query.get_or_404(course_id)
    is_enrolled = False
    if current_user.is_authenticated:
        is_enrolled = Enrollment.query.filter_by(
            student_id=current_user.id, 
            course_id=course_id
        ).first() is not None
    return render_template('course.html', course=course, is_enrolled=is_enrolled)

@main.route('/enroll/<int:course_id>', methods=['POST'])
@login_required
def enroll(course_id):
    course = Course.query.get_or_404(course_id)
    if not Enrollment.query.filter_by(student_id=current_user.id, course_id=course_id).first():
        enrollment = Enrollment(student_id=current_user.id, course_id=course_id)
        db.session.add(enrollment)
        db.session.commit()
        flash('Successfully enrolled in the course!', 'success')
    return redirect(url_for('main.course', course_id=course_id))

@main.route('/my-courses')
@login_required
def my_courses():
    enrollments = current_user.enrollments
    return render_template('my_courses.html', enrollments=enrollments)
