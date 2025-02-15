from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import smtplib
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session
from sqlalchemy import create_engine, select, insert, update, delete, TIMESTAMP, desc
from dataclasses import dataclass
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField, TextAreaField
from wtforms.validators import DataRequired, Email, Length

engine = create_engine("sqlite:///blog.db", echo=True)

class Base(DeclarativeBase):
    type_annotation_map = {
        datetime: TIMESTAMP(timezone=True)
    }

class Users(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key= True)
    email: Mapped[str] = mapped_column(unique= True)
    password: Mapped[str]

Base.metadata.create_all(engine)

e_mail = "danihart060@gmail.com"
password = "uzznekeniyumzqou"


app = Flask(__name__)
app.config["SECRET_KEY"] = "Bobo7711"

def get_blogposts():
    x = select(Posts).order_by(desc(Posts.date))
    with engine.connect() as conn:
        posts_db = conn.execute(x).all()
    blogposts = [{"title": each_post.title, "author": each_post.author, "month": each_post.date.date().strftime("%B"), "day": each_post.date.date().day, "year": each_post.date.date().year, "text": each_post.text, "id": each_post.id} for each_post in posts_db]
    return blogposts

@app.route("/")
def home():
    return render_template("index.html", posts=get_blogposts())

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

@app.route("/post/<num>")
def post(num):
    for post in get_blogposts():
        if post["id"] == int(num):
            blogpost = post
    texts = blogpost["text"].split("\n")
    return render_template("post.html", post=blogpost, texts=texts, route_no=num)

@app.route("/new-post", methods=["GET", "POST"])
def new_post():
    if request.method == "POST":
        with Session(engine) as session:
            session.execute(
                insert(Posts),
                [
                    {"title": request.form.get("name"), "author": request.form.get("email"), "text": request.form.get("message"), "date": datetime.now()}
                ]
            )
            session.commit()
        return redirect(url_for('home'))
    return render_template("new-post.html")

@app.route("/post/<num>/edit-post", methods=["GET", "POST"])
def edit_post(num):
    with Session(engine) as session:
        result = session.execute(select(Posts).where(Posts.id == num))
        post = result.scalars().first()
    return render_template("edit-post.html", post=post, num=num)

@app.route("/post/<num>/delete", methods=["GET", "POST"])
def delete_post(num):
    with Session(engine) as session:
        session.execute(
            delete(Posts).where(Posts.id == num)
        )
        session.commit()
    return redirect(url_for('home'))

@app.post("/new-route/<num>")
def new_route(num):
    title = request.form.get("name")
    author = request.form.get("email")
    msg = request.form.get("message")
    with Session(engine) as session:
        session.execute(
            update(Posts),
            [
                {"id": num, "title": title, "author": author, "text": msg, "date": datetime.now()}
            ]
        )
        session.commit()
    return redirect(url_for('home'))

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        with Session(engine) as session:
            session.execute(
                insert(Users),
                [
                    {"email": request.form.get("email"), "password": request.form.get("password")}
                ]
            )
            session.commit()
            return redirect(url_for("home"))
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    return render_template("login.html")
    
if __name__ == "__main__":
    app.run(debug=True)