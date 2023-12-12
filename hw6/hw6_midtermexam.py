# Copyright 2023 Yuqi Jin yuqijin8@bu.edu


# Part one
"""
Write a function with the following signature:

   def translate(msg,convert):


that converts the values of a sequence (msg) based on a translation dictionary (convert)
and returns the new sequence as a tuple.

This is best described with examples.


message = (5,6,7)
converter = {7:"this", 5:"a", "a":"one"}
a = translate(message, converter) 
print(a)


The result will be

    ('a', 6, 'this')

Basically, if an element of the message is a key of the translation dictionary, it should
be "translated" by being replaced with the value associated with that key in the translation dictionary.


Here are a few other examples

translate( (1,2,3),{1:"one",2:"two",3:"three"}) -> ("one","two","three")      # numbers to English 
translate( ("a","b","c"),{"a":"z","b":"y","c":"x"}) -> ("z","y","x")          # substitution cipher
translate( ("I","am","Paul"), {"am":"suis","I":"Je"}) -> ("Je","suis","Paul") # English to French
translate( ["I","am","Paul"], {}) -> ("I","am","Paul")                        # no translation
translate( range(5), {}) -> (0, 1, 2, 3, 4)                                   # no translation


"""

# You may include test code to test your function `translate`. 
# However, your program, if imported, should run through (no inputs, etc)  
def translate(msg, convert):
    message = []
    for char in msg:
        if char in convert:
            message.append(convert[char])
        else:
            message.append(char)
    
    return tuple(message)

# part 2
"""
Write a class 'SmartBulb' that models an internet-enabled 
dimmable light bulb:

- the constructor should require that it be provided an IPv4 address
  in the form of a 4-tuple of 8-bit integers, and a port number in int16 format.

- when the light is first created, the light is neither on nor off. It is "undeclared."

- the light can be turned off with an "off" method, "on" with a "on" method, or
dimmed to 0-100% with a "dim" method.

- objects of type SmartBulb should evaluate to "True" when the light is on, and 
"False" when the light is off.

- the brightness can be discovered with a "brightness" method-- returning a number
  between 0 (completely off) and 1 (fully on).

- whenever the requirements are not satisfied -- for the constructor, for the dim method,
or for the True/False evaluation, a ValueError exception should be raised.

Here is some example test code:

```
s = SmartBulb( (10,0,0,234), 64123 )
s.off()

if s:
  print("the light is on")

s.dim(0.3)
if s:
  print("the light is at", s.brightness()*100, "percent")

s.on()
if s:
  print("the light is at", s.brightness()*100, "percent")

q = SmartBulb( (10,0,0,234), 64123 )
try:
  if q:
    print("the light is on")
except:
  print("???")
```

The test code shown should print

the light is at 30.0 percent
the light is at 100 percent
???


"""

# You may include test code to test your class SmartBulb
# However, your program, if imported, should run through (no inputs, etc)
class SmartBulb:
    # build a constructor IPv4 address and port_number
    def __init__(self, ip_address, port):
        if not isinstance(ip_address, tuple) or len(ip_address) != 4:
            raise ValueError("The form of IPv4 address is invalid")
        if not all(0 <= octet <= 255 for octet in ip_address):
            raise ValueError("The form of IPv4 address is not 8-bit integers")
        if not isinstance(port, int):
            raise ValueError("The form of port number is invalid")
        if not 0 <= port <= 65535:
            raise ValueError("The form of port number is not int16 format")
        self.ip_address = ip_address
        self.port = port
        self.state = None # default bulb state is None also means undeclared
        self.brightness_level = 0.0  # default brightness value
    
    # build on method
    # on is true
    def on(self):
        self.state = True
        self.brightness_level = 1.0
    
    # build off method
    # off is false
    def off(self):
        self.state = False
        self.brightness_level = 0.0
    
    def dim(self, level):
        if not isinstance(level, (int, float)):
            raise ValueError("The input level value type is not valid")
        if not (0 <= level <= 100):
            raise ValueError("The brightness level should be between 0 and 100")
        self.state = True if level > 0 else False
        self.brightness_level = level 
    
    # build brightness method
    def brightness(self):
        return self.brightness_level
    
    # True/False evaluation
    # when state is None, it means undeclared
    def __bool__(self): 
        if self.state is None:
            raise ValueError("The state of the bulb is undeclared")
        return self.state

