import graphene
from .section import Section

class Course(graphene.ObjectType):
    course_id = graphene.String()
    name_en = graphene.String()
    name_th = graphene.String()
    midterm_exam_date = graphene.String()
    final_exam_date = graphene.String()
    sections = graphene.List(Section)
