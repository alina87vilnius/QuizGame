import requests
from html import unescape
from tkinter import *
from tkinter import ttk


GREEN = '#216954'
BG_COLOR = '#faf6e9'
QUESTION_COLOR = '#fffdf6'
FONT_COLOR = '#333333'
FONT = 'Verdana'
LOGO = 'logo.png'

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
    global category, difficulty
    category = combobox.get()
    difficulty = dif_var.get()
    dialog.destroy()


def get_question_base(category, difficulty):
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
    button.config(text='Check', command=check_answer)
    true.config(state=NORMAL)
    false.config(state=NORMAL)
    next_question = unescape(question_base[question_num]['question'])
    question_field.delete(1.0, END)
    question_field.insert(1.0, next_question)


def check_answer():
    global question_num
    correct_answer = question_base[question_num]['correct_answer']
    user_answer = answer.get()
    question_field.insert(END, "\n**********\n")
    if user_answer == correct_answer:
        question_field.insert(END, "You got it right!\n")
    else:
        question_field.insert(END, "That's wrong...\n")
    question_field.insert(END, f"The correct answer was: {correct_answer}.")
    button.config(text='Next question', command=ask_question)
    true.config(state=DISABLED)
    false.config(state=DISABLED)
    question_num += 1
    # if question_num == len(question_base):
    #     end_quiz()


# Dialog window. Selection of category and difficulty
dialog = Tk()
dialog.geometry('+350+250')
dialog.resizable(width=False, height=False)
dialog.title('QuizGame settings')
dialog.iconbitmap('ico.ico')

main_frame = Frame(dialog, padx=20, pady=10, bg=BG_COLOR)
main_frame.grid(row=0, column=0)

logo_image = PhotoImage(file=LOGO).subsample(2)
logo = Label(main_frame, image=logo_image, bg=BG_COLOR)
logo.grid(row=0, column=0, columnspan=3, pady=10)

label_category = Label(main_frame, text='Select category:', anchor="w")
label_category.config(font=(FONT, 10, 'normal'), bg=BG_COLOR, fg=FONT_COLOR)
label_category.grid(row=1, column=0, pady=10)

category = StringVar()
combobox = ttk.Combobox(main_frame, values=[key for key in CATEGORIES.keys()])
combobox.current(0)
combobox.config(font=(FONT, 10, 'normal'))
combobox.grid(row=1, column=1, columnspan=2, pady=10)

label_difficulty = Label(main_frame, text='Select difficulty:', anchor="w")
label_difficulty.config(font=(FONT, 10, 'normal'), bg=BG_COLOR, fg=FONT_COLOR)
label_difficulty.grid(row=2, column=0, pady=10)

difficulty = ''
dif_var = StringVar(value='easy')
easy = Radiobutton(main_frame, text='Easy', var=dif_var, value='easy')
easy.config(font=(FONT, 10, 'normal'), bg=BG_COLOR, fg=FONT_COLOR)
easy.config(activebackground=BG_COLOR)
easy.grid(row=2, column=1, pady=10)
medium = Radiobutton(main_frame, text='Not so easy', var=dif_var, value='medium')
medium.config(font=(FONT, 10, 'normal'), bg=BG_COLOR, fg=FONT_COLOR)
medium.config(activebackground=BG_COLOR)
medium.grid(row=2, column=2, pady=10)

button = Button(main_frame, text='OK', width=10, command=select)
button.config(font=(FONT, 10, 'bold'), bg=GREEN, fg=BG_COLOR)
button.config(bd=3, activebackground=BG_COLOR, activeforeground=FONT_COLOR)
button.grid(row=3, column=1, pady=10)

dialog.mainloop()

# Game window
root = Tk()
root.geometry('+350+250')
root.title('QuizGame')
root.iconbitmap('ico.ico')

main_frame = Frame(root, padx=40, pady=20, bg=BG_COLOR)
main_frame.grid(row=0, column=0)

logo_image = PhotoImage(file='logo.png')
logo = Label(main_frame, image=logo_image, bg=BG_COLOR)
logo.grid(row=0, column=0, columnspan=4, pady=30)

question_field = Text(main_frame, width=40, height=10, wrap=WORD)
question_field.config(font=(FONT, 10, 'normal'), bg=QUESTION_COLOR, fg=FONT_COLOR)
question_field.config(relief='flat', highlightthickness=3, borderwidth=6)
question_field.config(highlightbackground=GREEN, highlightcolor=GREEN)
question_field.grid(row=1, column=0, columnspan=4)

answer = StringVar(value='True')
true = Radiobutton(main_frame, text='True', variable=answer, value='True')
true.config(font=(FONT, 10, 'normal'), bg=BG_COLOR, fg=FONT_COLOR)
true.config(activebackground=BG_COLOR)
true.grid(row=2, column=0, columnspan=2, pady=10)
false = Radiobutton(main_frame, text='False', variable=answer, value='False')
false.config(font=(FONT, 10, 'normal'), bg=BG_COLOR, fg=FONT_COLOR)
false.config(activebackground=BG_COLOR)
false.grid(row=2, column=2, columnspan=2, pady=10)

button = Button(main_frame, text='Check', width=15, command=check_answer)
button.config(font=(FONT, 10, 'bold'), bg=GREEN, fg=BG_COLOR)
button.config(bd=3, activebackground=BG_COLOR, activeforeground=FONT_COLOR)
button.grid(row=3, column=1, columnspan=2, pady=10)

question_base = get_question_base(category, difficulty)
question_num = 0
ask_question()

root.mainloop()
