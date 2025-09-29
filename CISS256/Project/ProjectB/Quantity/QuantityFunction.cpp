#include <iostream>
#include <string>
#include <fstream>
#include <unordered_set>
using namespace std; 
// fstream - file upload, iostream is standard library 

int quantity; // Define Quantity 
bool carCount = false; //CarCount boolean

//Quantity function 
int getQuantity(int quantity) { 
    cout << "How many cars would you like to purchase? (or enter '999' to quit)"; //Quantity input request
        cin >> quantity; //Quantity output
        cout << "" << endl;
        if (quantity > 99 || quantity < 1) { 
            if (quantity == 999) {
                return 0; 
            }
            else {
            cout << "Please enter an integer value between 1 and 99." << endl; 
            cout << "" << endl; 
            cout << "redirecting..." << endl;
            } 
        }
        else { 
            cout << "" << endl; carCount = true; }
return quantity;
}

//Run quantity function 
int main() {
    quantity = getQuantity(quantity);
    if (quantity != 0) {
    cout << "You have selected a quantity of " << quantity << " cars.";
    }
return 0; 
}