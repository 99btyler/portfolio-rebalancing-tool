import sys


def input_as(type, prompt):
    while True:
        # - make sure input is of type
        try:
            if type == "int":
                the_input = int(input(prompt))
            elif type == "float":
                the_input = float(input(prompt))
        except ValueError:
            continue
        # - make sure input is valid
        if the_input > 0:
            break
    return the_input


amount_of_sections = input_as("int", "Enter amount of sections: ")
print(f"Heard! Dealing with {amount_of_sections} sections\n")

sections = {}
total_value = 0
total_percent = 0
for i in range(amount_of_sections):
    section = input("Enter name of section: ")
    section_value = input_as("float", "Enter section's value: ")
    total_value += section_value
    section_desiredpercent = input_as("int", "Enter section's desired percent: ")
    total_percent += section_desiredpercent
    sections[section] = [section_value, section_desiredpercent]
if total_percent < 100:
    sys.exit("\nERROR! total_percent didn't add to 100")
print(f"Heard! total_value = {total_value}")

amount_to_invest = input_as("float", "\nEnter amount you have to invest: ")
print(f"Heard! Dealing with {amount_to_invest} to invest")

print("\n----------")
new_total_value = total_value + amount_to_invest
total_difference = 0
for section in sections:
    needed_value = (sections[section][1] / 100.0) * new_total_value
    difference = needed_value - sections[section][0]
    total_difference += difference
    print(f"put {difference} in {section}")
print("----------")
print(f"total: {total_difference}")

print("\nNot doable? Either adjust amount_to_invest or section_desired_percent\n")
