import math
import random
import tkinter as tk
import pandas as pd

from solver import solver_result
from tabo_search import tabu_search_result
from simulated_annealing import sa_result
from genetic import genetic_result

random.seed(21)


def mark_choosen_days(choosen_days, calendar_days_labels):
    for day in choosen_days:
        calendar_days_labels[day-1].config(bg='limegreen')


def clear_calendar(calendar_days_labels):
    for label in calendar_days_labels:
        label.config(bg='white')


def display_objective_score(objective_score):
    objective_score_label.config(text=f'F = {objective_score:.3f}')


def fix_leap_day(leap_year):
    if leap_year:
        day_text = '29'
    else:
        day_text = ''

    blank_day = tk.Label(months_frames[1], text=day_text, bd=6, bg='white')
    blank_day.grid(row=4, column=0, sticky=tk.W)


def solve():
    ldm = []
    d = 1

    data_path = data_path_entry.get()
    dec_var_df = pd.read_csv(data_path)
    var_B_entry = dev_var_entries[decision_variables_names.index('B')]

    B = int(var_B_entry.get())
    P = dec_var_df['P'].tolist()

    method = METHOD_SELECTION.get()
    leap_year = LEAP_YEAR.get()

    fix_leap_day(leap_year)

    if method == 1:
        OBJECTIVE_SCORE, SOLUTION_DAYS = solver_result(P, B, ldm, d, leap_year=leap_year)  # noqa: E501
    elif method == 2:
        OBJECTIVE_SCORE, SOLUTION_DAYS = tabu_search_result(P, B, ldm, d, leap_year=leap_year)  # noqa: E501
    elif method == 3:
        OBJECTIVE_SCORE, SOLUTION_DAYS = sa_result(P, B, ldm, d, leap_year=leap_year)  # noqa: E501
    elif method == 4:
        OBJECTIVE_SCORE, SOLUTION_DAYS = genetic_result(P, B, ldm, d, leap_year=leap_year)  # noqa: E501

    clear_calendar(calendar_days_labels)
    mark_choosen_days(SOLUTION_DAYS, calendar_days_labels)
    display_objective_score(OBJECTIVE_SCORE)


if __name__ == "__main__":
    MONTH_NAMES = ["January", "February", "March", "April", "May", "June",
                   "July", "August", "September", "October", "November",
                   "December"]
    decision_variables_names = ['B']
    methods_names = ['Solver', 'Tabu search', 'Simulated annealing', 'Genetic']
    method_selection_values = [1, 2, 3, 4]

    root = tk.Tk()
    root.geometry('1100x470')
    root.resizable(False, False)

    # ===================== C A L E N D A R =====================

    calendar_frame = tk.Frame(root, bg='white', width=500, height=400)
    calendar_frame.place(relx=0.2, rely=0.04)

    months_frames = []
    for i in range(1, 13):
        x = math.ceil(i/4)

        if i <= 4:
            y = i - 1
        else:
            y = i - ((x-1)*4) - 1

        imonth_frame = tk.Frame(calendar_frame, width=80, height=60,
                                bg='white', bd=10)
        imonth_frame.grid(row=x, column=y)
        months_frames.append(imonth_frame)

    calendar_days_labels = []

    _ldm = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    for ld, month_frame in zip(_ldm, months_frames):
        for i in range(1, ld+1):
            x = math.ceil(i/7)

            if i <= 7:
                y = i - 1
            else:
                y = i - ((x-1)*7) - 1

            day_label = tk.Label(month_frame, text=i, bd=6, bg='white')
            day_label.grid(row=x-1, column=y, sticky=tk.W)
            calendar_days_labels.append(day_label)

            if ld == 28:
                blank_day = tk.Label(month_frame, text='', bd=6, bg='white')
                blank_day.grid(row=4, column=0, sticky=tk.W)

    r, c = 0, 0
    for month_name in MONTH_NAMES:
        if r != 0 and r % 4 == 0:
            r = 0
            c += 1

        gap = math.ceil((9 - len(month_name)) / 2)

        label_text = ' '*gap + month_name + ' '*gap
        month_label = tk.Label(calendar_frame, text=label_text, bg='white',
                               font=('Roboto', 10, 'bold'))
        month_label.place(relx=0.09+r*0.25, rely=c*0.33)

        r += 1

    # ================= D E C I S I O N - V A R I A B L E S ===================

    var_section_title = tk.Label(root, text='Decision variables',
                                 font=('Roboto', 11, 'bold'))
    var_section_title.place(relx=0.02, rely=0.05)

    dec_var_labels = []
    dev_var_entries = []
    for name in decision_variables_names:
        _label = tk.Label(root, text=f'{name}:', anchor=tk.W, width=10)
        _entry = tk.Entry(root, width=5)
        dec_var_labels.append(_label)
        dev_var_entries.append(_entry)

    for i, (label, entry) in enumerate(zip(dec_var_labels, dev_var_entries)):
        label.place(relx=0.053, rely=0.1+i*0.05)
        entry.place(relx=0.07, rely=0.1+i*0.05)

    data_path_entry = tk.Entry(root, width=18)
    data_path_label = tk.Label(root, text='Data path:', anchor=tk.W,
                               width=10)
    data_path_entry.place(relx=0.07, rely=0.15)
    data_path_label.place(relx=0.002, rely=0.15)

    _B_entry = dev_var_entries[decision_variables_names.index('B')]
    _B_entry.insert(tk.END, '40')

    data_path_entry.insert(tk.END, 'dec_variables.csv')

    # =================== S O L V E R - C O N T R O L L E R ===================

    METHOD_SELECTION = tk.IntVar()
    LEAP_YEAR = tk.IntVar()

    leap_year_sel_title = tk.Label(root, text='Leap year:',
                                   font=('Roboto', 11, 'bold'))
    leap_year_sel_title.place(relx=0.01, rely=0.25)

    selection_title = tk.Label(root, text='Optimization method:',
                               font=('Roboto', 11, 'bold'))
    selection_title.place(relx=0.01, rely=0.45)

    solve_button = tk.Button(root, text='Solve', command=solve, bg='limegreen',
                             activebackground='green')
    solve_button.place(relx=0.07, rely=0.75)

    objective_score_label = tk.Label(root, text='F = ?')
    objective_score_label.place(relx=0.07, rely=0.86)

    method_selection_buttons = []
    for name, val in zip(methods_names, method_selection_values):
        _radio_button = tk.Radiobutton(root, text=name, value=val,
                                       variable=METHOD_SELECTION)
        if name == 'Solver':
            _radio_button.select()
        method_selection_buttons.append(_radio_button)

    for i, button in enumerate(method_selection_buttons):
        button.place(relx=0.02, rely=0.5+i*0.05)

    leapy_true_butt = tk.Radiobutton(root, text='True', value=True,
                                     variable=LEAP_YEAR)
    leapy_false_butt = tk.Radiobutton(root, text='False', value=False,
                                      variable=LEAP_YEAR)
    leapy_false_butt.select()
    leapy_true_butt.place(relx=0.02, rely=0.3)
    leapy_false_butt.place(relx=0.02, rely=0.35)

    root.mainloop()
