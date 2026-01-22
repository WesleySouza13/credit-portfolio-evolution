# %% 
import os
import sys

print("CWD:", os.getcwd())
print("FILE:", __file__)
print("SYS.PATH:")
for p in sys.path:
    print("  ", p)


# %%
from src.data_eng.datarequest import Series_requests
# %%
print(os.getcwd())
# %%
