# Cod3BlackAgency Design Specifications

Visual identity specifications for GitHub profile and repositories.

---

## GitHub Profile Banner

**Dimensions**: 1280 x 640 px (2:1 ratio, recommended by GitHub)

**Design Brief**:
- Background: Dark (#0a0a0a to #1a1a1a gradient, subtle)
- Primary text: "Cod3BlackAgency" in clean sans-serif (Inter, SF Pro, or similar)
- Tagline: "Full-Stack Product Studio" in lighter weight
- Accent color: Electric blue (#0066ff) or agency brand color
- No imagery clutter - text-focused, minimalist
- Optional: subtle code/terminal pattern in background at low opacity

**Elements**:
```
+--------------------------------------------------+
|                                                  |
|              Cod3BlackAgency                     |
|         Full-Stack Product Studio                |
|                                                  |
|     AI Integration | Web Apps | Production MVPs  |
|                                                  |
+--------------------------------------------------+
```

**File format**: PNG or WebP, optimized for web

---

## Social Preview Image (OpenGraph)

**Dimensions**: 1200 x 630 px (standard OG image)

**Used for**: Link previews when sharing GitHub repos on social media, Slack, Discord

**Design Brief**:
- Same visual language as banner
- Include repo name prominently
- Brief tagline or description
- Cod3BlackAgency branding in corner
- Dark background, light text

**Template**:
```
+--------------------------------------------------+
|                                                  |
|  [Repo Icon]                                     |
|                                                  |
|           [Repository Name]                      |
|                                                  |
|     [One-line description]                       |
|                                                  |
|                          Cod3BlackAgency         |
+--------------------------------------------------+
```

**Current public-system customization**:
- c3bai: "AI Business Systems & Automation"
- Gratog: "Taste of Gratitude Commerce & Operations"
- nhbbi-crm: "Membership & Relationship Operations"
- asca-pwa: "Association PWA & Admin System"
- jds-horse-ranch-pwa: "Ranch Customer Experience"
- cod3blackagency-portfolio: "Verified Systems & Delivery Evidence"

**Retained asset customization**:
- sd-studio-web: "Remote AI Image Interface"
- family-powerhouse: "Family Coordination Platform"
- Ownly: "SaaS Starter Foundation"
- notionexporterpdf: "Notion PDF Export Utility"

Archived upstream/reference or superseded repositories such as `solovibe` and `cba-ai-platform` should not receive current flagship social-preview treatment.

---

## Logo

**Primary Logo**: Text-based "Cod3BlackAgency"
- Font: Inter Bold or similar geometric sans-serif
- The "3" in Cod3 is stylized (optional: different color or weight)
- Color: White on dark, or inverse

**Icon/Avatar**:
- Dimensions: 400 x 400 px (square, for GitHub avatar)
- Simplified: "C3B" monogram or abstract code bracket symbol
- Same color palette as banner

---

## Color Palette

| Name | Hex | Usage |
|------|-----|-------|
| Background Dark | #0a0a0a | Primary background |
| Background Mid | #1a1a1a | Cards, sections |
| Text Primary | #ffffff | Headings, primary text |
| Text Secondary | #a0a0a0 | Descriptions, muted text |
| Accent Blue | #0066ff | Links, highlights, CTAs |
| Accent Green | #00cc66 | Success states, badges |
| Border | #333333 | Dividers, card borders |

---

## Typography

**Headings**: Inter, SF Pro Display, or system sans-serif
- Bold weight (700)
- Clean, geometric

**Body**: Inter, SF Pro Text, or system sans-serif
- Regular weight (400)
- Line height: 1.5

**Code**: JetBrains Mono, Fira Code, or system monospace

---

## Implementation

### GitHub Profile Picture

Upload square logo/avatar (400x400) to GitHub account settings.

### Repository Social Preview

For each repo:
1. Go to repo Settings > General
2. Scroll to "Social preview"
3. Upload custom 1200x630 image

### Profile README Banner

```markdown
![Cod3BlackAgency](./assets/banner.png)
```

Or hosted externally:
```markdown
![Cod3BlackAgency](https://your-cdn.com/banner.png)
```

---

## Tools for Creation

- **Figma**: Design and export (free tier works)
- **Canva**: Quick social images
- **GIMP/Photoshop**: Image editing
- **Squoosh**: Image optimization before upload

---

## File Checklist

- [ ] banner.png (1280x640)
- [ ] og-default.png (1200x630)
- [ ] og-c3bai.png
- [ ] og-gratog.png
- [ ] og-nhbbi-crm.png
- [ ] og-asca-pwa.png
- [ ] og-jds-horse-ranch-pwa.png
- [ ] og-cod3blackagency-portfolio.png
- [ ] logo-dark.png (text logo on dark)
- [ ] logo-light.png (text logo on light)
- [ ] avatar.png (400x400)
