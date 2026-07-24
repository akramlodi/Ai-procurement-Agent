# AI Procurement Agent

A Next.js-based procurement intelligence MVP focused on helping a procurement officer manage procurement workspaces, upload documents, and prepare for AI-assisted supplier evaluation.

## Implemented so far

### Phase 1 — Procurement Workspace Dashboard
Completed:
- A shadcn-based procurement dashboard UI
- Create new procurement workspace flow
- Select and switch between existing workspaces
- Upload multiple procurement documents into the active workspace
- Display uploaded documents with metadata
- Local persistence of workspaces and uploaded documents in the browser

### Current stack
- Next.js 16
- React 19
- TypeScript
- Tailwind CSS
- shadcn/ui
- lucide-react

## Getting started

1. Install dependencies
   ```bash
   npm install
   ```

2. Run the development server
   ```bash
   npm run dev
   ```

3. Open the app in your browser
   - Dashboard: http://localhost:3000/dashboard

## Project structure

- app/ - app router pages
- components/ - reusable UI components
- public/ - static assets

## Notes

This MVP currently focuses on the first phase of the procurement workflow: workspace creation and document intake. Future phases can expand into AI analysis, supplier comparison, and report generation.
