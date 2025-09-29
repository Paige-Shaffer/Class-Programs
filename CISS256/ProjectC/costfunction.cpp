#include <iostream>
using namespace std;
#include <unordered_set>

//Declare Van Class
// Include containers for quantity, cost, extended cost equation
// Double to prepare for possible negative data 
class Van {
public:
    double cost;
    double quantity; 
    void setCost(double);
      void setQuantity(double);
      double getCost() const;
      double getQuantity() const;
      double getExtendedCost() const;
};

//Assign value to cost 
void Van::setCost(double c) {
    cost = c; 
}
//Assign value to quantity 
void Van::setQuantity(double q){
    quantity = q; 
}
//return value in cost container
double Van::getCost() const {
    return cost; 
}
//return value in quantity containter 
double Van::getQuantity() const {
    return quantity; 
}
//use quantity & cost; return cost function
double Van::getExtendedCost() const {
    return cost * quantity; 
}

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