# Import necessary libraries
from pyodide.http import open_url
from js import document, console

# Define the calculate_required_grades function
def calculate_required_grades(prelim_grade):
    # same implementation as your original function
    passing_grade = 75
    prelim_weight = 0.20
    midterm_weight = 0.30
    final_weight = 0.50
    grade_range = (0, 100)
    dean_lister_threshold = 90
    
    # Computation of prelim grade to 20%
    current_total = prelim_grade * prelim_weight
    # Calculation of grades required for midterm and finals
    required_total = passing_grade - current_total
    midterm_final_weight = midterm_weight + final_weight
    # Calculation of average grades required for midterm and finals
    min_required_average = required_total / midterm_final_weight
    # Calculation of required grades for Dean's Lister
    required_total_dean_lister = dean_lister_threshold - current_total
    min_required_average_dean_lister = required_total_dean_lister / midterm_final_weight

    # To make sure the grades entered is only between 0 and 100
    if not (grade_range[0] <= prelim_grade <= grade_range[1]):
        return "Error: Preliminary grade must be between 0 and 100."

    if min_required_average < grade_range[0]:
        min_required_average = grade_range[0]
    
    if min_required_average_dean_lister < grade_range[0]:
        min_required_average_dean_lister = grade_range[0]

    if prelim_grade < 70:
        return ("Prelim Grade: {:.2f}".format(prelim_grade),
                "Required Grade for Midterm: {:.2f}".format(min_required_average), 
                "Required Grade for Finals: {:.2f}".format(min_required_average), 
                "It is Difficult to Pass!", True,
                "It's impossible for you to be a Dean's Lister." if min_required_average_dean_lister > 100 else 
                "The Required Grade for you to be a Dean’s Lister is {:.2f} (Midterm) and {:.2f} (Finals).".format(min_required_average_dean_lister, min_required_average_dean_lister))

    else:
        return ("Prelim Grade: {:.2f}".format(prelim_grade),
                "Required Grade for Midterm: {:.2f}".format(min_required_average), 
                "Required Grade for Finals: {:.2f}".format(min_required_average), 
                "You Have a Chance to Pass!", False,
                "It's impossible for you to be a Dean's Lister." if min_required_average_dean_lister > 100 else 
                "The Required Grade for you to be a Dean’s Lister is {:.2f} (Midterm) and {:.2f} (Finals).".format(min_required_average_dean_lister, min_required_average_dean_lister))

# Define the main function
def main():
    # Get the input element
    input_element = document.getElementById("prelim_grade")
    
    # Add an event listener to the input element
    input_element.addEventListener("input", calculate_and_display_result)

def calculate_and_display_result(event):
    # Get the input value
    prelim_grade = float(event.target.value)
    
    # Calculate the result
    result = calculate_required_grades(prelim_grade)
    
    # Display the result
    if isinstance(result, tuple):
        prelim_grade_result, midterm_result, finals_result, message, pass_chance, dean_lister_message = result
        document.getElementById("result").innerHTML = """
            <h2>Result:</h2>
            <p>{}</p>
            <p>{}</p>
            <p>{}</p>
            <p>{}</p>
            <p>{}</p>
        """.format(prelim_grade_result, midterm_result, finals_result, message, dean_lister_message)
    else:
        document.getElementById("result").innerHTML = "<p style='color: red;'>{}</p>".format(result)

# Run the main function
main()