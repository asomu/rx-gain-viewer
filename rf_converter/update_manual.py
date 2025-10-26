# Update manual with s1p~s12p support
with open('사용자_매뉴얼.md', 'r', encoding='utf-8') as f:
    content = f.read()

# Update supported file formats section
old_text = '''### 지원하는 파일 형식
- ✅ `.s1p` - 1-port S-parameter
- ✅ `.s2p` - 2-port S-parameter (가장 일반적)
- ✅ `.s3p` - 3-port S-parameter
- ✅ `.s4p` - 4-port S-parameter
- ✅ 대소문자 구분 없음 (`.S2P`, `.s2p` 모두 인식)'''

new_text = '''### 지원하는 파일 형식
- ✅ `.s1p` ~ `.s12p` - 1-port ~ 12-port S-parameter
- ✅ `.s2p` - 2-port (가장 일반적)
- ✅ `.s8p`, `.s9p`, `.s10p`, `.s11p`, `.s12p` - 다중 포트 지원
- ✅ 대소문자 구분 없음 (`.S2P`, `.s2p` 모두 인식)

**지원 범위**: s1p, s2p, s3p, s4p, s5p, s6p, s7p, s8p, s9p, s10p, s11p, s12p'''

content = content.replace(old_text, new_text)

with open('사용자_매뉴얼.md', 'w', encoding='utf-8') as f:
    f.write(content)

print("[OK] Manual updated with s1p~s12p support")
