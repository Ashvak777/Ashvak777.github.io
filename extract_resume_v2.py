#!/usr/bin/env python3
"""
Improved Resume Text Extractor
Properly extracts and structures resume data from Word documents
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

def parse_experience_section(text):
    """Parse the experience section properly"""
    experiences = []
    
    # Split by "Client:" to separate different experiences
    sections = text.split("Client\t:")
    
    for section in sections[1:]:  # Skip the first empty section
        lines = section.strip().split('\n')
        
        experience = {
            'company': '',
            'role': '',
            'dates': '',
            'project': '',
            'responsibilities': [],
            'environment': ''
        }
        
        current_section = None
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Company name (first line after Client:)
            if not experience['company']:
                experience['company'] = line
                continue
                
            # Role and dates
            if line.startswith('Role\t:'):
                role_parts = line.split('\t')
                if len(role_parts) >= 2:
                    experience['role'] = role_parts[1].strip()
                    # Look for dates in the same line or next line
                    if len(role_parts) > 2:
                        dates_part = role_parts[-1].strip()
                        if '–' in dates_part or '-' in dates_part:
                            experience['dates'] = dates_part
                continue
                
            # Project
            if line.startswith('Project\t:'):
                experience['project'] = line.replace('Project\t:', '').strip()
                continue
                
            # Responsibilities
            if line == 'Responsibilities:':
                current_section = 'responsibilities'
                continue
                
            # Environment
            if line.startswith('Environment'):
                current_section = 'environment'
                experience['environment'] = line
                continue
                
            # Process content based on current section
            if current_section == 'responsibilities':
                if line.startswith('•') or line.startswith('-') or line.startswith('*'):
                    experience['responsibilities'].append(line)
                elif line.startswith('Environment'):
                    current_section = 'environment'
                    experience['environment'] = line
                else:
                    # If it's not a bullet point, it might be a continuation
                    if experience['responsibilities']:
                        experience['responsibilities'][-1] += ' ' + line
                    else:
                        experience['responsibilities'].append(line)
        
        if experience['company']:
            experiences.append(experience)
    
    return experiences

def parse_certifications_and_education(text):
    """Parse certifications and education sections"""
    certifications = []
    education = []
    
    lines = text.split('\n')
    current_section = None
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Detect sections
        if 'certifications:' in line.lower():
            current_section = 'certifications'
            continue
        elif 'education' in line.lower():
            current_section = 'education'
            continue
        elif 'skills:' in line.lower():
            current_section = 'skills'
            continue
            
        # Process content
        if current_section == 'certifications':
            if any(cert in line.lower() for cert in ['certified', 'microsoft', 'azure', 'power bi', 'fabric', 'associate', 'agile']):
                certifications.append(line)
        elif current_section == 'education':
            if any(edu in line.lower() for edu in ['university', 'college', 'degree', 'bachelor', 'master']):
                education.append(line)
    
    return certifications, education

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
    
    # Extract personal info from the beginning
    lines = text.split('\n')
    if len(lines) >= 4:
        sections['personal_info'] = {
            'name': lines[0].strip(),
            'phone': lines[1].strip(),
            'email': lines[2].strip(),
            'clearance': lines[3].strip()
        }
    
    # Find the experience section
    experience_start = text.find('PROFESSIONAL EXPERIENCE')
    if experience_start != -1:
        experience_text = text[experience_start:]
        sections['experience'] = parse_experience_section(experience_text)
    
    # Parse certifications and education
    sections['certifications'], sections['education'] = parse_certifications_and_education(text)
    
    # Extract skills from the technical proficiency section
    skills_start = text.find('TECHNICAL PROFICIENCY')
    if skills_start != -1:
        skills_text = text[skills_start:]
        lines = skills_text.split('\n')
        current_section = None
        
        for line in lines:
            line = line.strip()
            if 'skills:' in line.lower():
                current_section = 'skills'
                continue
            elif current_section == 'skills' and line:
                if not line.startswith('Certifications:') and not line.startswith('Skills:'):
                    sections['skills'].append(line)
    
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
            if exp.get('project'):
                updates.append(f"// Project: {exp.get('project')}")
            updates.append("// Key Responsibilities:")
            for resp in exp.get('responsibilities', [])[:6]:  # First 6 responsibilities
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
    with open('resume_data_v2.json', 'w', encoding='utf-8') as f:
        json.dump(sections, f, indent=2, ensure_ascii=False)
    
    # Generate HTML update suggestions
    updates = generate_html_updates(sections)
    
    with open('html_updates_v2.txt', 'w', encoding='utf-8') as f:
        f.write(updates)
    
    print("\n" + "="*50)
    print("IMPROVED RESUME EXTRACTION COMPLETE")
    print("="*50)
    print(f"📄 Full text saved to: resume_full_text.txt")
    print(f"📊 Structured data saved to: resume_data_v2.json")
    print(f"🔧 HTML update suggestions saved to: html_updates_v2.txt")
    print("\n📋 Key sections found:")
    for section, content in sections.items():
        if content:
            if isinstance(content, list):
                print(f"  - {section}: {len(content)} items")
            else:
                print(f"  - {section}: {len(str(content))} chars")
    
    print("\n💡 Next steps:")
    print("1. Review resume_data_v2.json for structured information")
    print("2. Check html_updates_v2.txt for suggested updates")
    print("3. Use the structured data to update your HTML")

if __name__ == "__main__":
    main() 