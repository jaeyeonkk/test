import datetime
from sqlalchemy import JSON, Column, ForeignKey, Integer, String, Text, Boolean, TIMESTAMP, func
from sqlalchemy.ext.declarative import declarative_base
from werkzeug.security import generate_password_hash, check_password_hash
from database.database import get_db_connection
from sqlalchemy.orm import Session
import pytz

Base = declarative_base()

kst = pytz.timezone('Asia/Seoul')  # 한국 시간


# 비밀번호는 암호화되어 저장되어야 하며, 일반 텍스트로 저장되지 않아야 함.
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50))
    user_email = Column(String(100), unique=True)
    password = Column(String(200))
    _is_active = Column(Boolean, default=True)  # changed to _is_active
    _authenticated = Column(Boolean, default=False)  # changed to _authenticated

    # 원시 비밀번호를 입력받아 해당 비밀번호의 해시를 생성하고 이를 'password' 필드에 저장
    # 사용자가 계정을 만들거나 비밀번호를 변경할 때 사용됨.
    def set_password(self, password):
        hashed_password = generate_password_hash(password)
        # print(f"Generated hash: {hashed_password}")
        self.password = hashed_password

    # 함수는 주어진 원시 비밀번호의 해시를 'password' 필드에 저장된 해시와 비교
    # 사용자가 로그인하려 할 때 사용자가 제공한 비밀번호가 데이터베이스에 저장된 해시와 일치하는지 확인하기 위해 사용
    def check_password(self, password):
        return check_password_hash(self.password, password)

    # 사용자의 id를 인자로 받아 해당하는 사용자를 반환
    @staticmethod
    def get(user_id):
        db_session = get_db_connection()
        user = db_session.query(User).filter_by(id=user_id).first()
        return user

    # Flask-Login integration
    def is_authenticated(self):  # added parentheses
        return self._authenticated  # changed to _authenticated

    def is_active(self):  # added parentheses
        return self._is_active  # changed to _is_active

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)  # Python 3에서는 문자열로 변환해야 합니다.


class QList(Base):
    __tablename__ = "q_list"

    q_level = Column(String, nullable=False)
    q_id = Column(Integer, primary_key=True, nullable=False)
    q_name = Column(String, nullable=False)
    q_content = Column(Text, nullable=False)
    ex_print = Column(Text, nullable=False)
    c_answer_code = Column(Text, nullable=False)
    cpp_answer_code = Column(Text, nullable=False)
    p_answer_code = Column(Text, nullable=False)
    j_answer_code = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)


class TypingGame(Base):
    __tablename__ = "typinggame"

    tq_id = Column(Integer, primary_key=True)
    code = Column(Text, nullable=True)
    language = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)


class DragGame(Base):
    __tablename__ = "draggame"

    dq_id = Column(Integer, primary_key=True)
    language = Column(String(255), nullable=False)
    text = Column(Text, nullable=True)
    code = Column(Text, nullable=True)
    answers = Column(JSON, nullable=True)
    options = Column(JSON, nullable=True)


class OutputGame(Base):
    __tablename__ = "outputgame"

    oq_id = Column(Integer, primary_key=True)
    language = Column(String(255), nullable=False)
    question = Column(Text, nullable=True)
    answer = Column(Text, nullable=True)

class Board(Base):
    __tablename__ = "board"

    board_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=True)
    file_path = Column(String(255), nullable=True)
    view = Column(Integer, nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.datetime.now(kst))
        
class Game_Score(Base):
    __tablename__ = "game_score"

    id = Column(Integer, primary_key=True)
    game_user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    output_score = Column(Integer, nullable=False)
    output_game_language = Column(String(255), nullable=True)
    output_created_at = Column(TIMESTAMP, default=datetime.datetime.now(kst))