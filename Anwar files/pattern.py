def print_pattern(rows):
    for i in range(1, rows + 1):
        print(' ' * (rows - i) + chr(65 + i - 1) * i)

rows = 3  # Number of rows in the pattern
print_pattern(rows)
