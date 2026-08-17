# -*- coding: utf-8 -*-
import io, subprocess
PATH = r"c:\Users\kelvinyye\WorkBuddy\20260314103829\index.html"
with io.open(PATH, "r", encoding="utf-8") as f:
    cur = f.read()

def bal(s):
    return s.count("<div"), s.count("</div>")

# baseline on disk
o, c = bal(cur)
print("DISK FILE div: open=%d close=%d (delta %d)" % (o, c, o-c))

# HEAD committed version baseline
import subprocess as sp
head = sp.run(["git", "show", "HEAD:index.html"], cwd=r"c:\Users\kelvinyye\WorkBuddy\20260314103829", capture_output=True, text=True).stdout
ho, hc = bal(head)
print("HEAD div: open=%d close=%d (delta %d)" % (ho, hc, ho-hc))

# Read the script to get NEW strings by importing its literals
import importlib.util
spec = importlib.util.spec_from_file_location("u", PATH.replace("index.html","update_20260713.py"))
# Instead just eval the new-content strings by reading the script text
src = io.open(PATH.replace("index.html","update_20260713.py"), "r", encoding="utf-8").read()

# Extract NEW_S0_CARDS, NEW_S6_CARD, NEW_0713, NEW_S8_CARD1, STATS_NEW by simple splitting
def grab(varname):
    # find varname = ''' ... '''
    i = src.index(varname + " = '''")
    j = src.index("'''", i + len(varname) + 5)
    k = src.index("'''", j+3)
    return src[j+3:k]

blocks = {
  "STATS_NEW": grab("STATS_NEW"),
  "NEW_S0_CARDS": grab("NEW_S0_CARDS"),
  "NEW_S6_CARD": grab("NEW_S6_CARD"),
  "NEW_0713": grab("NEW_0713"),
  "NEW_S8_CARD1": grab("NEW_S8_CARD1"),
}
for name, b in blocks.items():
    bo, bc = bal(b)
    print("%-14s open=%d close=%d delta=%d" % (name, bo, bc, bo-bc))

# Also the OLD_0629 removed block
i = src.index("OLD_0629 = '''")
j = src.index("'''", i+len("OLD_0629 = '''"))
k = src.index("'''", j+3)
old0629 = src[j+3:k]
oo, oc = bal(old0629)
print("%-14s open=%d close=%d delta=%d (REMOVED)" % ("OLD_0629", oo, oc, oo-oc))
