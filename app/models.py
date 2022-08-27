import flask
from datetime import datetime

from . import db


class school(db.Model):
    __tablename__ = 'school'

    school_id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(255), nullable = False)
    nickname = db.Column(db.String(128), nullable = False)
    associated_image = db.Column(db.String(128))


class sport_assignment(db.Model):
    __tablename__ = 'sport_assignment'

    assignment_id = db.Column(db.Integer, primary_key = True)
    associated_image = db.Column(db.String(128))
    description = db.Column(db.String(64))

    date_created = db.Column(db.DateTime, default = datetime.utcnow)
    last_updated = db.Column(db.DateTime, default = datetime.utcnow, 
            onupdate = datetime.utcnow)

    #relationships
    student_id = db.Column(db.Integer, db.ForeignKey('student.admission_no'), nullable = False)
    position_id = db.Column(db.Integer, db.ForeignKey('sport_position.position_id'),
            nullable = False)


class sport_event(db.Model):
    __tablename__ = 'sport_event'

    event_id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(255), nullable = False)
    associated_image = db.Column(db.String(128))
    date_held = db.Column(db.Date, nullable = False)

    associated_report = db.Column(db.Text)

    date_created = db.Column(db.DateTime, default = datetime.utcnow)
    last_updated = db.Column(db.DateTime, default = datetime.utcnow, 
            onupdate = datetime.utcnow)

    #relationships
    created_by = db.Column(db.Integer, db.ForeignKey('student.admission_no'))
    team_id = db.Column(db.Integer, db.ForeignKey('sport_team.team_id'), 
            nullable = False)


class sport_team(db.Model):
    __tablename__ = 'sport_team'

    team_id = db.Column(db.Integer, primary_key = True)
    team_name = db.Column(db.String(128), nullable = False)
    
    date_created = db.Column(db.DateTime, default = datetime.utcnow)
    last_updated = db.Column(db.DateTime, default = datetime.utcnow, 
            onupdate = datetime.utcnow)

    #relationships
    sport_id = db.Column(db.Integer, db.ForeignKey('sport.sport_id'), 
            nullable = False)


class sport_position(db.Model):
    __tablename__ = 'sport_position'

    position_id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(64), nullable = False)

    #relationships
    team_id = db.Column(db.Integer, db.ForeignKey('sport_team.team_id'), 
            nullable = False)



class sport_notification(db.Model):
    __tablename__ = 'sport_notification'

    notification_id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(255), nullable = False)
    associated_image = db.Column(db.String(128))
    description = db.Column(db.Text, nullable = False)

    date_created = db.Column(db.DateTime, default = datetime.utcnow)
    last_update = db.Column(db.DateTime, default = datetime.utcnow, 
            onupdate = datetime.utcnow)

    #relationships
    created_by = db.Column(db.Integer, db.ForeignKey('sport_coach.coach_id'), 
            nullable = False)


class sport_coach(db.Model):
    __tablename__ = 'sport_coach'

    coach_id = db.Column(db.Integer, primary_key = True)

    first_name = db.Column(db.String(64), nullable = False)
    middle_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))

    email_address = db.Column(db.String(128), nullable = False)
    phone_no = db.Column(db.String(32), nullable = False)
    residential_address = db.Column(db.String(128))
    associated_image = db.Column(db.String(255))

    year_appointed = db.Column(db.String(8), nullable = False)
    status = db.Column(db.String(32), default = 'active')

    #relationships
    sport_id = db.Column(db.Integer, db.ForeignKey('sport.sport_id'), 
            nullable = False)


class sport(db.Model):
    __tablename__ = 'sport'

    sport_id = db.Column(db.Integer, primary_key = True)
    sport_name = db.Column(db.String(128), unique = True, index = True, 
            nullable = False)
    year_established = db.Column(db.String(8))
    associated_image = db.Column(db.String(128))

    #relationships
    patron_id = db.Column(db.Integer, db.ForeignKey('teacher.teacher_id'))



