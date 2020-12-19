import calendar
import uuid
from datetime import datetime
from sqlalchemy import create_engine, func, desc
from sqlalchemy.orm import sessionmaker
from config import Config

from models import *


def create_token(session, user_id, class_code, exp, num_classes):
    """Create new token"""
    now = datetime.now()
    expiration = datetime.fromtimestamp(int(datetime.timestamp(now)) + exp*60)
    new_token = Presences(
        user_id,
        class_code,
        str(uuid.uuid4()),
        datetime.timestamp(now) + exp*60,
        False,
        int(num_classes),
        datetime.timestamp(now),
        .0
    )
    session.add(new_token)
    session.commit()
    return new_token.token


def get_professor_token(s, prof_id, POST_DATETIME, POST_TIMESTAMP):
    weekday = calendar.day_name[POST_DATETIME.weekday()]
    search = "%{}%".format(weekday)
    POST_TIME = str(POST_DATETIME.time())

    """Query for classes on that day"""
    classes = s.query(
        Classes.name, Classes.code,
        func.count(Classes.time_end).label("qtd"),
        func.min(Classes.time_start).label("start"),
        func.max(Classes.time_end).label("end")
    ).join(
        ProfessorClass, ProfessorClass.class_code == Classes.id
    ).filter(
        and_(
            ProfessorClass.professor_id == prof_id,
            Classes.date.like(search),
            Classes.time_start < POST_TIME,
            Classes.time_end > POST_TIME
        )
    ).group_by(
        Classes.code
    ).order_by(
        Classes.time_start
    ).first()

    if classes:
        """
        If professor have a class on that day,
        check if there's a valid token for that class
        """
        TODAY = POST_DATETIME.date()
        TODAY_TIMESTAMP_START = datetime.strptime(
            f'{TODAY} 00:00:00', '%Y-%m-%d %H:%M:%S').timestamp()
        TODAY_TIMESTAMP_END = datetime.strptime(
            f'{TODAY} 23:59:59', '%Y-%m-%d %H:%M:%S').timestamp()

        query = s.query(
            Presences.token,
            Presences.token_expire,
            Presences.presence
        ).filter(
            and_(
                Presences.user_id == prof_id,
                Presences.class_code == classes.code,
                Presences.date > TODAY_TIMESTAMP_START,
                Presences.date < TODAY_TIMESTAMP_END
            )
        ).order_by(
            desc(Presences.date)
        ).first()

        if query and not query.presence and query.token_expire > POST_TIMESTAMP:
            """If there's an avaible token, valid and not used"""
            return {
                "success": 1,
                "resp": f"{query.token}, 1"
            }

        elif query and query.presence:
            """Token already used"""
            # TODO - return a code
            return {
                "success": 0,
                "resp": f"Aula de {classes.name} já confirmada/iniciada"
            }

        else:
            """If there isn't an avaible token, create one"""
            token = create_token(s, prof_id, classes.code, 2, classes.qtd)
            return {
                "success": 1,
                "resp": f"{token}, 1"
            }

    return {
        "success": 0,
        "resp": "Bad, bad request"
    }


