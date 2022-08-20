import numpy as num
import pandas as pd

M_Balanceado = num.zeros(12)
M_Balanceado[4] =4

import numpy as num
import pandas as pd

fsi = num.zeros((10, 20, 12))
print(fsi)

# The counter function counts down from start to stop when start is bigger than stop,
# and counts up from start to stop otherwise. Fill in the blanks to make this work correctly.
def counter(start, stop):
    x = start
	if ___:
		return_string = "Counting down: "
		while x >= stop:
			return_string += str(x)
			if ___:
				return_string += ","
			___
	else:
		return_string = "Counting up: "
		while x <= stop:
			return_string += str(x)
			if ___:
				return_string += ","
			___
	return return_string

print(counter(1, 10)) # Should be "Counting up: 1,2,3,4,5,6,7,8,9,10"
print(counter(2, 1)) # Should be "Counting down: 2,1"
print(counter(5, 5)) # Should be "Counting up: 5"

kreuzberg turke
neucol turke
marchzan langweilig
schalotenbuch russisch