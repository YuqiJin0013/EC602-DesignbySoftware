"""hw4 checker: wedding"""
import hashlib
import itertools
import os
import random
import subprocess as sub
import sys
import time
import unittest

# 1.0 2021 wedding
# 1.1 negative speed scores no longer possible
# 1.2 better speed normalization
# 1.3 clean up process code, fix refcode numbers
# 2.0 adapt to curl_grading
# 3.0 python version
# 3.1 fall 2022 version
# 3.2 bug fixes
# 3.3 more bug fixes
# 3.5 fix false 100% value
# 3.6 allow itertools

COURSE = 'ec602'
SEMESTER = "fall2023"
hw="HW4"

DEBUG = True

TIME_ALLOWED = 30


VERSION, CURL_GRADING_VER = (3,6), (3, 6)



def update_curl_grading():
    print('updating curl_grading')
    from requests import get
    r = get('https://curl.bu.edu/static/content/curl_grading.py')
    with open('curl_grading.py','w') as f:
        f.write(r.text)

def get_curl_grading():
    from os import listdir
    files = listdir();
    if "curl_grading.py" not in files:
        update_curl_grading()

    import curl_grading as e
    if e.VERSION < CURL_GRADING_VER:
        update_curl_grading()
        from importlib import reload
        e = reload(e)

    return e

curl_grading = get_curl_grading()



popen_specs={'stdout':sub.PIPE,'stdin':sub.PIPE,'stderr':sub.PIPE,
'universal_newlines':True}


def ask_program(process,command):
    process.stdin.write(command+'\n')
    process.stdin.flush()
    return process.stdout.readline().strip()


def check(answer,youranswer,case):
    if youranswer != answer:
        return "problem with case {}\n correct: {}\n   yours: {}\n".format(case,repr(answer),repr(youranswer))   
    return ""

def hexcheck(answer,youranswer,case):
    phrase, myhex = answer.rsplit("= ",1)
    phrase, yourval = youranswer.rsplit("= ",1)
    yourval = yourval.split()
    yourval.sort()
    yourval = "\n".join(yourval)

    h = hashlib.sha256()
    h.update(yourval.encode())
    summary = h.hexdigest()[:10]

    if summary != myhex:
        return "problem with case {}. My digest: {}, your digest: {}\n".format(phrase,myhex,summary)
    return ""

def hexdigest_summary(text):
    h = hashlib.sha256()
    h.update(text.encode())
    return h.hexdigest()[:10]

# TEST CASE DATA
Tests={}
Tests['standard']= [
{'cmd':'tests','hex':'f31e6d4c65'},
]

Tests['barriers']=[
{'cmd':'b ab 1 0','ans':'2 |ab |ba'},
{'cmd':'b @#$%^ 5 0 1 2 3 4','ans':'1 |@|#|$|%|^'},
{'cmd':'b ABxy 1 2','ans':'5 AB|xy AB|yx BA|xy BA|yx yB|xA'},
{'cmd':'b ABCDEFGHI 2 3 6','hex':'a4404840f9'},
{'cmd':'bp ABCDEFGHI 2 3 6 30','ans':'39 IBC|DFE|HGA'},
{'cmd':'bp ABCDEFGHIabcdef 1 0 30','ans':'987 |ABCDEFGIHbacdfe'},
]

Tests['shuffles']=[
{'cmd':'s ab','ans':'2 ab ba'},
{'cmd':'s @#$%^','ans':'13 #$%^@ #@$%^ #@$^% #@%$^ @#$%^ @#$^% @#%$^ @$#%^ @$#^% ^#$%@ ^#%$@ ^$#%@ ^@#$%'},
{'cmd':'s ABxy','ans':'9 ABxy AByx AxBy BAxy BAyx BxyA yABx yBxA yxBA'},
{'cmd':'s ABCDEFGHI','hex':'62695215f1'},
{'cmd':'sp ABCDEFGHI 75','ans':'78 ICBEDFGHA'},
{'cmd':'sp ABCDEFGHIabcdef 200','ans':'1366 ABCEDGFHIabcdfe'},
]

Tests['speed'] =[
{'cmd':"""sp abcdefghijklmnopqrstu 24000
sp abcdefghijklmnopqrstu 24000
sp abcdefghijklmnopqrstuvwxyz12 10000
sp cdefghijklmnopqrstuvwxyz1234 100000
bp cdefghijklmnopqrstuvwxyz1234 3 5 10 16 1000""",
'ans':"""
24478 ucbedfhgikjmlnpoqrtsa
24478 ucbedfhgikjmlnpoqrtsa
710649 2bcdefgihkjlnmopqrtsuvxwyz1a
710649 4dfegihkjlmnoqprtsuwvyxz132c
268736 4defg|hijkl|monprq|tsvuxwy1z23c
""".strip().replace('\n'," ")
}
]

