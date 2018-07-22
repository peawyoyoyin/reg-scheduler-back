import graphene
from bs4 import BeautifulSoup

from .course import Course
from .section import Section
from .courselistitem import CourseListItem

from .scraper.courseinfo import CourseInfo
from .scraper.courselist import CourseList
from .fetcher.fetcher import Fetcher 

fetcher = Fetcher()

class Query(graphene.ObjectType):
    courses = graphene.List(CourseListItem, \
        semester=graphene.Int(required=True), year=graphene.Int(required=True), course_number=graphene.Int())
    course = graphene.Field(Course, \
        semester=graphene.Int(required=True), year=graphene.Int(required=True), course_number=graphene.Int(required=True))

    def resolve_courses(self, info, semester, year, course_number=''):
        raw = fetcher.get_course_list(semester, year, course_number)
        courses_list = CourseList(BeautifulSoup(raw, 'lxml'))
        result = []
        for course in courses_list.courses:
            result.append(CourseListItem(course_id=course.course_id, course_name=course.course_name))
        return result
    
    def resolve_course(self, info, semester, year, course_number):
        raw = fetcher.get_course_info(semester, year, course_number)
        course_info = CourseInfo(BeautifulSoup(raw, 'lxml'))
        sections = []
        for section in course_info.sections:
            s = Section(
                number = section.section_number,
                days = section.days,
                time = section.time,
                building = section.building,
                room = section.room,
                teacher = section.teacher,
                note = section.notes,
                capacity = section.capacity
            )
            sections.append(s)
        
        course_obj = Course(
            course_id = course_info.course_id,
            name_en = course_info.course_name_en,
            name_th = course_info.course_name_th,
            midterm_exam_date = course_info.midterm_exam_date,
            final_exam_date = course_info.final_exam_date,
            sections = sections
        )
        return course_obj

schema = graphene.Schema(query=Query)
