from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import datetime
import smtplib
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session, relationship
from sqlalchemy import create_engine, select, insert, update, delete, TIMESTAMP, desc, ForeignKey
from dataclasses import dataclass
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField, TextAreaField
from wtforms.validators import DataRequired, Email, Length
from werkzeug import security
from flask_login import LoginManager, login_user, login_required, UserMixin, current_user, logout_user
from dataclasses import dataclass
from functools import wraps
from flask_ckeditor import CKEditor
import os
from dotenv import load_dotenv

load_dotenv(".env")

login_manager = LoginManager()

engine = create_engine("sqlite:///blog.db", echo=True)

class Base(DeclarativeBase):
    type_annotation_map = {
        datetime: TIMESTAMP(timezone=True)
    }

@dataclass
class Users(Base, UserMixin):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key= True)
    email: Mapped[str] = mapped_column(unique= True)
    password: Mapped[str]
    children_posts = relationship("Posts", back_populates= "user")
    children_comments = relationship("Comments", back_populates="user")

@dataclass
class Posts(Base):
    __tablename__ = "posts"
    id: Mapped[int] = mapped_column(primary_key = True)
    title: Mapped[str]
    author: Mapped[str]
    text: Mapped[str]
    date: Mapped[datetime]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user = relationship("Users", back_populates="children_posts")
    comment = relationship("Comments", back_populates="post")

@dataclass
class Comments(Base):
    __tablename__ = "comments"
    id: Mapped[int] = mapped_column(primary_key=True)
    comment: Mapped[str]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id"))
    user = relationship("Users", back_populates="children_comments")
    post = relationship("Posts", back_populates="comment")

def admin_only(func):
    @wraps(func)
    def wrapper(**kwargs):
        post_id = kwargs.get("num")
        with Session(engine) as session:
            post = session.execute(select(Posts).where(Posts.id == post_id)).scalars().first()
        if current_user.id == 1 or current_user.id == post.user_id:
            return func(**kwargs)
        flash("You cannot access this page")
        return redirect(url_for('home'))
    return wrapper

# Base.metadata.create_all(engine)

e_mail = "danihart060@gmail.com"
password = os.getenv("PASSWORD")


app = Flask(__name__)
login_manager.init_app(app)
ckeditor = CKEditor(app)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config["CKEDITOR_SERVE_LOCAL"] = True

@login_manager.user_loader
def load_user(user_id):
    with Session(engine) as session:
        return session.execute(select(Users).where(Users.id == user_id)).scalars().first()


def get_blogposts():
    x = select(Posts).order_by(desc(Posts.date))
    with engine.connect() as conn:
        posts_db = conn.execute(x).all()
    blogposts = [{"title": each_post.title, "author": each_post.author, "month": each_post.date.date().strftime("%B"), "day": each_post.date.date().day, "year": each_post.date.date().year, "text": each_post.text, "id": each_post.id, "user_id": each_post.user_id} for each_post in posts_db]
    return blogposts

@app.route("/")
def home():
    try:
        return render_template("index.html", posts=get_blogposts(), user=current_user)
    except AttributeError:
        return render_template("index.html", posts=get_blogposts(), user=None)

@app.route("/about")
def get_about():
    return render_template("about.html")

@app.route("/contact", methods=["GET", "POST"])
def get_contact():
    if request.method == "GET":
        return render_template("contact.html", header_one="Contact Me")
    else:
        name = request.form["name"]
        email = request.form["email"]
        phone = request.form["phone"]
        msg = request.form["msg"]
        with smtplib.SMTP_SSL("smtp.gmail.com") as connection:
            connection.login(user=e_mail, password=password)
            connection.sendmail(from_addr=e_mail, to_addrs="ogunsanu17@gmail.com", msg=f"Subject:Contact ME\n\nName: {name}\nEmail: {email}\nPhone: {phone}\nMessage: {msg}") 
        return render_template("contact.html", header_one="Successfully sent message")

@app.route("/post/<num>", methods=["GET", "POST"])
def post(num):
    data = ''
    if request.method == "POST":
        data = request.form.get("ckeditor")
        with Session(engine) as session:
            session.execute(
                insert(Comments),
                [
                    {"user_id": current_user.id, "post_id": num, "comment": data}
                ]
            )
            session.commit()
    try:
        for post in get_blogposts():
            if post["id"] == int(num):
                blogpost = post
        texts = blogpost["text"].split("\n")
        with engine.connect() as conn:
            comments = conn.execute(select(Comments).order_by(desc(Comments.id))).all()
            print(comments)
        return render_template("post.html", post=blogpost, texts=texts, route_no=num, user=current_user, data=comments)
    except UnboundLocalError:
        return "Endpoint does not exist"

@app.route("/new-post", methods=["GET", "POST"])
@login_required
def new_post():
    if request.method == "POST":
        with Session(engine) as session:
            session.execute(
                insert(Posts),
                [
                    {"title": request.form.get("name"), "author": current_user.email, "text": request.form.get("message"),
                    "user_id": current_user.id, "date": datetime.now()}
                ]
            )
            session.commit()
        return redirect(url_for('home'))
    return render_template("new-post.html")

@app.route("/post/<num>/edit-post", methods=["GET", "POST"])
@login_required
@admin_only
def edit_post(num):
    if request.method == "GET":
        with Session(engine) as session:
            result = session.execute(select(Posts).where(Posts.id == num))
            post = result.scalars().first()
        return render_template("edit-post.html", post=post, num=num)
    title = request.form.get("name")
    msg = request.form.get("message")
    with Session(engine) as session:
        session.execute(
            update(Posts),
            [
                {"id": num, "title": title, "author": current_user.email, "text": msg, "date": datetime.now()}
            ]
        )
        session.commit()
    return redirect(url_for('home'))

@app.route("/post/<num>/delete", methods=["GET", "POST"])
@login_required
@admin_only
def delete_post(num):
    with Session(engine) as session:
        session.execute(
            delete(Posts).where(Posts.id == num)
        )
        session.commit()
    return redirect(url_for('home'))


@app.route("/register", methods=["GET", "POST"])
def register():
    logout_user()
    if request.method == "POST":
        pword = security.generate_password_hash(password=request.form.get("password"), method="scrypt", salt_length=8)
        with Session(engine) as session:
            user = session.execute(select(Users).where(Users.email == request.form.get("email"))).scalars().first()
            if user:
                flash("Email already exists. Please login")
                return redirect(url_for('home'))
            session.execute(
                insert(Users),
                [
                    {"email": request.form.get("email"), "password": pword}
                ]
            )
            session.commit()
            user = session.execute(select(Users).where(Users.email == request.form.get("email"))).scalars().first()
        login_user(user)
        flash("Logged in successfully")
        return redirect(url_for("home"))
    return render_template("register.html", user=current_user)

@app.route("/login", methods=["GET", "POST"])
def login():
    logout_user()
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        with Session(engine) as session:
            user = session.execute(select(Users).where(Users.email == email)).scalars().first()
            if not user:
                flash("Email does not exist")
                return redirect(url_for('login'))
            else:
                if security.check_password_hash(pwhash=user.password, password=password):
                    login_user(user)
                    return redirect(url_for('home'))
                else:
                    flash("Password incorrect")
                    return redirect(url_for('login'))
    return render_template("login.html", user=current_user)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True)