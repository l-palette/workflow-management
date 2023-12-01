from tkinter import *
import sqlite3
import tkinter.scrolledtext as tkst

t_name_editor = NONE
t_start_date_editor = NONE
t_type_editor = NONE
editor = NONE
var = NONE

#подключаемся к базе данных
conn = sqlite3.connect('db1.db')
c = conn.cursor()

#создаем таблицу projects(name,start_date,type)
c.execute("""CREATE TABLE IF NOT EXISTS projects (

        name text(20) not null,
        date date not null,
        id_type integer not null unique
         )""")

"""
CREATE TABLE IF NOT EXISTS documents (
  id_document INTEGER NOT NULL UNIQUE,
  document TEXT(20) NOT NULL,
  id_type INTEGER NOT NULL UNIQUE,
  date DATE NOT NULL,
  PRIMARY KEY (id_document),
  FOREIGN KEY (id_type) REFERENCES types (id_type)
);
"""

#создаем таблицу tasks(instruction,due_date,to_project)
c.execute("""CREATE TABLE IF NOT EXISTS tasks (
           instruction text,
           due_date real,
           to_project integer,
           id_employee integer not null unique
               )""")
"""
CREATE TABLE IF NOT EXISTS assignments (
  id_document INTEGER NOT NULL,
  id_assignment INTEGER NOT NULL,
  id_employee INTEGER NOT NULL,
  assignment TEXT(100) NOT NULL UNIQUE,
  date1 DATE NOT NULL,
  date2 DATE NOT NULL,
  PRIMARY KEY (id_document, id_assignment),
  FOREIGN KEY (id_document) REFERENCES documents (id_document),
  FOREIGN KEY (id_employee) REFERENCES employees (id_employee)
);
"""
class Page(Frame):
    def __init__(self, *args, **kwargs):
        Frame.__init__(self, *args, **kwargs)

    def show(self):
        self.lift()


