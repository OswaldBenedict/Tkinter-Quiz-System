import tkinter as tk
from tkinter import messagebox
import random
import os

QUESTIONS = [
   { #1
        "question": "What is the farthest man made object?",
        "choices": ["A. Voyager 1", "B. Voyager 2", "C. ISS", "D. Pioneer 10"],
        "answer": "A"  
    },

    { #2
        "question": "It is a region around a star where temperatures are just right for liquid water to exist on a planet's surface",
        "choices": ["A. Petrova Line", "B. Goldilocks Zone", "C. Danger Zone", "D. School Zone"],
        "answer": "B"

    },
    {#3
        "question": "What is the brightest star in the night sky?",
        "choices": ["A. Betelgeuse", "B. Rigel", "C. Polaris", "D. Sirius"],
        "answer": "D"

    },
    {#4
        "question": "What constellation resembles a dog",
        "choices": ["A. Big Dipper", "B. Orion", "C. Canis Major", "D. Draco"],
        "answer": "C"

    },
    {#5
        "question": "How many moons does Saturn have?",
        "choices": ["A. 293", "B. 67", "C. 357", "D. 500"],
        "answer": "A"

    },
    {#6
        "question": "What is the shape of the Earth?",
        "choices": ["A. Circle", "B. Sphere", "C. Oblate Spheroid", "D. Cube"],
        "answer": "C"

    },
    {#7
        "question": "Which planet is named after the Roman God of War?",
        "choices": ["A. Mars", "B. Saturn", "C. Earth", "D. Venus"],
        "answer": "A"

    },
    {#8
        "question": "What do you call the giant explosion that occurs when massive star dies?",
        "choices": ["A. Neutron Star", "B. Supernova", "C. Black Hole", "D. Event Horizon"],
        "answer": "B"

    },
    {#9
        "question": "It occurs when the Moon passes between the Sun and Earth during a new moon, casting a shadow on Earth and blocking some or all of the Sun's light",
        "choices": ["A. Solar Eclipse", "B. Lunar Eclipse", "C. Meteor Shower", "D. Partial Lunar Eclipse"],
        "answer": "A"

    },
    {#10
        "question": "Which Galaxy is our solar system located at?",
        "choices": ["A. Andromeda Galaxy", "B. Milky Way Galaxy", "C. Triangulum Galaxy", "D. Whirlpool Galaxy"],
        "answer": "B"

    }
]

#APP SETTINGS
TIME_LIMIT = 15
HIGH_SCORE_FILE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "high_score.txt" 
    )


BG_COLOR = "#F5F0E6"
PRIMARY_COLOR = "#02005A"
CORRECT_COLOR = "#2E7D32"
WRONG_COLOR = "#C62828"

root = tk.Tk()
root.title("Advanced Quiz Application")
root.geometry("700x640")
root.configure(bg="black")
root.resizable(False,False)


quiz_questions = []
currrent_question = 0
score = 0
time_left = TIME_LIMIT
wrong_answers = []
timer_job = None
answered = False
selected_answer = tk.StringVar()

timer_label = None
feedback_label = None
submit_button = None
next_button = None
choice_buttons = []

main_frame = tk.Frame(root, bg=BG_COLOR)
main_frame.pack(fill="both", expand=True, padx=30, pady=20)

######
def get_high_score():
    if os.path.exists(HIGH_SCORE_FILE):
        try:
            with open(HIGH_SCORE_FILE, "r") as file:
                return int(file.read().strip())
        except ValueError:
            return 0 
        return 0 


def save_high_score(new_score):
    if new_score > get_high_score():
        with open(HIGH_SCORE_FILE, "w") as file:
            file.write(str(new_score))
        return True
    return False

def clear_screen():
    for widget in main_frame.winfo_children():
        widget.destroy()

def get_choice_text(question, letter):
    for choice in question["choices"]:
        if choice.startswith(letter + "."):
            return choice
    return "No answer"


