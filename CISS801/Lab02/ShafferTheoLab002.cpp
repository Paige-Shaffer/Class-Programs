#include <iostream>
#include <vector>
#include <stdexcept>
#include <limits>
using namespace std; 

// Addition, Subtraction, Muliplication, Division of Integers 

// Add integers
int add(int term1, int term2) {
    return term1 + term2; 
}

// Subtract integers
int subtract(int term1, int term2) {
    return term1 - term2; 
}

// Multiply integers
int multiply(int term1, int term2) {
    return term1 * term2; 
}

// Divide integers - check for divide by 0
double divide(int term1, int term2) {
    if (term2 == 0) {
        throw invalid_argument("Terms can not be divided by zero.");
    }
    return static_cast<double>(term1) / term2;
}

// Overloaded Functions - double 

// Add - double
double add(double term1, double term2) { 
    return term1 + term2; }

// Subtract - double
double subtract(double term1, double term2) { 
    return term1 - term2; }

// Multiply - double
double multiply(double term1, double term2) { 
    return term1 * term2; }

// Divide - double 

double divide(double term1, double term2) {
    if (term2 == 0.0) {
        throw invalid_argument("Terms can not be divided by zero.");
    }
    return term1 / term2;
}

// Factorial Functions 

// Factorial function - integer 
// long long - capable of handling large calculations, as compared to int function 
long long factorial(int n) {
    if (n < 0) {
        throw invalid_argument("Please choose a non-negative number.");
    }
    if (n == 0 || n == 1) {
        return 1;
    }
    
    long long result = 1;
    for (int i = 2; i <= n; i++) {
        result *= i;
    }
    return result;
}
// No overloaded (double) factorial - could be added to handle numbers with scientific notation, but it wasn't specified as a need in this case.

// Polynomial Class 
class Polynomial {
    vector<double> coefficients;  // declare vector to store polynomial coefficents 
    public:
    Polynomial(vector<double> coefficient_values) : coefficients(coefficient_values) {} // constructor w/ vector parameter, initialize, empty

        // Polynomial Addition 
        Polynomial operator+(const Polynomial& other_polynomial) {
            // Create result vector to store sum coefficients
            vector<double> result_coefficients;
            
            // Determine the maximum degree needed for result polynomial
            // size_t for counting, I guess?? (Thank u google and stack overflow)
            const size_t max_degree = max(coefficients.size(), other_polynomial.coefficients.size());
            
            // Add corresponding coefficients
            for (size_t current_power = 0; current_power < max_degree; current_power++) {
                // coefficient from first polynomial (0 if beyond max)
                double first_coefficient = (current_power < coefficients.size()) ? coefficients[current_power] : 0.0;
                
                // Get coefficient from second polynomial (0 if beyond max)
                double second_coefficient = (current_power < other_polynomial.coefficients.size()) ? other_polynomial.coefficients[current_power] : 0.0;
                
                // Sum the coefficients and add to result
                result_coefficients.push_back(first_coefficient + second_coefficient);
            }
        
        return Polynomial(result_coefficients);
    }
        // Polynomial Substraction
        Polynomial operator-(const Polynomial& other_polynomial) {
            vector<double> result_coefficients;
            const size_t max_degree = max(coefficients.size(), other_polynomial.coefficients.size());
            // Subtract corresponding coefficents 
            for (size_t current_power = 0; current_power < max_degree; current_power++) {

                double first_coefficient = (current_power < coefficients.size()) ? coefficients[current_power] : 0.0;
                double second_coefficient = (current_power < other_polynomial.coefficients.size()) ? other_polynomial.coefficients[current_power] : 0.0;

                // Subtract coefficients and add to result
                result_coefficients.push_back(first_coefficient - second_coefficient);
            }
        
        return Polynomial(result_coefficients);
    }
        // Polynomial Multiplication 
        Polynomial operator*(const Polynomial& other_polynomial) {
            // When multiplying polynomials of degree m and n, result has degree m+n
            const size_t result_degree = coefficients.size() + other_polynomial.coefficients.size() - 1;
            vector<double> result_coefficients(result_degree, 0.0);
        
            // Multiply every term from first polynomial with every term from second
            for (size_t first_power = 0; first_power < coefficients.size(); first_power++) {
                for (size_t second_power = 0; second_power < other_polynomial.coefficients.size(); second_power++) {
                    // When multiplying x^first_power * x^second_power = x^(first_power + second_power)
                    const int result_power = first_power + second_power;
                    result_coefficients[result_power] += coefficients[first_power] * other_polynomial.coefficients[second_power];
                }
            }
        return Polynomial(result_coefficients);
    }
    // Evaluate Polynomials 
     double operator()(double input_value) {
        double polynomial_value = 0.0;    // Final evaluated value
        double current_power = 1.0;       // x^0, x^1, x^2, etc.
        
        // Evaluate polynomial - x^1 + x^2 ... 
        for (size_t term_index = 0; term_index < coefficients.size(); term_index++) {
            polynomial_value += coefficients[term_index] * current_power;
            current_power *= input_value;  // Update power
        }
        
        return polynomial_value;
    }

