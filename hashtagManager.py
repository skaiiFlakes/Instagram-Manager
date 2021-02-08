import os
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import concurrent.futures

os.system("cls")
file = open(r"C:\Users\ica\Coding Projects\Python\Instagram\hashtags.txt", "r").readlines()
popularities = []
popdict = {}

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

# taglist = [['#artstudio', '#instagramartist', '#photo', '#fineart', '#artjournal', '#love', '#artlover', '#traditionalart', '#drawings', '#artistofinstagram', '#art', '#artoftheday', '#artdaily', '#artistoninstagram', '#artsagram', '#sketchpad', '#hobby', '#coolart', '#myart', '#artsy'], ['#artjournal', '#artdaily', '#draw', '#art', '#artista', '#sketchpad',
# '#follow', '#instagramart', '#artofvisuals', '#artsagram', '#artwork', '#illustration', '#beautiful', '#artgram', '#fineart', '#artistoninstagram', '#artsy', '#sketchbook', '#hobby', '#drawings'], ['#artist', '#draw', '#photo', '#myart', '#drawings', '#instaart', '#beautiful', '#artgram', '#artistoninstagram',
# '#artjournal', '#love', '#follow', '#traditionalart', '#artsagram', '#artistic', '#art', '#sketchpad', '#artoftheday', '#sketchbook', '#cool'], ['#draw', '#artdaily', '#artsy', '#instagramart', '#follow', '#artist', '#arte', '#fineart', '#visualart', '#artoftheday', '#love', '#sketchbook', '#traditionalart', '#myart', '#beautiful', '#drawing', '#artgallery', '#coolart', '#instagramartist', '#artgram']]

taglist = generate_tags()

for i in range(variants):
    popularities.append([])

used_tags = []
for tags in taglist:
    for tag in tags:
        if tag not in used_tags:
            used_tags.append(tag)

# popdict = {'#traditionalart': 12762037, '#photo': 378511848, '#love': 2014229200, '#instagramartist': 1369926, '#artjournal': 3095900, '#fineart': 25879995, '#artstudio': 5702776, '#artlover': 6242234, '#artsagram': 478897, '#art': 754338285, '#artoftheday': 47662207, '#drawings': 27908827, '#artistofinstagram': 4150064, '#artdaily': 3598698, '#sketchpad': 472509, '#artistoninstagram': 12329792, '#hobby': 20611603, '#coolart': 858412, '#artsy': 34021189, '#artista': 9163433, '#myart': 22992600, '#draw': 83872454, '#artofvisuals': 38795891, '#illustration': 154276422, '#instagramart': 2715232,
# '#follow': 621601721, '#artgram': 4081377, '#beautiful': 718211943, '#artwork': 129387066, '#artist': 224911759, '#instaart': 76452693, '#sketchbook': 55936702, '#arte': 79920695, '#artistic': 23624160, '#cool': 168570394, '#visualart': 9462473, '#artgallery': 24042115, '#drawing': 220757439, '#design': 263653890, '#arts': 23999192, '#cute': 611299929, '#followforfollowback': 163510105, '#tbt': 562007916, '#instagood': 1286816968, '#fun': 408885298, '#like4like': 529719895, '#artlife': 9337565, '#artesanato': 13360268, '#me': 439936113, '#picoftheday': 627111069, '#myself': 23027945, '#photooftheday': 885204776, '#followme': 560612818}
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

