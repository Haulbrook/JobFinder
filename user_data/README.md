# Personal Job Search Materials

This directory contains your personal job search materials. **This folder is gitignored** and will not be pushed to GitHub.

## Directory Structure

```
user_data/
├── resumes/              # Your resume files
├── cover_letters/        # Cover letter templates
├── projects/            # Project descriptions & portfolios
└── portfolio/           # Portfolio materials, screenshots, etc.
```

## What Goes Where

### resumes/
Store all versions of your resume here:
- `resume_main.pdf` - Your primary resume
- `resume_tech.pdf` - Tech-focused version
- `resume_senior.pdf` - Senior role version
- `resume.docx` - Editable version

**Tip**: Keep multiple versions tailored for different roles

### cover_letters/
Store cover letter templates:
- `cover_letter_template.txt` - Base template
- `cover_letter_tech.txt` - Tech company template
- `cover_letter_startup.txt` - Startup template
- `cover_letter_enterprise.txt` - Enterprise template

JobFinder will use these as a base and customize them for specific jobs.

### projects/
Store project descriptions and details:
- `project1_description.md` - E-commerce platform project
- `project2_description.md` - ML pipeline project
- `project3_description.md` - Mobile app project
- `achievements.md` - List of key achievements

Include:
- Project name and description
- Technologies used
- Your role and contributions
- Results/impact (metrics if possible)
- Links to live demos or repos

### portfolio/
Store portfolio materials:
- `portfolio_website.pdf` - PDF of your portfolio site
- `screenshots/` - Project screenshots
- `presentations/` - Slide decks
- `certifications/` - Certificates and credentials

## How JobFinder Uses These Files

### 1. Profile Creation

When you create your profile, reference these files:

```
"Create my job search profile:
- Name: Your Name
- Email: you@email.com
- Resume path: /Users/thehaulbrooks/Desktop/JOB FINDER/user_data/resumes/resume_main.pdf
- Portfolio: https://yourportfolio.com
- ..."
```

### 2. Cover Letter Generation

JobFinder will:
1. Use your cover letter template as a base
2. Customize it based on the job description
3. Incorporate relevant projects from `projects/`
4. Add specific achievements that match the role

### 3. Application Preparation

When applying, JobFinder can:
- Attach the correct resume version
- Generate a tailored cover letter
- Reference specific projects that match the job
- Include relevant portfolio links

## File Formats

### Resumes
- **PDF** (recommended): `resume.pdf`
- **DOCX** (for ATS systems): `resume.docx`
- **Plain text** (for easy parsing): `resume.txt`

### Cover Letters
- **Plain text** (`.txt`): Easy to edit and customize
- **Markdown** (`.md`): Formatted but still text
- **PDF**: Final versions

### Projects
- **Markdown** (`.md`): Easy to read and edit
- Include links, images, and code snippets

## Example Files

See the template files included in each directory for examples of structure and content.

## Privacy & Security

**IMPORTANT:**
- This directory is automatically gitignored
- Files here will NOT be uploaded to GitHub
- Keep sensitive information here (not in git)
- Make backups of these files separately

## Tips

1. **Keep Multiple Resume Versions**
   - Frontend-focused
   - Backend-focused
   - Full-stack
   - Leadership/management

2. **Quantify Achievements**
   - "Increased performance by 40%"
   - "Reduced costs by $50K annually"
   - "Led team of 5 developers"

3. **Update Regularly**
   - Add new projects as you complete them
   - Update skills and technologies
   - Refresh achievements quarterly

4. **Tailor for Each Application**
   - Use relevant project examples
   - Highlight matching skills
   - Address specific job requirements

## Integration with JobFinder

JobFinder will automatically:
- Load your profile (including file paths)
- Access resumes when applying
- Use cover letter templates for generation
- Reference projects in applications
- Include portfolio links

## Backup Recommendation

Since these files are gitignored, back them up separately:

```bash
# Create a backup
cd "/Users/thehaulbrooks/Desktop/JOB FINDER"
tar -czf job_materials_backup_$(date +%Y%m%d).tar.gz user_data/

# Or sync to cloud storage
# cp -r user_data/ ~/Dropbox/JobSearch/
```

---

**Remember**: This folder is for YOUR EYES ONLY. Never commit personal information to public repositories!