#Projects page
class Page1(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)

        #поле для ввода
        #имя проэкта
        self.t_name = Entry(self, width=30)
        self.t_name.grid(row=0, column=1, padx=20, pady=(35, 0))

        #дата начала
        self.t_start_date = Entry(self, width=30)
        self.t_start_date.grid(row=1, column=1, padx=20)

        #тип проэкта
        self.t_type = Entry(self, width=30)
        self.t_type.grid(row=2, column=1, padx=20)

        self.delete_box = Entry(self, width=30)
        self.delete_box.grid(row=9, column=1, pady=5)

        #названия возле полей для ввода
        #имя
        self.t_name_lable = Label(self, text="Документ").grid(
            row=0, column=0, pady=(35, 0))

        #дата начала
        self.t_start_date_lable = Label(
            self, text="Дата").grid(row=1, column=0)

        #тип
        self.t_type_lable = Label(self, text="Тип").grid(row=2, column=0)
        #номер проэкта
        self.delete_box_lable = Label(self, text="ID документа").grid(
            row=9, column=0, pady=5)

        #создадим кнопки
        #добавить проект
        self.add_btn = Button(self, text="Добавить документ",
                              command=self.create_project)
        self.add_btn.grid(row=6, column=0, columnspan=2,
                          pady=10, padx=10, ipadx=139)

        #показать базу данных
        self.show_db_btn = Button(
            self, text="Список документов", command=self.query)
        self.show_db_btn.grid(row=13, column=0, columnspan=2,
                              pady=10, padx=10, ipadx=112)

        #удалить проект
        self.delete_btn = Button(self, text="Удалить документ ",
                                 command=self.remove_project)
        self.delete_btn.grid(row=10, column=0, columnspan=2,
                             pady=10, padx=10, ipadx=135)

        #обновить проект
        self.edit_btn = Button(self, text="Обновить документ",
                               command=self.update_project)
        self.edit_btn.grid(row=11, column=0, columnspan=2,
                           pady=10, padx=10, ipadx=133)

    #СОЗДАТЬ документ
    def create_project(self):
        conn = sqlite3.connect('db1.db')
        c = conn.cursor()
        #добавляем в табличку введенные name, start_date, type
        c.execute("INSERT INTO projects VALUES (:name, :start_date,:type)",
                  {

                      'name': self.t_name.get(),
                      'start_date': self.t_start_date.get(),
                      'type': self.t_type.get()

                  })

        conn.commit()
        conn.close()

        #очищаем поле ввода
        self.t_name.delete(0, END)
        self.t_start_date.delete(0, END)
        self.t_type.delete(0, END)

    #СПИСОК ДОКУМЕНТОВ
    def query(self):

        query = Tk()
        query.geometry("375x180")

        conn = sqlite3.connect('db1.db')
        c = conn.cursor()
        c.execute("SELECT *,oid  FROM projects")
        records = c.fetchall()

        print_records = ''
        for record in records:
            record = list(record)
            print_records += "Код документа: " + str(record[3]) + "\n"
            print_records += "Название: " + str(record[0]) + "\n"
            print_records += "Дата: " + str(record[1]) + "\n"
            print_records += "Тип: " + str(record[2]) + "\n"
            

        query_lable = Label(query, text=print_records)
        query_lable.grid(row=0, column=0, padx=95, pady=10)

        conn.commit()
        conn.close()

    #Удалить проект
    def remove_project(self):
        conn = sqlite3.connect('db1.db')
        c = conn.cursor()

        c.execute("DELETE from projects WHERE oid = ?", (self.delete_box.get(),))
        self.delete_box.delete(0, END)

        conn.commit()
        conn.close()

    #обновить проект
    def update_project(self):
        global t_name_editor
        global t_start_date_editor
        global t_type_editor
        global editor
        editor = Tk()
        editor.geometry("375x180")

        conn = sqlite3.connect('db1.db')

        c = conn.cursor()

        project_id = self.delete_box.get()
        c.execute("SELECT * FROM projects WHERE oid = ?", (project_id,))
        records = c.fetchall()

        #создать поля для ввода
        t_name_editor = Entry(editor, width=30)
        t_name_editor.grid(row=0, column=1, padx=20, pady=(10, 0))
        #
        t_start_date_editor = Entry(editor, width=30)
        t_start_date_editor.grid(row=1, column=1, padx=20)

        t_type_editor = Entry(editor, width=30)
        t_type_editor.grid(row=2, column=1, padx=20)

        #создать названия для полей для ввода

        t_name_lable_editor = Label(editor, text="Название документа").grid(
            row=0, column=0, pady=(10, 0))

        t_start_date_lable_editor = Label(
            editor, text="Дата").grid(row=1, column=0)

        t_type_lable_editor = Label(editor, text="Тип документа").grid(row=2, column=0)

        for record in records:
            t_name_editor.insert(0, record[0])
            t_start_date_editor.insert(0, record[1])
            t_type_editor.insert(0, record[2])

        #кнопка сохранить
        save_btn = Button(editor, text="Сохранить документ",
                          command=self.edit_project)
        save_btn.grid(row=4, column=0, columnspan=2,
                      pady=10, padx=10, ipadx=133)
    #редактирование
    def edit_project(self):
        conn = sqlite3.connect('db1.db')
        c = conn.cursor()

        project_id = self.delete_box.get()

        c.execute("""UPDATE projects SET
                name = :name,
                start_date = :start_date,
                type = :type
                WHERE oid = :oid""",
                  {
                      'name': t_name_editor.get(),
                      'start_date': t_start_date_editor.get(),
                      'type': t_type_editor.get(),
                      'oid': project_id
                  })

        conn.commit()
        conn.close()
        editor.destroy()


