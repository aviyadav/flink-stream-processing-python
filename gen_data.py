import csv
import random

users = ["user" + str(i) for i in range(1, 50)]
pages = ["/home", "/products", "/cart", "/checkout", "/settings", "/about"]
start = 1634567890
f = open("clicks.csv", "w", newline="")
w = csv.writer(f)
[
    w.writerow(
        [
            random.choice(users),
            random.choice(pages),
            start + i * 5,
            random.randint(10, 300),
        ]
    )
    for i in range(10000)
]
f.close()
