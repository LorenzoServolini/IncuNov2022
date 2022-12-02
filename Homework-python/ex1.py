def weird_sum():
    result = 0;
    for i in range(1,6):
      result += sum(i, i-1)
      print(sum(i, i-1))
    return result

def sum(a,b):
  sum = a+b
  return sum

print(weird_sum())