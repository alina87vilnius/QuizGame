import requests
import tkinter as tk
from tkinter import ttk
from html import unescape



GREEN = '#5eaaa8'
ORANGE = '#eb5e0b'
BG_COLOR = '#deeded'
QUESTION_COLOR = '#eef7f5'
FONT_COLOR = '#2f2519'
FONT = 'Verdana'
LOGO = 'new_logo.png'
ICO = 'new_ico.ico'

URL = 'https://opentdb.com/api.php?'
AMOUNT = 10
CATEGORIES = {
    'General Knowledge': 9,
    'Music': 12,
    'Video Games': 15,
    'Computers': 18,
    'Science & Nature': 17
}
DIFFICULTY = ['easy', 'medium']
TYPE = 'boolean'


def select():
    """Saves selected category and difficulty"""
    global category, difficulty
    category = combobox.get()
    difficulty = dif_var.get()
    dialog.destroy()


def get_question_base(category, difficulty):
    """Gets questions from API
     Creates a base of questions
     """
    parameters = {
        'amount': AMOUNT,
        'category': CATEGORIES[category],
        'difficulty': difficulty,
        'type': TYPE
    }
    response = requests.get(URL, parameters)
    question_json = response.json()
    return question_json['results']


def ask_question():
    """Updates score_label
    Configures button to 'Check'
    Enables true/false radiobuttons
    Shows a question
    """
    number_label.config(text=f'#{question_num+1}')
    button.config(text='Check', command=check_answer)
    true.config(state=tk.NORMAL)
    false.config(state=tk.NORMAL)
    next_question = unescape(question_base[question_num]['question'])
    question_field.delete(1.0, tk.END)
    question_field.insert(1.0, next_question)


def check_answer():
    """Configures button to 'Next question'
    Disables true/false radiobuttons
    Compares user answer with correct one
    Shows the result to the user
    Updates score variable if answer was correct
    Calls end_quiz() if there are no more questions
    """
    global question_num, score
    button.config(text='Next question', command=ask_question)
    true.config(state=tk.DISABLED)
    false.config(state=tk.DISABLED)
    correct_answer = question_base[question_num]['correct_answer']
    user_answer = answer.get()
    question_field.insert(tk.END, "\n**********\n")
    if user_answer == correct_answer:
        question_field.insert(tk.END, "You got it right!\n")
        score += 1
        score_label.config(text=f'Score: {score}')
    else:
        question_field.insert(tk.END, "That's wrong...\n")
    question_field.insert(tk.END, f"The correct answer was: {correct_answer}.")
    question_num += 1
    if question_num == len(question_base):
        end_quiz()


def end_quiz():
    """Configures button to 'Exit'
    Shows final score
    """
    button.config(text='Exit', command=root.destroy)
    question_field.insert(tk.END, "\n**********\nYou've done it!\n")
    question_field.insert(tk.END, f"Your final score is {score}/{len(question_base)}")


# Dialog window. Selection of category and difficulty
dialog = tk.Tk()
dialog.geometry('+350+250')
dialog.resizable(width=False, height=False)
dialog.title('QuizGame settings')
dialog.iconbitmap(ICO)

main_frame = tk.Frame(dialog, padx=20, pady=10, bg=BG_COLOR)
main_frame.grid(row=0, column=0)

logo_image = tk.PhotoImage(file=LOGO).subsample(2)
logo = tk.Label(main_frame, image=logo_image, bg=BG_COLOR)
logo.grid(row=0, column=0, columnspan=3, pady=10)

label_category = tk.Label(main_frame, text='Select category:', anchor="w")
label_category.config(font=(FONT, 10, 'normal'), bg=BG_COLOR, fg=FONT_COLOR)
label_category.grid(row=1, column=0, pady=10)

category = tk.StringVar()
combobox = ttk.Combobox(main_frame, values=[key for key in CATEGORIES.keys()])
combobox.current(0)
combobox.config(font=(FONT, 10, 'normal'))
combobox.grid(row=1, column=1, columnspan=2, pady=10)

