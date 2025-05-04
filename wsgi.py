from app import create_app

app = create_app()          # the server only sees this one object

if __name__ == "__main__":
    app.run(debug=True)
