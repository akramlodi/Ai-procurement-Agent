# AI Procurement Intelligence Platform (MVP)

## Enterprise Multi-Agent Procurement Copilot

# Vision

Build an AI-first procurement workspace for a Procurement Officer. The
goal is **not** to replace an ERP system, but to help a procurement
officer evaluate procurement documents, compare suppliers, answer
procurement questions, and generate recommendation reports using AI.

The MVP focuses on **one user** (Sarah, the Procurement Officer).
Authentication, approvals, and multi-user collaboration are
intentionally omitted so development can focus on the AI architecture.

------------------------------------------------------------------------

# User Persona

## Sarah - Procurement Officer

Sarah receives procurement documents from other departments and
suppliers.

Examples: - Purchase Request - Technical Specifications - Supplier
Quotations - Draft Contracts

Her job is to: - Organize procurement documents - Compare suppliers -
Understand contracts - Answer management questions - Recommend the best
supplier - Generate procurement reports

------------------------------------------------------------------------

# MVP Goals

-   AI-assisted document understanding
-   Intelligent supplier comparison
-   Natural language procurement assistant
-   Explainable AI with citations
-   Agent-based architecture using LangGraph

------------------------------------------------------------------------

# User Flow

## Step 1 - Dashboard

The application opens directly into a Dashboard (no authentication).

Sarah sees:

-   Existing Procurement Workspaces
-   Create New Procurement button

Example:

Laptop Procurement

Office Furniture Procurement

Network Equipment Procurement

------------------------------------------------------------------------

## Step 2 - Create Procurement Workspace

Sarah creates a new procurement workspace.

Example:

Name: Laptop Procurement

Description: Purchase of 100 laptops for IT department

Status: Evaluation

This workspace contains everything related to this procurement.

------------------------------------------------------------------------

## Step 3 - Upload Documents

Sarah uploads documents into the workspace.

Supported:

-   PDF
-   DOCX
-   XLSX
-   CSV

Typical uploads:

-   Purchase Request
-   Technical Specifications
-   Dell Quotation
-   HP Quotation
-   Lenovo Quotation
-   Draft Contract

------------------------------------------------------------------------

## Step 4 - AI Processing

Immediately after upload the system automatically:

1.  Extracts text
2.  Detects document type
3.  Extracts suppliers
4.  Extracts prices
5.  Extracts delivery dates
6.  Extracts warranty
7.  Extracts payment terms
8.  Creates document chunks
9.  Generates embeddings
10. Stores structured data in PostgreSQL
11. Vector Store pgvector (inside Supabase)

The user does not perform any manual extraction.

------------------------------------------------------------------------

## Step 5 - Procurement Overview

The workspace now shows

-   Procurement summary
-   Number of suppliers
-   Documents uploaded
-   AI Insights

Example:

✓ 3 quotations detected

✓ Lowest price: HP

✓ Best warranty: Lenovo

✓ Missing penalty clause

------------------------------------------------------------------------

## Step 6 - Supplier Comparison

Sarah clicks Supplier Comparison.

The application automatically generates a comparison table.

Columns include:

-   Supplier
-   Price
-   Warranty
-   Delivery Time
-   Payment Terms
-   Compliance
-   AI Score

Below the table the AI explains its recommendation.

------------------------------------------------------------------------

## Step 7 - Ask Questions

Sarah asks questions naturally.

Examples:

-   Which supplier is cheapest?
-   Why is Lenovo recommended?
-   Summarize this contract.
-   Does this contract contain a penalty clause?
-   Compare Dell and HP.
-   Which supplier has the lowest risk?

Every answer includes supporting citations.

------------------------------------------------------------------------

## Step 8 - Generate Report

Sarah clicks Generate Report.

The application generates:

-   Executive Summary
-   Supplier Comparison
-   Risk Assessment
-   AI Recommendation
-   Supporting Evidence

Export as PDF.

------------------------------------------------------------------------

# Agent Architecture

The user never interacts with agents directly.

LangGraph orchestrates all agents.

## 1. Planner Agent

Responsibilities:

-   Understand user intent
-   Decide which agents should execute
-   Build an execution plan
-   Return structured routing decisions

Example:

Question:

"Compare Dell and HP."

