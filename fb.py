import json
import random
import pprint
import csv

# fb info
with open('switch.json') as infile:
    info = json.load(infile)
    comments = info['data']

# ticket info
with open('attendees-updated.csv') as csv_infile:
    csv_reader = csv.reader(csv_infile)
    attendees = set()
    for row in csv_reader:
        tup = ' '.join(row).lower()
        if tup != '\ufefffirst name last name':
            attendees.add((tup))
print('# of attendees: {}'.format(len(attendees)))
# pprint.pprint(attendees)

 # all entries
all = []
for comment in comments:
    all.append(comment['from']['name'])
print('# of all entries: {}'.format(len(all)))

# tagged entries
tag = []
for comment in comments:
    if 'message_tags' in comment:
        tag.append(comment['from']['name'])
print('# of tagged entries: {}'.format(len(tag)))
# unique tagged entries
tag_unique = set()
for comment in comments:
    if 'message_tags' in comment:
        tag_unique.add((comment['from']['name'], comment['message_tags'][0]['id']))
print('# of unique tagged entries: {}'.format(len(tag_unique)))

# user tagged entries
user_tag = []
for comment in comments:
    if 'message_tags' in comment:
        if comment['message_tags'][0]['type'] == 'user':
            user_tag.append(comment['from']['name'].lower())
print('# of user tagged entries: {}'.format(len(user_tag)))
# unique user tagged entries
user_unique = set()
for comment in comments:
    if 'message_tags' in comment:
        if comment['message_tags'][0]['type'] == 'user':
            user_unique.add((comment['from']['name'].lower(), comment['message_tags'][0]['id']))
print('# of unique user tagged entries: {}'.format(len(user_unique)))

# valid entries (no duplicates, users only, no self-tag)
valid = set()
for comment in comments:
    if 'message_tags' in comment:
        if comment['message_tags'][0]['type'] == 'user':
            if comment['message_tags'][0]['id'] != comment['from']['id']:
                valid.add((comment['from']['name'].lower() , comment['message_tags'][0]['id']))
print('# of valid entries: {}'.format(len(valid)))
# pprint.pprint(valid)

# get all unique valid commenters
valid_commenters = []
for v in valid:
    valid_commenters.append(v[0].lower())
valid_commenters = set(valid_commenters)
print('# of unique valid commenters: {}'.format(len(valid_commenters)))
# pprint.pprint(valid_commenters)

# average valid entries per valid commenter
print('\naverage # of comments per valid person: {}\n'.format(round(len(valid)/len(valid_commenters), 2)))

# keep only eligible comments
eligible = set(valid)
to_remove = set()
for e in eligible:
    if e[0] not in attendees:
        to_remove.add(e)
# print('len of names to remove from eligible: {}'.format(len(to_remove)))
for r in to_remove:
    eligible.remove(r)
print('# of eligible comments: {}'.format(len(eligible)))
# pprint.pprint(eligible)

# number of eligible commenters
eligible_commenters = set()
for e in eligible:
    eligible_commenters.add(e[0])
print('# of eligible commenters: {}'.format(len(eligible_commenters)))
# pprint.pprint(eligible_commenters)

# average eligible entries per eligible commenter
print('\naverage # of comments per eligible person: {}\n'.format(round(len(eligible)/len(eligible_commenters), 2)))

# factor in the ticket holders for the final set
final = set(eligible)
for a in attendees:
    final.add((a, '1'))
    final.add((a, '2'))
    final.add((a, '3'))
print('# of final comments: {}'.format(len(final)))
# pprint.pprint(final)

for i in range(20):
    final.add(('allen gour', i+5))

for i in range(10):
    final.add(('jessica yang', i+5))

# number of final commenters
final_commenters = set()
for f in final:
    final_commenters.add(f[0])
print('# of final commenters: {}'.format(len(final_commenters)))

# average eligible entries per final commenter
print('\naverage # of comments per final person: {}\n'.format(round(len(final)/len(final_commenters), 2)))

# count of each person's final entry
tracker = dict()
for f in final:
    if f[0] in tracker:
        tracker[f[0]] += 1
    else:
        tracker[f[0]] = 1
# pprint.pprint(tracker)

# stats
num_final_comments = len(final)
num_final_commenters = len(final_commenters)

final_stats = dict()
for f in tracker.keys():
    final_stats[f] = (tracker[f], round(tracker[f]/num_final_commenters, 3))
print('FINAL STATS')
pprint.pprint(final_stats)
# print('length of final_stats: {}'.format(len(final_stats)))


def num(name, cat):
    if (cat == 'ALL'):
        return all.count(name)
    elif (cat == 'TAG'):
        return tag.count(name)
    elif (cat == 'USER'):
        return user_tag.count(name)
    else:
        return False

def num_unique(name, cat):
    counter = dict()
    if (cat == 'TAG'):
        to_count = tag_unique
    elif (cat == 'USER'):
        to_count = user_unique
    elif (cat == 'VALID'):
        to_count = valid
    for com in to_count:
        if com[0] in counter:
            counter[com[0]] += 1
        else:
            counter[com[0]] = 1
    return counter[name]

def list_unique_tags(name):
    for com in valid:
        if com[0] == name:
            print(com[1])

# number of unique commenters
print('\n# of unique commenters (all): {}'.format(len(set(all))))
print('# of unique commenters (tag): {}'.format(len(set(tag))))
print('# of unique commenters (user): {}'.format(len(set(user_tag))))


# friends check
friends = ['Allen Gour', 'Jessica Yang', 'Brendon Chiang', 'Ben Hwang', 'Hilton Nguyen']
# all entries
# print('\nFriend entries (all):')
# for friend in friends:
#     print('\t# of entries for {}: {}'.format(friend, num(friend, 'ALL')))
# tagged entries
'''
print('\nFriend entries (tagged):')
for friend in friends:
     print('\t# of entries for {}: {}'.format(friend, num(friend, 'TAG')))
# unique tagged entries
print('\nFriend entries (unique tagged)')
for friend in friends:
    print('\t# of entries for {}: {}'.format(friend, num_unique(friend, 'TAG')))
# user tagged entries
print('\nFriend entries (user):')
for friend in friends:
    print('\t# of entries for {}: {}'.format(friend, num(friend.lower(), 'USER')))
# unique user tagged entries
print('\nFriend entries (unique user)')
for friend in friends:
    print('\t# of entries for {}: {}'.format(friend, num_unique(friend.lower(), 'USER')))
# valid entries
print('\nFriend entries (valid)')
for friend in friends:
    print('\t# of entries for {}: {}'.format(friend, num_unique(friend.lower(), 'VALID')))
print('\n')
'''
# print('\nall of Allen\'s tags:')
# list_unique_tags('Allen Gour')

# +20 new tags
# 2127041077326892/?fields=comments.limit(10){from,message,message_tags}


# WINNERS

# pick a winner at random
def winner(contestants):
    winner = random.choice(list(contestants))
    return winner[0]

# run it sample number of times
winners = []
sample = 10
for i in range(sample):
    winners.append(winner(final))

# count the stats
wins = dict()
for w in winners:
    if w in wins:
        wins[w] += 1
    else:
        wins[w] = 1

# winning stats for given sample size
win_stats = dict()
for w in wins.keys():
    win_stats[w] = (wins[w], round(wins[w]/sample, 3))
print('\nWIN STATS')
pprint.pprint(win_stats)

print('\nWINNER (1 DRAW): {}'.format(winner(final).upper()))