class Page2(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)

        conn = sqlite3.connect('db1.db')
        c = conn.cursor()
        c.execute("SELECT name FROM projects")
        list1 = c.fetchall()
        if not list1:
            list1.append("Здесь пока пусто")

        global var

        #создать поля для ввода текста
        self.t_instruction = tkst.ScrolledText(self, height=5, width=22)
        self.t_instruction.grid(row=0, column=1, padx=0, pady=(15, 0))

        self.t_due_date = Entry(self, width=32)
        self.t_due_date.grid(row=1, column=1, padx=20)

        self.delete_box = Entry(self, width=32)
        self.delete_box.grid(row=4, column=1, pady=5)

        self.employee = Entry(self, width=32)
        self.employee.grid(row=4, column=1, pady=5)

        var = StringVar()
        var.set("Документ")
        l = []
        for j in range(len(list1)):
            list1[j] = str(list1[j][0])
        self.which_project = OptionMenu(self,  var, *list1)
        self.which_project.grid(row=2, column=1, padx=20,)

        #Описание полей для ввода текста
        self.t_instruction_lable = Label(self, text="Поручение").grid(
            row=0, column=0, padx=20, pady=(15, 0))

        self.t_due_date_lable = Label(
            self, text="Дата окончания").grid(row=1, column=0, pady=10)

        self.t_which_project_lable = Label(
            self, text="Выбрать документ").grid(row=2, column=0, pady=10)

        self.delete_box_lable = Label(self, text="ID поручения").grid(
            row=4, column=0, pady=5)
        self.employee_lable = Label(self, text="ID сотрудника").grid(
            row=4, column=0, pady=5)

        #кнопки

        self.add_btn = Button(self, text="Добавить поручение",
                              command=self.add_task)
        self.add_btn.grid(row=3, column=0, columnspan=2,
                          pady=10, padx=10, ipadx=136)

        self.show_db_btn = Button(
            self, text="Показать список поручений", command=self.query2)
        self.show_db_btn.grid(row=6, column=0, columnspan=2,
                              pady=10, padx=10, ipadx=112)

        self.delete_btn = Button(self, text="Удалить поручение",
                                 command=self.remove_task)
        self.delete_btn.grid(row=5, column=0, columnspan=2,
                             pady=10, padx=10, ipadx=135)

        conn.commit()
        conn.close()

    def add_task(self):
        conn = sqlite3.connect('db1.db')
        c = conn.cursor()

        c.execute("INSERT INTO tasks VALUES (:instruction, :due_date,:to_project,:id_employee)",
                  {
                      'instruction': self.t_instruction.get(1.0, END),
                      'due_date': self.t_due_date.get(),
                      'to_project': var.get(),
                      'id_employee': self.employee.get()
                  })

        conn.commit()
        conn.close()

        self.t_instruction.delete(1.0, END)
        self.t_due_date.delete(0, END)
    #СПИСОК ПОРУЧЕНИЙ
    def query2(self):

        query2 = Tk()
        query2.geometry("375x180")

        conn = sqlite3.connect('db1.db')
        c = conn.cursor()
        c.execute("SELECT *,oid  FROM tasks")
        records = c.fetchall()

        print_records = ''
        for record in records:
            record = list(record)
            print_records += "Документ: " + str(record[2]) + "\n"
            print_records += "Код поручения: " + str(record[3]) + "\n"
            print_records += "Поручение: " + str(record[0]) 
            print_records += "Дата окончания: " + str(record[1]) + "\n"
            print_records += "Сотрудник: " + str(record[4]) + "\n\n"
            
        query_lable = Label(query2, text=print_records)
        query_lable.grid(row=0, column=0, padx=60, pady=10)

        conn.commit()
        conn.close()

    def remove_task(self):
        conn = sqlite3.connect('db1.db')
        c = conn.cursor()

        c.execute("DELETE from tasks WHERE oid = " + self.delete_box.get())
        self.delete_box.delete(0, END)

        conn.commit()
        conn.close()

