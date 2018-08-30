# StackOverflow-lite-v2

- StackOverflow-lite is a platform where people can ask questions and provide answers.

- This branch contains API endpoints for the above application and tests
- This is v2 of the API v1 can be found [HERE](https://github.com/joshNic/Stack0verflow-lite/tree/Develop)
# Tools Used
- `Python3.6` - A High Level Programming Language
- `Flask` - Python based web framework
- `Pytest` - A Python testing  framework which makes it easy to write small tests, yet scales to support complex functional testing for applications and libraries
- `Virtualenv` - A tool to create isolated virtual environment
- `Postgresql` - PostgreSQL is a powerful, open source object-relational database system.
# Running the tests
To run tests run this command below in your terminal

```
py.test --cov-report term --cov=app
```

# Installation
**Clone this _Repository_**
```
$ https://github.com/joshNic/StackOverflow-lite-v2/tree/challenge_3
$ cd StackOverflow-lite
```
**Create virtual environment and install it**
```
$ virtualenv --python = python3 venv
$ source / venv/bin/activate
```
**Install all the necessary _dependencies_ by**
```
$ pip install - r requirements.txt
```
**Run _app_ by**
```
$ Python run.py
$ Run the server At the terminal or console type
```
# End Points
|           End Point | Functionality |
| -------------------------------------- | ----------------------------------------- |
|     POST   api/v2/question | Post a new Question |
|     POST api/v2/question/<int: questionId > /answer | Post answer to question |
|     GET  api/v2/question/<int: questionId > |             Get a specific question |
|     GET  api/v2/questions | Get all Questions |
|     PUT  api/v2/question/<int: questionId >/answer/<int: answer_id> |Update answer and answer status (it allows a questioner owner to update answer status and an answer author to update answer body) |
|     PUT api/v2/question/<int: questionId> | Update a question   |
|     POST api/v2/auth/signup | Allow a user to register on the system    |
|     GET api/v2/auth/login   | Allow a user to login the system  |
# End Points Reponse structure
# Get Questions Endpoint Response Structure
```
Response 200 (application/json)
{
    "question_id": 1,
    "question_title": "What does 404 mean",
    "question_body": "So i came across this and i dont know what it means"
}
```
# Get single Questions Endpoint Response Structure
```
+ Parameters
    + questionId: __(required, number) - ID of the Question in form of an integer
Response 200 (application/json)
{
    "question_id": {questionId},
    "question_title": "What does 404 mean",
    "question_body": "So i came across this and i dont know what it means"
}
```
# Post Questions Endpoint Response Structure
```
Response 201 (application/json)
body
    {
        "question_title": "What does 404 mean",
        "question_body": "So i came across this and i dont know what it means"
    }
```

# Post Answer Endpoint Response Structure
```
+ Parameters
    + questionId: __(required, number) - ID of the Question you are answering in form of an integer
Response 201 (application/json)
body
    {
        "question_id": {questionId},
        "answer_body": "So i came across this and i dont know what it means"
    }
```

# Contributors
- [Joshua Mugisha](https://github.com/joshNic)

