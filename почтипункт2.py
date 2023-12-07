from tkinter import *
import sqlite3
import tkinter.scrolledtext as tkst
t_document_editor = NONE
t_date_editor = NONE
t_type_editor = NONE
editor = NONE
var = NONE
conn = sqlite3.connect('db7.db')
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS departments(id_department INTEGER NOT NULL, department TEXT(20) NOT NULL,PRIMARY KEY (id_department));")
c.execute("CREATE TABLE IF NOT EXISTS employees(id_employee INTEGER NOT NULL, employee TEXT(30) NOT NULL,id_department INTEGER NOT NULL,PRIMARY KEY (id_employee),FOREIGN KEY (id_department) REFERENCES departments (id_department));")
c.execute("CREATE TABLE IF NOT EXISTS documents(document TEXT(20) NOT NULL,type TEXT NOT NULL ,date REAL NOT NULL,PRIMARY KEY(document));")
c.execute("CREATE TABLE IF NOT EXISTS types(id_type INTEGER NOT NULL,type TEXT(20) NOT NULL,PRIMARY KEY (id_type));")
c.execute("CREATE TABLE IF NOT EXISTS assignments (to_document INTEGER,id_employee INTEGER NOT NULL,assignment TEXT(100) NOT NULL ,date1 REAL NOT NULL,date2 REAL NOT NULL,FOREIGN KEY(id_employee) REFERENCES employees (id_employee));")

c.execute("INSERT INTO departments(id_department, department) SELECT * FROM (VALUES (1, 'Маркетинг'), (2, 'Финансы'), (3, 'Кадры'), (4, 'Продаж'), (5, 'IT'), (6, 'Снабжение'), (7, 'Безопасность'), (8, 'Поддержка')) AS new_departments WHERE NOT EXISTS (SELECT 1 FROM departments WHERE id_department = new_departments.column1)")
c.execute("INSERT INTO types(id_type, type) SELECT * FROM (VALUES (1, 'Протокол'), (2, 'Приказ'), (3, 'Заявление'), (4, 'Письмо'), (5, 'Указ'), (6, 'Распоряжение'), (7, 'Служебная записка'), (8, 'План')) AS new_types WHERE NOT EXISTS (SELECT 1 FROM types WHERE id_type = new_types.column1)")
conn.commit()
conn.close()
class Page(Frame):
    def __init__(self, *args, **kwargs):
        Frame.__init__(self, *args, **kwargs)
    def show(self):
        self.lift()
        
        
class Page1_Documents(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        conn = sqlite3.connect('db7.db')
        c = conn.cursor()
        self.t_document = Entry(self, width=30)
        self.t_document.grid(row=0, column=1, padx=20, pady=(35, 0))

        self.t_date = Entry(self, width=30)
        self.t_date.grid(row=1, column=1, padx=20)

        self.t_document_lable = Label(self, text="Документ").grid(row=0, column=0, pady=(35, 0))
        self.t_date_lable = Label(self, text="Дата").grid(row=1, column=0)
        self.t_type_lable = Label(self, text="Тип").grid(row=2, column=0, pady=10)

        self.add_btn = Button(self, text="Добавить документ", command=self.create_document)
        self.add_btn.grid(row=6, column=0, columnspan=2, pady=10, padx=10, ipadx=150)
        
        self.show_db_btn = Button(self, text="Список документов", command=self.query)
        self.show_db_btn.grid(row=13, column=0, columnspan=2, pady=10, padx=10, ipadx=150)

        list1 = ['Протокол','Приказ','Заявление','Письмо','Указ','Распоряжение','Служебная записка','План']
        global var
        var = StringVar()
        var.set("Тип")
        l = []
        for j in range(len(list1)):
            list1[j] = str(list1[j])
            
        self.t_type = OptionMenu(self, var, *list1)
        self.t_type.grid(row=2, column=1, padx=20,)
    def create_document(self):
        conn = sqlite3.connect('db7.db',timeout=1)
        c = conn.cursor()
        c.execute("INSERT INTO documents VALUES (:document, :type, :date)",
                  {
                      'document': self.t_document.get(),
                      'type': var.get(),
                      'date': self.t_date.get()
                      
                  })
        conn.commit()
        conn.close()

        self.t_document.delete(0, END)
        self.t_date.delete(0, END)
    
    
    def query(self):
        from tkinter import ttk
        global query
        global t_search_label
        global t_search
        query = Tk()
        query.geometry("375x300")

        conn = sqlite3.connect('db7.db')
        c = conn.cursor()
        c.execute("SELECT *, oid FROM documents")
        records = c.fetchall()
        tree = ttk.Treeview(query)
        tree["columns"] = ("Название", "Тип", "Дата")
        tree.heading("#0", text="Код")
        tree.heading("Название", text="Название")
        tree.heading("Тип", text="Тип")
        tree.heading("Дата", text="Дата")
        tree.column("Название", width=150)
        tree.column("#0", width=40)
        tree.column("Тип", width=150)
        tree.column("Дата", width=80)
        for record in records:
            tree.insert("", "end", text=record[3], values=(record[0], record[1], record[2]))

        tree.grid(row=2, column=0, padx=10, pady=10)
       

        t_search_label = Entry(query, width=30)
        t_search_label.grid(row=0, column=0, padx = 20, pady=(10, 0))

        t_search = Button(query, text="Поиск", command=lambda: search(self))
        t_search.grid(row=1,column=0,columnspan=1,pady=0, padx=0, ipadx=10)
        
        conn.commit()
        conn.close()
        
        def search(self):
            from tkinter import ttk
            conn = sqlite3.connect('db7.db')
            c = conn.cursor()
            search_query = t_search_label.get()
            tree.delete(*tree.get_children())
            columns = ['document','type','date']
            search_query = [f"%{search_query}%"]*len(columns)
            if_query =  " LIKE ? OR ".join(columns) + " LIKE ?"
            q = f"SELECT * FROM documents WHERE {if_query}"

            c.execute(q, (*search_query,))
            records = c.fetchall()
            print(records)
            for record in records:
                tree.insert("", "end", text=record[0], values=(record[0], record[1], record[2]))
            conn.commit()
            conn.close()

        
        


class MainView(Frame):
    def __init__(self, *args, **kwargs):
        Frame.__init__(self, *args, **kwargs)
        p1 = Page1_Documents(self)

        buttonframe = Frame(self)
        container = Frame(self)
        buttonframe.pack(side="top", fill="x", expand=False)
        container.pack(side="top", fill="both", expand=True)

        p1.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        #p2.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        #p3.place(in_=container, x=0, y=0, relwidth=1, relheight=1)

        b1 = Button(buttonframe, text="Документы", command=p1.lift)
        #b2 = Button(buttonframe, text="Поручения", command=p2.lift)
        #b3 = Button(buttonframe, text="Фильтры", command=p3.lift)

        b1.pack(side="left")
        #b2.pack(side="left")
        #b3.pack(side="left")

        p1.show()


if __name__ == "__main__":
    root = Tk()
    main = MainView(root)
    main.pack(side="top", fill="both", expand=True)
    root.wm_geometry("500x500")
    root.mainloop()
conn.commit()
conn.close()
