def calculate_optimal_fare(d, t, v1, r, v2):
  # TODO: return minimal taxi fare (e.g. "3.14") or "Won't make it!"
  if v1 / 60.0 * t < d and v2 / 60.0 * t < d:
      return "Won't make it!"
      
  elif (v2 / 60.0)*t >= d:
      return '0.00'
      
  else:
     return "{0:.2f}".format(r * v1 * (d-v2 * (t/60.00)) / (v1-v2))
print calculate_optimal_fare(41, 237, 143, 3, 10) 
