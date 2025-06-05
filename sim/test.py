from .units import Unit, Value
from .initvals import IV
from .funcs import TERMS

leak = TERMS.leak(IV.V)
potassium = TERMS.potassium(IV.V, IV.n)
sodium = TERMS.sodium(IV.V, IV.m, IV.h)

print(leak, potassium, sodium)
print(leak + potassium + sodium)
