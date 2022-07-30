import language_tool_python
import re
import string
import random
from numpy.random import choice


"""LET'S GET STARTED"""

# open our file
with open('data/bri/data_stack_resumes.txt', 'r') as resume_script:
    # open txt file and read to string
    resume_file = resume_script.read()
    # lowercase everything in the string
    resume_file = resume_file.lower()

# regex to keep only punctuation or words more than two letters long, may or may not contain an apostrophe in the middle
resume_string = re.findall(r"[.,]|[a-z]+[']?[a-z]+", resume_file)
# adds things to out list of unwanted words
more_drops = ['state', 'city', 'name', 'company',
              'college', 'am', 'the', 'to', 'in']
# toss those words to the curbs
stop_dropped_resume = [w for w in resume_string if not w in more_drops]


"""CREATE OUR NESTED DICT TO SAVE HOW OFTEN ONE WORD FOLLOWS ANOTHER"""

resume_dict = {}
# for loop that runs over every word in our string, but stating to stop at the last word
for i, word in enumerate(stop_dropped_resume[:-1]):
    # setting this word to be the word right after the one we were on
    this_word = stop_dropped_resume[i+1]
    # if this_word isn't in our dictionary already...
    if this_word not in resume_dict:
        # start our counter dict
        next_count = {}
        # add our new word to be a key in our resume dict and the count dict to be its value
        resume_dict[this_word] = next_count
    # if it is already in there....
    else:
        # create empty dictionary with this_word as the key and next_count as the value
        next_count = resume_dict[this_word]
    # if the next word(word) is in our nested dict already...
    if word in next_count:
        # add one to its count
        next_count[word] += 1
    # if its not already in there
    else:
        # lets add it and set its count to 1
        next_count[word] = 1


"""START THE STORY"""

# starting out story off blank
story = []
# Pick the first word at random from our initial string
first_word = random.choice(stop_dropped_resume)
# while loop to make sure we dont start on punctuation
while first_word in string.punctuation:
    # if it was punctuation, choose again
    first_word = random.choice(stop_dropped_resume)
# if story is blank...
if story == []:
    # set story up with our first word
    story.append(first_word)


"""CREATE THE WEIGHTED PROB ALGORITHM TO DETERMINE THE NEXT WORD"""

# function to get the next word using weighted probability
def whos_next():
    # set our current word to be the last word of the story string
    current_word = story[-1]
    # pick out our nested dict for specific word
    for outer_word, inner_dict in resume_dict.items():
        # get the next words and instances
        word_self_total = inner_dict.items()
        # seperate the instances
        total_occurances = inner_dict.values()
        # pull the dictionary for the current word
        if outer_word == current_word:
            # add the total times a word followed current word
            total = sum(total_occurances)
            # set empty variable for the percent chance of each word occuring
            probs = []
            # set a list of all words that came after current word
            hopefuls = []
            # set an empty list to grab the count of each word
            likely = []
            # pull every number of times each word came after current
            for number in total_occurances:
                # factor the percent chance of a word being next
                percent = number / total
                # add each percent to our probs list
                probs.append(percent)
            # pull words and their values from our inner dict
            for word, num in word_self_total:
                # add each word to our hopefuls list
                hopefuls.append(word)
                # add each number to our likely list
                likely.append(num)
            # making our rng_says a global variable
            global rng_says
            # weighted rng based off the percent probability of word occuring
            rng_says = choice(hopefuls, p=probs)
            # change rng output from numpy to string
            next_word = str(rng_says)
            # add our next word string to the story
            story.append(next_word)
            

"""ADD WORDS TO OUR STORY, DROP WHITE SPACE, CAPITALIZE, AND NEWLINE"""

# -----ADD WORDS-------
# while our story is less than this long
while len(story) < 400:
    # call our function
    whos_next()
# set our full story to be
whole_story = ' '.join(story)
# apparently, the code like to run forever unless we put a print function here
print(whole_story)

# ------REMOVE WHITESPACE AND CAPITALIZE FIRST WORD OF SENTENCES------
# replace white space preceding punctuation
whole_story = re.sub(r'\s([?.,!](?:\s|$))', r'\1', whole_story)
# re split the story, this time on sentences
sentences = re.split('[?.]', whole_story)
# set a new clean variable
cap_sent = []
# for every sentense in our story...
for sentence in sentences:
    # strip the left white space and capitalize the first word and add it to a new list
    cap_sent.append((sentence.lstrip().capitalize() + '.'))
# turn our story back into a string by joining them back in together
cap_sent = ' '.join(cap_sent)

# -------ADD NEWLINES AND BEGINNING OF PARAGRAPH TABS------
# back to splitting our text on periods
splittext = cap_sent.split(".")
# for every 5 to 10 sentences...
for x in range(4, len(splittext), random.randint(5, 8)):
    # add a new line and start the next sentence tabbed in
    splittext[x] = "\n"+"\t"+splittext[x].lstrip()
# throw it all back together into a string
text = ".".join(splittext)
# add a tab to the first line so it matches its friends
text = f'\t'+text

# -------SPELL CHECK AND SAVE------
# set our spell check function to english and assign it to a variable
tool = language_tool_python.LanguageTool('en-US')
# set our checker to auto correct
checked_text = tool.correct(text)
# open a new file in the generated resume folder
text_file = open(f'finished_resumes/generated_resumes.txt', 'w')
# write our resume to it
text_file.write(text)
# shut it down. our work here is done
text_file.close()


"""THE END"""