from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta

engine = create_engine('sqlite:///todo.db?check_same_thread=False')
Base = declarative_base()

Session = sessionmaker(bind=engine)


class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String, default='Nieokreślone Zadanie')
    deadline = Column(Date, default=datetime.today())

    def __init__(self,task, deadline):
        self.task = task
        self.deadline = deadline

    def __repr__(self):
        return self.task


Base.metadata.create_all(engine)


class ToDoList:

    def __init__(self):
        global Session
        self.session = Session()

    def __repr__(self):
        return f'I am a todo list'

    def query_all(self):
        return self.session.query(Table).all()

    def query_timed(self,task_day = datetime.today().date()):
        return self.session.query(Table).filter(Table.deadline == task_day).all()

    def query_earlier(self,task_day = datetime.today().date()):
        return self.session.query(Table).filter(Table.deadline < task_day).order_by(Table.deadline).all()

    def print_all(self,rows):
        for i, row in enumerate(rows):
            print(f"{i + 1}. {row}. {row.deadline.day} {row.deadline.strftime('%b')}")

    def display(self, filter_value=None):
        # Do think, if it shouldn`t be split to two funcs, one for query and one for printing

        weekdays = {0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday', 4: 'Friday', 5: 'Saturday', 6: 'Sunday'}
        task_day = datetime.today().date()

        # Tasks for today
        if filter_value == 0:
            print(f"Today {task_day.day} {task_day.strftime('%b')}")
            rows = self.query_timed(task_day)

            if rows:
                for i, row in enumerate(rows):
                    print(f'{i+1}) {row}')
            else:
                print('Nothing to do!')

        # Tasks for the week
        elif filter_value == 7:
            for i in range(filter_value):
                print(f'\n{weekdays[task_day.weekday()]} {task_day.day} {task_day.strftime("%b")}')

                rows = self.query_timed(task_day)
                if rows:
                    for j, row in enumerate(rows):
                        print(f'{j+1}) {row}')
                else:
                    print('Nothing to do!')

                task_day += timedelta(days=1)

        # Missed tasks
        elif filter_value == -1:
            rows = self.query_earlier()

            print('Missed tasks:')
            self.print_all(rows)

        # All tasks
        else:
            rows = self.query_all()
            if rows:
                self.print_all(rows)
            else:
                print('Nothing to do!')

        print('\n')

    def add_task(self):
        print('Enter task')
        task = input()
        print('Enter deadline')
        deadline = datetime.strptime(input(), '%Y-%m-%d').date()

        new_row = Table(task=task, deadline=deadline)
        self.session.add(new_row)
        self.session.commit()

    def delete_row(self,row):
        self.session.delete(row)
        self.session.commit()

    def delete_task(self):
        print('Choose the number of the task you want to delete:')

        rows= self.query_all()
        self.print_all(rows)

        selection = int(input())
        self.delete_row(rows[selection - 1])

        print('The task has been deleted!')


    def menu(self):
        run = True

        while run:
            print("""1) Today's tasks
2) Week's tasks
3) All tasks
4) Missed tasks
5) Add task
6) Delete task
0) Exit
                  """)
            option = input()

            if option == '1':
                self.display(0)
            elif option == '2':
                self.display(7)
            elif option == '3':
                self.display()
            elif option == '4':
                self.display(-1)
            elif option == '5':
                self.add_task()
            elif option == '6':
                self.delete_task()
            elif option == '0':
                run = False
            else:
                print('Unknown command')

if __name__ = '__main__':
    todo = ToDoList()
    todo.menu()

