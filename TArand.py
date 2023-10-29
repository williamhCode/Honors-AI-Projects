students = ['Juan', 'Charlene', 'Marcus', 'Thomas', 'Clark', 'Jonathan', 'Annie', 'Darren']
not_presenting = ['Jonathan', 'Annie', 'Darren', 'Thomas', 'Marcus']
make_up = False

if make_up:
    presenting = not_presenting
else:
    presenting = [student for student in students if student not in not_presenting]

import random
random.shuffle(presenting)
print()
for i, student in enumerate(presenting):
    print(student)
    print() if i == len(presenting) - 1 else input()