def show_start_screen():
    clear_screen()
    tk.Label(main_frame, text="Space Quiz", 
             font=("Segoe UI", 28,"bold"),
             bg=BG_COLOR,fg=PRIMARY_COLOR).pack(pady=(60,10))
    tk.Label(main_frame, text="Test your space knowledge with this quiz!",
             font=("Segoe UI", 13), bg=BG_COLOR).pack(pady=5)
    tk.Label(main_frame,
             text=f"{len(QUESTIONS)} questions | {TIME_LIMIT} seconds per question",
             font=("Segoe UI", 13), bg=BG_COLOR).pack(pady=5)
    tk.Label(main_frame, text=f"High Score: {get_high_score()} / {len(QUESTIONS)}",
             font=("Segoe UI", 16, "bold"), bg=BG_COLOR).pack(pady=20)
    tk.Button(main_frame, text="Start Quiz", font=("Segoe UI", 16, "bold"),
              bg=PRIMARY_COLOR, fg="white", width=15,
              command=start_quiz).pack(pady=20)



def start_quiz():
    global quiz_questions, currrent_question, score, wrong_answers
    quiz_questions = random.sample(QUESTIONS, len(QUESTIONS))
    currrent_question = 0
    score = 0
    wrong_answers = []
    show_question()

def show_question():
    global time_left, answered, timer_label, feedback_label
    global submit_button, next_button, choice_buttons

    clear_screen()
    answered = False
    selected_answer.set("")
    time_left = TIME_LIMIT
    question = quiz_questions[currrent_question]

    #progress and timer
    top_frame = tk.Frame(main_frame, bg=BG_COLOR)
    top_frame.pack(fill="x")
    tk.Label(top_frame, text=f"Question {currrent_question + 1} of {len(quiz_questions)}",
            font=("Segoe UI", 13, "bold"),
            bg=BG_COLOR).pack(side="left")
    timer_label = tk.Label(top_frame, text="", font=("Segoe UI", 13, "bold"),
                            bg=BG_COLOR)
    timer_label.pack(side="right")

    tk.Label(main_frame, text=f"Score: {score}", font=("Segoe UI", 12),
             bg=BG_COLOR).pack(anchor="w", pady=(5,0))

    tk.Label(main_frame, text=question["question"],
            font=("Segoe UI", 18, "bold"), wraplength=620, justify="left",
            bg=BG_COLOR).pack(pady=25, anchor="w")

    #Answer choices
    choice_buttons = []
    for choice in question["choices"]:
        letter = choice[0]
        button = tk.Radiobutton(main_frame, text=choice,
                                variable=selected_answer, value=letter,
                                font=("Segoe UI", 14), bg=BG_COLOR,
                                activebackground=BG_COLOR, anchor="w")
        button.pack(fill="x", pady=4)
        choice_buttons.append(button)

    feedback_label = tk.Label(main_frame, text="", font=("Segoe UI", 13, "bold"),
                              bg=BG_COLOR, wraplength=620)
    feedback_label.pack(pady=15)

    button_frame = tk.Frame(main_frame, bg=BG_COLOR)
    button_frame.pack()
    submit_button = tk.Button(button_frame, text="Submit Answer",
                              font=("Segoe UI", 13, "bold"), bg=PRIMARY_COLOR,
                              fg="white", width=15, command=submit_answer)
    submit_button.pack(side="left", padx=10)

    last_question = currrent_question == len(quiz_questions) - 1
    next_button = tk.Button(button_frame,
                            text="See Results" if last_question else "Next Question",
                            font=("Segoe UI", 13, "bold"), width=15,
                            state="disabled", command=next_question)
    next_button.pack(side="left", padx=10)

    update_timer()


def update_timer():
    global time_left, timer_job
    if answered:
        return
    timer_label.config(text=f"Time left: {time_left} s", 
                       fg=WRONG_COLOR if time_left <= 5 else "black")
    if time_left == 0:
        time_up()
        return
    time_left -= 1
    timer_job = root.after(1000, update_timer)

def stop_timer():
    global timer_job
    if timer_job is not None:
        root.after_cancel(timer_job)
        timer_job = None

def lock_choices():
    for button in choice_buttons:
        button.config(state="disabled")


