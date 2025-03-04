# AI Flashcards App
## Tech Stack
- Backend: Python (Flask), SQLAlchemy (SQLite)
- Frontend: Javascript (React), Material UI
- AI Integration: Google Gemini API
  
## Authentication Requirements
- [x] Sign up using email, name, and password
- [x] Login using email and password
- [ ] Login using either email or name and password
- [ ] Implement security best practices: input validation, password (at least 8 characters, does not include username)
- [ ] Sign up using Google
- [ ] Sign in using Google

## CRUD Operations Requirement
- [x] Create, Read, Update and Delete Folders
- [x] Create, Read, Update and Delete Cards
- [ ] AI-generated flashcards from users' input including prompt (text) and PDFs
- [ ] Attach media (including URLs, and text materials) to the card
- [ ] Check progress for reviewing each card (each concept should be reviewed 4 times - forgetting curve)
- [ ] Check progress for each folder (the proportion of cards fully reviewed)

## Nice-to-have Features
- [ ] Monthly exams generated from the user's card database
- [ ] Collaborate with friends to create cards

## Run Locally (on Mac)
### Clone Github Repo
```shell
git clone https://github.com/thuinanutshell/ai-flashcards-app
```
### Backend
```shell
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
export PYTHONPATH={project-absolute-path}
python3 run.py
```
### Frontend
```shell
cd frontend
npm install
npm start
```