def get_student_token(s, student_id, POST_DATETIME, POST_TIMESTAMP):
    weekday = calendar.day_name[POST_DATETIME.weekday()]
    search = "%{}%".format(weekday)
    POST_TIME = str(POST_DATETIME.time())

    """Query for classes on that day"""
    classes = s.query(
        Classes.name, Classes.code,
        func.count(Classes.time_end).label("qtd"),
        func.min(Classes.time_start).label("start"),
        func.max(Classes.time_end).label("end")
    ).join(
        StudentClass, StudentClass.class_code == Classes.id
    ).filter(
        and_(
            StudentClass.student_id == student_id,
            Classes.date.like(search),
            # Classes.time_start < POST_TIME,
            Classes.time_end > POST_TIME
        )
    ).group_by(
        Classes.code
    ).order_by(
        Classes.time_start
    ).first()

    if classes:
        """
        If student have a class on that day,
        check if there's a valid token for that class
        """
        TODAY = POST_DATETIME.date()
        TODAY_TIMESTAMP = datetime.strptime(
            f'{TODAY} 23:59:59', '%Y-%m-%d %H:%M:%S')
        query = s.query(
            Presences.token,
            Presences.token_expire,
            Presences.presence
        ).filter(
            and_(
                Presences.user_id == student_id,
                Presences.class_code == classes.code,
                Presences.token_expire > POST_TIMESTAMP,
                Presences.token_expire < TODAY_TIMESTAMP
            )
        ).order_by(
            desc(Presences.date)
        ).first()

        if query and not query.presence and query.token_expire > POST_TIMESTAMP:
            """If there's an avaible token, valid and not used"""
            return {
                "success": 1,
                "resp": f"{query.token}, 2"
            }

        elif query and query.presence:
            """Token already used"""
            # TODO - return a code
            return {
                "success": 0,
                "resp": f"{classes.name}, presença confirmada"
            }

        else:
            """If there isn't an avaible token"""
            return {
                "success": 0,
                "resp": "Nenhuma aula em andamento no momento"
            }


def read_token(data={}):

    try:
        FORM = data['token']
        TOKEN, USER_TYPE = FORM.split(", ")
        POST_DATETIME = datetime.now()
        POST_TIMESTAMP = datetime.timestamp(POST_DATETIME)

        engine = create_engine(Config.SQLALCHEMY_DATABASE_URI, echo=True)
        Session = sessionmaker(bind=engine)
        session = Session()

        TODAY = POST_DATETIME.date()
        TODAY_TIMESTAMP = datetime.strptime(
            f'{TODAY} 23:59:59', '%Y-%m-%d %H:%M:%S').timestamp()

        query = session.query(
            Presences.class_code,
            Presences.presence,
            Presences.num_classes.label("qtd"),
            Presences.confirmation_date,
            Presences.token
        ).filter(
            and_(
                Presences.token == TOKEN,
                Presences.presence == False,
                Presences.token_expire > POST_TIMESTAMP,
                Presences.token_expire < TODAY_TIMESTAMP
            )
        ).first()

        if query:
            """Update Presences"""
            session.query(
                Presences.presence,
                Presences.confirmation_date
            ).filter(
                Presences.token == TOKEN
            ).update(
                {
                    Presences.presence: True,
                    Presences.confirmation_date: POST_TIMESTAMP
                }, synchronize_session=False
            )
            session.commit()

            if USER_TYPE == "1":
                """Crate a token for each student in that class"""
                classes = session.query(
                    Classes.id, Classes.code
                ).filter(
                    and_(
                        Classes.code == query.class_code
                    )
                ).first()

                students = session.query(
                    StudentClass.student_id.label("id"),
                    StudentClass.class_code.label("code")
                ).filter(
                    and_(
                        StudentClass.class_code == classes.id
                    )
                ).all()

                for student in students:
                    create_token(session, student.id,
                                 classes.code, 40, query.qtd)

                return {"resp": f"Aula confirmada e código gerado para os alunos matriculados na matéria {query.class_code}"}
            return {"resp": f"{query.class_code} - Presença confirmada"}

    except Exception as e:
        return {"resp": f"Bad, bad request: {e}"}
    # TODO - Positive return


def authentication(data={}):

    POST_USERNAME = data['username']
    POST_PASSWORD = data['password']
    POST_DATETIME = datetime.now()
    POST_TIMESTAMP = datetime.timestamp(POST_DATETIME)

    engine = create_engine(Config.SQLALCHEMY_DATABASE_URI, echo=True)
    Session = sessionmaker(bind=engine)
    session = Session()

    """Query for user"""
    query = session.query(User).filter(User.username.in_(
        [POST_USERNAME]), User.password.in_([POST_PASSWORD]))
    user = query.first()

    if user and user.user_type == 1:  # If there's user and it is a professor
        res = get_professor_token(
            session, user.id, POST_DATETIME, POST_TIMESTAMP
        )
        return res

    elif user and user.user_type == 2:  # If there's user and it is a student
        res = get_student_token(
            session, user.id, POST_DATETIME, POST_TIMESTAMP
        )
        return res

    return None
