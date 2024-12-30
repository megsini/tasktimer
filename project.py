# project.py
import tkinter as tk
from tkinter import ttk
from datetime import datetime, timedelta
import json
from pathlib import Path

def format_time(seconds):
    """Convert seconds to MM:SS format.
    
    Args:
        seconds (int): Number of seconds
        
    Returns:
        str: Time in MM:SS format
    """
    minutes = seconds // 60
    remaining_seconds = seconds % 60
    return f"{minutes:02d}:{remaining_seconds:02d}"

def save_task_history(task_name, duration, status):
    """Save completed task to JSON file.
    
    Args:
        task_name (str): Name of the task
        duration (int): Duration in minutes
        status (str): 'completed' or 'dismissed'
    """
    history_file = Path("task_history.json")
    today = datetime.now().strftime("%Y-%m-%d")
    
    if history_file.exists():
        with open(history_file) as f:
            history = json.load(f)
    else:
        history = {}
    
    if today not in history:
        history[today] = []
        
    history[today].append({
        "name": task_name,
        "duration": duration,
        "status": status
    })
    
    with open(history_file, "w") as f:
        json.dump(history, f)

def get_daily_stats():
    """Get statistics for today's tasks.
    
    Returns:
        tuple: (total_minutes, completed_tasks, all_tasks)
    """
    history_file = Path("task_history.json")
    today = datetime.now().strftime("%Y-%m-%d")
    
    if not history_file.exists():
        return 0, 0, []
        
    with open(history_file) as f:
        history = json.load(f)
        
    if today not in history:
        return 0, 0, []
        
    today_tasks = history[today]
    total_minutes = sum(task["duration"] for task in today_tasks)
    completed_tasks = sum(1 for task in today_tasks if task["status"] == "completed")
    
    return total_minutes, completed_tasks, today_tasks

