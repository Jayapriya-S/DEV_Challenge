from flask import render_template, request, redirect, url_for
from src.models import db, DevelopmentGoal
from datetime import datetime, date

def init_routes(app):
    @app.route('/')
    def index():
        goals = DevelopmentGoal.query.all()
        return render_template("index.html", goals=goals)

    @app.route('/add_goal', methods=["GET", "POST"])
    def add_goal():
        if request.method == "POST":
            try:
                description = request.form["description"].strip()
                target_date_str = request.form["target_date"]

                # Validate description
                if not description:
                    return "Goal description cannot be empty.", 400
                if len(description) > 200:
                    return "Goal description cannot exceed 200 characters.", 400

                # Convert string date to datetime object
                target_date = datetime.strptime(target_date_str, "%Y-%m-%d").date()

                # Validate target date is not in the past
                if target_date < date.today():
                    return "Target date cannot be in the past.", 400

                new_goal = DevelopmentGoal(
                    description=description,
                    target_date=target_date
                )
                db.session.add(new_goal)
                db.session.commit()
                return redirect(url_for("index"))
            except ValueError as e:
                # Handle invalid date format
                return "Invalid date format. Please use YYYY-MM-DD format.", 400
        return render_template("add_goal.html", today=date.today())

    @app.route('/delete_goal/<int:goal_id>')
    def delete_goal(goal_id):
        goal = DevelopmentGoal.query.get_or_404(goal_id)
        db.session.delete(goal)
        db.session.commit()
        return redirect(url_for('index'))

    @app.route('/complete_goal/<int:goal_id>')
    def complete_goal(goal_id):
        goal = DevelopmentGoal.query.get_or_404(goal_id)
        goal.completed = True
        db.session.commit()
        return redirect(url_for('index'))
