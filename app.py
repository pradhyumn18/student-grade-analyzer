from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "secretkey"

students = []

class Student:
    def __init__(self, roll, name, math, science, english):
        self.roll = roll
        self.name = name
        self.__math = int(math)
        self.__science = int(science)
        self.__english = int(english)

    def total_marks(self):
        return self.__math + self.__science + self.__english

    def percentage(self):
        return round(self.total_marks() / 3, 2)

    def calculate_gpa(self):
        return round((self.percentage() / 100) * 10, 2)

    def result(self):
        if self.__math >= 35 and self.__science >= 35 and self.__english >= 35:
            return "Pass"
        else:
            return "Fail"

    def grade(self):
        percent = self.percentage()
        if percent >= 90:
            return "A+"
        elif percent >= 75:
            return "A"
        elif percent >= 60:
            return "B"
        elif percent >= 50:
            return "C"
        elif percent >= 35:
            return "D"
        else:
            return "Fail"

    def get_marks(self):
        return self.__math, self.__science, self.__english


@app.route('/', methods=['GET', 'POST'])
def index():
    search_query = request.args.get('search', '')

    if request.method == 'POST':
        roll = request.form['roll']
        name = request.form['name']
        math = int(request.form['math'])
        science = int(request.form['science'])
        english = int(request.form['english'])

        # VALIDATION
        if not (0 <= math <= 100 and 0 <= science <= 100 and 0 <= english <= 100):
            flash("Marks must be between 0 and 100 only!")
            return redirect(url_for('index'))

        student = Student(roll, name, math, science, english)
        students.append(student)
        return redirect(url_for('index'))

    filtered_students = [s for s in students if search_query.lower() in s.name.lower()]

    count = len(students)
    pass_count = len([s for s in students if s.result() == "Pass"])
    pass_percentage = round((pass_count / count) * 100, 2) if count > 0 else 0

    if count > 0:
        avg_math = round(sum(s.get_marks()[0] for s in students) / count, 2)
        avg_science = round(sum(s.get_marks()[1] for s in students) / count, 2)
        avg_english = round(sum(s.get_marks()[2] for s in students) / count, 2)
    else:
        avg_math = avg_science = avg_english = 0

    return render_template(
        'index.html',
        students=filtered_students,
        count=count,
        pass_percentage=pass_percentage,
        avg_math=avg_math,
        avg_science=avg_science,
        avg_english=avg_english
    )


@app.route('/delete/<int:index>')
def delete(index):
    if 0 <= index < len(students):
        students.pop(index)
    return redirect(url_for('index'))


@app.route('/clear')
def clear():
    students.clear()
    return redirect(url_for('index'))


@app.route('/edit/<int:index>', methods=['GET', 'POST'])
def edit(index):
    if request.method == 'POST':
        roll = request.form['roll']
        name = request.form['name']
        math = int(request.form['math'])
        science = int(request.form['science'])
        english = int(request.form['english'])

        if not (0 <= math <= 100 and 0 <= science <= 100 and 0 <= english <= 100):
            flash("Marks must be between 0 and 100 only!")
            return redirect(url_for('edit', index=index))

        students[index].roll = roll
        students[index].name = name
        students[index]._Student__math = math
        students[index]._Student__science = science
        students[index]._Student__english = english

        return redirect(url_for('index'))

    student = students[index]
    return render_template('edit.html', student=student, index=index)


if __name__ == '__main__':
    app.run(debug=True)