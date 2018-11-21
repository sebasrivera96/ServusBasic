start;
dim arrSeries[20] als float;
dim limit, ANS, it als float;
dim i, j als float;

def main{
    druck "This program calculates the Fibonnaci series up to 20";
    druck "Type the number of the element you want to print";
    eingabe limit;
    lass arrSeries[0] <- 1;
    lass arrSeries[1] <- 1;
    
    wenn(limit >= 3){
        fur it<-2 in limit{
            lass i <- it-1;
            lass j <- it-2;
            lass arrSeries[it] <- arrSeries[i] + arrSeries[j];
        }
    }
    
    lass it <- limit-1;
    lass ANS <- arrSeries[it];

    druck "The element you are looking for is";
    druck ANS;

    return;
}

ende;