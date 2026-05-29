# Expert Framework Builder - Project Startup and Operation Flow Documentation

## 📋 Document Overview

This document provides a comprehensive guide to the Expert Framework Builder project, from startup to operation, including all stages, involved files, and system components. This project is a Docker-based full-stack application with a React + Vite frontend, FastAPI backend, and Firebase Firestore database.

---

## 🚀 I. Project Startup Process

### 1.1 Environment Preparation

#### **Prerequisites**
- Docker Desktop installed and running
- Git (for code updates)
- `.env` file in project root directory (contains sensitive information, provided via email or Teams direct message)

#### **Environment Configuration Files**

**Frontend `.env` file location:** Project root directory
```
VITE_API_BASE_URL=http://localhost:8000
VITE_FIREBASE_API_KEY=<your-firebase-key>
VITE_FIREBASE_AUTH_DOMAIN=<your-auth-domain>
VITE_FIREBASE_PROJECT_ID=<your-project-id>
VITE_FIREBASE_STORAGE_BUCKET=<your-storage-bucket>
VITE_FIREBASE_MESSAGING_SENDER_ID=<your-sender-id>
VITE_FIREBASE_APP_ID=<your-app-id>
```

**Backend `.env` file location:** Project root directory (shared with frontend)
```
OPENAI_API_KEY=<your-openai-key>
ANTHROPIC_API_KEY=<your-anthropic-key>
GOOGLE_APPLICATION_CREDENTIALS=<path-to-firebase-credentials>
```

**Involved Files:**
- `/.env` - Environment variables configuration
- `/docker-compose.yml` - Docker orchestration configuration
- `/Dockerfile` - Docker image build configuration
- `/vite.config.js` - Vite frontend build configuration

---

### 1.2 Startup Methods

#### **Method 1: Cloud Deployment (GCP)**

**Steps:**

1. **Stop existing containers**
   ```bash
   docker-compose down
   ```

2. **Update code to latest version**
   ```bash
   git pull origin main
   ```

3. **Clean build and rebuild images**
   ```bash
   docker-compose build --no-cache
   ```

4. **Start services (background mode)**
   ```bash
   docker-compose up -d
   ```

5. **View real-time logs**
   ```bash
   docker-compose logs -f
   ```

**Involved Files:**
- `/docker-compose.yml` - Defines frontend and backend service configuration
- `/Dockerfile` - Backend Python environment build
- `/frontend/Dockerfile` - Frontend Node environment build
- `/.env` - Environment variables configuration

**Service Architecture:**
- **Frontend Service:** Runs on container port 5173, mapped to host port 3000
- **Backend Service:** Runs on container port 8000, mapped to host port 8000
- **Network:** Frontend and backend communicate via Docker internal network

---

#### **Method 2: Local Deployment**

**Steps:**

1. **Ensure Docker Desktop is running**
   - Windows: Check system tray icon
   - Mac: Check menu bar icon

2. **Build and start services**
   ```bash
   docker-compose build --no-cache
   docker-compose up -d
   docker-compose logs -f
   ```

**Involved files are the same as cloud deployment**

**Access URLs:**
- Frontend application: `http://localhost:3000`
- Backend API: `http://localhost:8000`
- API documentation: `http://localhost:8000/docs`

---

## 🌐 II. User Flow and Involved Files

### 2.1 Landing Page

**User Scenario:** Page users see when first visiting the application or when not logged in

**Flow:**
1. User visits `http://localhost:3000` or production domain
2. System detects user is not logged in and displays Landing Page
3. Landing Page shows project introduction, features, and getting started guide
4. User can choose "Login" or "Sign Up"

**Involved Files:**
- **Frontend:**
  - `/src/components/LandingPage.jsx` - Landing Page main component
  - `/src/App.jsx` - Route configuration (root path "/" points to LandingPage)
  - `/src/contexts/AuthContext.jsx` - Authentication context (detects login status)

**Key Features:**
- Project introduction and value proposition display
- Navigation to login/signup pages
- Responsive design for different devices

---

### 2.2 Login and Registration Flow

#### **2.2.1 Registration Flow**

**User Scenario:** New users creating an account

**Flow:**
1. User clicks "Sign Up" button on Landing Page
2. Redirects to `/signup` route
3. User enters email, password, and password confirmation
4. System validates if email suffix is in admin whitelist
5. Upon validation, creates Firebase Authentication account
6. Creates user document in Firestore
7. Automatically redirects to Tenant creation flow

**Involved Files:**

**Frontend:**
- `/src/components/Signup.jsx` - Registration form component
- `/src/contexts/AuthContext.jsx` - Handles Firebase registration logic
- `/src/lib/firebase.js` - Firebase configuration and initialization
- `/src/App.jsx` - Registration route configuration (`/signup`)

**Backend:**
- `/backend/routes/auth.py` - User authentication API endpoints (if additional validation exists)
- `/backend/models.py` - User data model definition

**Database (Firestore):**
- `users` collection - Stores user basic information
  ```json
  {
    "uid": "user-unique-id",
    "email": "user@example.com",
    "tenantId": null,  // Initially empty, created later
    "role": "expert",
    "createdAt": "2025-11-25T00:00:00Z"
  }
  ```
- `whitelisted_domains` collection - Admin-set whitelist email suffixes

**Key Validation Logic:**
```javascript
// Email whitelist validation in Signup.jsx
const emailDomain = email.split('@')[1];
const isWhitelisted = await checkDomainWhitelist(emailDomain);
if (!isWhitelisted) {
  throw new Error('Your email domain is not whitelisted');
}
```

