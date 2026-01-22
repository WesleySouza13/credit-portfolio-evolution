
# %%
from datarequest import Series_requests

code = [20541, 433, 24369, 29037]
start = '01/03/2012'
end = '31/12/2025'
# %% 
response = Series_requests(code, start, end)
data = response.get_data()
response.concat()

response.to_parquet()
# %%
