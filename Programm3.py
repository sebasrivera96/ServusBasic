start;
dim operation als float;
dim X, Y, ANS als float;
dim loop als float;
dim it1, it2 als float;
dim num, den als float;
dim factorialDP[10] als float;
dim numeratorX[10] als float;

def selectOperation{
    tun{
        druck "Menu of operations press a number to execute a operation";
        druck "1 to calculate the factorial of a number";
        druck "2 to calculate X to the power of Y";
        druck "3 to calculate e to the X using Taylor series";
        eingabe operation;
    } solange(operation <= 0 && operation > 3);
    return;
}

def factorialUser{
    druck "Give a number to calculate its factorial";
    eingabe X;
    lass ANS <- 1;
    wenn(X >= 2){
        lass X <- X + 1;
        fur it1 <- 2 in X{
            lass ANS <- ANS * it1;
        }
    }
    return;
}

def fillFactorialDP{
    lass factorialDP[0] <- 1;
    fur it1 <- 1 in 10{
        lass it2 <- it1 - 1;
        lass factorialDP[it1] <- factorialDP[it2] * it1;
    }
    # druck factorialDP;
    return;
}

def xToPowY{
    druck "Give a number to be the base X";
    eingabe X;
    druck "Give a number to be the exponent Y";
    eingabe Y;
    lass ANS <- 1;
    wenn(Y > 0){
        # lass Y <- Y + 1;
        fur it1 <- 0 in Y{
            lass ANS <- ANS * X;
        }
    }
    return;
}

def fillNumeratorX{
    lass numeratorX[0] <- 1;
    fur it1 <- 1 in 10{
        lass it2 <- it1 - 1;
        lass numeratorX[it1] <- numeratorX[it2] * X;
    }
    # druck numeratorX;
    return;
}

def eToPowX{
    druck "Give a number to be the power X";
    eingabe X;

    gosub fillFactorialDP;
    gosub fillNumeratorX;

    fur it1 <- 0 in 10{
        lass ANS <- ANS + (numeratorX[it1] / factorialDP[it1]);
    }

    return;
}

def main{
    lass loop <- 0;
    tun{
        gosub selectOperation;
        wenn(operation == 1){
            gosub factorialUser;

        }
        wenn(operation == 2){
            gosub xToPowY;
        }
        wenn(operation == 3){
            gosub eToPowX;
        }

        druck "The answer is";
        druck ANS;
        tun{
            druck "Press 1 to perform a new operation";
            druck "Press 0 to exit";
            eingabe loop;
        }solange(loop != 1 && loop != 0);
    } solange(loop == 1);
    return;
}

ende;