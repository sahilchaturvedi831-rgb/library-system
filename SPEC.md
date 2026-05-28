# Voter Intelligence Platform - Specification

## Project Overview
**Project Name:** Voter Intelligence Platform (VIP)
**Type:** AI-Powered Political Data Management System
**Core Functionality:** Convert static voter lists into a dynamic Knowledge Graph enabling booth-level voter intelligence, hyper-local issue mapping, personalized communication, and real-time governance feedback.
**Target Users:** Political campaign teams, volunteers, party administrators

---

## Architecture

### Technology Stack
- **Backend:** Python with Flask
- **Database:** SQLite (with graph-like relationships)
- **AI/ML:** Scikit-learn (profiling), TextBlob (sentiment analysis)
- **Frontend:** HTML/CSS/JavaScript (single-page application)
- **Data Format:** JSON APIs

---

## Database Schema

### Tables

#### 1. voters
| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER PRIMARY KEY | Unique voter ID |
| name | TEXT | Voter full name |
| age | INTEGER | Voter age |
| gender | TEXT | Male/Female/Other |
| address | TEXT | Full address |
| booth_id | INTEGER | Reference to booth |
| family_id | INTEGER | Family group reference |
| occupation | TEXT | Job category |
| income_level | TEXT | Low/Middle/High |
| issue_priority | TEXT | Primary concern |
| political_inclination | TEXT | Party preference |
| sentiment_score | REAL | -1 to 1 (AI computed) |
| turnout_probability | REAL | 0-100% (AI predicted) |
| is_influencer | INTEGER | 0/1 - social influence |
| is_swing_voter | INTEGER | 0/1 - uncertain vote |
| created_at | TEXT | Timestamp |
| updated_at | TEXT | Timestamp |

#### 2. booths
| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER PRIMARY KEY | Booth ID |
| name | TEXT | Booth name/number |
| area | TEXT | Locality |
| total_voters | INTEGER | Count |
| satisfaction_score | REAL | 0-100% |

#### 3. issues
| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER PRIMARY KEY | Issue ID |
| booth_id | INTEGER | Reference to booth |
| title | TEXT | Issue name |
| category | TEXT | Category (water/road/employment) |
| affected_count | INTEGER | Voters affected |
| percentage | REAL | % of booth voters |
| sentiment | TEXT | Positive/Negative/Neutral |
| created_at | TEXT | Timestamp |

#### 4. schemes
| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER PRIMARY KEY | Scheme ID |
| name | TEXT | Scheme name |
| description | TEXT | Details |
| eligibility_criteria | TEXT | Who qualifies |
| beneficiary_count | INTEGER | Total beneficiaries |

#### 5. scheme_beneficiaries
| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER PRIMARY KEY | ID |
| voter_id | INTEGER | Voter reference |
| scheme_id | INTEGER | Scheme reference |
| benefit_date | TEXT | When benefits started |

#### 6. communications
| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER PRIMARY KEY | Message ID |
| voter_id | INTEGER | Target voter |
| message | TEXT | Message content |
| channel | TEXT | SMS/WhatsApp/App/Email |
| status | TEXT | Sent/Delivered/Failed |
| sent_at | TEXT | Timestamp |

#### 7. feedback
| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER PRIMARY KEY | Feedback ID |
| voter_id | INTEGER | Voter reference |
| subject | TEXT | Topic |
| content | TEXT | Message |
| sentiment | TEXT | Positive/Negative/Neutral |
| source | TEXT | Form/Social/IVR |
| created_at | TEXT | Timestamp |

#### 8. volunteers
| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER PRIMARY KEY | Volunteer ID |
| name | TEXT | Name |
| phone | TEXT | Contact |
| assigned_booths | TEXT | JSON array of booth IDs |
| visits_count | INTEGER | Field visits |

#### 9. visits
| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER PRIMARY KEY | Visit ID |
| voter_id | INTEGER | Voter visited |
| volunteer_id | INTEGER | Who visited |
| notes | TEXT | Visit notes |
| outcome | TEXT | Result |
| visited_at | TEXT | Timestamp |

---

## API Endpoints

### Voters
- `GET /api/voters` - List all voters (with pagination, filters)
- `GET /api/voters/<id>` - Get voter details with graph
- `POST /api/voters` - Add new voter
- `PUT /api/voters/<id>` - Update voter
- `DELETE /api/voters/<id>` - Remove voter
- `GET /api/voters/search` - Search voters
- `GET /api/voters/booth/<booth_id>` - Voters by booth

### Booths
- `GET /api/booths` - List all booths
- `GET /api/booths/<id>` - Booth dashboard with issues
- `POST /api/booths` - Create booth

