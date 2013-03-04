# Unigram
U00:%x[-2,1]
U01:%x[-1,1]
U02:%x[0,1]
U03:%x[1,1]
U04:%x[2,1]
U05:%x[-1,1]/%x[0,1]
U06:%x[0,1]/%x[1,1]

U10:%x[-2,2]
U11:%x[-1,2]
U12:%x[0,2]
U13:%x[1,2]
U14:%x[2,2]
U15:%x[-2,2]/%x[-1,2]
U16:%x[-1,2]/%x[0,2]
U17:%x[0,2]/%x[1,2]
U18:%x[1,2]/%x[2,2]

U20:%x[-2,2]/%x[-1,2]/%x[0,2]
U21:%x[-1,2]/%x[0,2]/%x[1,2]
U22:%x[0,2]/%x[1,2]/%x[2,2]

# Case:

#initCaps and zone
U23:%x[-1,6]/%x[-1,17]
U24:%x[0,6]/%x[0,17]
U26:%x[1,6]/%x[1,17]
#allCaps
U27:%x[0,3]/%x[0,17]
#First
U28:%x[0,5]
#mixedCaps
U29:%x[0,4]/%x[0,17]
#initCase previous and next 
U30:%x[-1,6]/%x[1,6]/%x[0,6]
U31:%x[-1,6]/%x[-1,1]
U32:%x[1,6]/%x[1,1]
#initCase and token
#U131:%x[0,6]/%x[0,1]
#initCase and First
U33:%x[0,6]/%x[0,5]
#only one Cap
U34:%x[0,9]
#initCaps and end with period
U39:%x[0,7]
#allCaps and period
#U40:%x[0,8]

# digits:

#4digits-
#U35:%x[0,12]
#2digits-
#U36:%x[0,11]
#containsDigit-
#U37:%x[0,10]
#DigitSlash+
U38:%x[0,13]

# sign:
#Dollar+
U41:%x[0,14]
#Percent+
U42:%x[0,15]
#DigitPeriod+ 
U43:%x[0,16]

#zone-
#U44:%x[0,17]

#rare words
U45:%x[0,18]

#ICOC
U46:%x[0,19]/%x[0,1]


# Bigram
B