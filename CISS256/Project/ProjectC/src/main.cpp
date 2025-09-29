#include <iostream>
#include <c:\Users\pshaf\ciss256\Project\ProjectC\src\cost.h>
#include <unordered_set>
using namespace std;


int main() {
    double number; //temporary value hold
    double extendedCost;
    bool vertify = false; //verify want
    string yn;
    Van extended; //hold extended data 
    unordered_set<string> validyes = {"Y", "y","Yes","yes","YES"}; //verify interest is yes
    unordered_set<string> validno = {"N", "n","No","no","NO"}; //verify interest is no

    //verify interest in purchase
    cout << "You would like to purchase an extended vehicle?";
    cin >> yn;
    if (validyes.count(yn) > 0) {
        cout << "How many vans would you like?";
        cin >> number; 
        extended.setQuantity(number);
        extended.setCost(50000);
        cout << "Please hold while we calculate the cost of your order" << endl;
        cout << "loading..." << endl;
         if (extended.getQuantity() > 10) {
            extendedCost = extended.getExtendedCost() * 0.97; // 3% discount
        } 
        else {
            extendedCost = extended.getExtendedCost();
        }
        cout << "The total cost of your order is " << extendedCost << endl;
        cout << "Thank you for your order"; 
        return 0; 
    }
    if (validno.count(yn) > 0) {
        cout << "Have a good day";
        return 0;
    }


}  