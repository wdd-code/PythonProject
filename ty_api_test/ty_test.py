import urllib.parse
file_str = urllib.parse.quote('Template (5)_20250307110538434.csv')
file_str2 = urllib.parse.unquote('%E6%B5%8B%E8%AF%95')
file3 = urllib.parse.quote(file_str2)
print(file_str)
print(file_str2)
print(file3)