class WeddingTestCase(unittest.TestCase):
    "hw4_wedding.py"
    def fullfail(self,test,msg):
      self.Points[test] = 0
      self.fail(msg)

    def run_test(self,testname, points=None):
        "run 'testname' check the answer, deduct points if specified"
        for test in Tests[testname]:
            cmd=test['cmd']
            with self.subTest(CASE=f"{testname}:{cmd}"):
              try:
                T = sub.run(['python','hw4_wedding.py'],input=f"{cmd}\nquit\n",
                  stdout=sub.PIPE,stderr=sub.PIPE,universal_newlines=True,timeout=TIME_ALLOWED)
                _,result = T.stdout.split("n barriers ind\n")
                result += "\n" + T.stderr
                result = result.strip()
              except Exception as e:
                self.fullfail(testname,str(e))

              if 'hex' in test:
                  hexs = hexdigest_summary(result)
                  ans = test['hex']
                  if hexs != ans:
                      msg=f"My hexdigest: {ans} Your hexdigest: {hexs}\n"
                      if not points:
                          self.fullfail(testname,msg)
                      else:
                          self.Points[testname] -= points
                          self.fail(msg)
              elif 'ans' in test:
                  result = result.replace('\n',' ')
                  if result  != test['ans']:
                    msg=f"your answer:\n{result}\nanswer:\n{test['ans']}"
                    if not points:
                          self.fullfail(testname,msg)
                    else:
                      self.Points[testname] -= points
                      self.fail(msg)


    @classmethod
    def setUpClass(cls):
        cls.Points={"standard":10,"shuffles":25,"barriers":25,"speed":30,"style":10}
        cls.MaxPoints = cls.Points.copy() 
        cls.Penalty = {'libraries':100,'authors':100}
        cls.stylemax = cls.Points['style']
        cls.authorlimit = 3
        cls.valid_includes ={"itertools"}

        cls.refcode = {'lines':125,'words':437}
        cls.msgs=[]
        cls.realfilename = tested_programs[cls.__doc__]

        with open(cls.realfilename) as f:
            cls.file_contents=f.read()



        cls.code_metrics = curl_grading.code_analysis_py('hw4_wedding.py')


    test_libraries = curl_grading.test_libraries
    test_authors = curl_grading.test_authors
    test_style = curl_grading.test_style

    def test_barriers(self):
      "barriers. various additional tests"
      self.run_test('barriers',self.Points['barriers']/len(Tests['barriers']))

    def test_shuffles(self):
      "shuffles. various additional tests"
      self.run_test('shuffles',self.Points['shuffles']/len(Tests['shuffles']))

    def test_standard(self):
      "standard. standard tests included in main."
      self.run_test('standard')

  
    def test_speed(self):
      "speed. is your program efficient"
      # my program is 0.56 g/s rating
      speed_rating = 1
      # speed_rating > 1 : your computer is fast
      # 
      start_time = time.time()
      self.run_test('speed')
      end_time = time.time()
      duration = end_time - start_time
      your_time = duration * speed_rating
      self.msgs.append(f'speed: your computers speed (larger is faster): {speed_rating:.3g}')
      self.msgs.append(f'speed: your actual duration {duration:5.3g}')
      self.msgs.append(f'speed: your normalized time {your_time:5.3g}')

      # my program takes 6.7 seconds
      TARGET = 12
      BONUS_TARGET = 7
      if your_time > TARGET:
        timepenalty = 5*(your_time - TARGET)
        self.Points['speed'] -=  timepenalty
        if self.Points['speed'] < 0:
          self.Points['speed'] = 0
        self.msgs.append(f'speed: target is {TARGET}, 5 pts off for each second over.\n')
        
        self.fail(f'Failed to make target time of {TARGET}. Your normalized time:{your_time:.2g}.')
      elif your_time < BONUS_TARGET:
        bonus = 2 * (BONUS_TARGET - your_time)
        if self.Points['speed']:
           self.Points['speed'] += bonus
           self.msgs.append(f'speed: bonus points awarded! {bonus:5.3g}\n')
      else:
        self.msgs.append(f"speed: met target time of {TARGET} sec\n")



testcases={
'hw4_wedding.py':WeddingTestCase,
}
programs = ['hw4_wedding.py']
tested_programs = {x:x for x in programs}



if __name__ == '__main__':
    s= ' ({0} Checker Version {1}.{2})'.format(hw,*VERSION)
    g={}
    for prog in testcases:
        print(f'\n\n {hw} checker version',VERSION,"checking",prog)
        testcases[prog].program = prog
        report, g[prog] = curl_grading.check_program(testcases[prog],
          versioninfo=s,course=COURSE)
        print(report)
    print(f'\nGrade Summary for {hw}')
    print("=====================")
    for prog in testcases:
      print(prog,f"{g[prog]:5.2f}")