---

#### **2.2.2 Login Flow**

**User Scenario:** Registered users logging into the system

**Flow:**
1. User visits `/login` route or clicks "Login" from Landing Page
2. Enters email and password
3. Firebase Authentication validates credentials
4. Upon successful validation, loads user information from Firestore
5. If user has tenantId, redirects to `/{tenantId}/frameworks`
6. If user has no tenantId, displays Tenant creation modal

**Involved Files:**

**Frontend:**
- `/src/components/Login.jsx` - Login form component
- `/src/contexts/AuthContext.jsx` - Authentication context
- `/src/lib/firebase.js` - Firebase authentication methods
- `/src/App.jsx` - Login route and root path redirect logic

**Key Route Logic:**
```javascript
// RootRedirect component in App.jsx
function RootRedirect() {
  if (!user) return <Navigate to="/login" />
  if (!user.tenantId) return <TenantCreationModal />
  return <Navigate to={`/${user.tenantId}/frameworks`} />
}
```

**Involved Firebase Services:**
- Firebase Authentication - User credential validation
- Firestore `users` collection - Load user details

---

### 2.3 Tenant Creation Flow

**User Scenario:** Newly registered users or users without Tenant need to create organization workspace

**Flow:**
1. After login, system detects `user.tenantId === null`
2. Automatically displays `TenantCreationModal` modal
3. User enters Tenant ID (subdomain) and organization name
4. System validates Tenant ID uniqueness and format
5. Creates Tenant record and associates with user
6. Updates user's tenantId field
7. Redirects to `/{tenantId}/frameworks`

**Involved Files:**

**Frontend:**
- `/src/components/TenantCreationModal.jsx` - Tenant creation modal
- `/src/contexts/AuthContext.jsx` - Updates user tenantId
- `/src/lib/firebase.js` - Firestore write operations
- `/src/App.jsx` - Detects tenantId and displays modal

**Database (Firestore):**
- `tenants` collection - Stores tenant information
  ```json
  {
    "tenantId": "my-organization",
    "name": "My Organization",
    "ownerId": "user-uid",
    "members": ["user-uid"],
    "createdAt": "2025-11-25T00:00:00Z",
    "subdomain": "my-organization"
  }
  ```
- `users` collection - Updates user's tenantId field

**Key Validation:**
- Tenant ID format: lowercase letters, numbers, hyphens, 3-20 characters
- Uniqueness check: Query Firestore to ensure Tenant ID is not duplicated

---

### 2.4 Create Framework Page

**User Scenario:** Expert users create new evaluation frameworks through text or files

**Page Route:** `/{tenantId}/create`

**Flow:**

#### **2.4.1 Create via Text**

1. User inputs text in "Paste Text" tab (maximum 10,000 characters)
2. User selects whether to enable Privacy Protection
   - **Enabled:** Text is first sent to local LLM on GCP to extract keywords, then passed to OpenAI
   - **Disabled:** Text is sent directly to OpenAI API
3. Clicks "Generate Draft" button
4. System calls backend API to generate framework
5. Framework is saved to Firestore
6. Redirects to framework editor page

**Involved Files:**

**Frontend:**
- `/src/components/CreateFramework.jsx` - Create framework main component (1080 lines)
- `/src/components/PrivacyLockDialog.jsx` - Privacy Protection toggle dialog
- `/src/components/LoadingDialog.jsx` - Generation process loading dialog
- `/src/lib/api.js` - API call methods
  - `generateFrameworkFromText(text, useGlobalLLM, model)`
  - `generateFrameworkFromFiles(files, useGlobalLLM, model)`

**Backend:**
- `/backend/routes/frameworks.py` - Framework generation API
  - `POST /api/frameworks/generate-from-text` - Text generation endpoint
  - Uses modules:
    - `llm_local.py` - Local LLM keyword extraction (when Privacy Protection enabled)
    - `llm_global.py` - OpenAI API calls
- `/backend/models.py` - Framework data model

**Privacy Protection Workflow:**

```python
# Processing logic in frameworks.py
if use_global_llm:
    # Use OpenAI directly
    framework = call_openai_framework(text, model)
else:
    # Use local LLM to extract keywords
    keywords = extract_seed(text)  # llm_local.py
    # Pass keywords to OpenAI
    framework = call_openai_framework(keywords, model)
```

**API Endpoint Details:**
```python
@router.post("/generate-from-text")
async def generate_from_text(
    request: TextGenerateRequest,
    db: Session = Depends(get_db)
):
    # 1. Process text based on privacy settings
    # 2. Call LLM to generate framework
    # 3. Calculate confidence score
    # 4. Save to database
    # 5. Return framework ID and data
```

---

#### **2.4.2 Create via File**

**Supported File Formats:**
- PDF
- Word documents (.doc, .docx)
- Excel spreadsheets (.xls, .xlsx)
- Plain text (.txt)
- Markdown (.md)

**Flow:**
1. User switches to "Upload File" tab
2. Drags files or clicks to select files (supports multiple file upload)
3. System validates file size (single file ≤ 2MB)
4. Displays selected file list, user can delete files
5. Selects Privacy Protection setting
6. Clicks "Generate Draft"
7. Backend extracts file content and generates framework
8. Saves and redirects to editor page

**Involved Files:**

