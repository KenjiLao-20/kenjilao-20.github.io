from flask import Flask, render_template, request

app = Flask(__name__)

def calculate_required_grades(prelim_grade):
    passing_grade = 75
    prelim_weight = 0.20
    midterm_weight = 0.30
    final_weight = 0.50
    grade_range = (0, 100)
    dean_lister_threshold = 90
    
#Computation of prelim grade to 20%
    current_total = prelim_grade * prelim_weight
#Calculation of grades required for midterm and finals
    required_total = passing_grade - current_total
    midterm_final_weight = midterm_weight + final_weight
#Calculation of average grades required for midterm and finals
    min_required_average = required_total / midterm_final_weight
#Calculation of required grades for Dean's Lister
    required_total_dean_lister = dean_lister_threshold - current_total
    min_required_average_dean_lister = required_total_dean_lister / midterm_final_weight

#To make sure the grades entered is only between 0 and 100
    if not (grade_range[0] <= prelim_grade <= grade_range[1]):
        return "Error: Preliminary grade must be between 0 and 100."

    if min_required_average < grade_range[0]:
        min_required_average = grade_range[0]
    
    if min_required_average_dean_lister < grade_range[0]:
        min_required_average_dean_lister = grade_range[0]

    if prelim_grade < 70:
        return ("Required Grade for Midterm and Finals to Pass: {:.2f}".format(min_required_average), 
                "It is Difficult to Pass!", True,
                "It's impossible for you to be a Dean's Lister." if min_required_average_dean_lister > 100 else 
                "The Required Grade for you to be a Dean’s Lister is {:.2f} (Midterm) and {:.2f} (Finals).".format(min_required_average_dean_lister, min_required_average_dean_lister))

    else:
        return ("Required Grade for Midterm and Finals to Pass: {:.2f}".format(min_required_average),
                "You Have a Chance to Pass!", False,
                "It's impossible for you to be a Dean's Lister." if min_required_average_dean_lister > 100 else 
                "The Required Grade for you to be a Dean’s Lister is {:.2f} (Midterm) and {:.2f} (Finals).".format(min_required_average_dean_lister, min_required_average_dean_lister))

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    message = None
    pass_chance = None
    dean_lister_message = None
    if request.method == 'POST':
        prelim_grade = float(request.form['prelim_grade'])
        result = calculate_required_grades(prelim_grade)
        if isinstance(result, tuple):
            result, message, pass_chance, dean_lister_message = result
    return render_template('index.html', result=result, message=message, pass_chance=pass_chance, dean_lister_message=dean_lister_message)

if __name__ == '__main__':
    app.run(debug=True)