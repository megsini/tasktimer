# Task Timer with Progress Tracking
#### Video Demo: [https://drive.google.com/file/d/160y51Rj5JBok_uCQ48k4Ads42iR8pAA9/view?usp=sharing]
#### Description:

The Task Timer with Progress Tracking is a productivity application designed to help users manage their work sessions and maintain records of their completed and incomplete tasks. This project extends beyond traditional timer applications by incorporating progress tracking functionality, enabling users to monitor their work patterns and task completion rates.

### Project Components

The application consists of three key files:

- `project.py`: The main application file containing:
  - Timer functionality and controls
  - Task management system
  - Progress tracking implementation
  - User interface using tkinter
  - Data storage and retrieval logic

- `test_project.py`: A comprehensive test suite that:
  - Validates timer functionality
  - Tests task management features
  - Verifies progress tracking accuracy
  - Ensures data persistence reliability

- `requirements.txt`: Lists all project dependencies including:
  - Required Python packages
  - Version specifications
  - Essential libraries for application execution

### Features

1. **Custom Timer Settings**
   - Customisable work and break durations
   - Support for various time management methods, including the Pomodoro technique
   - Flexible timer controls (start, pause, resume)

2. **Task Management**
   - Task naming functionality
   - Completion status tracking
   - Dismissal options for incomplete tasks

3. **Progress Tracking**
   - Comprehensive task history
   - Completion status logging
   - Total work time calculation

### Design Decisions

Key design choices implemented during development:

1. **User Interface**
   - Minimalist design to reduce distractions
   - Clear visual feedback for timer states

2. **Progress Tracking**
   - Inclusion of dismissed tasks in the log for complete work history
   - Separate tracking for completed versus dismissed tasks for accurate productivity metrics
   - Total work time tracking across multiple sessions for tasks exceeding standard work time

3. **Data Persistence**
   - Local storage implementation for data privacy and quick access
   - Efficient data structure for task logging

### Future Enhancements

Planned improvements for future versions include:

- Task categories and tags
- Detailed analytics and statistics
- Export functionality for progress data
- Integration with laptop top bar for timer visibility
- Break time notifications

### Technical Requirements

- Python 3.x
- Tkinter library
- SQLite3 for data storage
- Additional Python packages (detailed in requirements.txt)

This project, developed as part of CS50's introduction to Python programming, demonstrates the practical application of core programming concepts including GUI development, data persistence, and event-driven programming.
