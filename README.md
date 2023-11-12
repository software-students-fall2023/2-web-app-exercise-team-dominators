# Web Application Exercise

A little exercise to build a web application following an agile development process. See the [instructions](instructions.md) for more detail.

## Product vision statement

To develop a user-friendly and efficient event ticket tracker that offers real-time notifications, fast search, event watchlist, and price detection, addressing the frustrations of event enthusiasts who has low budget and meeting their needs for convenience and information accessibility.

## User stories

[Link to Issues](https://github.com/software-students-fall2023/2-web-app-exercise-team-dominators/issues)

## Task boards

[Link to Sprint 1](https://github.com/orgs/software-students-fall2023/projects/6)
[Meetings](https://docs.google.com/document/d/114rBlqlLAI8gh3qC9gGgjGsPDPorCrgCo4xRm_N32e4/edit)

## Set up our program

### Install Required Software

Python, pip (Python package installer), Virtual environment (venv), MongoDB running on your system

### Clone our project to your local machine

### Create a Virtual Environment

In your project directory, run:

```bash
python -m venv venv
```

Activate the virtual environment:

```bash
source venv/bin/activate
```

### Install Dependencies

```python
pip install -r requirements.txt
```

### **Set Up Environment Variables**

```python
export FLASK_APP=app.py
export FLASK_ENV=development
export MONGO_URI="mongodb+srv://ys4323:Syysyysyy1@cluster0.ocmpb3f.mongodb.net/?retryWrites=true&w=majority"
```

### **Run the Flask Application**

Navigate to the directory containing your Flask app and run:

```python
python app.py
```

### Access the Application

Open a web browser and navigate to the address provided by Flask, typically `http://127.0.0.1:5000`.