class related_book(db.Model):
    __tablename__ = "related_book"

    related_book_id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(255), nullable = False)
    year_of_production = db.Column(db.String(4))
    reference = db.Column(db.String(255))
    image = db.Column(db.String(128))

    #relationships
    book_author_id = db.Column(db.Integer, db.ForeignKey('book_author.author_id'), 
            nullable = False)
    book_category_id = db.Column(db.Integer, db.ForeignKey('book_category.category_id'),
            nullable = False)


class author_assignment(db.Model):
    __tablename__ = 'author_assignment'

    assignment_id = db.Column(db.Integer, primary_key = True)

    author_id = db.Column(db.Integer, db.ForeignKey('book_author.author_id'), 
            nullable = False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.book_id'), nullable = False)

    date_created = db.Column(db.DateTime, default = datetime.utcnow)
    last_updated = db.Column(db.DateTime, default = datetime.utcnow,
            onupdate = datetime.utcnow)


class publisher_contact(db.Model):
    __tablename__ = 'publisher_contact'

    contact_id = db.Column(db.Integer, primary_key = True)
    contact_detail = db.Column(db.String(32), nullable = False)
    
    #relationships
    publisher_id = db.Column(db.Integer, db.ForeignKey('publisher.publisher_id'), 
            nullable = False)

    date_created = db.Column(db.DateTime, default = datetime.utcnow)
    last_updated = db.Column(db.DateTime, default = datetime.utcnow, 
            onupdate = datetime.utcnow)


class publisher(db.Model):
    __tablename__ = 'publisher'

    publisher_id = db.Column(db.Integer, primary_key = True)
    publisher_name = db.Column(db.String(255), nullable = False, index = True)
    location = db.Column(db.String(255), nullable = False)
    reference = db.Column(db.String(255))
    image = db.Column(db.String(128))

    date_created = db.Column(db.DateTime, default = datetime.utcnow)
    last_updated = db.Column(db.DateTime, default = datetime.utcnow, 
            onupdate = datetime.utcnow)


class book_assignment(db.Model):
    _tablename__ = "book_assignment"

    assignment_id = db.Column(db.Integer, primary_key = True)

    date_created = db.Column(db.DateTime, default = datetime.utcnow)
    last_updated = db.Column(db.DateTime,default = datetime.utcnow)

    #relationships
    student_id = db.Column(db.Integer, db.ForeignKey('student.admission_no'), 
            nullable = False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.book_id'), nullable = False)


class book_category(db.Model):
    __tablename__ = 'book_category'

    category_id = db.Column(db.Integer, primary_key = True, index = True, 
            nullable = False)
    category_name = db.Column(db.String(64), nullable = False)


class book(db.Model):
    __tablename__ = 'book'

    book_id = db.Column(db.Integer, primary_key = True, index = True, nullable = False)

    title = db.Column(db.String(128), nullable = False)
    year_of_production = db.Column(db.String(4),nullable = False, index = True)
    image = db.Column(db.String(128))

    status = db.Column(db.String(32), default = "available")

    #relationships
    book_category_id = db.Column(db.Integer, db.ForeignKey('book_category.category_id'), 
            nullable = False)
    publisher_id = db.Column(db.Integer, db.ForeignKey('publisher.publisher_id'), 
            nullable = False)


class book_author(db.Model):
    __tablename__ = 'book_author'


    author_id = db.Column(db.Integer, primary_key = True, nullable = False, index = True)

    first_name = db.Column(db.String(64), nullable = False)
    middle_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    gender = db.Column(db.String(32), nullable = False, default = 'Female')
    residential_address = db.Column(db.String(255))
    email_address = db.Column(db.String(255))
    phone_no = db.Column(db.String(32))
    associated_image = db.Column(db.String(255))

    date_created = db.Column(db.DateTime, default = datetime.now)
    last_updated = db.Column(db.DateTime, default = datetime.now, onupdate = datetime.now)


class medical_intake(db.Model):
    intake_id = db.Column(db.Integer, primary_key = True)
    time_taken = db.Column(db.DateTime, default = datetime.now)
    
    #relationships
    record_id = db.Column(db.Integer, db.ForeignKey('medical_record.record_id'))


class medication_stock(db.Model):
    stock_id = db.Column(db.Integer, primary_key = True)
    description = db.Column(db.String(64), nullable = False)
    units = db.Column(db.String(32), nullable = False)


class current_stock(db.Model):
    current_stock_id = db.Column(db.Integer, primary_key = True)
    stock_id = db.Column(db.Integer, db.ForeignKey('medication_stock.stock_id'))
    quantity = db.Column(db.Integer, default = 1)

    date_created = db.Column(db.DateTime, default = datetime.now)
    last_updated = db.Column(db.DateTime, default = datetime.now, onupdate = datetime.now)


class hospital_services(db.Model):
    service_id = db.Column(db.Integer, primary_key = True)
    description = db.Column(db.Integer, nullable = False)

    #relationships
    hospital_id = db.Column(db.Integer, db.ForeignKey('hospital.hospital_id'))


class hospital(db.Model):
    hospital_id = db.Column(db.Integer, primary_key = True)
    hospital_name = db.Column(db.String(128), nullable = False)
    location_address = db.Column(db.String(128))
    email_address = db.Column(db.String(128))
    phone_no = db.Column(db.String(32))
    associated_image = db.Column(db.String(128))


class doctor_speciality(db.Model):
    doc_speciality_id = db.Column(db.Integer, primary_key = True)
    description = db.Column(db.String(128), nullable = False)

    #relationships
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.doctor_id'))


class doctor(db.Model):
    doctor_id = db.Column(db.Integer, primary_key = True)

    first_name = db.Column(db.String(64), nullable = False)
    middle_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    gender = db.Column(db.String(32), nullable = False, default = 'Female')
    date_of_birth = db.Column(db.Date, nullable = False)
    national_id_no = db.Column(db.Integer, nullable = False)

    residential_address = db.Column(db.String(255))
    email_address = db.Column(db.String(255))
    phone_no = db.Column(db.String(32))
    associated_image = db.Column(db.String(255))

    status = db.Column(db.String(32))

    date_created = db.Column(db.DateTime, default = datetime.now)
    last_updated = db.Column(db.DateTime, default = datetime.now, onupdate = datetime.now)

    #relationships
    hospital_id = db.Column(db.Integer, db.ForeignKey('hospital.hospital_id'))


class reference_medication(db.Model):
    ref_med_id = db.Column(db.Integer, primary_key = True)
    description = db.Column(db.String(128), nullable = False)
    dosage = db.Column(db.String(16), nullable = False)
    frequency = db.Column(db.Integer, nullable = False)
    period = db.Column(db.Integer, nullable = False)

    #relationships
    reference_id = db.Column(db.Integer, db.ForeignKey('reference.reference_id'))


class medication(db.Model):
    medication_id = db.Column(db.Integer, primary_key = True)

    dosage = db.Column(db.String(16), nullable = False)
    frequency = db.Column(db.Integer, nullable = False)
    period = db.Column(db.Integer, nullable = False)

    #relationships
    stock_id = db.Column(db.Integer, db.ForeignKey('medication_stock.stock_id'))


class san_room(db.Model):
    san_room_id = db.Column(db.Integer, primary_key = True)
    description = db.Column(db.String(32))

    date_created = db.Column(db.DateTime, default = datetime.now)
    last_updated = db.Column(db.DateTime, default = datetime.now, onupdate = datetime.now)


class bed(db.Model):
    bed_id = db.Column(db.Integer, primary_key = True)
    description = db.Column(db.String(32), nullable = False)

    date_created = db.Column(db.DateTime, default = datetime.now)
    last_updated = db.Column(db.DateTime, default = datetime.now, onupdate = datetime.now)

    #relationships
    san_room_id = db.Column(db.Integer, db.ForeignKey('san_room.san_room_id'))


class inpatient_admission(db.Model):
    inpatient_id = db.Column(db.Integer, primary_key = True)

    date_created = db.Column(db.DateTime, default = datetime.now)
    last_updated = db.Column(db.DateTime, default = datetime.now, onupdate = datetime.now)

    #relationships
    record_id = db.Column(db.Integer, db.ForeignKey('medical_record.record_id'))
    bed_id = db.Column(db.Integer, db.ForeignKey('bed.bed_id'))


class reference(db.Model):
    reference_id = db.Column(db.Integer, primary_key = True)
    date_created = db.Column(db.DateTime, default = datetime.now)
    last_updated = db.Column(db.DateTime, default = datetime.now, onupdate = datetime.now)

    #relationships
    record_id = db.Column(db.Integer, db.ForeignKey('medical_record.record_id'))
    hospital_id = db.Column(db.Integer, db.ForeignKey('hospital.hospital_id'))


class diagnosis(db.Model):
    diagnosis_id = db.Column(db.Integer, primary_key = True)
    description = db.Column(db.String(255), nullable = False)

    #relationships
    record_id = db.Column(db.Integer, db.ForeignKey('medical_record.record_id'))


class nurse(db.Model):
    nurse_id = db.Column(db.Integer, primary_key = True)

    first_name = db.Column(db.String(64), nullable = False)
    middle_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    gender = db.Column(db.String(32), nullable = False, default = 'Female')
    date_of_birth = db.Column(db.Date, nullable = False)
    national_id_no = db.Column(db.Integer, nullable = False)

    residential_address = db.Column(db.String(255))
    email_address = db.Column(db.String(255))
    phone_no = db.Column(db.String(32))
    associated_image = db.Column(db.String(255))

    status = db.Column(db.String(32))

    date_created = db.Column(db.DateTime, default = datetime.now)
    last_updated = db.Column(db.DateTime, default = datetime.now, onupdate = datetime.now)


class medical_record(db.Model):
    record_id = db.Column(db.Integer, primary_key = True)

    date_created = db.Column(db.DateTime, default = datetime.now)
    last_updated = db.Column(db.DateTime, default = datetime.now, onupdate = datetime.now)

    #relationships
    nurse_id = db.Column(db.Integer, db.ForeignKey('nurse.nurse_id'))
    student_id = db.Column(db.Integer,db.ForeignKey('student.admission_no'))


class teacher(db.Model):
    teacher_id = db.Column(db.Integer, primary_key = True)

    TSC_no = db.Column(db.String(32), nullable = False)
    first_name = db.Column(db.String(64), nullable = False)
    middle_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    gender = db.Column(db.String(32), nullable = False, default = 'Female')
    date_of_birth = db.Column(db.Date, nullable = False)
    national_id_no = db.Column(db.Integer, nullable = False)

    residential_address = db.Column(db.String(255))
    email_address = db.Column(db.String(255))
    phone_no = db.Column(db.String(32))
    associated_image = db.Column(db.String(255))

    date_created = db.Column(db.DateTime, default = datetime.now)
    last_updated = db.Column(db.DateTime, default = datetime.now, onupdate = datetime.now)


class classroom(db.Model):
    class_id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(32), nullable = False)

    class_teacher = db.Column(db.Integer, db.ForeignKey('teacher.teacher_id'))
    associated_image = db.Column(db.String(255))

    facebook = db.Column(db.String(128))
    instagram = db.Column(db.String(128))
    twitter = db.Column(db.String(128))

    date_created = db.Column(db.DateTime, default = datetime.now)
    last_updated = db.Column(db.DateTime, default = datetime.now, onupdate = datetime.now)


class subject(db.Model):
    subject_id = db.Column(db.Integer, primary_key = True)
    subject_title = db.Column(db.String(64), nullable = False)
    associated_image = db.Column(db.String(255))

    HOS = db.Column(db.Integer)
    email_address = db.Column(db.String(128), nullable = False)
    phone_no = db.Column(db.String(32), nullable = False)

    date_created = db.Column(db.DateTime, default = datetime.now)
    last_updated = db.Column(db.DateTime, default = datetime.now, onupdate = datetime.now)


class class_assignment(db.Model):
    class_assignment_id = db.Column(db.Integer, primary_key = True)

    class_id = db.Column(db.Integer, db.ForeignKey('classroom.class_id'), 
            nullable = False)
    subject_assignment_id = db.Column(db.Integer, 
            db.ForeignKey('subject_assignment.subject_assignment_id'),
            nullable = False)

    date_created = db.Column(db.DateTime, default = datetime.now)
    last_updated = db.Column(db.DateTime, default = datetime.now, onupdate = datetime.now)


class subject_assignment(db.Model):
    subject_assignment_id = db.Column(db.Integer, primary_key = True)

    subject_id = db.Column(db.Integer, db.ForeignKey('classroom.class_id'), nullable = False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.teacher_id'), 
            nullable = False)

    date_created = db.Column(db.DateTime, default = datetime.now)
    last_updated = db.Column(db.DateTime, default = datetime.now, onupdate = datetime.now)


class KCSE_Results(db.Model):

    __tablename__ = 'KCSE_Results'

    KCSE_ID = db.Column(db.Integer, primary_key = True)
    year = db.Column(db.String(16), nullable = False)

    A = db.Column(db.Integer)
    A_minus = db.Column(db.Integer)
    B_plus = db.Column(db.Integer)
    B = db.Column(db.Integer)
    B_minus = db.Column(db.Integer)
    C_plus = db.Column(db.Integer)
    C = db.Column(db.Integer)
    C_minus = db.Column(db.Integer)
    D_plus = db.Column(db.Integer)
    D = db.Column(db.Integer)
    D_minus = db.Column(db.Integer)
    E = db.Column(db.Integer)


class exam_assignment(db.Model):

    __tablename__ = 'exam_assignment'

    assignment_id = db.Column(db.Integer, primary_key = True)
    exam_id = db.Column(db.Integer, db.ForeignKey('exam.exam_id'))
    admission_no = db.Column(db.Integer, db.ForeignKey('student.admission_no'))

    maths = db.Column(db.Integer)
    english = db.Column(db.Integer)
    kiswahili = db.Column(db.Integer)
    biology = db.Column(db.Integer)
    chemistry = db.Column(db.Integer)
    physics = db.Column(db.Integer)

    business = db.Column(db.Integer)
    art = db.Column(db.Integer)
    music = db.Column(db.Integer)
    computer = db.Column(db.Integer)
    agriculture = db.Column(db.Integer)
    electricity = db.Column(db.Integer)
    french = db.Column(db.Integer)
    german = db.Column(db.Integer)

    geography = db.Column(db.Integer)
    CRE = db.Column(db.Integer)
    history = db.Column(db.Integer)

    last_updated = db.Column(db.DateTime, default = datetime.now, 
            onupdate = datetime.now)


class exam(db.Model):

    __tablename__ = 'exam'

    exam_id = db.Column(db.Integer, primary_key = True)
    exam_title = db.Column(db.String(255), nullable = False)
    date_created = db.Column(db.DateTime, default = datetime.now)
    last_updated = db.Column(db.DateTime, default = datetime.now, 
            onupdate = datetime.now)


class obc_achievement(db.Model):

    __tablename__ = 'obc_achievement'

    achievement_id = db.Column(db.Integer, primary_key = True)
    description = db.Column(db.String(255), nullable = False)
    year = db.Column(db.String(16), nullable = False)

    #relationships
    obc_id = db.Column(db.Integer, db.ForeignKey('obc.obc_id'))


class obc_event(db.Model):

    __tablename__ = 'obc_event'

    event_id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(128), nullable = False)
    description = db.Column(db.Text, nullable = False)
    date_scheduled = db.Column(db.DateTime, nullable = False)
    start_time = db.Column(db.Time, nullable = False)
    end_time = db.Column(db.Time, nullable = False)
    venue = db.Column(db.String(64), nullable = False)

    associated_image = db.Column(db.String(128))

    date_registered = db.Column(db.DateTime, default = datetime.now)
    last_updated = db.Column(db.DateTime, default = datetime.now,
            onupdate = datetime.now)



