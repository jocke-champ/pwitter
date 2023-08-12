from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user, login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from .forms import TweetForm, CommentForm
from .models import Tweet, User, Comment
from .login_manager import login_manager
from .database import db

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
def home():
    if current_user.is_authenticated:
        form = TweetForm()
        if form.validate_on_submit():
            tweet = Tweet(text=form.tweet.data, author=current_user)
            db.session.add(tweet)
            db.session.commit()
            flash('Your tweet is now live!')
            return redirect(url_for('home'))
        tweets = Tweet.query.order_by(Tweet.timestamp.desc()).all()
        return render_template('index.html', title='Home', form=form, tweets=tweets)
    else:
        return render_template('home.html')
    
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@views.route('/<username>', methods=['GET', 'POST'])
@login_required
def profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    tweets = Tweet.query.filter_by(user_id=user.id).order_by(Tweet.timestamp.desc()).all()

    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(text=form.comment.data, user_id=current_user.id, tweet_id=form.tweet_id.data)
        db.session.add(comment)
        db.session.commit()
        flash('Your comment has been posted!')
        return redirect(url_for('profile', username=username))

    return render_template('profile.html', user=user, tweets=tweets, form=form)


@views.route('/tweet/<tweet_id>')
@login_required
def single_tweet(tweet_id):
    return 'Page for tweet {}'.format(tweet_id)

@views.route('/tweet/<int:tweet_id>/comment', methods=['GET', 'POST'])
@login_required  # Only logged-in users can comment
def comment(tweet_id):
    form = CommentForm()
    tweet = Tweet.query.get_or_404(tweet_id)
    if form.validate_on_submit():
        comment = Comment(text=form.comment.data, author=current_user, tweet=tweet)
        db.session.add(comment)
        db.session.commit()
        flash('Your comment is now live!')
        return redirect(url_for('tweet', tweet_id=tweet_id))
    return render_template('comment.html', form=form, tweet=tweet)


@views.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user is None or not check_password_hash(user.password_hash, request.form['password']):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user)
        return redirect(url_for('index'))
    return render_template('login.html')

@views.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@views.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == 'POST':
        user = User(username=request.form['username'], 
                    password_hash=generate_password_hash(request.form['password']))
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html')