class Page3(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)

        conn = sqlite3.connect('db1.db')
        c = conn.cursor()
        c.execute("SELECT name FROM projects")
        list1 = c.fetchall()
        if not list1:
            list1.append("Здесь пока пусто")

        global var

        #создать поля для ввода текста
        self.t_instruction = tkst.ScrolledText(self, height=5, width=22)
        self.t_instruction.grid(row=0, column=1, padx=0, pady=(15, 0))

        self.t_due_date = Entry(self, width=32)
        self.t_due_date.grid(row=1, column=1, padx=20)

        self.delete_box = Entry(self, width=32)
        self.delete_box.grid(row=4, column=1, pady=5)

        var = StringVar()
        var.set("Документ")
        l = []
        for j in range(len(list1)):
            list1[j] = str(list1[j][0])
        self.which_project = OptionMenu(self,  var, *list1)
        self.which_project.grid(row=2, column=1, padx=20,)

        #Описание полей для ввода текста
        self.t_instruction_lable = Label(self, text="Поручение").grid(
            row=0, column=0, padx=20, pady=(15, 0))

        self.t_due_date_lable = Label(
            self, text="Дата окончания").grid(row=1, column=0, pady=10)

        self.t_which_project_lable = Label(
            self, text="Выбрать документ").grid(row=2, column=0, pady=10)

        self.delete_box_lable = Label(self, text="ID поручения").grid(
            row=4, column=0, pady=5)

        #кнопки

        self.add_btn = Button(self, text="Добавить поручение",
                              command=self.add_task)
        self.add_btn.grid(row=3, column=0, columnspan=2,
                          pady=10, padx=10, ipadx=136)

        self.show_db_btn = Button(
            self, text="Показать список поручений", command=self.query2)
        self.show_db_btn.grid(row=6, column=0, columnspan=2,
                              pady=10, padx=10, ipadx=112)

        self.delete_btn = Button(self, text="Удалить поручение",
                                 command=self.remove_task)
        self.delete_btn.grid(row=5, column=0, columnspan=2,
                             pady=10, padx=10, ipadx=135)

        conn.commit()
        conn.close()

    def add_task(self):
        conn = sqlite3.connect('db1.db')
        c = conn.cursor()

        c.execute("INSERT INTO tasks VALUES (:instruction, :due_date,:to_project)",
                  {
                      'instruction': self.t_instruction.get(1.0, END),
                      'due_date': self.t_due_date.get(),
                      'to_project': var.get()
                  })

        conn.commit()
        conn.close()

        self.t_instruction.delete(1.0, END)
        self.t_due_date.delete(0, END)
    #СПИСОК ПОРУЧЕНИЙ
    def query2(self):

        query2 = Tk()
        query2.geometry("375x180")

        conn = sqlite3.connect('db1.db')
        c = conn.cursor()
        c.execute("SELECT *,oid  FROM tasks")
        records = c.fetchall()

        print_records = ''
        for record in records:
            record = list(record)
            print_records += "Документ: " + str(record[2]) + "\n"
            print_records += "Код поручения: " + str(record[3]) + "\n"
            print_records += "Поручение: " + str(record[0]) 
            print_records += "Дата окончания: " + str(record[1]) + "\n\n"
            
        query_lable = Label(query2, text=print_records)
        query_lable.grid(row=0, column=0, padx=60, pady=10)

        conn.commit()
        conn.close()

    def remove_task(self):
        conn = sqlite3.connect('db1.db')
        c = conn.cursor()

        c.execute("DELETE from tasks WHERE oid = " + self.delete_box.get())
        self.delete_box.delete(0, END)

        conn.commit()
        conn.close()


class MainView(Frame):
    def __init__(self, *args, **kwargs):
        Frame.__init__(self, *args, **kwargs)
        p1 = Page1(self)
        p2 = Page2(self)
        p3 = Page3(self)

        buttonframe = Frame(self)
        container = Frame(self)
        buttonframe.pack(side="top", fill="x", expand=False)
        container.pack(side="top", fill="both", expand=True)

        p1.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p2.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p3.place(in_=container, x=0, y=0, relwidth=1, relheight=1)

        b1 = Button(buttonframe, text="Документы", command=p1.lift)
        b2 = Button(buttonframe, text="Поручения", command=p2.lift)
        b3 = Button(buttonframe, text="Фильтры", command=p3.lift)

        b1.pack(side="left")
        b2.pack(side="left")
        b3.pack(side="left")

        p1.show()


if __name__ == "__main__":
    root = Tk()
    main = MainView(root)
    main.pack(side="top", fill="both", expand=True)
    root.wm_geometry("375x500")
    root.mainloop()

# commit changes
conn.commit()
# close connection
conn.close()