class club_schedule(db.Model):
    schedule_id = db.Column(db.Integer, primary_key = True)
    day = db.Column(db.String(32), nullable = False)
    start_time = db.Column(db.Time, nullable = False)
    end_time = db.Column(db.Time, nullable = False)
    description = db.Column(db.String(255), nullable = False)

    #relationships
    club_id = db.Column(db.Integer, db.ForeignKey('club.club_id'))


class speaker(db.Model):

    __tablename__ = 'speaker'

    speaker_id = db.Column(db.Integer, primary_key = True)
    first_name = db.Column(db.String(64), nullable = False)
    last_name = db.Column(db.String(64), nullable = False)
    gender = db.Column(db.String(32), nullable = False)
    email_address = db.Column(db.String(128), nullable = False, unique = True)
    profession = db.Column(db.String(128), nullable = False)

    date_registered = db.Column(db.DateTime, default = datetime.now)
    last_updated = db.Column(db.DateTime, default = datetime.now,
            onupdate = datetime.now)

    #relationships
    event_id = db.Column(db.Integer, db.ForeignKey('event.event_id'))



class obc(db.Model):

    __tablename__ = 'obc'

    obc_id = db.Column(db.Integer, primary_key = True)
    adm_no = db.Column(db.Integer, nullable = False, index = True)
    first_name = db.Column(db.String(64), nullable = False)
    last_name = db.Column(db.String(64), nullable = False)
    middle_name = db.Column(db.String(64))
    gender = db.Column(db.String(32), nullable = False)
    date_of_birth = db.Column(db.DateTime, nullable = False)
    email_address = db.Column(db.String(255), nullable = False, unique = True)
    phone_no = db.Column(db.String(32), nullable = False, unique = True)
    residential_address = db.Column(db.String(255), nullable = False)
    profession = db.Column(db.String(255), nullable = False)
    status = db.Column(db.String(128), nullable = False)
    associated_image = db.Column(db.String(128))
    year = db.Column(db.String(16), nullable = False)

    date_registered = db.Column(db.DateTime, default = datetime.now)
    last_updated = db.Column(db.DateTime, default = datetime.now,
            onupdate = datetime.now)

    #relationships
    house_id = db.Column(db.Integer, db.ForeignKey('house.house_id'))