    // Display Polynomials 
       void print() {
        const double zero_tolerance = 1e-10;
        bool is_first_term = true;
        
        // Print from highest degree to lowest
        for (int current_power = coefficients.size() - 1; current_power >= 0; current_power--) {
            if (abs(coefficients[current_power]) > zero_tolerance) {
                // Handle sign and spacing
                if (!is_first_term) {
                    cout << (coefficients[current_power] > 0 ? " + " : " - ");
                } else if (coefficients[current_power] < 0) {
                    cout << "-";
                }
                
                // Print coefficient (skip if 1 and not constant term)
                const double absolute_coefficient = abs(coefficients[current_power]);
                if (absolute_coefficient != 1.0 || current_power == 0) {
                    cout << absolute_coefficient;
                }
                
                // Print variable and exponent
                if (current_power > 0) {
                    cout << "x";
                    if (current_power > 1) {
                        cout << "^" << current_power;
                    }
                }
                
                is_first_term = false;
            }
        }
        
        if (is_first_term) {
            cout << "0";
        }
    }

    // Get polynomial degree 
      int getDegree() const {
        return coefficients.size() - 1;
    }
};

// Calculator function 
int main() {
    int choice;
    bool running = true;
    
    cout << "=== SCIENTIFIC CALCULATOR ===" << endl;
    
    while (running) {
        cout << "\n=== MAIN MENU ===" << endl;
        cout << "1. Integer Operations" << endl;
        cout << "2. Double Operations" << endl;
        cout << "3. Factorial Calculation" << endl;
        cout << "4. Polynomial Operations" << endl;
        cout << "5. Exit" << endl;
        cout << "Enter your choice (1-5): ";
        
        cin >> choice;
        
        // Clear input buffer
        cin.clear();
        cin.ignore(numeric_limits<streamsize>::max(), '\n');
        
        switch (choice) {
            case 1: { // Integer Operations
                int a, b;
                cout << "\n--- INTEGER OPERATIONS ---" << endl;
                cout << "Enter first integer: ";
                cin >> a;
                cout << "Enter second integer: ";
                cin >> b;
                
                cout << "\nResults:" << endl;
                cout << a << " + " << b << " = " << add(a, b) << endl;
                cout << a << " - " << b << " = " << subtract(a, b) << endl;
                cout << a << " * " << b << " = " << multiply(a, b) << endl;
                
                try {
                    cout << a << " / " << b << " = " << divide(a, b) << endl;
                } catch (const invalid_argument& e) {
                    cout << "Division Error: " << e.what() << endl;
                }
                break;
            }
            
            case 2: { // Double Operations
                double a, b;
                cout << "\n--- DOUBLE OPERATIONS ---" << endl;
                cout << "Enter first number: ";
                cin >> a;
                cout << "Enter second number: ";
                cin >> b;
                
                cout << "\nResults:" << endl;
                cout << a << " + " << b << " = " << add(a, b) << endl;
                cout << a << " - " << b << " = " << subtract(a, b) << endl;
                cout << a << " * " << b << " = " << multiply(a, b) << endl;
                
                try {
                    cout << a << " / " << b << " = " << divide(a, b) << endl;
                } catch (const invalid_argument& e) {
                    cout << "Division Error: " << e.what() << endl;
                }
                break;
            }
            
            case 3: { // Factorial Calculation
                int n;
                cout << "\n--- FACTORIAL CALCULATION ---" << endl;
                cout << "Enter a non-negative integer: ";
                cin >> n;
                
                try {
                    long long result = factorial(n);
                    cout << n << "! = " << result << endl;
                } catch (const invalid_argument& e) {
                    cout << "Error: " << e.what() << endl;
                }
                break;
            }
            
            case 4: { // Polynomial Operations
                cout << "\n--- POLYNOMIAL OPERATIONS ---" << endl;
                
                // Sample polynomials
                vector<double> coeffs1 = {1, 2, 3}; // 3x^2 + 2x + 1
                vector<double> coeffs2 = {2, 1};     // x + 2
                
                Polynomial p1(coeffs1);
                Polynomial p2(coeffs2);
                
                cout << "Polynomial 1: ";
                p1.print();
                cout << endl;
                
                cout << "Polynomial 2: ";
                p2.print();
                cout << endl;
                
                // Perform operations
                Polynomial sum = p1 + p2;
                Polynomial difference = p1 - p2;
                Polynomial product = p1 * p2;
                
                cout << "\nPolynomial Operations Results:" << endl;
                cout << "Sum: ";
                sum.print();
                cout << endl;
                
                cout << "Difference: ";
                difference.print();
                cout << endl;
                
                cout << "Product: ";
                product.print();
                cout << endl;
                
                // Evaluate polynomials
                double x;
                cout << "\nEnter a value x to evaluate the polynomials: ";
                cin >> x;
                
                cout << "p1(" << x << ") = " << p1(x) << endl;
                cout << "p2(" << x << ") = " << p2(x) << endl;
                cout << "Degree of p1: " << p1.getDegree() << endl;
                cout << "Degree of p2: " << p2.getDegree() << endl;
                
                break;
            }
            
            case 5: { // Exit
                running = false;
                cout << "Thank you for using the calculator." << endl;
                break;
            }
            
            default: {
                cout << "Invalid choice. Please enter a number between 1 and 5." << endl;
                break;
            }
        }
        
        // Pause before continuing
        if (running) {
            cout << "\nPress Enter to continue...";
            cin.get();
        }
    }
    
    return 0;
}