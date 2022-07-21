# 📚 Documentation Setup Guide

This guide will help you set up and deploy the NasirPy documentation website using GitHub Pages.

## 🎯 What We're Building

A professional documentation website with:
- ✅ Modern Material Design theme
- ✅ Automatic GitHub Pages deployment
- ✅ Search functionality
- ✅ Mobile-responsive design
- ✅ Code syntax highlighting
- ✅ Interactive examples

## 📋 Prerequisites

- GitHub repository with admin access
- Basic familiarity with Markdown
- Python 3.7+ (for local development)

## 🚀 Quick Setup (5 minutes)

### Step 1: Enable GitHub Pages

1. **Go to your repository settings**:
   - Navigate to `https://github.com/itx-nasir/nasirpy/settings`
   - Click on "Pages" in the left sidebar

2. **Configure Pages source**:
   - Source: "GitHub Actions"
   - This allows our workflow to deploy automatically

### Step 2: Commit Documentation Files

The documentation structure is already created in your `docs/` folder:

```
docs/
├── mkdocs.yml          # Main configuration
├── requirements.txt    # Python dependencies
└── docs/
    ├── index.md        # Homepage
    ├── getting-started/
    │   ├── installation.md
    │   └── quickstart.md
    └── ... (other pages)
```

### Step 3: Trigger Deployment

1. **Commit and push** the documentation files:
   ```bash
   git add docs/ .github/workflows/docs.yml
   git commit -m "Add documentation site"
   git push origin main
   ```

2. **Check the deployment**:
   - Go to the "Actions" tab in your repository
   - You should see a "Deploy Documentation" workflow running
   - Wait for it to complete (usually 2-3 minutes)

3. **Access your site**:
   - Your documentation will be available at: `https://itx-nasir.github.io/nasirpy`

## 🛠️ Local Development

To work on the documentation locally:

### 1. Install Dependencies

```bash
cd docs
pip install -r requirements.txt
```

### 2. Start Development Server

```bash
mkdocs serve
```

This starts a local server at `http://127.0.0.1:8000` with live reload.

### 3. Make Changes

Edit any `.md` file in the `docs/docs/` folder and see changes instantly in your browser.

## 📝 Adding Content

### Creating New Pages

1. **Create a new Markdown file**:
   ```bash
   # Example: Add a new tutorial
   touch docs/docs/tutorials/advanced-routing.md
   ```

2. **Add content**:
   ```markdown
   # Advanced Routing
   
   Learn about advanced routing patterns in NasirPy...
   ```

3. **Update navigation** in `mkdocs.yml`:
   ```yaml
   nav:
     - Home: index.md
     - Tutorials:
       - Advanced Routing: tutorials/advanced-routing.md
   ```

### Using Special Features

#### Code Blocks with Highlighting

```python
from nasirpy import App

app = App()

@app.get("/")
async def hello():
    return {"message": "Hello!"}
```

#### Admonitions (Info Boxes)

```markdown
!!! tip "Pro Tip"
    This is a helpful tip for users.

!!! warning "Important"
    Pay attention to this warning.

!!! example "Try This"
    Here's something to experiment with.
```

#### Tabbed Content

```markdown
=== "Python"
    ```python
    print("Hello, World!")
    ```

=== "JavaScript"
    ```javascript
    console.log("Hello, World!");
    ```
```

## 🎨 Customization

### Changing Colors

Edit `mkdocs.yml` to change the theme colors:

```yaml
theme:
  name: material
  palette:
    primary: blue  # Change to: red, pink, purple, etc.
    accent: blue
```

### Adding Your Logo

1. Add your logo to `docs/docs/assets/logo.png`
2. Update `mkdocs.yml`:
   ```yaml
   theme:
     logo: assets/logo.png
   ```

### Custom CSS

1. Create `docs/docs/stylesheets/extra.css`
2. Add custom styles
3. Include in `mkdocs.yml`:
   ```yaml
   extra_css:
     - stylesheets/extra.css
   ```

## 🔧 Troubleshooting

### Common Issues

#### Build Fails

**Error**: `ModuleNotFoundError: No module named 'mkdocs'`

**Solution**: Install dependencies:
```bash
cd docs
pip install -r requirements.txt
```

#### Pages Not Updating

**Error**: Changes don't appear on the live site

**Solutions**:
1. Check the GitHub Actions workflow completed successfully
2. Clear your browser cache
3. Wait a few minutes for CDN to update

#### Navigation Not Working

**Error**: Links return 404

**Solution**: Check file paths in `mkdocs.yml` match actual file locations:
```yaml
nav:
  - Home: index.md  # Should be docs/docs/index.md
```

### Getting Help

If you encounter issues:

1. **Check the [MkDocs documentation](https://www.mkdocs.org/)**
2. **Review [Material theme docs](https://squidfunk.github.io/mkdocs-material/)**
3. **Look at the GitHub Actions logs** for deployment errors
4. **Open an issue** in the repository

## 📈 SEO and Analytics

### Adding Google Analytics

1. Get your Google Analytics tracking ID
2. Add to `mkdocs.yml`:
   ```yaml
   extra:
     analytics:
       provider: google
       property: G-XXXXXXXXXX
   ```

### SEO Optimization

The documentation is already optimized with:
- ✅ Proper meta descriptions
- ✅ Structured navigation
- ✅ Mobile-responsive design
- ✅ Fast loading times
- ✅ Search functionality

## 🎯 Repository Integration

### Update Your Main README

Add a documentation badge and link:

```markdown
[![Documentation](https://img.shields.io/badge/docs-live-brightgreen?style=flat-square)](https://itx-nasir.github.io/nasirpy)

## 📚 Documentation

Complete documentation is available at: **[https://itx-nasir.github.io/nasirpy](https://itx-nasir.github.io/nasirpy)**
```

### Repository Settings

Update your repository:

1. **Description**: Use the short description we created
2. **Website**: Set to `https://itx-nasir.github.io/nasirpy`
3. **Topics**: Add the recommended tags

## 🎉 Final Result

Your documentation site will have:

- **Professional appearance** with Material Design
- **Fast search** across all content
- **Mobile-friendly** responsive design
- **Automatic deployment** on every push
- **SEO optimized** for better discoverability
- **Educational focus** perfect for your framework

## 📊 Measuring Success

Track your documentation's impact:

- **GitHub Pages analytics** (if enabled)
- **Repository traffic** in GitHub Insights
- **User engagement** through issues and discussions
- **Community growth** via stars and forks

---

**🎉 Congratulations!** You now have a professional documentation website that will significantly boost your project's visibility and help users understand your educational framework.

**Your documentation URL**: `https://itx-nasir.github.io/nasirpy` 