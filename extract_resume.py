#!/usr/bin/env python3
"""
Resume Text Extractor
Extracts text from Word document and structures it for HTML updates
"""

import docx
import json
import re
from pathlib import Path

def extract_text_from_docx(file_path):
    """Extract text from DOCX file"""
    try:
        doc = docx.Document(file_path)
        full_text = []
        
        for paragraph in doc.paragraphs:
            if paragraph.text.strip():
                full_text.append(paragraph.text.strip())
        
        return '\n'.join(full_text)
    except Exception as e:
        print(f"Error reading DOCX file: {e}")
        return None

def structure_resume_data(text):
    """Structure the resume text into organized sections"""
    sections = {
        'personal_info': {},
        'summary': '',
        'experience': [],
        'skills': [],
        'education': [],
        'certifications': []
    }
    
    lines = text.split('\n')
    current_section = None
    current_experience = None
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Detect sections
        if 'professional experience' in line.lower() or 'work experience' in line.lower():
            current_section = 'experience'
            continue
        elif 'education' in line.lower():
            current_section = 'education'
            continue
        elif 'skills' in line.lower() or 'technical' in line.lower():
            current_section = 'skills'
            continue
        elif 'certification' in line.lower():
            current_section = 'certifications'
            continue
        elif 'summary' in line.lower() or 'objective' in line.lower():
            current_section = 'summary'
            continue
            
        # Process content based on current section
        if current_section == 'experience':
            # Look for company/client patterns
            if any(keyword in line.lower() for keyword in ['client:', 'company:', 'gisa', 'scotiabank', 'rbc', 'bell', 'wsib']):
                if current_experience:
                    sections['experience'].append(current_experience)
                current_experience = {
                    'company': line,
                    'role': '',
                    'dates': '',
                    'responsibilities': [],
                    'environment': ''
                }
            elif current_experience:
                # Check for role and dates
                if 'role:' in line.lower():
                    current_experience['role'] = line
                elif 'dates:' in line.lower() or '–' in line or '-' in line:
                    current_experience['dates'] = line
                elif 'environment' in line.lower():
                    current_experience['environment'] = line
                elif line.startswith('•') or line.startswith('-') or line.startswith('*'):
                    current_experience['responsibilities'].append(line)
                elif 'responsibilities:' in line.lower():
                    continue  # Skip the header
                else:
                    # If it's not a responsibility bullet, it might be a continuation
                    if current_experience['responsibilities']:
                        current_experience['responsibilities'][-1] += ' ' + line
                    else:
                        current_experience['responsibilities'].append(line)
        
        elif current_section == 'skills':
            if any(skill in line.lower() for skill in ['power bi', 'azure', 'sql', 'python', 'fabric', 'microsoft', 'data', 'etl']):
                sections['skills'].append(line)
        
        elif current_section == 'education':
            if any(edu in line.lower() for edu in ['university', 'college', 'degree', 'bachelor', 'master', 'certified']):
                sections['education'].append(line)
        
        elif current_section == 'certifications':
            if any(cert in line.lower() for cert in ['certified', 'microsoft', 'azure', 'power bi', 'fabric', 'associate']):
                sections['certifications'].append(line)
        
        elif current_section == 'summary':
            sections['summary'] += line + ' '
    
    # Add the last experience if exists
    if current_experience:
        sections['experience'].append(current_experience)
    
    return sections

def generate_html_updates(sections):
    """Generate HTML update suggestions"""
    updates = []
    
    # Experience updates
    if sections['experience']:
        updates.append("// EXPERIENCE UPDATE:")
        for exp in sections['experience']:
            updates.append(f"// Company: {exp.get('company', 'N/A')}")
            updates.append(f"// Role: {exp.get('role', 'N/A')}")
            updates.append(f"// Dates: {exp.get('dates', 'N/A')}")
            updates.append("// Key Responsibilities:")
            for resp in exp.get('responsibilities', [])[:5]:  # First 5 responsibilities
                updates.append(f"// - {resp}")
            if exp.get('environment'):
                updates.append(f"// Environment: {exp.get('environment')}")
            updates.append("")
    
    # Skills updates
    if sections['skills']:
        updates.append("// SKILLS UPDATE:")
        updates.append("// Add these skills to the appropriate categories:")
        for skill in sections['skills']:
            updates.append(f"// - {skill}")
        updates.append("")
    
    # Certifications update
    if sections['certifications']:
        updates.append("// CERTIFICATIONS UPDATE:")
        for cert in sections['certifications']:
            updates.append(f"// - {cert}")
        updates.append("")
    
    # Summary update
    if sections['summary']:
        updates.append("// SUMMARY UPDATE:")
        updates.append(f"// {sections['summary'][:300]}...")
        updates.append("")
    
    return '\n'.join(updates)

def main():
    docx_file = "resume/Ashvak_PowerBI_Fabric_Developer.docx"
    
    if not Path(docx_file).exists():
        print(f"Error: {docx_file} not found!")
        return
    
    print("Extracting text from resume...")
    text = extract_text_from_docx(docx_file)
    
    if not text:
        print("Failed to extract text from document")
        return
    
    # Save full text for debugging
    with open('resume_full_text.txt', 'w', encoding='utf-8') as f:
        f.write(text)
    
    print("Structuring resume data...")
    sections = structure_resume_data(text)
    
    # Save structured data
    with open('resume_data.json', 'w', encoding='utf-8') as f:
        json.dump(sections, f, indent=2, ensure_ascii=False)
    
    # Generate HTML update suggestions
    updates = generate_html_updates(sections)
    
    with open('html_updates.txt', 'w', encoding='utf-8') as f:
        f.write(updates)
    
    print("\n" + "="*50)
    print("RESUME EXTRACTION COMPLETE")
    print("="*50)
    print(f"📄 Full text saved to: resume_full_text.txt")
    print(f"📊 Structured data saved to: resume_data.json")
    print(f"🔧 HTML update suggestions saved to: html_updates.txt")
    print("\n📋 Key sections found:")
    for section, content in sections.items():
        if content:
            if isinstance(content, list):
                print(f"  - {section}: {len(content)} items")
            else:
                print(f"  - {section}: {len(str(content))} chars")
    
    print("\n💡 Next steps:")
    print("1. Review resume_data.json for structured information")
    print("2. Check html_updates.txt for suggested updates")
    print("3. Use the structured data to update your HTML")

if __name__ == "__main__":
    main() 