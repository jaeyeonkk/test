from sqlalchemy import JSON, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from werkzeug.security import generate_password_hash, check_password_hash

Base = declarative_base()


# 비밀번호는 암호화되어 저장되어야 하며, 일반 텍스트로 저장되지 않아야 함.
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50))
    user_email = Column(String(100), unique=True)
    password = Column(String(200))

    # 원시 비밀번호를 입력받아 해당 비밀번호의 해시를 생성하고 이를 'password' 필드에 저장
    # 사용자가 계정을 만들거나 비밀번호를 변경할 때 사용됨.
    def set_password(self, password):
        hashed_password = generate_password_hash(password)
        #print(f"Generated hash: {hashed_password}")
        self.password = hashed_password

    # 함수는 주어진 원시 비밀번호의 해시를 'password' 필드에 저장된 해시와 비교
    # 사용자가 로그인하려 할 때 사용자가 제공한 비밀번호가 데이터베이스에 저장된 해시와 일치하는지 확인하기 위해 사용
    def check_password(self, password):
        return check_password_hash(self.password, password)


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
    answer = Column(Text, nullable=False)


class TypingGame(Base):
    __tablename__ = "typinggame"

    id = Column(Integer, primary_key=True)
    code = Column(Text, nullable=True)
    language = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)


class DragGame(Base):
    __tablename__ = "draggame"

    id = Column(Integer, primary_key=True)
    language = Column(String(255), nullable=False)
    text = Column(Text, nullable=True)
    code = Column(Text, nullable=True)
    answers = Column(JSON, nullable=True)
    options = Column(JSON, nullable=True)


class OutputGame(Base):
    __tablename__ = "outputgame"

    id = Column(Integer, primary_key=True)
    language = Column(String(255), nullable=False)
    question = Column(Text, nullable=True)
    answer = Column(Text, nullable=True)