**Frontend:**
- `/src/components/CreateFramework.jsx` - File upload UI and drag-drop handling

**Backend:**
- `/backend/routes/frameworks.py`
  - `POST /api/frameworks/generate-from-file` - Single file generation
  - `POST /api/frameworks/generate-from-files` - Multiple file generation
- File processing tools:
  - PDF: `PyPDF2` or `pdfplumber`
  - Word: `python-docx`
  - Excel: `openpyxl`

**File Content Extraction Logic:**
```python
# frameworks.py
def read_file_content(file_path: str, filename: str) -> str:
    ext = filename.lower().split('.')[-1]
    if ext == 'pdf':
        return extract_pdf_text(file_path)
    elif ext in ['doc', 'docx']:
        return extract_docx_text(file_path)
    elif ext in ['xls', 'xlsx']:
        return extract_excel_text(file_path)
    # ...other formats
```

**Database Storage (Firestore):**
- `frameworks` collection
  ```json
  {
    "id": "framework-xxxxx",
    "creatorId": "user-uid",
    "tenantId": "my-organization",
    "metadata": {
      "title": "DF-EVAL-101 — Model/Agent Evaluation Kickoff",
      "version": "1.0",
      "tags": ["Tag1", "Tag2", "Tag3"],
      "family": "Technology",
      "confidence": 0.77,
      "lastUpdated": "2025-11-25T12:35:45Z"
    },
    "steps": [...],
    "artefacts": {...},
    "risks": [...],
    "escalation": [...],
    "publishStatus": "draft",
    "createdAt": "2025-11-25T12:30:00Z"
  }
  ```

---

### 2.5 Me (Your Frameworks) Page

**User Scenario:** Experts view and manage all frameworks they've created

**Page Route:** `/{tenantId}/frameworks`

**Flow:**
1. User redirects to this page by default after login
2. System loads all user's frameworks from Firestore
3. Displays frameworks grouped by Family (category)
4. Each framework displays as a card, including:
   - Framework title and version
   - Confidence score
   - Key Artefacts preview (maximum 3)
   - Creation and update time
5. User available actions:
   - **View** - View framework details
   - **Edit** - Edit framework
   - **Download** - Export as .docx file
   - **Publish** - Publish to Library or Organization
   - **Duplicate** - Copy framework
   - **Delete** - Delete framework

**Involved Files:**

**Frontend:**
- `/src/components/YourFrameworks.jsx` - Framework list main component
- `/src/components/FrameworkCard.jsx` - Single framework card component (20KB)
- `/src/components/PublishModal.jsx` - Publish options modal
- `/src/lib/firebase.js` - Firestore query methods
  - `getMyFrameworks(userId)` - Get user frameworks
  - `deleteFramework(frameworkId)` - Delete framework
  - `duplicateFramework(frameworkId)` - Duplicate framework

**Backend:**
- `/backend/routes/frameworks.py`
  - `GET /api/frameworks/my-frameworks?user_id={uid}` - Get user framework list
  - `GET /api/frameworks/my-frameworks/by-family` - Get grouped by category
  - `DELETE /api/frameworks/{framework_id}` - Delete framework
  - `POST /api/frameworks/export-docx` - Export as Word document

**Framework Grouping Logic:**
```javascript
// YourFrameworks.jsx
const groupedFrameworks = frameworks.reduce((groups, framework) => {
  const family = framework.metadata.family || 'Other';
  if (!groups[family]) groups[family] = [];
  groups[family].push(framework);
  return groups;
}, {});
```

**Framework Family Types:**
```python
# models.py
FRAMEWORK_GROUPS = [
    "Technology",
    "Healthcare",
    "Research",
    "Financial",
    "Compliance",
    "Other"
]
```

---

### 2.6 Framework Editor Page

**User Scenario:** Experts edit and refine generated frameworks

**Page Route:** `/{tenantId}/editor/{frameworkId}`

**Page Structure:**

#### **Left Navigation Bar (5 sections):**
1. **Metadata** - Metadata editing
2. **Framework Stages** - Framework stages and steps
3. **Artefacts** - Artefacts management
4. **Risks** - Risk assessment
5. **Escalation** - Escalation mechanism

#### **Main Feature Areas:**

---

#### **2.6.1 Metadata Editing**

**Features:**
- Edit framework title (Title)
- Modify version number (Version)
- Add/edit tags (Tags)
- View last update time
- View Points of View (POV) - Framework core principles
- View Confidence Score - Framework completeness indicator

**Involved Files:**
- `/src/components/FrameworkEditor.jsx` - Main editor (1881 lines)
  - Metadata section: Renders metadata form
  - Auto-save logic: 2-second debounce save to Firestore and localStorage

**Data Structure:**
```javascript
metadata: {
  title: "DF-EVAL-101 — Model/Agent Evaluation Kickoff",
  version: "1.0",
  tags: "Tag1, Tag2, Tag3",
  lastUpdated: "2025-11-25T12:35:45Z",
  pov: [
    "Establishing clear evaluation criteria...",
    "A structured approach to evaluation..."
  ],
  confidence: 0.77
}
```

**Confidence Score Calculation:**
```python
# frameworks.py
def calculate_confidence(framework: dict) -> float:
    # Calculate based on the following factors:
    # - Step completeness (steps)
    # - Artefacts definition clarity
    # - Risk assessment coverage
    # - Escalation mechanism completeness
    return score  # 0.0 - 1.0
```

---

#### **2.6.2 Framework Stages**

