import os
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import concurrent.futures

os.system("cls")
file = open(r"path to text file", "r").readlines() # input path to text file containing hashtags
popularities = []
popdict = {}

# change these values to your liking
variants = 8
tags_per_list = 22
max_dupes_per_tag = 6
max_dupe_tags = 45
find_popularity = False

def generate_tags():
    tries = 0
    if variants > len(file) or tags_per_list > len(file) or tags_per_list > 30:
        return None
    while True:
        list = []
        duped_tags = {}
        for i in range(variants):
            list.append([])
        for tags in list:
            for i in range(tags_per_list):
                while True:
                    rand_tag = random.choice(file).strip()
                    if rand_tag not in tags:
                        tags.append(rand_tag)
                        break
        for tags in list:
            for tag in tags:
                dupes = 0
                if tag not in duped_tags:
                    for i in range(variants):
                        if tag in list[i]:
                            dupes += 1
                    if dupes > 1:
                        duped_tags[tag]= dupes
        print(f"generation {tries}")
        is_correct = True
        if max_dupe_tags != None and not len(duped_tags) < max_dupe_tags:
            is_correct = False
        if max_dupes_per_tag != None:
            for i in range(max_dupes_per_tag, variants+1):
                if i in duped_tags.values():
                    is_correct = False
        if is_correct == True:
            print(f"\nNum of Duped Tags: {len(duped_tags)}")
            print(f"Duped Tags: {duped_tags.values()}\n")
            return list
        else:
            tries += 1

def find_tag_popularity(tag):
    driver = webdriver.Chrome()
    driver.minimize_window()
    driver.get(f'https://instagram.com/explore/tags/{tag.replace("#", "")}/')
    try:
        posts = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "g47SY"))).text
    finally:
        driver.quit()
    posts = int(posts.replace(",", ""))
    return tag, posts

# if you already have a list of hashtags for each variant, paste them below to reduce runtime and comment out the generate tags function
# taglist = [[], []] 
taglist = generate_tags()

for i in range(variants):
    popularities.append([])

used_tags = []
for tags in taglist:
    for tag in tags:
        if tag not in used_tags:
            used_tags.append(tag)

# if you already have a dictionary containing the popularity for your tags, just paste them here to reduce run time               
# popdict = {}
               
poplist = taglist.copy()

use_multiprocessors = False
if find_popularity == True:
    if use_multiprocessors == True:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            results = [executor.submit(find_tag_popularity, tag) for tag in used_tags if tag not in popdict.keys()]
            for f in concurrent.futures.as_completed(results):
                popdict[f.result()[0]] = f.result()[1]
                print(popdict)
                print('\n')
    else:
        x = 0
        y = 0
        for tag in used_tags:
            if tag not in popdict.keys():
                y += 1
        for tag in used_tags:
            if tag not in popdict.keys():
                x += 1
                print(f"{x}/{y}")
                print(tag)
                data = find_tag_popularity(tag)
                popdict[data[0]] = data[1]
                print(popdict)
                print('\n')

    for x in range(len(poplist)):
        for y in range(len(poplist[x])):
            poplist[x][y] = popdict.get(poplist[x][y])

    totalpoplist = []
    for pops in poplist:
        total = 0
        for pop in pops:
            total += pop
        totalpoplist.append(total)

    variant = 0
    for tags in taglist:
        print(f"| VARIANT: {variant+1} | POPULARITY: {'{:,}'.format(totalpoplist[variant])} |")
        for tag in tags:
            for key, value in popdict.items():
                if tag == value:
                    print(key, end=" ")
        variant += 1
        print('\n\n')

else:
    variant = 0
    for tags in taglist:
        print(f"| VARIANT: {variant+1} |")
        for tag in tags:
                print(tag, end=" ")
        variant += 1
        print('\n\n')