class event(db.Model):

    __tablename__ = 'event'

    event_id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(128), nullable = False)
    description = db.Column(db.Text, nullable = False)
    date_scheduled = db.Column(db.DateTime, nullable = False)
    start_time = db.Column(db.Time, nullable = False)
    end_time = db.Column(db.Time, nullable = False)
    venue = db.Column(db.String(64), nullable = False)
    
    associated_image = db.Column(db.String(128))

    date_registered = db.Column(db.DateTime, default = datetime.now)
    last_updated = db.Column(db.DateTime, default = datetime.now,
            onupdate = datetime.now)

    #relationships
    club_id = db.Column(db.Integer, db.ForeignKey('club.club_id'))


class founder(db.Model):

    __tablename__ = 'founder'

    founder_id = db.Column(db.Integer, primary_key = True)
    names = db.Column(db.String(128), nullable = False)
    gender = db.Column(db.String(32), nullable = False)
    email_address = db.Column(db.String(128))

    date_registered = db.Column(db.DateTime, default = datetime.now)
    last_updated = db.Column(db.DateTime, default = datetime.now,
            onupdate = datetime.now)

    #relationships
    club_id = db.Column(db.Integer, db.ForeignKey('club.club_id'))


class achievement(db.Model):

    __tablename__ = 'achievement'

    achievement_id = db.Column(db.Integer, primary_key = True)
    description = db.Column(db.String(128), nullable = False)
    year_achieved = db.Column(db.String(32), nullable = False)

    date_registered = db.Column(db.DateTime, default = datetime.now)
    last_updated = db.Column(db.DateTime, default = datetime.now,
            onupdate = datetime.now)

    #relationships
    club_id = db.Column(db.Integer, db.ForeignKey('club.club_id'))