**Features:**
- View and edit framework stages (Steps)
- Each stage includes:
  - Stage name (name)
  - Stage description (description)
  - Sub-steps list (subSteps)
- Can add new stages or delete existing ones
- Can reorder stages

**Involved Files:**
- `/src/components/FrameworkEditor.jsx` - Stage editing UI

**Data Structure:**
```javascript
steps: [
  {
    id: "step-1",
    name: "Planning Phase",
    description: "Initial planning and preparation",
    subSteps: [
      "Resource allocation",
      "Timeline development",
      "Risk assessment"
    ]
  },
  {
    id: "step-2",
    name: "Execution Phase",
    description: "Implementation of the plan",
    subSteps: ["Task execution", "Progress monitoring"]
  }
]
```

---

#### **2.6.3 Artefacts Management**

**Features:**
- **Default Artefact** - Default artefact (usually report or document package)
- **Additional Artefacts** - Additional artefacts list
- Supports free editing of Artefact Outlines:
  - Add new artefacts
  - Edit artefact names and descriptions
  - Enable/disable artefacts (selected field)
  - Delete artefacts
- **AI Fill Feature** - Use AI to automatically fill artefact descriptions

**Involved Files:**

**Frontend:**
- `/src/components/FrameworkEditor.jsx` - Artefacts editing area
- `/src/components/ArtefactEditor.jsx` - Artefact detail editor (20KB)
- `/src/components/ArtefactEditor.css` - Editor styles

**Backend:**
- `/backend/routes/frameworks.py`
  - `POST /api/frameworks/ai-fill` - AI fill artefact descriptions

**Data Structure:**
```javascript
artefacts: {
  default: {
    type: "Evaluation Results Summary",
    description: "A concise report summarizing findings..."
  },
  additional: [
    {
      id: "art-1",
      name: "Stakeholder Feedback Report",
      description: "Document capturing stakeholder input...",
      selected: true
    },
    {
      id: "art-2",
      name: "Risk Assessment Document",
      description: "Analysis of potential risks...",
      selected: true
    }
  ]
}
```

**AI Fill API Call:**
```javascript
// ArtefactEditor.jsx
const fillWithAI = async (artefactName) => {
  const response = await fetch(`${API_BASE_URL}/api/frameworks/ai-fill`, {
    method: 'POST',
    body: JSON.stringify({
      artefactName,
      frameworkContext: frameworkData.metadata.title
    })
  });
  const { description } = await response.json();
  // Update artefact description
};
```

---

#### **2.6.4 Risks**

**Features:**
- Lists potential risks during framework execution
- Each risk includes:
  - Risk title (title)
  - Risk description (description)
- Can add, edit, delete risk items

**Involved Files:**
- `/src/components/FrameworkEditor.jsx` - Risks editing section

**Data Structure:**
```javascript
risks: [
  {
    id: "risk-1",
    title: "Data Privacy Concerns",
    description: "Sensitive data handling requires compliance..."
  },
  {
    id: "risk-2",
    title: "Resource Constraints",
    description: "Limited team availability may delay progress..."
  }
]
```

---

#### **2.6.5 Escalation**

**Features:**
- Defines situations requiring escalation and corresponding measures
- Each escalation rule includes:
  - Trigger condition (trigger)
  - Response action (action)
- Can add, edit, delete escalation rules

**Involved Files:**
- `/src/components/FrameworkEditor.jsx` - Escalation editing section

**Data Structure:**
```javascript
escalation: [
  {
    id: "esc-1",
    trigger: "Critical security vulnerability detected",
    action: "Escalate to security team and pause deployment"
  },
  {
    id: "esc-2",
    trigger: "Budget overrun exceeds 20%",
    action: "Escalate to finance director for approval"
  }
]
```

---

#### **2.6.6 Merge Feature**

**User Scenario:** Merge multiple frameworks into current framework

**Flow:**
1. User clicks "Merge Frameworks" button
2. Opens `MergeModeDialog` to select merge method:
   - **Manual Merge** - Manual drag-and-drop merge
   - **AI Merge** - AI intelligent merge
3. Enters different merge modes based on selection

**Manual Merge:**
- Displays draggable framework list
- User drags frameworks into different parts of current framework
- System automatically merges Steps, Artefacts, Risks, Escalation

**AI Merge:**
- User selects frameworks to merge
- Backend AI analyzes framework content and intelligently merges
- Avoids duplicate content, optimizes structure

**Involved Files:**

**Frontend:**
- `/src/components/MergeModeDialog.jsx` - Merge method selection dialog
- `/src/components/ManualMergeMode.jsx` - Manual merge interface
- `/src/components/AIMergeMode.jsx` - AI merge interface (13KB)
- `/src/components/DraggableItem.jsx` - Draggable component
- `/src/components/DroppableFramework.jsx` - Drop target component

**Backend:**
- `/backend/routes/frameworks.py`
  - `POST /api/frameworks/ai-merge` - AI merge endpoint

**AI Merge API Logic:**
```python
# frameworks.py
@router.post("/ai-merge")
async def ai_merge_frameworks(request: AIMergeRequest):
    # 1. Get target framework and source frameworks
    target_framework = get_framework(request.target_id)
    source_frameworks = [get_framework(id) for id in request.source_ids]
    
    # 2. Call OpenAI to analyze content
    merged_content = call_openai_merge(target_framework, source_frameworks)
    
    # 3. Deduplicate and optimize
    optimized = optimize_merged_framework(merged_content)
    
    # 4. Return merged result
    return {"success": True, "framework": optimized}
```

