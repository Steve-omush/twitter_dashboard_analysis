from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from passlib.hash import bcrypt

# Create engine
DATABASE_URL = "postgresql://voste:steve@localhost/users"
engine = create_engine(DATABASE_URL)

# Create base class
Base = declarative_base()

# Define User model
class User(Base):
    __tablename__ = 'users'
    __table_args__ = {'schema': 'new_schema'}
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

# Create tables
Base.metadata.create_all(engine)

# Create session
Session = sessionmaker(bind=engine)

# Streamlit app code
import streamlit as st

st.title('User Authentication')

option = st.sidebar.selectbox('Menu', ['Sign Up', 'Login'])

if option == 'Sign Up':
    st.title('Sign Up')
    username = st.text_input('Username')
    email = st.text_input('Email')
    password = st.text_input('Password', type='password')
    if st.button('Sign Up'):
        if not username:
            st.error('Please enter your username')
        elif not email:
            st.error('Please enter your email')
        elif not password:
            st.error('Please enter your password')
        else:
            session = Session()
            hashed_password = bcrypt.hash(password)
            new_user = User(username=username, email=email, password=hashed_password)
            session.add(new_user)
            session.commit()
            session.close()
            st.success('Sign up successful!')

elif option == 'Login':
    st.title('Log In')
    username = st.text_input('Username')
    password = st.text_input('Password', type='password')
    if st.button('Login'):
        session = Session()
        user = session.query(User).filter_by(username=username).first()
        if user and bcrypt.verify(password, user.password):
            st.success('Logged in successfully!')
        else:
            st.error('Invalid username or password')
        session.close()



# Real ONE
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from passlib.hash import bcrypt
import streamlit as st

# Create engine
DATABASE_URL = "postgresql://voste:steve@localhost/users"
engine = create_engine(DATABASE_URL)

# Create base class
Base = declarative_base()

# Define User model
class User(Base):
    __tablename__ = 'users'
    __table_args__ = {'schema': 'new_schema'}
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

# Create tables
Base.metadata.create_all(engine)

# Create session
Session = sessionmaker(bind=engine)

def sign_up(username, email, password):
    session = Session()
    hashed_password = bcrypt.hash(password)
    new_user = User(username=username, email=email, password=hashed_password)
    session.add(new_user)
    session.commit()
    session.close()

def login(username, password):
    session = Session()
    user = session.query(User).filter_by(username=username).first()
    session.close()
    if user and bcrypt.verify(password, user.password):
        return user
    return None

def main():
    st.title('User Authentication')

    logged_in = st.session_state.get('logged_in', False)
    username = st.session_state.get('username', '')

    option = st.sidebar.selectbox('Menu', ['Sign Up', 'Login'])

    if option == 'Sign Up':
        st.title('Sign Up')
        username = st.text_input('Username')
        email = st.text_input('Email')
        password = st.text_input('Password', type='password')
        if st.button('Sign Up'):
            if not username:
                st.error('Please enter your username')
            elif not email:
                st.error('Please enter your email')
            elif not password:
                st.error('Please enter your password')
            else:
                sign_up(username, email, password)
                st.success('Sign up successful!')

    elif option == 'Login':
        st.title('Log In')
        username = st.text_input('Username')
        password = st.text_input('Password', type='password')
        if st.button('Login'):
            user = login(username, password)
            if user:
                st.session_state['logged_in'] = True
                st.session_state['username'] = username
                st.success('Logged in successfully!')
                st.experimental_rerun()

    if logged_in:
        st.title(f"Welcome {username}")
        st.write("This is the user page. You can customize this page further.")

if __name__ == '__main__':
    main()
