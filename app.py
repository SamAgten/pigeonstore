from flask import Flask, render_template, session, redirect, url_for, request, flash
import sqlite3
from flask_sqlalchemy import SQLAlchemy
from website import create_app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)