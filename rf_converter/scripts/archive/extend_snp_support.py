# Extend SnP file support to s1p ~ s12p
import re

# 1. Update UI file_selector.py
print("1. Updating file_selector.py...")
with open('ui_pyqt6/widgets/file_selector.py', 'r', encoding='utf-8') as f:
    content = f.read()

old_pattern = r'''# Find all \.s2p files \(case insensitive\)
        snp_files = list\(folder_path\.glob\('\*\.s2p'\)\) \+ list\(folder_path\.glob\('\*\.S2P'\)\)

        # Also check for other SnP formats
        for ext in \['s1p', 's3p', 's4p', 'S1P', 'S3P', 'S4P'\]:
            snp_files\.extend\(folder_path\.glob\(f'\*\.\{ext\}'\)\)'''

new_code = '''# Find all SnP files from s1p to s12p (case insensitive)
        snp_files = []
        
        # Support s1p ~ s12p
        for i in range(1, 13):
            snp_files.extend(folder_path.glob(f'*.s{i}p'))
            snp_files.extend(folder_path.glob(f'*.S{i}P'))'''

content = re.sub(old_pattern, new_code, content)

with open('ui_pyqt6/widgets/file_selector.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("   [OK] file_selector.py updated")

# 2. Update Core conversion_service.py
print("2. Updating conversion_service.py...")
with open('core/services/conversion_service.py', 'r', encoding='utf-8') as f:
    content = f.read()

content = re.sub(
    r"valid_extensions = \['.s1p', '.s2p', '.s3p', '.s4p'\]",
    "valid_extensions = [f'.s{i}p' for i in range(1, 13)]  # s1p ~ s12p",
    content
)

with open('core/services/conversion_service.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("   [OK] conversion_service.py updated")

# 3. Update SnpReader
print("3. Updating snp_reader.py...")
with open('core/parsers/snp_reader.py', 'r', encoding='utf-8') as f:
    content = f.read()

old_code = '''    def _detect_num_ports(self) -> int:
        """Detect number of ports from file extension"""
        ext = self.file_path.suffix.lower()
        if ext == '.s1p':
            return 1
        elif ext == '.s2p':
            return 2
        elif ext == '.s3p':
            return 3
        elif ext == '.s4p':
            return 4
        else:
            raise ValueError(f"Unknown SnP file extension: {ext}")'''

new_code = '''    def _detect_num_ports(self) -> int:
        """Detect number of ports from file extension (s1p ~ s12p)"""
        ext = self.file_path.suffix.lower()
        
        # Extract port number from extension (.s2p -> 2, .s12p -> 12)
        import re
        match = re.match(r'\.s(\d+)p', ext)
        if match:
            num_ports = int(match.group(1))
            if 1 <= num_ports <= 12:
                return num_ports
        
        raise ValueError(f"Unsupported SnP file extension: {ext} (s1p~s12p supported)")'''

content = content.replace(old_code, new_code)

with open('core/parsers/snp_reader.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("   [OK] snp_reader.py updated")

print("")
print("[SUCCESS] All files updated!")
print("Supported: s1p ~ s12p")
print("")
print("[WARNING] GUI restart required")