label_difficulty = tk.Label(main_frame, text='Select difficulty:', anchor="w")
label_difficulty.config(font=(FONT, 10, 'normal'), bg=BG_COLOR, fg=FONT_COLOR)
label_difficulty.grid(row=2, column=0, pady=10)

difficulty = ''
dif_var = tk.StringVar(value='easy')
easy = tk.Radiobutton(main_frame, text='Easy', var=dif_var, value='easy')
easy.config(font=(FONT, 10, 'normal'), bg=BG_COLOR, fg=FONT_COLOR)
easy.config(activebackground=BG_COLOR)
easy.grid(row=2, column=1, pady=10)
medium = tk.Radiobutton(main_frame, text='Not so easy', var=dif_var, value='medium')
medium.config(font=(FONT, 10, 'normal'), bg=BG_COLOR, fg=FONT_COLOR)
medium.config(activebackground=BG_COLOR)
medium.grid(row=2, column=2, pady=10)

button = tk.Button(main_frame, text='OK', width=10, command=select)
button.config(font=(FONT, 10, 'bold'), bg=ORANGE, fg=QUESTION_COLOR)
button.config(bd=3, activebackground=BG_COLOR, activeforeground=FONT_COLOR)
button.grid(row=3, column=1, pady=10)

dialog.mainloop()

# Game window
root = tk.Tk()
root.geometry('+350+250')
root.title('QuizGame')
root.iconbitmap(ICO)

main_frame = tk.Frame(root, padx=40, pady=20, bg=BG_COLOR)
main_frame.grid(row=0, column=0)

logo_image = tk.PhotoImage(file=LOGO)
logo = tk.Label(main_frame, image=logo_image, bg=BG_COLOR)
logo.grid(row=0, column=0, columnspan=4, pady=30)

question_num = 0
number_label = tk.Label(main_frame, text=f'#{question_num+1}', width=4)
number_label.config(font=(FONT, 10, 'bold'), bg=GREEN, fg=QUESTION_COLOR)
number_label.grid(row=1, column=0, sticky=tk.W, padx=12)

score = 0
score_label = tk.Label(main_frame, text=f'Score: {score}', width=16)
score_label.config(font=(FONT, 10, 'bold'), bg=GREEN, fg=QUESTION_COLOR)
score_label.grid(row=1, column=2, columnspan=2, padx=16)

question_field = tk.Text(main_frame, width=40, height=10, wrap=tk.WORD)
question_field.config(font=(FONT, 10, 'normal'), bg=QUESTION_COLOR, fg=FONT_COLOR)
question_field.config(relief='flat', highlightthickness=3, borderwidth=6)
question_field.config(highlightbackground=GREEN, highlightcolor=GREEN)
question_field.grid(row=2, column=0, columnspan=4)

answer = tk.StringVar(value='True')
true = tk.Radiobutton(main_frame, text='True', variable=answer, value='True')
true.config(font=(FONT, 10, 'normal'), bg=BG_COLOR, fg=FONT_COLOR)
true.config(activebackground=BG_COLOR)
true.grid(row=3, column=0, columnspan=2, pady=10)
false = tk.Radiobutton(main_frame, text='False', variable=answer, value='False')
false.config(font=(FONT, 10, 'normal'), bg=BG_COLOR, fg=FONT_COLOR)
false.config(activebackground=BG_COLOR)
false.grid(row=3, column=2, columnspan=2, pady=10)

button = tk.Button(main_frame, text='Check', width=15, command=check_answer)
button.config(font=(FONT, 10, 'bold'), bg=ORANGE, fg=QUESTION_COLOR)
button.config(bd=3, activebackground=BG_COLOR, activeforeground=FONT_COLOR)
button.grid(row=4, column=1, columnspan=2, pady=10)

question_base = get_question_base(category, difficulty)
ask_question()

root.mainloop()
