#include <iostream>
#include <vector>
#include <memory>
#include <math.h>
using namespace std;

// Base class - Shape
class Shape {
public:
    virtual double area() { return 0; }
    virtual ~Shape() {} 
};

// Derived class - Circle
class Circle : public Shape {
private:
    double radius;
public:
    Circle(double r) : radius(r) {}
    double area() override {
        return M_PI * radius * radius;
    }
};

// Derived class - Rectangle
class Rectangle : public Shape {
private:
    double width, height;
public:
    Rectangle(double w, double h) : width(w), height(h) {}
    double area() override {
        return width * height;
    }
};

// Function to calculate total area 
double totalArea(const vector<unique_ptr<Shape>>& shapes) {
    double total = 0;
    for (const auto& shape : shapes) {
        total += shape->area();
    }
    return total;
}

int main() {
    vector<unique_ptr<Shape>> shapes;
    
    // Get number of circles
    int numCircles;
    cout << "Enter the number of circles: ";
    cin >> numCircles;
    
    // Input circles
    for (int i = 0; i < numCircles; i++) {
        double radius;
        cout << "Enter radius for circle " << (i + 1) << ": ";
        cin >> radius;
        shapes.push_back(make_unique<Circle>(radius));
    }
    
    // Get number of rectangles
    int numRectangles;
    cout << "Enter the number of rectangles: ";
    cin >> numRectangles;
    
    // Input rectangles
    for (int i = 0; i < numRectangles; i++) {
        double width, height;
        cout << "Enter width for rectangle " << (i + 1) << ": ";
        cin >> width;
        cout << "Enter height for rectangle " << (i + 1) << ": ";
        cin >> height;
        shapes.push_back(make_unique<Rectangle>(width, height));
    }
    
    // Calculate and display total area
    cout << "\nTotal area: " << totalArea(shapes) << endl;
    
    // Display individual areas
    cout << "\nIndividual areas:" << endl;
    for (int i = 0; i < shapes.size(); i++) {
        if (i < numCircles) {
            cout << "Circle " << (i + 1) << ": " << shapes[i]->area() << endl;
        } else {
            int rectIndex = i - numCircles + 1;
            cout << "Rectangle " << rectIndex << ": " << shapes[i]->area() << endl;
        }
    }

    return 0;
}