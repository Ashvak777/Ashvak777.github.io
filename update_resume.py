#!/usr/bin/env python3
"""
Resume Update Helper
Helps manage resume updates and automatically updates the extraction tool
"""

import os
import shutil
from pathlib import Path
import glob

def list_resume_files():
    """List all resume files in the resume folder"""
    resume_dir = Path("resume")
    if not resume_dir.exists():
        print("❌ Resume folder not found!")
        return []
    
    files = list(resume_dir.glob("*.docx"))
    return files

def update_extraction_script(filename):
    """Update the extraction script with the new filename"""
    script_path = "extract_resume.py"
    
    if not Path(script_path).exists():
        print("❌ extract_resume.py not found!")
        return False
    
    # Read the current script
    with open(script_path, 'r') as f:
        content = f.read()
    
    # Update the filename
    old_line = 'docx_file = "resume/Ashvak_PowerBI_Fabric_Developer.docx"'
    new_line = f'docx_file = "resume/{filename}"'
    
    if old_line in content:
        content = content.replace(old_line, new_line)
        
        # Write the updated script
        with open(script_path, 'w') as f:
            f.write(content)
        
        print(f"✅ Updated extract_resume.py to use: {filename}")
        return True
    else:
        print("❌ Could not find the filename line in extract_resume.py")
        return False

def main():
    print("📁 Resume Management Tool")
    print("=" * 40)
    
    # List current resume files
    files = list_resume_files()
    
    if not files:
        print("📝 No resume files found in resume/ folder")
        print("\n💡 To add a resume:")
        print("1. Place your .docx file in the resume/ folder")
        print("2. Run this script again")
        return
    
    print(f"📄 Found {len(files)} resume file(s):")
    for i, file in enumerate(files, 1):
        print(f"  {i}. {file.name}")
    
    if len(files) == 1:
        filename = files[0].name
        print(f"\n🎯 Using: {filename}")
        
        # Update the extraction script
        if update_extraction_script(filename):
            print("\n🔄 Running resume extraction...")
            os.system("python3 extract_resume.py")
            
            print("\n✅ Resume update complete!")
            print("📋 Next steps:")
            print("1. Review resume_data.json for structured information")
            print("2. Check html_updates.txt for suggested updates")
            print("3. Update your HTML with new information")
        else:
            print("❌ Failed to update extraction script")
    else:
        print("\n🤔 Multiple resume files found. Please:")
        print("1. Keep only the latest resume in the resume/ folder")
        print("2. Run this script again")

if __name__ == "__main__":
    main() 