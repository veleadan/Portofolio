from setuptools import setup, find_packages

setup(
    name="my_fastapi_app",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "fastapi",
        "uvicorn",
        "sqlalchemy",
        "pydantic",
        "alembic",
        "starlette",
    ],
    entry_points={
        'console_scripts': [
            'my_fastapi_app=my_fastapi_app.main:app',
        ],
    },
)

# Security scheme pentru Swagger
security_scheme = {
    "sessionAuth": {
        "type": "apiKey",
        "in": "cookie",
        "name": "session",
        "description": "Autentificare cu sesiune"
    }
}