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
