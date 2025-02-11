from flask import Flask, render_template, url_for, flash, redirect, request
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_user, current_user, logout_user, login_required, UserMixin
from config import Config
from models import db, User, Lesson, Quiz, LessonCompletion
from forms import RegistrationForm, LoginForm

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

# Define user_loader function
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Initialize the database and create sample data
with app.app_context():
    db.create_all()

    # Check if there are existing lessons and quizzes
    if Lesson.query.count() < 30:
        lessons_data = [
            {"title": "Lesson 1: Hangul", "content": "Hangul is the alphabet of the Korean language, consisting of 24 letters (14 consonants and 10 vowels). It was created by King Sejong the Great and his scholars in the 15th century to promote literacy among the Korean people."},
            {"title": "Lesson 2: Basic Phrases", "content": "In this lesson, you'll learn essential phrases for greetings, introductions, and expressing gratitude in Korean. Mastering these phrases will help you communicate effectively in everyday situations."},
            {"title": "Lesson 3: Numbers", "content": "Learn how to count from 1 to 100 in Korean. Numbers are essential for telling time, ordering food, and many other everyday activities. Korean numbers have both native Korean and Sino-Korean (Chinese origin) systems."},
            {"title": "Lesson 4: Greetings", "content": "Greetings are crucial in Korean culture. You'll learn how to greet people depending on the time of day and the formality level. Understanding proper greetings shows respect and enhances interpersonal relationships."},
            {"title": "Lesson 5: Days of the Week", "content": "Know the names of the days of the week in Korean and how they are used in sentences. This knowledge helps in scheduling appointments, planning events, and discussing weekly routines."},
            {"title": "Lesson 6: Colors", "content": "Colors are essential for describing objects and expressing preferences. Learn common colors in Korean and how to use them in sentences. Mastering colors enhances your ability to describe the world around you."},
            {"title": "Lesson 7: Food", "content": "Explore Korean cuisine by learning the names of popular dishes and ingredients. Food is an integral part of Korean culture, and knowing food-related vocabulary helps in ordering at restaurants and understanding menus."},
            {"title": "Lesson 8: Family", "content": "Families play a central role in Korean society. Learn the names of family members and how to address them respectfully. Understanding family vocabulary improves your ability to discuss relationships and social dynamics."},
            {"title": "Lesson 9: Occupations", "content": "Discover various occupations and professions in Korean. Knowing occupational terms is useful for career discussions, understanding job advertisements, and learning about different industries."},
            {"title": "Lesson 10: Weather", "content": "Learn how to talk about the weather in Korean, including vocabulary for different weather conditions and climate patterns. Weather-related conversations are common in daily life and help in planning activities."},
            {"title": "Lesson 11: Time", "content": "Master telling time in Korean, including hours, minutes, and different time expressions. Time-related vocabulary is crucial for scheduling appointments, catching transportation, and planning daily activities."},
            {"title": "Lesson 12: Directions", "content": "Navigate Korean cities by learning how to ask for and give directions. Understanding directional vocabulary and phrases is essential for finding locations, using public transportation, and exploring new places."},
            {"title": "Lesson 13: Transportation", "content": "Explore transportation options in Korean, including vocabulary for vehicles, public transportation, and travel-related phrases. Knowing transportation terms is useful for commuting and traveling."},
            {"title": "Lesson 14: Shopping", "content": "Learn phrases and vocabulary for shopping in Korean, including how to ask for prices, make purchases, and describe items. Shopping is a common activity where language skills are highly beneficial."},
            {"title": "Lesson 15: Health", "content": "Understand health-related vocabulary in Korean, including terms for common illnesses, symptoms, and medical professionals. Knowing health-related terms is essential for seeking medical assistance and discussing wellness."},
            {"title": "Lesson 16: Emotions", "content": "Express emotions and feelings in Korean by learning emotional vocabulary and phrases. Understanding how to communicate emotions enhances interpersonal relationships and self-expression."},
            {"title": "Lesson 17: Sports", "content": "Explore sports-related vocabulary in Korean, including names of sports, equipment, and terms used in sports activities. Sports are popular in Korean culture, and knowing sports vocabulary is useful for discussing games and activities."},
            {"title": "Lesson 18: Technology", "content": "Discover technology-related vocabulary in Korean, including terms for devices, software, and digital communication. Technology plays a significant role in modern society, and understanding tech terms is essential for daily life."},
            {"title": "Lesson 19: Animals", "content": "Learn the names of common animals in Korean and how to describe them. Animals are part of everyday life and culture, and knowing animal vocabulary enhances your ability to discuss pets, wildlife, and conservation."},
            {"title": "Lesson 20: Travel", "content": "Prepare for travel by learning travel-related phrases and vocabulary in Korean. Knowing travel terms helps in navigating airports, booking accommodations, and communicating with locals."},
            {"title": "Lesson 21: Nature", "content": "Explore vocabulary related to nature in Korean, including terms for landscapes, plants, and natural phenomena. Understanding nature vocabulary enhances appreciation for the environment and outdoor activities."},
            {"title": "Lesson 22: Culture", "content": "Understand aspects of Korean culture, including traditions, customs, and cultural practices. Learning about culture promotes cultural awareness and facilitates deeper connections with Korean society."},
            {"title": "Lesson 23: Festivals", "content": "Learn about Korean festivals and celebrations, including traditional and modern festivals. Festivals are important cultural events that showcase Korean heritage and provide opportunities for community engagement."},
            {"title": "Lesson 24: Music", "content": "Discover Korean music genres, artists, and musical instruments. Music is a significant aspect of Korean culture, and knowing music-related terms enhances enjoyment and understanding of Korean music."},
            {"title": "Lesson 25: History", "content": "Explore key events and historical figures in Korean history. Understanding Korean history provides insights into the nation's development, culture, and societal changes over time."},
            {"title": "Lesson 26: Art", "content": "Learn about Korean art forms, artists, and artistic movements. Art reflects cultural expression and creativity, and knowing art-related terms deepens appreciation for Korean artistic traditions."},
            {"title": "Lesson 27: Cuisine", "content": "Discover traditional Korean cuisine, including popular dishes, cooking methods, and culinary traditions. Korean food is renowned for its flavors and diversity, making culinary knowledge essential for food enthusiasts."},
            {"title": "Lesson 28: Fashion", "content": "Explore Korean fashion trends, designers, and clothing styles. Fashion plays a significant role in Korean culture, and understanding fashion-related terms enhances awareness of trends and personal style."},
            {"title": "Lesson 29: Business", "content": "Understand Korean business culture, practices, and industry terms. Business knowledge is valuable for professionals interested in Korean markets, commerce, and economic activities."},
            {"title": "Lesson 30: Media", "content": "Explore Korean media and entertainment, including television, movies, and digital platforms. Media plays a crucial role in shaping cultural narratives and understanding contemporary Korean society."},
        ]
        quizzes_data = [
            {"lesson_id": 1, "question": "What is the Korean alphabet called?", "answer": "Hangul"},
            {"lesson_id": 2, "question": "How do you say 'Hello' in Korean?", "answer": "안녕하세요"},
            {"lesson_id": 3, "question": "What is the Korean word for 'one'?", "answer": "하나"},
            {"lesson_id": 4, "question": "How do you say 'Goodbye' in Korean?", "answer": "안녕히 가세요"},
            {"lesson_id": 5, "question": "What is the Korean word for 'Monday'?", "answer": "월요일"},
            {"lesson_id": 6, "question": "How do you say 'Red' in Korean?", "answer": "빨간색"},
            {"lesson_id": 7, "question": "What is the Korean word for 'rice'?", "answer": "밥"},
            {"lesson_id": 8, "question": "How do you say 'mother' in Korean?", "answer": "어머니"},
            {"lesson_id": 9, "question": "What is the Korean word for 'teacher'?", "answer": "선생님"},
            {"lesson_id": 10, "question": "How do you say 'It's sunny' in Korean?", "answer": "날씨가 맑다"},
            {"lesson_id": 11, "question": "What is the Korean word for 'hour'?", "answer": "시간"},
            {"lesson_id": 12, "question": "How do you say 'left' in Korean?", "answer": "왼쪽"},
            {"lesson_id": 13, "question": "What is the Korean word for 'bus'?", "answer": "버스"},
            {"lesson_id": 14, "question": "How do you say 'How much is it?' in Korean?", "answer": "얼마에요?"},
            {"lesson_id": 15, "question": "What is the Korean word for 'hospital'?", "answer": "병원"},
            {"lesson_id": 16, "question": "How do you say 'happy' in Korean?", "answer": "행복한"},
            {"lesson_id": 17, "question": "What is the Korean word for 'soccer'?", "answer": "축구"},
            {"lesson_id": 18, "question": "How do you say 'computer' in Korean?", "answer": "컴퓨터"},
            {"lesson_id": 19, "question": "What is the Korean word for 'cat'?", "answer": "고양이"},
            {"lesson_id": 20, "question": "How do you say 'train station' in Korean?", "answer": "기차역"},
            {"lesson_id": 21, "question": "What is the Korean word for 'mountain'?", "answer": "산"},
            {"lesson_id": 22, "question": "How do you say 'tradition' in Korean?", "answer": "전통"},
            {"lesson_id": 23, "question": "What is the Korean word for 'holiday'?", "answer": "휴일"},
            {"lesson_id": 24, "question": "How do you say 'music' in Korean?", "answer": "음악"},
            {"lesson_id": 25, "question": "What is the Korean word for 'king'?", "answer": "왕"},
            {"lesson_id": 26, "question": "How do you say 'painting' in Korean?", "answer": "그림"},
            {"lesson_id": 27, "question": "What is the Korean word for 'kimchi'?", "answer": "김치"},
            {"lesson_id": 28, "question": "How do you say 'fashion' in Korean?", "answer": "패션"},
            {"lesson_id": 29, "question": "What is the Korean word for 'business'?", "answer": "사업"},
            {"lesson_id": 30, "question": "How do you say 'newspaper' in Korean?", "answer": "신문"},
        ]

        # Populate lessons and quizzes if none exist
        for lesson_info in lessons_data:
            lesson = Lesson.query.filter_by(title=lesson_info['title']).first()
            if not lesson:
                lesson = Lesson(title=lesson_info['title'], content=lesson_info['content'])
                db.session.add(lesson)
        
        for quiz_info in quizzes_data:
            quiz = Quiz.query.filter_by(lesson_id=quiz_info['lesson_id']).first()
            if not quiz:
                quiz = Quiz(lesson_id=quiz_info['lesson_id'], question=quiz_info['question'], answer=quiz_info['answer'])
                db.session.add(quiz)
        
        db.session.commit()