class club(db.Model):

    __tablename__ = 'club'

    club_id = db.Column(db.Integer, primary_key = True)
    club_name = db.Column(db.String(128), unique = True, nullable = False)
    year_founded = db.Column(db.String(32), nullable = False)
    mission = db.Column(db.Text, nullable = False)
    vision = db.Column(db.Text, nullable = False)
    venue = db.Column(db.String(64), nullable = False)
    email_address = db.Column(db.String(128), nullable = False)
    about_us = db.Column(db.Text, nullable = False)
    associated_image = db.Column(db.String(255))

    date_registered = db.Column(db.DateTime, default = datetime.now)
    last_updated = db.Column(db.DateTime, default = datetime.now, 
            onupdate = datetime.now)


class punishment(db.Model):

    __tablename__ = 'punishment'

    punishment_id = db.Column(db.Integer, primary_key = True)
    offence = db.Column(db.String(1024),nullable = False)
    punishment = db.Column(db.String(255), nullable = False)
    overseer = db.Column(db.String(255), nullable = False)
    date = db.Column(db.Date, nullable = False)
    start_time = db.Column(db.Time, nullable = False)
    end_time = db.Column(db.Time, nullable = False)

    #relationships
    admission_no = db.Column(db.Integer, db.ForeignKey('student.admission_no'))