### Issues
- `GET /api/issues` - List issues
- `GET /api/issues/booth/<booth_id>` - Issues for booth
- `POST /api/issues` - Report issue
- `GET /api/issues/heatmap` - All issues by booth

### Schemes
- `GET /api/schemes` - List government schemes
- `GET /api/schemes/eligibility/<voter_id>` - Check voter eligibility
- `POST /api/schemes/apply` - Apply beneficiary

### Analytics (AI)
- `GET /api/ai/profile/<voter_id>` - Voter profile analysis
- `GET /api/ai/sentiment` - Overall sentiment analysis
- `POST /api/ai/analyze-feedback` - Analyze feedback text
- `GET /api/ai/predictions/turnout` - Turnout predictions
- `GET /api/ai/predictions/swing` - Swing voter analysis

### Communications
- `GET /api/communications` - Message history
- `POST /api/communications/send` - Send personalized message

### Volunteers
- `GET /api/volunteers` - List volunteers
- `POST /api/volunteers` - Register volunteer
- `POST /api/visits` - Record field visit

---

## Frontend Pages

### 1. Dashboard (`/`)
- Overview stats cards
- Booth heatmap
- Recent activities
- Quick actions

### 2. Voters (`/voters`)
- Searchable/filterable table
- Quick view panel
- Add/Edit voter modal

### 3. Voter Profile (`/voters/:id`)
- Personal details
- Family graph
- Issues list
- Scheme benefits
- Communication history
- AI sentiment indicator

### 4. Booth Dashboard (`/booths/:id`)
- Booth overview
- Top 5 issues with percentages
- Voter demographics
- Influencer list
- Risk/swing voters
- Scheme penetration

### 5. Issues Map (`/issues`)
- All issues by booth
- Filter by category
- Sentiment indicators
- Resolution status

### 6. AI Analytics (`/analytics`)
- Voter profiling charts
- Sentiment analysis
- Turnout predictions
- Swing voter map

### 7. Communication Center (`/communications`)
- Message composer (AI-assisted)
- Channel selection
- Message templates
- Delivery status

### 8. Volunteer Management (`/volunteers`)
- Volunteer list
- Assignment management
- Visit tracking

---

## AI Components

### 1. Voter Profiling
- Classification by: Age group, Occupation, Income, Issue priority
- Uses simple rule-based + statistical clustering

### 2. Sentiment Analysis
- TextBlob-based polarity detection
- Categories: Positive (>0.1), Neutral, Negative (<-0.1)

### 3. Turnout Prediction
- Logistic regression model
- Features: past turnout, sentiment, influencer contact

### 4. Swing Voter Detection
- Low sentiment score + undecided inclination
- Contact frequency analysis

### 5. Issue Analysis
- Categorization of reported issues
- Trend detection over time

---

## Privacy & Ethics Features
- Data encryption at rest (SQLite with encryption)
- Consent management (opt-in flag)
- Role-based access control
- Audit logging
- Data export/delete options

---

## File Structure
```
voter_platform/
├── app.py                    # Main Flask application
├── config.py                 # Configuration
├── models.py                 # Database models
├── ai/
│   ├── __init__.py
│   ├── profiler.py          # Voter profiling
│   ├── sentiment.py         # Sentiment analysis
│   └── predictions.py       # Turnout/swing predictions
├── routes/
│   ├── __init__.py
│   ├── voters.py
│   ├── booths.py
│   ├── issues.py
│   ├── schemes.py
│   ├── analytics.py
│   ├── communications.py
│   └── volunteers.py
├── static/
│   ├── index.html
│   ├── style.css
│   └── script.js
└── data/
    └── voter_platform.db
```

---

## Acceptance Criteria

### Core Functionality
- [ ] Can add/view/edit/delete voters
- [ ] Can create and manage booths
- [ ] Can report and track issues at booth level
- [ ] Can view voter knowledge graph (family, issues, schemes)
- [ ] AI sentiment analysis works on feedback text
- [ ] Can generate booth-level issue reports
- [ ] Can send personalized communications

### AI Features
- [ ] Voter profiling by demographic categories
- [ ] Sentiment classification of feedback
- [ ] Turnout probability prediction
- [ ] Swing voter identification

### UI/UX
- [ ] Responsive dashboard with stats
- [ ] Interactive booth heatmap
- [ ] Searchable voter list
- [ ] Visual sentiment indicators
- [ ] Message composer with templates

### Privacy
- [ ] Consent flag on voter records
- [ ] Data export functionality
- [ ] Audit trail for data access
