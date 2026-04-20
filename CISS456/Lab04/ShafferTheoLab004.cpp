#include <iostream>
using namespace std;

// Template class definition
template <typename T>
class Stack {
private:
    static const int MAX = 100;  
    T arr[MAX];                 
    int top;                    

public:
    // Constructor initializes empty stack
    Stack() {
        top = -1;
    }

    // Element to stack
    void push(T value) {
        if (top >= MAX - 1) {
            cout << "Stack overflow! Cannot push " << value << endl;
        } else {
            arr[++top] = value;
            cout << value << " pushed to stack." << endl;
        }
    }

    // Pop the top element from stack
    void pop() {
        if (isEmpty()) {
            cout << "Stack underflow! Cannot pop." << endl;
        } else {
            cout << arr[top--] << " popped from stack." << endl;
        }
    }

    // Check if the stack is empty
    bool isEmpty() const {
        return top == -1;
    }

    // Display all elements in the stack
    void display() const {
        if (isEmpty()) {
            cout << "Stack is empty." << endl;
        } else {
            cout << "Stack contents (top to bottom): ";
            for (int i = top; i >= 0; i--) {
                cout << arr[i] << " ";
            }
            cout << endl;
        }
    }
};

// Main function to test the generic stack
int main() {
    // int test stack
    Stack<int> intStack;
    intStack.push(10);
    intStack.push(20);
    intStack.push(30);
    intStack.display();
    intStack.pop();
    intStack.display();

    cout << endl;

    //string test stack
    Stack<string> stringStack;
    stringStack.push("Hello");
    stringStack.push("World");
    stringStack.display();
    stringStack.pop();
    stringStack.display();

    return 0;
}
