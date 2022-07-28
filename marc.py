import json
import re
import string
import random
import re
from numpy.random import choice
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords



# lets get started
with open('data/Resume/CHEF/chef_resumes.txt', 'r') as resume_script:
    # open txt file and read to string, string to lower
    resume_file = resume_script.read()
    resume_file = resume_file.lower()




resume_string = re.findall(r"[A-Za-z]+|[.,]", resume_file)


more_drops = ['state', 'city', 'name', 'company', 'college']
stop_dropped_resume = [w for w in resume_string if not w in more_drops]

# # encode the string into ‘ASCII’ and error as ‘ignore’ to remove Unicode characters
# no_nonsense = str.encode(str(resume_string), "utf-8", "ignore")
# # # # decode the string back in its form
# no_nonsense_resume = no_nonsense.decode()

# print(stop_dropped_resume[:1000])


# for loop that runs over every word in test

resume_dict = {}

for i, word in enumerate(resume_string[:-1]):
    this_word = resume_string[i+1]
    # if this_word is in dict, asssign it to 'next_count'
    if this_word not in resume_dict:
        next_count = {}
        resume_dict[this_word] = next_count

    # if not, create empty dictionary with this_word as the key and next_count as the value
    else:
        next_count = resume_dict[this_word]

    if word in next_count:
        next_count[word] += 1
    else:
        next_count[word] = 1
this_word = resume_string[i+1]

# print(json.dumps(resume_dict, sort_keys=True, indent=3))

first_word = random.choice(resume_string)
while first_word in string.punctuation:
    first_word = random.choice(resume_string)
print(first_word)



story = []

def start_story(str):
    """function to start the story"""
    if story == []:
        # set story up with a first word
        story.append(first_word)
    else:
        # dont start the story if its already been started
        pass
    return story

start_story(resume_string)




def whos_next():
    """function to get the next word using weighted probability"""
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
            
            probs = []
            # set empty variable for the percent chance of each word occuring
            hopefuls = []
            # set a list of all words that came after current word
            likely = []
            # set an empty list to grab the count of each word
            for number in total_occurances:
                # pull every number of times each word came after current
                percent = number / total
                # factor the percent chance of a word being next
                probs.append(percent)
                # add each percent to our probs list
            for word, num in word_self_total:
                # pull words and their values from our inner dict
                hopefuls.append(word)
                # add each word to our hopefuls list
                likely.append(num)
                # add each number to our likely list
                global rng_says
            rng_says = choice(hopefuls, p=probs)
            # weighted rng based off the percent probability of word occuring
            # return rng_says
            next_word = str(rng_says)
            # change rng output from numpy to string
            story.append(next_word)
            # add our next word string to the story





"""add words to the story"""


while len(story) < 1500:
    whos_next()
whole_story = ' '.join(story)
print(whole_story)


# this drops the spaces
whole_story = re.sub(r'\s([?.,!](?:\s|$))', r'\1', whole_story)


sentences = re.split('[?.]', whole_story)
cap_sent = []
for sentence in sentences:
    cap_sent.append((sentence.lstrip().capitalize() + '.'))
cap_sent = ' '.join(cap_sent)


random.randint(5, 10)
splittext = cap_sent.split(".")
for x in range(5, len(splittext), random.randint(5, 10)):
    splittext[x] = "\n"+"\t"+splittext[x].lstrip()
text = ".".join(splittext)
print(text)