class TaskTimer:
    def __init__(self, root):
        self.root = root
        self.root.title("Task Timer")
        self.root.geometry("400x600")
        
        style = ttk.Style()
        style.configure("Timer.TLabel", font=("Helvetica", 48))
        
        self.setup_variables()
        self.create_widgets()
        self.setup_timer()
    
    def setup_variables(self):
        self.task_name = tk.StringVar()
        self.work_time = tk.StringVar()
        self.break_time = tk.StringVar()
        self.timer_text = tk.StringVar(value="00:00")
        self.cycle_text = tk.StringVar()
        self.total_time_text = tk.StringVar()
        
        self.is_running = False
        self.is_break = False
        self.remaining_seconds = 0
        self.current_cycle = 0
        self.total_time_spent = 0
        self.current_cycle_time = 0
    
    def create_widgets(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky="nsew")
        
        # Task name entry
        ttk.Label(main_frame, text="Task Name").grid(row=0, column=0, pady=5)
        ttk.Entry(main_frame, textvariable=self.task_name).grid(row=0, column=1, pady=5)
        
        # Time inputs
        time_frame = ttk.Frame(main_frame)
        time_frame.grid(row=1, column=0, columnspan=2, pady=10)
        
        ttk.Label(time_frame, text="Work (min)").grid(row=0, column=0)
        ttk.Entry(time_frame, textvariable=self.work_time, width=10).grid(row=0, column=1)
        
        ttk.Label(time_frame, text="Break (min)").grid(row=0, column=2)
        ttk.Entry(time_frame, textvariable=self.break_time, width=10).grid(row=0, column=3)
        
        # Timer display
        ttk.Label(main_frame, textvariable=self.timer_text, style="Timer.TLabel").grid(row=2, column=0, columnspan=2, pady=20)
        ttk.Label(main_frame, textvariable=self.cycle_text).grid(row=3, column=0, columnspan=2)
        ttk.Label(main_frame, textvariable=self.total_time_text).grid(row=4, column=0, columnspan=2)
        
        # Control buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=5, column=0, columnspan=2, pady=20)
        
        self.start_button = ttk.Button(button_frame, text="Start", command=self.toggle_timer)
        self.start_button.grid(row=0, column=0, padx=5)
        
        ttk.Button(button_frame, text="View Progress", command=self.show_progress).grid(row=0, column=1, padx=5)
        
        self.complete_button = ttk.Button(button_frame, text="Complete", command=self.complete_task, state="disabled")
        self.complete_button.grid(row=1, column=0, padx=5, pady=10)
        
        self.dismiss_button = ttk.Button(button_frame, text="Dismiss", command=self.dismiss_task, state="disabled")
        self.dismiss_button.grid(row=1, column=1, padx=5, pady=10)
    
    def setup_timer(self):
        self.timer = None
    
    def toggle_timer(self):
        if not self.is_running:
            if self.remaining_seconds == 0:
                try:
                    work_minutes = int(self.work_time.get())
                    self.remaining_seconds = work_minutes * 60
                except ValueError:
                    return
                    
            self.is_running = True
            self.start_button.configure(text="Pause")
            self.complete_button.configure(state="normal")
            self.dismiss_button.configure(state="normal")
            self.update_timer()
        else:
            self.is_running = False
            self.start_button.configure(text="Start")
            if self.timer:
                self.root.after_cancel(self.timer)
    
    def update_timer(self):
        if self.is_running and self.remaining_seconds > 0:
            self.timer_text.set(format_time(self.remaining_seconds))
            self.cycle_text.set(f"{'Break' if self.is_break else 'Work'} Time (Cycle {self.current_cycle + 1})")
            
            if not self.is_break:
                self.current_cycle_time += 1
                total_minutes = (self.total_time_spent + self.current_cycle_time) // 60
                self.total_time_text.set(f"Total work time: {total_minutes} minutes")
            
            self.remaining_seconds -= 1
            self.timer = self.root.after(1000, self.update_timer)
        elif self.remaining_seconds == 0:
            if not self.is_break and self.break_time.get():
                self.total_time_spent += self.current_cycle_time
                self.current_cycle_time = 0
                self.is_break = True
                try:
                    break_minutes = int(self.break_time.get())
                    self.remaining_seconds = break_minutes * 60
                except ValueError:
                    return
                self.current_cycle += 1
                self.update_timer()
            elif self.is_break and self.work_time.get():
                self.is_break = False
                try:
                    work_minutes = int(self.work_time.get())
                    self.remaining_seconds = work_minutes * 60
                except ValueError:
                    return
                self.update_timer()
            else:
                self.reset_timer()
    
    def reset_timer(self):
        self.is_running = False
        self.is_break = False
        self.remaining_seconds = 0
        self.current_cycle = 0
        self.timer_text.set("00:00")
        self.cycle_text.set("")
        self.total_time_text.set("")
        self.start_button.configure(text="Start")
        self.complete_button.configure(state="disabled")
        self.dismiss_button.configure(state="disabled")
        if self.timer:
            self.root.after_cancel(self.timer)
    
    def complete_task(self):
        if self.task_name.get():
            total_minutes = (self.total_time_spent + self.current_cycle_time) // 60
            save_task_history(self.task_name.get(), total_minutes, "completed")
            self.reset_timer()
            self.task_name.set("")
            self.work_time.set("")
            self.break_time.set("")
    
    def dismiss_task(self):
        if self.task_name.get():
            total_minutes = (self.total_time_spent + self.current_cycle_time) // 60
            save_task_history(self.task_name.get(), total_minutes, "dismissed")
            self.reset_timer()
            self.task_name.set("")
            self.work_time.set("")
            self.break_time.set("")
    
    def show_progress(self):
        progress_window = tk.Toplevel(self.root)
        progress_window.title("Progress")
        progress_window.geometry("300x400")
        
        total_minutes, completed_tasks, tasks = get_daily_stats()
        
        ttk.Label(progress_window, text="Today", font=("Helvetica", 16, "bold")).pack(pady=10)
        
        stats_frame = ttk.Frame(progress_window)
        stats_frame.pack(pady=10)
        
        ttk.Label(stats_frame, text=f"Minutes\n{total_minutes}", font=("Helvetica", 12)).grid(row=0, column=0, padx=20)
        ttk.Label(stats_frame, text=f"Completed\n{completed_tasks}", font=("Helvetica", 12)).grid(row=0, column=1, padx=20)
        
        task_frame = ttk.Frame(progress_window)
        task_frame.pack(pady=10, fill="both", expand=True)
        
        for task in tasks:
            task_text = f"{task['duration']}min - {task['name']}"
            if task['status'] == 'dismissed':
                task_text += " (dismissed)"
            ttk.Label(task_frame, text=task_text).pack(pady=2)

def main():
    print("Starting Task Timer application...")  # Add this line
    root = tk.Tk()
    print("Created root window...")  # Add this line
    app = TaskTimer(root)
    print("Created TaskTimer app...")  # Add this line
    root.mainloop()
    
if __name__ == "__main__":
    main()