class student(db.Model):

    __tablename__ = 'student'

    admission_no = db.Column(db.Integer, primary_key = True)
    first_name = db.Column(db.String(64), nullable = False)
    last_name = db.Column(db.String(64), nullable = False)
    middle_name = db.Column(db.String(64))

    gender = db.Column(db.String(32))
    date_of_birth = db.Column(db.DateTime)
    nationality = db.Column(db.String(64))
    email_address = db.Column(db.String(128), unique = True)
    phone_no = db.Column(db.String(32), unique = True)
    nemis = db.Column(db.String(32), unique = True)
    residence = db.Column(db.String(128))

    date_registered = db.Column(db.DateTime, default = datetime.now)
    last_updated = db.Column(db.DateTime, default = datetime.now,
            onupdate = datetime.now)

    associated_image = db.Column(db.String(255))
    status = db.Column(db.String(32), default = 'active')

    #relationship
    house_id = db.Column(db.Integer, db.ForeignKey('house.house_id'))


class house(db.Model):

    __tablename__ = 'house'

    house_id = db.Column(db.Integer, primary_key = True)
    house_title = db.Column(db.String(64), nullable = False)
    year_established = db.Column(db.String(32), nullable = False)
    opened_by = db.Column(db.String(128), nullable = False)

    sister_house = db.Column(db.String(64), nullable = False)
    motto = db.Column(db.String(128), nullable = False)
    bed_cover = db.Column(db.String(64), nullable = False)
    associated_image = db.Column(db.String(128))

    date_registered = db.Column(db.DateTime, default = datetime.now)
    last_updated = db.Column(db.DateTime, default = datetime.now,
            onupdate = datetime.now)
