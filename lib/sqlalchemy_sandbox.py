#!/usr/bin/env python3

from datetime import datetime

from sqlalchemy import (create_engine, desc, func,
    CheckConstraint, PrimaryKeyConstraint, UniqueConstraint,
    Index, Column, DateTime, Integer, String)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Student(Base):
    __tablename__ = 'students'

    Index('index_name', 'name')

    id = Column(Integer(), primary_key=True)
    name = Column(String())
    email = Column(String(55))
    grade = Column(Integer())
    birthday = Column(DateTime())
    enrolled_date = Column(DateTime(), default = datetime.now())

    def __repr__(self):
        return f"Student {self.id}: " \
            + f"{self.name}, " \
            + f"Grade {self.grade}"
        

if __name__ == '__main__':
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    albert_einstein = Student(
        name = "Albert Einstein",
        email = "albert.einstein@zurich.edu",
        grade = 6,
        birthday = datetime(
            year=1879,
            month=3,
            day=14
        ),
    )

    alan_turing = Student(
        name="Alan Turing",
        email="alan.turing@sherborne.edu",
        grade=11,
        birthday=datetime(
            year=1912,
            month=6,
            day=23
        ),
    )

    session.bulk_save_objects([albert_einstein, alan_turing])
    session.commit()

    # students = session.query(Student)
    # print([student for student in students])

    # this is same result as above 
    students = session.query(Student).all()
    print(students)
    # all names
    names = session.query(Student.name).all()
    print(names)

    #names in order by name
    students_by_name = session.query(
        Student.name).order_by(
        Student.name).all()
    print(students_by_name)

    #names in order by grade descending (name, grade)
    students_by_grade_desc = session.query(
        Student.name, Student.grade).order_by(
            desc(Student.grade)).all()  
    print(students_by_grade_desc)

        # find oldest student by date -> return just one
    # oldest_student = session.query(
    #     Student.name, Student.birthday).order_by(
    #         Student.birthday).limit(1).all()
    # print(oldest_student)

    # excecutes limit(1) (same as above) without list interpretation
    oldest_student = session.query(
        Student.name, Student.birthday).order_by(
            Student.birthday).first()
    print(oldest_student)

    #counts student objects
    student_count = session.query(func.count(Student.id)).first()
    print(student_count)

    # filter has a column, standard operator, and a value
    query = session.query(Student).filter(Student.name.like('%Alan%'),
        Student.grade == 11).all()
    for record in query:
        print(record.name)

        # updating data
    # for student in session.query(Student):
    #     student.grade +=1
    # session.commit()
    # print([(student.name, student.grade) for student in session.query(Student)])

    # same result as above but without creating objects beforehand
    session.query(Student).update({
        Student.grade: Student.grade +1
    })
    print([(
        student.name,
        student.grade
    ) for student in session.query(Student)])

    # deleting data (first retrieve, then delete, then try to retrieve)
    query = session.query(Student).filter(
        Student.name == "Albert Einstein")
    albert_einstein = query.first()
    session.delete(albert_einstein)
    session.commit()
    albert_einstein = query.first()
    print(albert_einstein)

    # another way to delete if you knwo the criteria
    query = session.query(
        Student).filter(Student.name == "Albert Einstein")
    query.delete()
    albert_einstein = query.first()
    print(albert_einstein)