---

#### **2.6.7 Auto-save Mechanism**

**Feature:** Prevents user data loss, automatically saves edited content

**Save Strategy:**
- **Trigger Condition:** After any field modification
- **Debounce Delay:** 2 seconds (avoids frequent saves)
- **Dual Save:**
  1. Firestore - Cloud persistence
  2. LocalStorage - Local backup

**Involved Files:**
- `/src/components/FrameworkEditor.jsx` - Auto-save logic

**Implementation Code:**
```javascript
// FrameworkEditor.jsx
useEffect(() => {
  if (!isSaved && frameworkData && id) {
    const timer = setTimeout(async () => {
      try {
        // 1. Save to Firestore
        await updateFramework(id, {
          metadata: frameworkData.metadata,
          steps: frameworkData.steps,
          artefacts: frameworkData.artefacts,
          risks: frameworkData.risks,
          escalation: frameworkData.escalation
        });
        
        // 2. Backup to localStorage
        localStorage.setItem(
          `framework-draft-${id}`,
          JSON.stringify(frameworkData)
        );
        
        console.log('✅ Auto-saved');
        setIsSaved(true);
      } catch (error) {
        console.error('❌ Auto-save failed:', error);
      }
    }, 2000);  // 2-second debounce
    
    return () => clearTimeout(timer);
  }
}, [frameworkData, isSaved, id]);
```

**Local Draft Recovery:**
- If local draft timestamp is newer than cloud, prompts user to recover
- User can choose to restore local version or use cloud version

---

#### **2.6.8 Export Feature**

**Supported Formats:**
- **.docx** - Word document (recommended)
- **.md** - Markdown file

**Export Flow:**
1. User clicks "Export .doc" or other export button
2. Frontend calls backend export API
3. Backend generates document based on framework data
4. Returns file for user download

**Involved Files:**

**Frontend:**
- `/src/components/FrameworkEditor.jsx` - Export button and download logic

**Backend:**
- `/backend/routes/frameworks.py`
  - `POST /api/frameworks/export-docx` - Generate Word document
  - `POST /api/frameworks/export-markdown` - Generate Markdown file
  - `generate_docx(framework_data)` - Word generation function (200 lines)
  - `generate_markdown(framework_data)` - Markdown generation function

**Word Document Generation Logic:**
```python
# frameworks.py
def generate_docx(framework_data: dict) -> bytes:
    from docx import Document
    doc = Document()
    
    # 1. Add title
    doc.add_heading(framework_data['metadata']['title'], 0)
    
    # 2. Add metadata table
    table = doc.add_table(rows=4, cols=2)
    table.cell(0, 0).text = 'Version'
    table.cell(0, 1).text = framework_data['metadata']['version']
    # ...
    
    # 3. Add Steps
    doc.add_heading('Framework Stages', 1)
    for step in framework_data['steps']:
        doc.add_heading(step['name'], 2)
        doc.add_paragraph(step['description'])
        # ...
    
    # 4. Add Artefacts, Risks, Escalation
    # ...
    
    # 5. Save to BytesIO
    from io import BytesIO
    buffer = BytesIO()
    doc.save(buffer)
    return buffer.getvalue()
```

---

### 2.7 Marketplace (Library) Page

**User Scenario:** Browse and use public framework templates published by other users

**Page Route:** `/library`

**Flow:**
1. User clicks "Marketplace" in navigation bar
2. System loads all frameworks with `publishStatus === 'library'` from Firestore
3. Displays grouped by category (Compliance, Technology, Healthcare, etc.)
4. User can:
   - View framework details
   - Download framework templates
   - Copy framework to their own workspace

**Involved Files:**

**Frontend:**
- `/src/components/Library.jsx` - Marketplace main component (9KB)
- `/src/components/LibraryCard.jsx` - Framework card display (10KB)
- `/src/lib/firebase.js` - Query public frameworks
  - `getPublishedFrameworks()` - Get Library frameworks

**Database Query:**
```javascript
// firebase.js
export const getPublishedFrameworks = async () => {
  const q = query(
    collection(db, 'frameworks'),
    where('publishStatus', '==', 'library'),
    orderBy('createdAt', 'desc')
  );
  const snapshot = await getDocs(q);
  return snapshot.docs.map(doc => ({ id: doc.id, ...doc.data() }));
};
```

**Framework Categories:**
```javascript
const categories = [
  { name: 'Compliance', count: 6 },
  { name: 'Technology', count: 1 },
  { name: 'Healthcare', count: 1 },
  { name: 'Research', count: 4 },
  { name: 'Financial', count: 2 },
  { name: 'Other', count: 15 }
];
```

---

### 2.8 Tenant Settings Page

**User Scenario:** Manage organization settings and member invitations

**Page Route:** `/{tenantId}/settings`

**Feature Modules:**

#### **2.8.1 Tenant Information Display**
- Tenant ID (subdomain)
- Organization name
- Creator information
- Creation time

#### **2.8.2 Member Management**
- Displays all current organization members
- Member list displays:
  - Member avatar/initial letters
  - Member email
  - Join time

#### **2.8.3 Invitation Feature**

**Invitation Flow:**
1. Organization owner clicks "Invite" button
2. System generates unique invitation token
3. Creates invitation link: `http://app.com/invite/{token}`
4. User copies link and sends to invitee
5. Invitee clicks link:
   - If not logged in, redirects to login first
   - After login, automatically joins organization
   - Updates user's tenantId

