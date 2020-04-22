from apluslms_shepherd.auth.models import User

user1 = User(id='1',
            email="test1@aalto.fi",
            display_name="Teacher",
            sorting_name="Smith",
            full_name="TEACHER SMITH",
            roles="Teacher")

user2 = User(id='2',
            email="test2@aalto.fi",
            display_name="Instructor",
            sorting_name="Johnson",
            full_name="INSTRUCTOR JOHNSON",
            roles="Instructor")

user3 = User(id='3',
            email="test3@aalto.fi",
            display_name="TA",
            sorting_name="Davis",
            full_name="TA DAVIS",
            roles="TA")