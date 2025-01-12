from src.models import DevelopmentGoal
from datetime import datetime

def test_index_page(client):
    """Test index page loads correctly"""
    response = client.get('/')
    assert response.status_code == 200
    assert b'Your Goals' in response.data

def test_add_goal_page(client):
    """Test add goal page loads correctly"""
    response = client.get('/add_goal')
    assert response.status_code == 200
    assert b'Add New Goal' in response.data

def test_add_goal_past_date(client, db, past_date):
    """Test adding goal with past date fails"""
    response = client.post('/add_goal', data={
        'description': 'Past Goal',
        'target_date': past_date
    })
    assert response.status_code == 400
    assert b'Target date cannot be in the past' in response.data

def test_add_goal_invalid_date(client, db):
    """Test adding goal with invalid date format"""
    response = client.post('/add_goal', data={
        'description': 'Invalid Date Goal',
        'target_date': 'invalid-date'
    })
    assert response.status_code == 400

def test_complete_goal(client, db, future_date):
    """Test marking a goal as complete"""
    # First create a goal
    goal = DevelopmentGoal(description='Complete me', target_date=datetime.strptime(future_date, '%Y-%m-%d').date())
    db.session.add(goal)
    db.session.commit()

    response = client.get(f'/complete_goal/{goal.id}', follow_redirects=True)
    assert response.status_code == 200

    updated_goal = DevelopmentGoal.query.get(goal.id)
    assert updated_goal.completed is True

def test_delete_goal(client, db, future_date):
    """Test deleting a goal"""
    # First create a goal
    goal = DevelopmentGoal(description='Delete me', target_date=datetime.strptime(future_date, '%Y-%m-%d').date())
    db.session.add(goal)
    db.session.commit()

    response = client.get(f'/delete_goal/{goal.id}', follow_redirects=True)
    assert response.status_code == 200

    deleted_goal = DevelopmentGoal.query.get(goal.id)
    assert deleted_goal is None

def test_complete_nonexistent_goal(client, db):
    """Test completing a goal that doesn't exist"""
    response = client.get('/complete_goal/999', follow_redirects=True)
    assert response.status_code == 404

def test_delete_nonexistent_goal(client, db):
    """Test deleting a goal that doesn't exist"""
    response = client.get('/delete_goal/999', follow_redirects=True)
    assert response.status_code == 404

# Positive Test Cases
def test_index_page_empty(client, db):
    """Test index page with no goals"""
    # Ensure database is empty
    db.session.query(DevelopmentGoal).delete()
    db.session.commit()
    
    response = client.get('/')
    assert response.status_code == 200
    assert b'Your Goals' in response.data
    assert b'No goals yet' in response.data  # Update template to show this message

def test_add_goal_form_elements(client):
    """Test all form elements present on add goal page"""
    response = client.get('/add_goal')
    assert b'description' in response.data
    assert b'target_date' in response.data
    assert b'Add Goal' in response.data

def test_add_valid_goal_min_length(client, db, future_date):
    """Test adding goal with minimum length description"""
    response = client.post('/add_goal', data={
        'description': 'Test',
        'target_date': future_date
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'Test' in response.data

def test_add_valid_goal_max_length(client, db, future_date):
    """Test adding goal with maximum length description"""
    long_desc = 'x' * 200  # Max length is 200
    response = client.post('/add_goal', data={
        'description': long_desc,
        'target_date': future_date
    }, follow_redirects=True)
    assert response.status_code == 200
    assert bytes(long_desc, 'utf-8') in response.data

def test_complete_goal_updates_ui(client, db, future_date):
    """Test UI updates when goal is marked complete"""
    goal = DevelopmentGoal(description='Complete me', target_date=datetime.strptime(future_date, '%Y-%m-%d').date())
    db.session.add(goal)
    db.session.commit()

    response = client.get(f'/complete_goal/{goal.id}', follow_redirects=True)
    assert b'(Completed)' in response.data
    assert b'Mark as Complete' not in response.data

# Negative Test Cases
def test_add_goal_empty_description(client, db, future_date):
    """Test adding goal with empty description"""
    response = client.post('/add_goal', data={
        'description': '',
        'target_date': future_date
    })
    assert response.status_code == 400

def test_add_goal_too_long_description(client, db, future_date):
    """Test adding goal with description > 200 chars"""
    response = client.post('/add_goal', data={
        'description': 'x' * 201,
        'target_date': future_date
    })
    assert response.status_code == 400

def test_add_goal_no_date(client, db):
    """Test adding goal without target date"""
    response = client.post('/add_goal', data={
        'description': 'No Date Goal'
    })
    assert response.status_code == 400

def test_add_goal_invalid_date_format(client, db):
    """Test various invalid date formats"""
    invalid_dates = ['2024', '2024-13-01', '2024-01-32', 'invalid']
    for invalid_date in invalid_dates:
        response = client.post('/add_goal', data={
            'description': 'Invalid Date Goal',
            'target_date': invalid_date
        })
        assert response.status_code == 400

def test_complete_already_completed_goal(client, db, future_date):
    """Test completing an already completed goal"""
    goal = DevelopmentGoal(
        description='Already Complete',
        target_date=datetime.strptime(future_date, '%Y-%m-%d').date(),
        completed=True
    )
    db.session.add(goal)
    db.session.commit()

    response = client.get(f'/complete_goal/{goal.id}', follow_redirects=True)
    assert response.status_code == 200  # Should still work but not change state

def test_delete_completed_goal(client, db, future_date):
    """Test deleting a completed goal"""
    goal = DevelopmentGoal(
        description='Delete Complete',
        target_date=datetime.strptime(future_date, '%Y-%m-%d').date(),
        completed=True
    )
    db.session.add(goal)
    db.session.commit()

    response = client.get(f'/delete_goal/{goal.id}', follow_redirects=True)
    assert response.status_code == 200
    assert DevelopmentGoal.query.get(goal.id) is None

def test_invalid_goal_ids(client):
    """Test various invalid goal IDs"""
    invalid_ids = [0, -1, 'abc', '!@#']
    for invalid_id in invalid_ids:
        response = client.get(f'/complete_goal/{invalid_id}')
        assert response.status_code == 404
        response = client.get(f'/delete_goal/{invalid_id}')
        assert response.status_code == 404
