# 1:44
import sqlite3
from tkinter import *
from tkinter import ttk

conn = sqlite3.connect('time.db')
c = conn.cursor()
c.execute("Create table if not exists tblstudents (studid integer primary key, studname text, score integer)")
conn.commit()

window = Tk()
window.title("Student Records")


s= ttk.Style()
s.theme_use('clam')

def update_tree():
    for item in tree.get_children():
        tree.delete(item)
    c.execute("Select * from tblstudents")
    for row in c:
        tree.insert('', "end", values=(row[0], row[1], row[2]))


def add_rec():
    try:
        studid = int(studid_entry.get())
        studname = studname_entry.get()
        score = int(score_entry.get())
        c.execute("insert into tblstudents values (?,?,?)", (studid, studname, score,))
        conn.commit()
        update_tree()
        clear_entries()
        sum()
    except ValueError:
        print("Score must be an integer.")

def delete_rec():
    studid = int(studid_entry.get())
    c.execute("Select * from tblstudents where studid=?", (studid,))
    existing_record = c.fetchone()
    if existing_record:
        c.execute("Delete from tblstudents where studid=?", (studid,))
        conn.commit()
        update_tree()
        clear_entries()
        sum()
    else:
        print("No such Records")

def highest_lowest():
    c.execute("Select studname from tblstudents order by score desc limit 1")
    highest_result = c.fetchone()
    highest_name = highest_result[0] if highest_result else "N/A"
    highest_label.config(text="Highest Score: " + highest_name)

    c.execute("Select studname from tblstudents order by score asc limit 1")
    lowest_result = c.fetchone()
    lowest_name = lowest_result[0] if lowest_result else "N/A"
    lowest_label.config(text="Lowest Score: "+ lowest_name)


def clear_entries():
    studid_entry.delete(0, END)
    studname_entry.delete(0,END)
    score_entry.delete(0,END)

studid_label = Label(window, text="Student ID:")
studid_label.grid(row=0, column=0)
studid_entry = Entry(window, width=30)
studid_entry.grid(row=0, column=1)


studname_label = Label(window, text="Student Name:")
studname_label.grid(row=1, column=0)
studname_entry = Entry(window, width=30)
studname_entry.grid(row=1, column=1)

score_label = Label(window, text="Score:")
score_label.grid(row=2, column=0)
score_entry = Entry(window, width=30)
score_entry.grid(row=2, column=1)

add_button = Button(window, text="Add Record", command=add_rec)
add_button.grid(row=3, column=0)

delete_button = Button(window, text="Delete Record", command=delete_rec)
delete_button.grid(row=3, column=1)

highest_label = Label(window, text="Highest Score:")
highest_label.grid(row=4, column=0)

lowest_label = Label(window, text="Lowest Score:")
lowest_label.grid(row=5, column=0)

sum_score = Label(window, text="Total: ")
sum_score.grid(row=8,column=0)

def sum():
    c.execute("select sum(score) from tblstudents")
    sum_result = c.fetchone()
    sum_score_result = sum_result[0] if sum_result else "N/A"
    sum_score.config(text="Total: " + str(sum_score_result))



tree = ttk.Treeview(window, columns = ("c1", "c2", "c3"), show='headings', height=5)
tree.column("#1", anchor=CENTER)
tree.heading("#1", text="Student ID")
tree.column("#2", anchor=CENTER)
tree.heading("#2", text="Student Name")
tree.column("#3", anchor=CENTER)
tree.heading("#3", text="Score")

tree.grid(row=10, column=0, columnspan=2)
update_tree()
highest_lowest()
sum()

window.mainloop()
conn.close()
