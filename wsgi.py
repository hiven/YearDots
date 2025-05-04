from app import create_app        # noqa: E402  (after .env is loaded)

app = create_app()

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
