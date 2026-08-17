roll_number = 1024170013

digits = [int(digit) for digit in str(roll_number)]
L = [digit * 10 for digit in digits]

scores = tuple(L[:8])

print(scores)

highest = max(scores)
highest_index = scores.index(highest)

lowest = min(scores)
lowest_count = scores.count(lowest)

print(highest)
print(highest_index)
print(lowest)
print(lowest_count)

reversed_scores = list(reversed(scores))
print(reversed_scores)

score = int(input("Enter a score: "))

if score in scores:
    print(scores.index(score))
else:
    print("Score is not present in the tuple.")

try:
    scores[0] = 100
except TypeError as e:
    print(e)

first_score, second_score, *remaining_scores = scores

print(first_score)
print(second_score)
print(remaining_scores)