@app.route('/')
def index():
    lessons = Lesson.query.all()
    return render_template('index.html', lessons=lessons)

@app.route('/lesson/<int:lesson_id>')
@login_required
def lesson(lesson_id):
    lesson = Lesson.query.get_or_404(lesson_id)
    return render_template('lesson.html', lesson=lesson)

@app.route('/quiz/<int:lesson_id>', methods=['GET', 'POST'])
@login_required
def quiz(lesson_id):
    quiz = Quiz.query.filter_by(lesson_id=lesson_id).first()
    if request.method == 'POST':
        user_answer = request.form['answer']
        correct = user_answer.strip().lower() == quiz.answer.lower()
        if correct:
            completion = LessonCompletion(user_id=current_user.id, lesson_id=lesson_id)
            db.session.add(completion)
            db.session.commit()
        return render_template('quiz.html', quiz=quiz, correct=correct, answered=True)
    return render_template('quiz.html', quiz=quiz)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You can now log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/profile')
@login_required
def profile():
    completions = LessonCompletion.query.filter_by(user_id=current_user.id).all()
    completed_lessons = [Lesson.query.get(completion.lesson_id) for completion in completions]
    return render_template('profile.html', completed_lessons=completed_lessons)

if __name__ == '__main__':
    app.run(debug=True)