**Involved Files:**

**Frontend:**
- `/src/components/TenantSettings.jsx` - Settings page main component
- `/src/components/InviteAccept.jsx` - Invitation acceptance page (13KB)
- `/src/App.jsx` - Invitation route configuration (`/invite/:token`)

**Database (Firestore):**
- `invitations` collection
  ```json
  {
    "token": "unique-token-xxxxx",
    "tenantId": "my-organization",
    "inviterId": "inviter-uid",
    "expiresAt": "2025-12-25T00:00:00Z",
    "createdAt": "2025-11-25T00:00:00Z",
    "status": "pending"  // pending | accepted | expired
  }
  ```
- After invitation acceptance:
  - Updates `users` collection `tenantId`
  - Updates `tenants` collection `members` array
  - Updates `invitations` `status` to 'accepted'

**Invitation Link Generation:**
```javascript
// TenantSettings.jsx
const generateInviteLink = async () => {
  const token = generateToken();  // Generate random token
  await createInvitation({
    token,
    tenantId: user.tenantId,
    inviterId: user.uid,
    expiresAt: Date.now() + 7 * 24 * 60 * 60 * 1000  // 7-day validity
  });
  const link = `${window.location.origin}/invite/${token}`;
  navigator.clipboard.writeText(link);  // Copy to clipboard
  alert('Invite link copied!');
};
```

**Invitation Acceptance Logic:**
```javascript
// InviteAccept.jsx
useEffect(() => {
  const acceptInvite = async () => {
    const invitation = await getInvitationByToken(token);
    
    if (!invitation || invitation.status !== 'pending') {
      setError('Invalid or expired invitation');
      return;
    }
    
    // Update user tenantId
    await updateUserTenant(user.uid, invitation.tenantId);
    
    // Add user to organization
    await addTenantMember(invitation.tenantId, user.uid);
    
    // Mark invitation as accepted
    await updateInvitationStatus(token, 'accepted');
    
    // Redirect to organization workspace
    navigate(`/${invitation.tenantId}/frameworks`);
  };
  
  acceptInvite();
}, [token]);
```

---

### 2.9 My Organization Page

**User Scenario:** View frameworks published by all members within the organization

**Page Route:** `/{tenantId}/organization`

**Flow:**
1. User clicks "My Organization" in navigation bar
2. System queries all members of current organization
3. Loads all frameworks published to organization by members (`publishStatus === 'organization'`)
4. Displays grouped by category
5. User can:
   - View organization frameworks
   - Download frameworks
   - Copy frameworks to their own workspace

**Involved Files:**

**Frontend:**
- `/src/components/YourOrganization.jsx` - Organization frameworks page
- `/src/components/FrameworkCard.jsx` - Reuses framework card component
- `/src/lib/firebase.js`
  - `getOrganizationFrameworks(tenantId)` - Query organization frameworks

**Database Query:**
```javascript
// firebase.js
export const getOrganizationFrameworks = async (tenantId) => {
  const q = query(
    collection(db, 'frameworks'),
    where('tenantId', '==', tenantId),
    where('publishStatus', '==', 'organization'),
    orderBy('createdAt', 'desc')
  );
  const snapshot = await getDocs(q);
  return snapshot.docs.map(doc => ({ id: doc.id, ...doc.data() }));
};
```

**Publishing Framework to Organization:**
```javascript
// PublishModal.jsx
const publishToOrganization = async (frameworkId) => {
  await updateFramework(frameworkId, {
    publishStatus: 'organization',
    publishedAt: new Date().toISOString()
  });
  alert('Framework published to organization!');
};
```

---

### 2.10 Admin Panel Page

**User Scenario:** Administrators manage whitelist email domains

**Page Route:** `/admin`

**Features:**
- Add email domains allowed to register (e.g., `example.com`)
- Delete whitelist domains
- View all whitelist domain lists

**Involved Files:**

**Frontend:**
- `/src/components/AdminPanel.jsx` - Admin panel (13KB)

**Database (Firestore):**
- `whitelisted_domains` collection
  ```json
  {
    "domain": "example.com",
    "addedBy": "admin-uid",
    "addedAt": "2025-11-25T00:00:00Z"
  }
  ```

**Whitelist Validation:**
```javascript
// Signup.jsx
const checkDomainWhitelist = async (domain) => {
  const q = query(
    collection(db, 'whitelisted_domains'),
    where('domain', '==', domain)
  );
  const snapshot = await getDocs(q);
  return !snapshot.empty;
};
```

---

## 🗂️ III. Key Files Functionality Summary

### 3.1 Frontend File Structure

