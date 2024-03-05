import pickle
from pathlib import Path

import streamlit_authenticator as stauth

names = ["Steve Omush", "Rebecca Jackson"]
usernames = ["somush", "rjackson"]
passwords = ["XXX", "XXX"]

# Hash The Passwords
hashed_passwords = stauth.Hasher(passwords).generate()

# Put the Hashed Passwords to a Pickle File.  Save in the Current Working Directory
file_path = Path(__file__).parent / "hashed_pw.pkl"
# Open the file in binary mode and dump passwords in it
with file_path.open("wb") as file:
    pickle.dump(hashed_passwords, file)