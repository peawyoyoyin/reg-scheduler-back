import graphene

class Section(graphene.ObjectType):
    number = graphene.Int()
    days = graphene.List(graphene.String)
    time = graphene.String()
    building = graphene.String()
    room = graphene.String()
    teacher = graphene.String()
    note = graphene.String()
    capacity = graphene.Int()
