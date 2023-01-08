#!/bin/bash
###########Command line 1
#Change the permits in order to execute the file.
#chmod 700 command1A.sh

#Run the file 
#./command1A.sh
rows=`sed -n '$=' "hero-network.csv"`

# Goal of this command line: What is the most popular pair of heroes (often appearing together in the comics)?
# Description:
# This command line question is split in two parts that are:
# - Construction of the dataset (file command1A.sh)
# - Research of the most popular pair of heroes (file command1B.sh)


# Construction of the dataset:
# In this script using a while loop we iterate on the dataset and create a dataset called pair.txt that contain
# for each pair, the elements of the pair sorted in alphabetical order

# NOTE : we will work on a preprocess dataset, not "hero-network.csv".
# The only difference in that dataset is that "sephero_network" uses ";" as separator and not ","

a=1
b=1
while  IFS=$';' read -r -a myArray; do #Start the loop, every iteration will be a row of the csv file
a=`echo $((a+b))`;                     #Counter used to stop the while loop
if  [[ $a  -gt 2 ]];                    
then
prima=`echo "${myArray[1]}"`           #Sort the rows 
seconda=`echo "${myArray[2]}"`         #Sort the rows 
echo "$prima" > file.txt               #Sort the rows 
printf "$seconda" >> file.txt          #Sort the rows 
sort file.txt > file1.txt              #Sort the rows 
prima=`head -1 file1.txt`              #Sort the rows 
seconda=`tail -1 file1.txt`            #Sort the rows 
anothervariable="$prima""-""$seconda"  #Combined the two names of the heroes and create the pair
echo $anothervariable;
fi;
if (($a > $rows))                      #If statement create to stop the loop
then 
    break;
    fi;
done < "sephero_network.csv" > pair.txt   #store in a new dataset


#Change the permits in order to execute the file.
#chmod 700 command1B.sh

#Run the file 
#./command1B.sh


# Research of the most popular pair of heroes :
# We simply used AWK in order to count all the couples.

#Most popular couple of heroes
awk -F"\t" 'NR > 0 {arr[$1]++; spend[$1] += 1}END{for (a in arr) print a ","  sprintf("%.0f", spend[a]);}' "pair.txt" | sort -t ',' -k2 -nr > most_popular_heroes.csv

##print the first 5
head -10 most_popular_heroes.csv



###########Command line 2
#Change the permits in order to execute the file.
#chmod 700 command2.sh

#Run the file 
#./command2.sh

# We simply used AWK in order to count all of comics per hero.
# NOTE : we will work on a preprocess dataset, "sepedges.csv".
# The only difference in that dataset is that edges use ";" as separator and not ","


#Find the number of comics per hero.
awk -F";" 'NR > 1 {arr[$2]++; spend[$2] += 1}END{for (a in arr) print a ","  sprintf("%.0f", spend[a]);}' "sepedges.csv" | sort -t ',' -k2 -nr > comics_per_hero.csv

##print the first 5
head -10 comics_per_hero.csv

###########Command line 3
#Change the permits in order to execute the file.
#chmod 700 command3.sh

#Run the file 
#./command3.sh

# We simply used AWK in order to count all of comics per hero, after that the compute the mean.
# NOTE : we will work on a preprocess dataset, "sepedges.csv".
# The only difference in that dataset is that edges use ";" as separator and not ","


#The average number of heroes in comics.
awk -F';' 'NR > 1 {arr[$3]++; spend[$3] += 1}END{for (a in arr) print a ";"  sprintf("%.0f", spend[a]);}' "sepedges.csv" | sort -t ',' -k2 -nr | awk -F';' 'NR > 0 {count[a]++ ; spend[a] += $2}END{for (i in count) print "Average number of heroes in comics: " spend[i]/count[i]}'


