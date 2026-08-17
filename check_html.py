import codecs

with codecs.open('c:/Users/kelvinyye/WorkBuddy/20260314103829/index.html', 'r', 'utf-8') as f:
    content = f.read()

print('Total chars:', len(content))
print('</html> at:', content.rfind('</html>'))
print('</body> at:', content.rfind('</body>'))
print('footer at:', content.find('class="footer"'))
print('Has Section 7:', 'Section 7' in content)

# Find S7 section and check if it's properly closed
s7_idx = content.find('Section 7')
if s7_idx > 0:
    print('S7 section found at char:', s7_idx)
    # Count open/close div after S7
    after_s7 = content[s7_idx:]
    opens = after_s7.count('<div')
    closes = after_s7.count('</div>')
    print('DIVs after S7 - open:', opens, 'close:', closes)

# Show what's after the last timeline-item
last_timeline = content.rfind('timeline-item')
if last_timeline > 0:
    after = content[last_timeline:last_timeline+500]
    print('After last timeline-item:')
    print(after)

print()
print('Last 300 chars of file:')
print(repr(content[-300:]))