Planner decides:

-   SQL Agent
-   Retrieval Agent
-   Procurement Expert Agent

No reasoning happens here.

------------------------------------------------------------------------

## 2. SQL Agent

Responsible for structured procurement data.

Reads:

-   Suppliers
-   Quotations
-   Procurement metadata
-   Extracted prices
-   Delivery dates
-   Warranty
-   Payment terms

Example questions:

-   Which supplier is cheapest?
-   Show all suppliers.
-   Compare delivery dates.

The SQL Agent converts natural language into SQL queries over PostgreSQL
(Supabase).

------------------------------------------------------------------------

## 3. Retrieval Agent

Responsible for document retrieval.

Uses:

-   Vector Store pgvector (inside Supabase)
-   Hybrid Retrieval
-   BM25 + Embeddings (future enhancement)

Retrieves:

-   Contracts
-   Quotations
-   Technical Specifications
-   Purchase Requests

Returns only relevant context.

------------------------------------------------------------------------

## 4. Procurement Expert Agent

The reasoning agent.

Combines:

-   SQL results
-   Retrieved document context
-   User question

Produces:

-   Comparisons
-   Recommendations
-   Explanations
-   Procurement insights

------------------------------------------------------------------------

## 5. Critic Agent

Final quality check.

Verifies:

-   Every claim is supported
-   Citations exist
-   No contradictory statements
-   Response is complete

Only then returns the final answer.

------------------------------------------------------------------------

# LangGraph Flow

Question

↓

Planner

↓

(SQL Agent + Retrieval Agent)

↓

Procurement Expert

↓

Critic

↓

Answer

LangGraph is used because it provides explicit graph-based
orchestration, state management, branching, retries, and easy
extensibility for adding future agents.

------------------------------------------------------------------------

# Data Architecture

## Structured Data (Supabase PostgreSQL)

Stores:

-   Procurement Workspaces
-   Suppliers
-   Quotations
-   Contracts (metadata)
-   Extracted procurement fields
-   Reports

Used by SQL Agent.

------------------------------------------------------------------------

## Vector Database (Vector Store
pgvector (inside Supabase)B)

Stores:

-   Document chunks
-   Embeddings
-   Metadata

Used by Retrieval Agent.

------------------------------------------------------------------------

## File Storage

Supabase Storage

Stores:

-   PDFs
-   DOCX
-   XLSX
-   CSV

------------------------------------------------------------------------

# Suggested Tech Stack

## Frontend

-   Next.js 
-   TypeScript
-   Tailwind CSS
-   shadcn/ui


## Backend

-   FastAPI (AI services)
-   Next.js Route Handlers (UI APIs)

## Database

-   Supabase PostgreSQL
-   Supabase Storage

## AI

-   LangGraph (agent orchestration)
-   LangChain (document loaders, retrievers, prompts)
-   Gemini 2.5 Flash Lite (planning & reasoning)
-   Gemini 2.5 Flash Lite (information extraction)
-   Vector Store pgvector (inside Supabase)
-   sentence-transformers/all-MiniLM-L6-v2 embeddings via @huggingface/inference

## Document Processing

-   Docling
-   PyMuPDF
-   python-docx
-   Polars
-   Pandas

## Deployment

-   Vercel (Next.js)
-   Railway or Render (FastAPI)
-   Supabase
-   Vector Store pgvector (inside Supabase)

## Observability

-   LangSmith
-   PostHog (will be done later)

------------------------------------------------------------------------

# Why LangGraph?

LangGraph is the core of the application.

It enables:

-   Planner-first architecture
-   Explicit execution graphs
-   Parallel execution of SQL and Retrieval agents
-   Shared graph state
-   Retry and error handling
-   Easy addition of future agents

The application is intentionally designed around **decision making**
rather than a simple chatbot. Every user request is first planned, then
routed to the appropriate specialists before being synthesized into a
grounded, explainable response.

------------------------------------------------------------------------

# Future Enhancements

-   Authentication
-   Multiple user roles
-   Approval workflows
-   ERP integrations
-   Knowledge Graph (Neo4j)
-   Procurement analytics dashboard
-   Email ingestion
-   Agent memory
-   Fine-tuned procurement models
