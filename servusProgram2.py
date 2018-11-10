start;
# frei;
dim f1, f2, f3, i, j, k als float;
dim MAT1[5][5] als float;
dim MAT2[5][5] als float;
dim MAT3[5][5] als float;

lass f1 <- 8.9 + 3 - 2;
lass f2 <- 0;
lass f3 <- 3 + 2;

druck MAT1;
# lass i <- (f3 > f2) ? 0 : f2;

# fur i <- 0 in 5{
#     fur j <- 0 in 5{
#         lass MAT1[i][j] <- 2.3;
#     }
# }

# wenn (f2 == 0) && f3 > 0 {
#     druck "IF TRUE";
# }
# sonst {
#     druck "IF FALSE";
# }

# waerend (f2 <= f3){
#     druck f2;
#     lass f2  <- f2 + 1;
# }

# druck "dowhile loop";
# tun{
#     lass f3 <- f3 + 3;
#     druck f3;
# } solange (f3 < 30);

# druck "This is a for loop";
# fur i <- 0 in 2{
#     fur j <- 0 in 3{
#         fur k <- 0 in 3{
#             druck k;
#         }
#         druck j;
#     }
#     druck i;
# }
ende;