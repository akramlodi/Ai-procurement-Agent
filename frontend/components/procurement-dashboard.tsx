"use client"

import type { FormEvent } from "react"
import { useEffect, useMemo, useRef, useState } from "react"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Separator } from "@/components/ui/separator"
import { toast } from "sonner"
import { CheckCircle2, FileText, FolderKanban, Loader2, PlusCircle, Sparkles, Upload, XCircle } from "lucide-react"

const API_BASE = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000"

type ProcurementDocument = {
  id: string
  filename: string
  document_type: string
  document_status: string
  ai_summary: string | null
  uploaded_at: string
}

type ProcurementWorkspace = {
  id: string
  name: string
  description: string
  status: string
  createdAt: string
  documents: ProcurementDocument[]
}

export function ProcurementDashboard() {
  const [workspaces, setWorkspaces] = useState<ProcurementWorkspace[]>([])
  const [activeWorkspaceId, setActiveWorkspaceId] = useState("")
  const [workspaceName, setWorkspaceName] = useState("")
  const [workspaceDescription, setWorkspaceDescription] = useState("")
  const [selectedFiles, setSelectedFiles] = useState<FileList | null>(null)
  const [isLoaded, setIsLoaded] = useState(false)
  const [isCreating, setIsCreating] = useState(false)
  const [isUploading, setIsUploading] = useState(false)
  const pollRef = useRef<ReturnType<typeof setInterval> | null>(null)

  useEffect(() => {
    fetchWorkspaces()
  }, [])

  async function fetchWorkspaces() {
    try {
      const res = await fetch(`${API_BASE}/api/workspaces`)
      if (!res.ok) throw new Error("Failed to fetch workspaces")
      const data = await res.json()
      const mapped: ProcurementWorkspace[] = data.map((row: Record<string, string>) => ({
        id: row.id,
        name: row.name,
        description: row.description,
        status: row.status,
        createdAt: row.created_at,
        documents: [],
      }))
      setWorkspaces(mapped)
      if (mapped.length) setActiveWorkspaceId(mapped[0].id)
    } catch {
      toast.error("Could not load workspaces from server")
    } finally {
      setIsLoaded(true)
    }
  }

  async function fetchDocuments(workspaceId: string) {
    try {
      const res = await fetch(`${API_BASE}/api/workspaces/${workspaceId}/documents`)
      if (!res.ok) return
      const docs = await res.json()
      setWorkspaces((current) =>
        current.map((ws) =>
          ws.id === workspaceId
            ? { ...ws, documents: docs.map((d: Record<string, string>) => ({
                id: d.id,
                filename: d.filename,
                document_type: d.document_type,
                document_status: d.document_status,
                ai_summary: d.ai_summary,
                uploaded_at: d.uploaded_at,
              }))}
            : ws,
        ),
      )
    } catch {
      // silent — will retry on next poll
    }
  }

  useEffect(() => {
    if (!activeWorkspaceId) return
    fetchDocuments(activeWorkspaceId)
  }, [activeWorkspaceId])

  useEffect(() => {
    if (pollRef.current) clearInterval(pollRef.current)
    if (!activeWorkspaceId) return

    const hasProcessing = workspaces
      .find((ws) => ws.id === activeWorkspaceId)
      ?.documents.some((d) => d.document_status === "processing")

    if (hasProcessing) {
      pollRef.current = setInterval(() => {
        fetchDocuments(activeWorkspaceId)
      }, 3000)
    }

    return () => {
      if (pollRef.current) clearInterval(pollRef.current)
    }
  }, [activeWorkspaceId, workspaces])

  useEffect(() => {
    if (!activeWorkspaceId && workspaces.length) {
      setActiveWorkspaceId(workspaces[0].id)
    }
  }, [activeWorkspaceId, workspaces])

  const activeWorkspace = useMemo(
    () => workspaces.find((workspace) => workspace.id === activeWorkspaceId) ?? workspaces[0],
    [activeWorkspaceId, workspaces],
  )

  const summary = useMemo(() => {
    const totalDocuments = workspaces.reduce((sum, workspace) => sum + workspace.documents.length, 0)
    const pendingReview = workspaces.filter((workspace) => workspace.status === "Evaluation").length

    return {
      totalWorkspaces: workspaces.length,
      totalDocuments,
      pendingReview,
    }
  }, [workspaces])

  const createWorkspace = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault()

    const name = workspaceName.trim()
    if (!name) return

    setIsCreating(true)
    try {
      const res = await fetch(`${API_BASE}/api/workspaces`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          name,
          description: workspaceDescription.trim() || "New procurement workspace for document review and supplier evaluation.",
          status: "Draft",
        }),
      })

      if (!res.ok) throw new Error("Failed to create workspace")

      const row = await res.json()
      const createdWorkspace: ProcurementWorkspace = {
        id: row.id,
        name: row.name,
        description: row.description,
        status: row.status,
        createdAt: row.created_at,
        documents: [],
      }

      setWorkspaces((current) => [createdWorkspace, ...current])
      setActiveWorkspaceId(createdWorkspace.id)
      setWorkspaceName("")
      setWorkspaceDescription("")
      toast.success("Workspace created")
    } catch {
      toast.error("Failed to create workspace. Is the backend running?")
    } finally {
      setIsCreating(false)
    }
  }

  const uploadDocuments = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault()

    if (!activeWorkspace || !selectedFiles?.length) return

    const formData = new FormData()
    Array.from(selectedFiles).forEach((file) => formData.append("files", file))

    setIsUploading(true)
    try {
      const res = await fetch(`${API_BASE}/api/workspaces/${activeWorkspace.id}/documents`, {
        method: "POST",
        body: formData,
      })

      if (!res.ok) throw new Error("Upload failed")

      const created = await res.json()
      const newDocs: ProcurementDocument[] = created.map((d: Record<string, string>) => ({
        id: d.id,
        filename: d.filename,
        document_type: d.document_type,
        document_status: d.document_status,
        ai_summary: d.ai_summary,
        uploaded_at: d.uploaded_at,
      }))

      setWorkspaces((current) =>
        current.map((ws) =>
          ws.id === activeWorkspace.id
            ? { ...ws, documents: [...newDocs, ...ws.documents] }
            : ws,
        ),
      )

      toast.success(`${newDocs.length} document(s) uploaded, processing started`)
    } catch {
      toast.error("Failed to upload documents. Is the backend running?")
    } finally {
      setIsUploading(false)
      setSelectedFiles(null)
      const input = document.getElementById("document-upload") as HTMLInputElement | null
      if (input) input.value = ""
    }
  }

  function statusBadge(status: string) {
    if (status === "completed") return <Badge variant="secondary" className="bg-emerald-100 text-emerald-700 dark:bg-emerald-900 dark:text-emerald-300">Completed</Badge>
    if (status === "processing") return <Badge variant="secondary" className="bg-amber-100 text-amber-700 dark:bg-amber-900 dark:text-amber-300"><Loader2 className="mr-1 h-3 w-3 animate-spin" />Processing</Badge>
    if (status === "failed") return <Badge variant="secondary" className="bg-red-100 text-red-700 dark:bg-red-900 dark:text-red-300"><XCircle className="mr-1 h-3 w-3" />Failed</Badge>
    return <Badge variant="outline">{status}</Badge>
  }

  return (
    <div className="flex flex-1 flex-col">
      <div className="flex flex-col gap-4 py-4 md:gap-6 md:py-6">
        <div className="px-4 lg:px-6">
          <div className="rounded-2xl border bg-background/95 p-6 shadow-sm">
            <div className="flex flex-col gap-4 lg:flex-row lg:items-start lg:justify-between">
              <div className="space-y-2">
                <div className="flex items-center gap-2">
                  <Sparkles className="h-5 w-5 text-primary" />
                  <p className="text-sm font-medium text-muted-foreground">Procurement workspace cockpit</p>
                </div>
                <h2 className="text-2xl font-semibold tracking-tight">Manage sourcing intake, supplier documents, and next steps in one place.</h2>
                <p className="max-w-2xl text-sm text-muted-foreground">
                  Create a workspace, add procurement documents, and keep the evaluation context ready for AI-assisted review.
                </p>
              </div>
              <div className="flex flex-wrap gap-2">
                <Badge variant="secondary">{summary.totalWorkspaces} workspaces</Badge>
                <Badge variant="secondary">{summary.totalDocuments} documents</Badge>
                <Badge variant="secondary">{summary.pendingReview} evaluating</Badge>
              </div>
            </div>
          </div>
        </div>

        <div className="grid gap-4 px-4 lg:grid-cols-[1.1fr_0.9fr] lg:px-6">
          <Card className="border-border/60">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <PlusCircle className="h-5 w-5" />
                Create procurement workspace
              </CardTitle>
              <CardDescription>
                Start a new evaluation record for a sourcing event, contract review, or supplier comparison.
              </CardDescription>
            </CardHeader>
            <CardContent>
              <form className="space-y-4" onSubmit={createWorkspace}>
                <div className="space-y-2">
                  <Label htmlFor="workspace-name">Workspace name</Label>
                  <Input
                    id="workspace-name"
                    placeholder="Example: Network Equipment Procurement"
                    value={workspaceName}
                    onChange={(event) => setWorkspaceName(event.target.value)}
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="workspace-description">Description</Label>
                  <Input
                    id="workspace-description"
                    placeholder="Describe the procurement scope"
                    value={workspaceDescription}
                    onChange={(event) => setWorkspaceDescription(event.target.value)}
                  />
                </div>
                <Button type="submit" className="w-full" disabled={isCreating || !workspaceName.trim()}>
                  {isCreating ? "Creating..." : "Create workspace"}
                </Button>
              </form>
            </CardContent>
          </Card>

          <Card className="border-border/60">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <FolderKanban className="h-5 w-5" />
                Existing workspaces
              </CardTitle>
              <CardDescription>Select a workspace to attach documents and track progress.</CardDescription>
            </CardHeader>
            <CardContent className="space-y-3">
              {workspaces.map((workspace) => {
                const isActive = workspace.id === activeWorkspace?.id

                return (
                  <button
                    key={workspace.id}
                    type="button"
                    onClick={() => setActiveWorkspaceId(workspace.id)}
                    className={`w-full rounded-xl border p-4 text-left transition ${isActive ? "border-primary bg-primary/5" : "border-border/60 bg-background hover:bg-muted/40"}`}
                  >
                    <div className="flex items-start justify-between gap-2">
                      <div>
                        <p className="font-medium">{workspace.name}</p>
                        <p className="mt-1 text-sm text-muted-foreground">{workspace.description}</p>
                      </div>
                      <Badge variant="secondary">{workspace.status}</Badge>
                    </div>
                    <div className="mt-3 flex items-center justify-between text-sm text-muted-foreground">
                      <span>{workspace.documents.length} documents</span>
                      <span>{workspace.createdAt}</span>
                    </div>
                  </button>
                )
              })}
            </CardContent>
          </Card>
        </div>

        <div className="px-4 lg:px-6">
          <Card className="border-border/60">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Upload className="h-5 w-5" />
                Upload documents
              </CardTitle>
              <CardDescription>
                Add purchase requests, technical specs, quotations, and contract files to the active workspace.
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="rounded-xl border border-dashed border-border/70 bg-muted/20 p-4">
                <form className="space-y-4" onSubmit={uploadDocuments}>
                  <div className="space-y-2">
                    <Label htmlFor="document-upload">Select files</Label>
                    <Input
                      id="document-upload"
                      type="file"
                      multiple
                      accept=".pdf,.docx"
                      onChange={(event) => setSelectedFiles(event.target.files)}
                    />
                  </div>
                  <div className="flex items-center justify-between gap-2 rounded-lg bg-background/80 p-3 text-sm">
                    <span className="text-muted-foreground">
                      {activeWorkspace ? `Active workspace: ${activeWorkspace.name}` : "Create a workspace to begin"}
                    </span>
                    <Button type="submit" disabled={isUploading || !activeWorkspace || !selectedFiles?.length}>
                      {isUploading ? (
                        <><Loader2 className="mr-2 h-4 w-4 animate-spin" />Uploading...</>
                      ) : (
                        "Add to workspace"
                      )}
                    </Button>
                  </div>
                </form>
              </div>

              <Separator />

              <div className="space-y-3">
                <div className="flex items-center justify-between">
                  <h3 className="font-medium">Documents in {activeWorkspace?.name ?? "the selected workspace"}</h3>
                  <Badge variant="outline">{activeWorkspace?.documents.length ?? 0} files</Badge>
                </div>
                {activeWorkspace?.documents.length ? (
                  <div className="space-y-2">
                    {activeWorkspace.documents.map((document) => (
                      <div key={document.id} className="flex items-center justify-between rounded-lg border border-border/60 bg-background px-3 py-2">
                        <div className="flex items-center gap-2">
                          <FileText className="h-4 w-4 text-primary" />
                          <div>
                            <p className="text-sm font-medium">{document.filename}</p>
                            <p className="text-xs text-muted-foreground">{document.document_type}</p>
                          </div>
                        </div>
                        <div className="flex items-center gap-2">
                          {statusBadge(document.document_status)}
                        </div>
                      </div>
                    ))}
                  </div>
                ) : (
                  <p className="rounded-lg border border-dashed border-border/60 p-4 text-sm text-muted-foreground">
                    No documents added yet. Upload a request, quote, or contract to populate the workspace.
                  </p>
                )}
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  )
}
