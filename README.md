# Backend clone  of social media app by using FastAPI

#### This API  has 4 routes

## 1) Post route

#### This route is reponsible for creating post, deleting post, updating post and Checkinh post

## 2) Users route

#### This route is about creating users and searching user by id

## 3) Auth route

#### This route is about login system

## 4) Vote route

 #### This route is about likes or vote system and this route contain code for upvote or back vote there is not logic about down vote

# how to run locally
First clone this repo by using following command
````

git clone https://github.com/lokhandeganesh/fastapi-course-freecodecamp.git

````
then 
````

cd fastapi-course

````

Then install fastapp using all flag like 

````

pip install uv

````

Then go this repo folder in your local computer run follwoing command
````

uv run uvicorn app.main:app --port 8000 --reload

````

Then you can use following link to use the  API, our swagger protected using docshield,
check .env file for password, this can be changed in main.py files DocShield section.

````

http://127.0.0.1:8000/docs 

````

## After run this API you need a database in postgres 
Create a database in postgres then create a file name .env and write the following things in you file, we can copy .env-test for refernce and rename it to .env with valid values

````
DATABASE_HOSTNAME = localhost
DATABASE_PORT = 5432
DATABASE_PASSWORD = passward_that_you_set
DATABASE_NAME = name_of_database
DATABASE_USERNAME = User_name
SECRET_KEY = 09d25e094faa2556c818166b7a99f6f0f4c3b88e8d3e7 
ALGORITHM = HS256
ACCESS_TOKEN_EXPIRE_MINUTES = 60(base)
ADMIN_PASS = admin_pass
#DEVELOPER_PASS = developer_pass
#VIEWER_PASS = viewer_pass

````
### Note: SECRET_KEY in this exmple is just a psudo key. You need to get a key for youself and you can get the SECRET_KEY  from fastapi documantion
 

### Here is the link of the playlist on youtube you can learn all about FASTAPI
 
<div id="badges">
  <a href="https://www.youtube.com/watch?v=Yw4LmMQXXFs&list=PL8VzFQ8k4U1L5QpSapVEzoSfob-4CR8zM&index=2">
    <img src="https://freshidea.com/jonah/youtube-api/subscribers-badge.php?label=Subscribers&style=for-the-badge&color=red&labelColor=ce4630" alt="youtube Badge"/>
  </a>