```
/src
├── main.jsx                    # Application entry point
├── App.jsx                     # Main application component and route configuration
├── App.css                     # Global styles
├── index.css                   # Base styles
│
├── components/                 # React components
│   ├── LandingPage.jsx         # Landing page (9KB)
│   ├── Login.jsx               # Login page (9KB)
│   ├── Signup.jsx              # Registration page
│   ├── TenantCreationModal.jsx # Tenant creation modal
│   ├── TenantRoute.jsx         # Tenant route protection component
│   ├── PrivateRoute.jsx        # Login route protection component
│   ├── Navbar.jsx              # Navigation bar
│   ├── CreateFramework.jsx     # Create framework page (36KB)
│   ├── YourFrameworks.jsx      # My frameworks list
│   ├── FrameworkCard.jsx       # Framework card component (20KB)
│   ├── FrameworkEditor.jsx     # Framework editor (70KB)
│   ├── ArtefactEditor.jsx      # Artefact editor (20KB)
│   ├── ArtefactEditor.css      # Editor styles
│   ├── Library.jsx             # Marketplace page (9KB)
│   ├── LibraryCard.jsx         # Library framework card (10KB)
│   ├── YourOrganization.jsx    # Organization frameworks page
│   ├── TenantSettings.jsx      # Tenant settings page
│   ├── InviteAccept.jsx        # Invitation acceptance page (13KB)
│   ├── AdminPanel.jsx          # Admin panel (13KB)
│   ├── MergeModeDialog.jsx     # Merge mode dialog
│   ├── ManualMergeMode.jsx     # Manual merge mode
│   ├── AIMergeMode.jsx         # AI merge mode (13KB)
│   ├── DraggableItem.jsx       # Draggable component
│   ├── DroppableFramework.jsx  # Drop target component (6KB)
│   ├── PrivacyLockDialog.jsx   # Privacy Protection dialog
│   ├── PrivacyNoticeDialog.jsx # Privacy notice dialog
│   ├── PublishModal.jsx        # Publish options modal
│   ├── LoadingDialog.jsx       # Loading dialog
│   └── MigrationTool.jsx       # Data migration tool
│
├── contexts/                   # React Context
│   └── AuthContext.jsx         # Authentication context
│
├── lib/                        # Utility libraries
│   ├── firebase.js             # Firebase configuration and methods
│   └── api.js                  # Backend API call methods
│
└── utils/                      # Utility functions
    ├── DataCleanupButton.jsx   # Data cleanup button
    ├── cleanupData.js          # Data cleanup script
    └── updateFrameworkTenants.js # Framework tenant update script
```

---

### 3.2 Backend File Structure

```
/backend
├── main.py                     # FastAPI application entry point
├── db.py                       # Database connection configuration
├── models.py                   # Data model definitions
├── auth.py                     # Authentication middleware
│
├── routes/                     # API routes
│   ├── frameworks.py           # Framework-related APIs (2506 lines)
│   │   ├── generate-from-text    # Text generate framework
│   │   ├── generate-from-file    # File generate framework (single)
│   │   ├── generate-from-files   # File generate framework (multiple)
│   │   ├── my-frameworks         # Get user framework list
│   │   ├── my-frameworks/by-family # Get frameworks by category
│   │   ├── /{id}                 # Get framework details
│   │   ├── /{id}/binding         # Get framework binding info
│   │   ├── PUT /{id}             # Update framework
│   │   ├── DELETE /{id}          # Delete framework
│   │   ├── export-markdown       # Export Markdown
│   │   ├── export-docx           # Export Word document
│   │   ├── regenerate            # Regenerate framework
│   │   ├── ai-merge              # AI merge frameworks
│   │   └── ai-fill               # AI fill content
│   │
│   └── auth.py                 # Authentication-related APIs (if any)
│
└── llm/                        # LLM modules
    ├── llm_local.py            # Local LLM (keyword extraction)
    └── llm_global.py           # OpenAI API calls
```

---

### 3.3 Core Data Models

#### **User**
```json
{
  "uid": "user-unique-id",
  "email": "user@example.com",
  "tenantId": "my-organization",
  "role": "expert",
  "createdAt": "2025-11-25T00:00:00Z"
}
```

#### **Tenant**
```json
{
  "tenantId": "my-organization",
  "name": "My Organization",
  "ownerId": "user-uid",
  "members": ["user-uid-1", "user-uid-2"],
  "createdAt": "2025-11-25T00:00:00Z",
  "subdomain": "my-organization"
}
```

#### **Framework**
```json
{
  "id": "framework-xxxxx",
  "creatorId": "user-uid",
  "tenantId": "my-organization",
  "metadata": {
    "title": "Framework Title",
    "version": "1.0",
    "tags": ["tag1", "tag2"],
    "family": "Technology",
    "confidence": 0.77,
    "lastUpdated": "2025-11-25T12:35:45Z",
    "pov": ["Point of view 1", "Point of view 2"]
  },
  "steps": [
    {
      "id": "step-1",
      "name": "Step Name",
      "description": "Step description",
      "subSteps": ["Sub-step 1", "Sub-step 2"]
    }
  ],
  "artefacts": {
    "default": {
      "type": "Report Type",
      "description": "Description"
    },
    "additional": [
      {
        "id": "art-1",
        "name": "Artefact Name",
        "description": "Description",
        "selected": true
      }
    ]
  },
  "risks": [
    {
      "id": "risk-1",
      "title": "Risk Title",
      "description": "Risk description"
    }
  ],
  "escalation": [
    {
      "id": "esc-1",
      "trigger": "Trigger condition",
      "action": "Action to take"
    }
  ],
  "publishStatus": "draft",  // draft | library | organization
  "createdAt": "2025-11-25T00:00:00Z",
  "updatedAt": "2025-11-25T12:35:45Z"
}
```

#### **Invitation**
```json
{
  "token": "unique-token-xxxxx",
  "tenantId": "my-organization",
  "inviterId": "inviter-uid",
  "expiresAt": "2025-12-25T00:00:00Z",
  "createdAt": "2025-11-25T00:00:00Z",
  "status": "pending"
}
```

