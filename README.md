# WnCC_Convener_CodingTask
Here is the code for the 1st question.
Some points to be noted are:
 1. I have scraped lyrics of all songs of all singers. It was relatively slow and I used multiprocessing to fasten it. It could take           around 9-10 minutes to run for say 5 singers like Eminem with lots of songs.
 2. Input.txt should be in the same path as python or the code should be changed appropriately.
 3. I have used lyrics.az to scrape the lyrics. If any artist is not found in their database, I have take the occurence of word in their       song to be zero, though an alarm is raised in the terminal.
 4.Output is printed both on the terminal and in a file output.txt
