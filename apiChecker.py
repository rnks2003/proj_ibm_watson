import os
for i in os.environ:
    print(f"{i} === {os.environ[i]}")

print('\n\n\n')
print(os.environ)