#### **Whitelisted Domain**
```json
{
  "domain": "example.com",
  "addedBy": "admin-uid",
  "addedAt": "2025-11-25T00:00:00Z"
}
```

---

## 🔄 IV. Data Flow and System Interactions

### 4.1 Framework Generation Flow Data Flow

```
User inputs text/file
    ↓
CreateFramework.jsx
    ↓
api.js: generateFrameworkFromText()
    ↓
POST /api/frameworks/generate-from-text
    ↓
[Privacy Protection decision]
    ↓
├─ Enabled: llm_local.py → extract_seed()
│           ↓
│       llm_global.py → call_openai_framework(keywords)
│
└─ Disabled: llm_global.py → call_openai_framework(text)
    ↓
frameworks.py: save_framework_to_db()
    ↓
Firestore: frameworks collection
    ↓
Return framework_id
    ↓
Redirect to FrameworkEditor
```

---

### 4.2 Framework Editing and Saving Flow

```
User modifies framework content
    ↓
FrameworkEditor.jsx: setFrameworkData()
    ↓
[2-second debounce]
    ↓
updateFramework(id, data)
    ↓
├─ Firestore: Update frameworks document
│
└─ LocalStorage: Save local backup
    ↓
setIsSaved(true)
```

---

### 4.3 Invitation Flow Data Flow

```
Organization owner clicks "Invite"
    ↓
TenantSettings.jsx: generateInviteLink()
    ↓
Create invitation document in Firestore
    ↓
Generate invitation link: /invite/{token}
    ↓
Copy link and send to invitee
    ↓
Invitee clicks link
    ↓
InviteAccept.jsx: Get token
    ↓
Query invitation document
    ↓
Validate status and expiry
    ↓
Update user.tenantId
    ↓
Add user to tenant.members
    ↓
Update invitation.status = 'accepted'
    ↓
Redirect to /{tenantId}/frameworks
```

---

## 🛠️ V. Development and Debugging

### 5.1 View Logs

**Docker container logs:**
```bash
# View all service logs
docker-compose logs -f

# View frontend logs
docker-compose logs -f frontend

# View backend logs
docker-compose logs -f backend
```

**Frontend browser logs:**
- Open browser developer tools (F12)
- Check Console tab
- Key log identifiers:
  - `✅` - Successful operation
  - `❌` - Error information
  - `🔄` - Data synchronization

**Backend API logs:**
- FastAPI automatically generates logs
- Visit `http://localhost:8000/docs` to view API documentation
- View real-time request logs in terminal

---

### 5.2 Common Issue Troubleshooting

**Issue 1: Container fails to start**
- Check if Docker Desktop is running
- Check if ports 3000 and 8000 are occupied
- View error information in `docker-compose logs`

**Issue 2: API call fails**
- Check if API keys in `.env` file are correct
- Check if backend service is running normally
- View request details in browser Network tab

**Issue 3: Firebase connection fails**
- Check if Firebase configuration is correct
- Check network connection
- Verify if Firebase project has Firestore enabled

**Issue 4: Auto-save fails**
- Check Firestore write permissions
- View error information in browser Console
- Verify if user is logged in

---

### 5.3 Development Tools

**Recommended IDE:**
- VSCode + Extensions:
  - ESLint
  - Prettier
  - Tailwind CSS IntelliSense
  - Python

**API Testing Tools:**
- Postman - Test backend APIs
- FastAPI Swagger UI - `http://localhost:8000/docs`

**Database Management:**
- Firebase Console - Manage Firestore data online

---

## 📚 VI. Technology Stack Summary

### Frontend Technology Stack
- **Framework:** React 18
- **Build Tool:** Vite
- **Routing:** React Router v6
- **State Management:** React Context API
- **Styling:** Tailwind CSS
- **Database:** Firebase Firestore
- **Authentication:** Firebase Authentication
- **Drag & Drop:** React DnD (in Merge feature)

### Backend Technology Stack
- **Framework:** FastAPI
- **Database:** Firebase Firestore
- **LLM:**
  - Local LLM (keyword extraction)
  - OpenAI GPT-4o (framework generation)
- **Document Processing:**
  - python-docx (Word)
  - PyPDF2/pdfplumber (PDF)
  - openpyxl (Excel)
- **Deployment:** Docker + Docker Compose

### Cloud Services
- **Hosting Platform:** Google Cloud Platform (GCP)
- **Database:** Firebase Firestore
- **Authentication:** Firebase Authentication
- **Storage:** Firebase Storage (if needed)

---

## 🎯 VII. Future Development Suggestions

### 7.1 Feature Enhancement Suggestions
- Add framework version control and history
- Implement framework commenting and collaboration features
- Support more file format exports (PDF, PPT)
- Add framework sharing and permission management
- Implement real-time collaborative editing
- Organizaiton's owner can see the members activity(by a pie chart)

### 7.2 Performance Optimization Suggestions
- Implement framework content lazy loading
- Optimize rendering performance for large frameworks
- Add CDN acceleration for static resources
- Implement API response caching

### 7.3 User Experience Improvements
- Add framework template library
- Implement drag-and-drop sorting for framework lists
- Add keyboard shortcut support
- Improve mobile responsiveness

---

## 📞 Support and Contact

For questions or more information, please contact via:
- Email: [michaelgu0927@gmail.com]

---

**Document Version:** 1.0  
**Last Updated:** 2025-11-25  
**Maintainer:** [Zheyu Gu]
