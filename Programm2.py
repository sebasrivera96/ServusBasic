start;

dim Arr1[10] als float;
dim len, num, tNum als float;
dim i, tI, j als float;
dim loop als float;
dim target1, target2 als float;

def insertElemente{
	fur i <- 0 in len{
		druck "Gib eine neue Elemente";
		eingabe num;
		lass Arr1[i] <- num;
	}
	return;
}

def orderElemente{
	lass target1 <- len - 1;

	fur i <- 0 in target1{
		lass target2 <- len - i - 1;

		fur j <- 0 in target2{
			lass tI <- j+1;

			wenn(Arr1[j] > Arr1[tI]){
				lass tNum <- Arr1[tI];
				lass Arr1[tI] <- Arr1[j];
				lass Arr1[j] <- tNum;
			}
		}
	}
	return;
}

def main{
	lass loop <- 0;
	druck "Bubble Sort Sorting Algorithmus";
	tun{
		tun{
			druck "Wie viele Elemente";
			eingabe len;
		}solange(len <= 0 || len > 10);
		
		gosub insertElemente;
		gosub orderElemente;

		druck "Die Elemente wurden bestellt";
		druck Arr1;
		tun{
			druck "Druck 1 um eine neue array zu bestellen";
			druck "Druck 0 um das Programm zu beenden";
			eingabe loop;

		}solange(loop != 0 && loop != 1);
		
	}solange(loop == 1);
	
	return;
}

ende;