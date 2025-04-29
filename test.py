# Importing necessary libraries
import math

# Function to calculate the area of a circle
def calculate_circle_area(radius: float) -> float:
    """
    Function to calculate the area of a circle given its radius.
    
    Parameters:
        radius (float): The radius of the circle.
        
    Returns:
        float: The area of the circle.
    """
    if radius <= 0:
        raise ValueError("Radius must be a positive number.")

    area = math.pi * (radius ** 2)
    return area

# Main function to demonstrate the circle area calculation
def main():
    """
    Main function to prompt the user for input and display the circle area.
    """
    try:
        # Taking input from the user
        radius_input = float(input("Enter the radius of the circle: "))

        # Calculating the area
        area = calculate_circle_area(radius_input)

        # Displaying the result
        print(f"The area of the circle with radius {radius_input} is {area:.2f}.")
        print("Well done !!")

    except ValueError as e:
        print(f"Error: {e}")

# Entry point for the program
if __name__ == "__main__":
    main()
