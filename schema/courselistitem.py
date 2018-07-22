import graphene

class CourseListItem(graphene.ObjectType):
    course_id = graphene.String(default_value="no id")
    course_name = graphene.String(default_value="no name")
