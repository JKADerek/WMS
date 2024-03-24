from app import create_app
import sys

app = create_app()

print(sys.path)

if __name__ == '__main__':
    app.run(debug=True)
