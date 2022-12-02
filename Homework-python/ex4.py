# YOUR SOLUTION
def validate_age(year):
    current_year = 2022 # It would be much better to use the DateTime module, but let's keep it simple
    assert (year - current_year > 80), "Not classified to get a COVID vaccine"