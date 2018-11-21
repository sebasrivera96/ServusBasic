start;

dim Reihen1, Spalten1 als float;
dim Reihen2, Spalten2 als float;
dim Reihen3, Spalten3 als float;
dim Mat1[5][5], Mat2[5][5], Mat3[5][5] als float;
dim option als float;
dim i, j, k als float; # These are iterators

def getAbmessungenMatrix1{
    druck "Gib die Reihen und Spalten der Matrix 1 an";
    eingabe Reihen1;
    eingabe Spalten1;
    return;
}

def getAbmessungenMatrix2{
    druck "Gib die Reihen und Spalten der Matrix 2 an";
    eingabe Reihen2;
    eingabe Spalten2;
    return;
}

def fillMatrix1{
    druck "Daten fuer MAT1 einfuegen";
    fur i <- 0 in Reihen1{
        fur j <- 0 in Spalten1{
            eingabe Mat1[i][j];
        }
    }
    return;
}

def fillMatrix2{
    druck "Daten fuer MAT2 einfuegen";
    fur i <- 0 in Reihen2{
        fur j <- 0 in Spalten2{
            eingabe Mat2[i][j];
        }
    }
    return;
}

def sumMats{
    wenn (Reihen1 == Reihen2 && Spalten1 == Spalten2){
        gosub fillMatrix1;
        gosub fillMatrix2;
        
        lass Reihen3 <- Reihen1;
        lass Spalten3 <- Spalten1;

        fur i <- 0 in Reihen3{
            fur j <- 0 in Spalten3{
                lass Mat3[i][j] <- Mat1[i][j] + Mat2[i][j]; 
            }
        }
        druck "Antowort in Mat3";
        druck Mat3;
    }
    sonst{
        druck "Die Matrizen konnten nicht addiert werden";
    }
    return;
}

def multMats{
    wenn (Spalten1 == Reihen2){
        gosub fillMatrix1;
        gosub fillMatrix2;

        lass Reihen3 <- Reihen1;
        lass Spalten3 <- Spalten2;

        fur i <- 0 in Reihen3{
            fur j <- 0 in Spalten3{
                fur k <- 0 in Reihen2{ # oder Spalten1
                    lass Mat3[i][j] <- Mat3[i][j] + (Mat1[i][k] * Mat2[k][j]);
                } 
            }
        }
        druck "Antowort in Mat3";
        druck Mat3;        
    }
    sonst{
        druck "Die Matrizen konnten nicht multiplitziert werden";
    }
    return;
}

def main{
    
    druck "AUFPASSEN Maximale Abmessungen 5 x 5";

    tun{
        gosub getAbmessungenMatrix1;
    } solange((Reihen1 > 5) || (Spalten1 > 5) || Reihen1 <= 0 || Spalten1 <= 0);

    tun{
        gosub getAbmessungenMatrix2;
    } solange (Reihen2 > 5 || Reihen2 <= 0 || Spalten2 > 5 || Spalten2 <= 0);
    
    druck "Menue fuer Matrixoperationen";
    druck "Druecken Sie 1 zum Summieren";
    druck "Druecken Sie 2 zum Multiplizieren";
    eingabe option;

    wenn (option == 1){
        gosub sumMats;
    }
    sonst{
        gosub multMats;
    }
    
    return;
}

ende;