# example test case #
# s = SmartBulb( (10,0,0,234), 64123 )
# s.off()

# if s:
#   print("the light is on")

# s.dim(0.3)
# if s:
#   print("the light is at", s.brightness()*100, "percent")

# s.on()
# if s:
#   print("the light is at", s.brightness()*100, "percent")

# q = SmartBulb( (10,0,0,234), 64123 )
# try:
#   if q:
#     print("the light is on")
# except:
#   print("???")

# part 3
"""
You are provided a database of student records, (as a list of tuples)
each of which has one of these formats

    student-id-formatA, LastName, Firstname, Middlename
    student-id-formatA, LastName, Firstname

    student-id-formatB, LastName, Firstname, Middlename
    student-id-formatB, LastName, Firstname

The two formats for student IDs look like this

student-id-formatA:  uX  where x is a decimal number between 1000 and 999999
student-id-formatB:  uqqqqqqqq where `qqqqqqqq` is an eight-digit zero-filled number.

There is overlap in these formats, in the sense that if the numerical value
of `X` and `qqqqqqqq` are the same, then this is the same person.

The university wants to merge these records and use a new format called "student-id-formatC"
for all student ids, like this:

    Uxxx-yyy-zzz

The new student number `xxxyyyzzz` is a nine-digit zero-filled decimal number


Other facts:

- some students can appear in the database more than once: either with or 
without a middle name, and either in ID-A format or ID-B format.

- any two people with the same student number (whether written in A, B, or C format)  
*ARE* the same person, even if their names appear differently.

YOUR TASKS

1. Count the number of unique students in the database, naming the result  `n_students`

2. Convert the database into one with a single format: a JSON object
  which is an array of student objects, each object in the format

  {"id":formatC, "last":LastName, "first":FirstName, "middle":MiddleName}

  You should use `json.dumps` to create your final database, with name `student_database`

  NOTE NOTE NOTE
  --------------

  DO NOT create a new file: if you use json.dump instead of json.dumps you will get a zero
  on this part of the exam.


Specifications
--------------

- If the middle name is empty, then the key "middle" should still be present, but
  its value should be the empty string.

- Duplicates should be eliminated, with preference to those records that
  had a middle name included.

- If a student appears twice or more in the original database with all three names 
  defined, the record that appears later in the database (by index) should be kept. 
  This represents the situation whereby an individual has changed their name.


The database to use is available on the course website at 


 https://curl.bu.edu:9602/inclass/raw_student_info.json

as a json file.

"""
"""Write a python function student_merge with the following signature
def student_merge(fname : str ) -> int, str
    that returns the values of n_students and student_database as described in the midterm exam part three. """
import json
import pandas as pd

def convert_to_format_C(str, length):
    start_letter = str[0]
    numbers = str[1:]
    result = start_letter + numbers.zfill(length - 1)
    result = result[0:4] + '-' + result[4:7] + '-' + result[7:]
    result = result.capitalize()
    return result

def student_merge(fname: str) -> (int, str):
    with open(fname) as file:
        db = json.load(file)
        
    for record in db:
        # even they don't have middle name, append the empty string
        if len(record) == 3:
            record.append("")
        if record[0].startswith('u0'):
            # cut the leading zeros if this id has 
            record[0] = record[0][0] + record[0][1:].lstrip('0')
    
    # create new panda frame{"id":formatC, "last":LastName, "first":FirstName, "middle":MiddleName}
    df = pd.DataFrame(db, columns = ["id", "last", "first", "middle"])
    df = df.drop_duplicates(subset = ['id'], keep = 'last')
    
    df['id'] = df['id'].apply(convert_to_format_C, length = 10)
    n_students = df['id'].nunique()
    student_database = json.dumps(df.to_dict(orient='records'), indent=2)
    
    return n_students, student_database

# fname = "raw_student_info.json"
# n_students, student_database = student_merge(fname)
# print("Number of unique students:", n_students)
# print("Student Database:", student_database)