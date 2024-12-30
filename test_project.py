# test_project.py
import json
from pathlib import Path
import pytest
from project import format_time, save_task_history, get_daily_stats
from datetime import datetime

def test_format_time():
    assert format_time(0) == "00:00"
    assert format_time(61) == "01:01"
    assert format_time(3600) == "60:00"
    assert format_time(30) == "00:30"
    assert format_time(90) == "01:30"

def test_save_task_history(tmp_path):
    # Create a temporary file path
    test_file = tmp_path / "task_history.json"
    original_path = Path("task_history.json")
    
    # Temporarily replace the real file path with our test path
    Path.exists = lambda x: test_file.exists()
    
    # Test saving a new task
    save_task_history("Test Task", 30, "completed")
    
    # Verify the file was created and contains correct data
    assert test_file.exists()
    with open(test_file) as f:
        data = json.load(f)
    
    today = datetime.now().strftime("%Y-%m-%d")
    assert today in data
    assert len(data[today]) == 1
    assert data[today][0]["name"] == "Test Task"
    assert data[today][0]["duration"] == 30
    assert data[today][0]["status"] == "completed"

def test_get_daily_stats(tmp_path):
    # Create a temporary file path
    test_file = tmp_path / "task_history.json"
    original_path = Path("task_history.json")
    
    # Set up test data
    today = datetime.now().strftime("%Y-%m-%d")
    test_data = {
        today: [
            {"name": "Task 1", "duration": 30, "status": "completed"},
            {"name": "Task 2", "duration": 45, "status": "dismissed"},
            {"name": "Task 3", "duration": 60, "status": "completed"}
        ]
    }
    
    # Write test data to file
    with open(test_file, "w") as f:
        json.dump(test_data, f)
    
    # Temporarily replace the real file path with our test path
    Path.exists = lambda x: test_file.exists()
    
    # Test getting stats
    total_minutes, completed_tasks, tasks = get_daily_stats()
    
    # Verify results
    assert total_minutes == 135  # 30 + 45 + 60
    assert completed_tasks == 2  # Only tasks with "completed" status
    assert len(tasks) == 3  # All tasks
    assert tasks[0]["name"] == "Task 1"
    assert tasks[1]["duration"] == 45
    assert tasks[2]["status"] == "completed"