def submit_answer():
    global score, answered
    if answered:
        return
    choice = selected_answer.get()
    if choice == "":
        messagebox.showwarning("No answer", "Please seect an answer first.")
        return

    answered = True
    stop_timer()
    lock_choices()
    submit_button.config(state="disabled")

    question = quiz_questions[currrent_question]
    if choice == question["answer"]:
        score += 1
        feedback_label.config(text="Correct!", fg=CORRECT_COLOR)
    else:
        wrong_answers.append({
            "question": question["question"],
            "your_answer": get_choice_text(question, choice),
            "correct_answer": get_choice_text(question, question["answer"])
        })
        feedback_label.config(
            text="Wrong! Correct answer: " 
                 + get_choice_text(question, question["answer"]), 
            fg=WRONG_COLOR)
    next_button.config(state="normal")

def time_up():
    global answered
    answered = True
    lock_choices()
    submit_button.config(state="disabled")

    question = quiz_questions[currrent_question]
    wrong_answers.append({
        "question": question["question"],
        "your_answer": "No answer (time is up)",
        "correct_answer": get_choice_text(question, question["answer"])
    })
    feedback_label.config(
        text="Time is up! Correct answer: " 
             + get_choice_text(question, question["answer"]),
        fg=WRONG_COLOR)
    next_button.config(state="normal")

def next_question():
    global currrent_question
    currrent_question += 1
    if currrent_question < len(quiz_questions):
        show_question()
    else:
        show_results()


def show_results():
    clear_screen()
    total = len(quiz_questions)
    percentage = (score / total) * 100
    new_record = save_high_score(score)

    if percentage >= 90:
        message = "Excellent Work!"
    elif percentage >= 70:
        message = "Good Job!"
    elif percentage >= 50:
        message = "Not bad. Keep practicing!"
    else:
        message = "Review the topic and try again."

    tk.Label(main_frame, text="Quiz Complete!", font=("Segoe UI", 26, "bold"),
             bg=BG_COLOR, fg=PRIMARY_COLOR).pack(pady=(10, 5))
    tk.Label(main_frame, text= f"Score: {score} / {total} ({percentage:.0f}%)",
             font=("Segoe UI", 18, "bold"), bg=BG_COLOR).pack()
    tk.Label(main_frame, text=message, font=("Segoe UI", 14),
             bg=BG_COLOR).pack(pady=3)

    record_text = "New high score!" if new_record else f"High Score: {get_high_score()} / {total}"
    tk.Label(main_frame, text=record_text, font=("Segoe UI", 13, "bold"),
             bg=BG_COLOR, fg=CORRECT_COLOR).pack(pady=3)

    tk.Label(main_frame, text="Answer Review (incorrect answers)",
             font=("Segoe UI", 13, "bold"), bg=BG_COLOR).pack(pady=(10,3), anchor="w")

    review_frame = tk.Frame(main_frame,bg=BG_COLOR)
    review_frame.pack(fill="both", expand=True)
    scrollbar = tk.Scrollbar(review_frame)
    scrollbar.pack(side="right", fill="y")
    review_box = tk.Text(review_frame, height=10, wrap="word",
                         font=("Segoe UI", 11), yscrollcommand=scrollbar.set)
    review_box.pack(side="left", fill="both", expand=True)
    scrollbar.config(command=review_box.yview)

    if not wrong_answers:
        review_box.insert("end", "Perfect! You answered every question correctly.")
    else:
        for number, item in enumerate(wrong_answers, start=1):
            review_box.insert("end", f"{number}. {item['question']}\n")
            review_box.insert("end", f"   Your answer: {item['your_answer']}\n")
            review_box.insert("end", f"   Correct answer: {item['correct_answer']}\n\n")
    review_box.config(state="disabled")

    button_frame = tk.Frame(main_frame, bg=BG_COLOR)
    button_frame.pack(pady=15)
    tk.Button(button_frame, text="Restart Quiz", font=("Segoe UI", 13, "bold"),
              bg=PRIMARY_COLOR, fg="white", width=15,
              command=restart_quiz).pack(side="left", padx=10)
    tk.Button(button_frame, text="Exit", font=("Segoe UI", 13, "bold"),
              width=15, command=on_close).pack(side="left", padx=10)


def restart_quiz():
    start_quiz()

def on_close():
    stop_timer()
    root.destroy()


root.protocol("WM_DELETE_WINDOW", on_close)
show_start_screen()
root.mainloop()