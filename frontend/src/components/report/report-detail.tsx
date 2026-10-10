"use client";

import Link from "next/link";
import { useParams } from "next/navigation";
import { useEffect, useRef, useState } from "react";
import { ApiError, analyzeReport, getDocument } from "@/lib/api/client";
import type { AnalysisResponse, DocumentStatusResponse } from "@/lib/api/types";
import { formatBytes, formatDate } from "@/lib/format";
import { describeDocumentStatus } from "@/lib/result-status";
import { PageHeader } from "@/components/layout/page-header";
import { AnalysisResults } from "@/components/report/analysis-results";
import { Badge } from "@/components/ui/badge";
import { Button, buttonClasses } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { EmptyState, Skeleton, Spinner } from "@/components/ui/feedback";
import { IconArrowLeft, IconDocument, IconRefresh } from "@/components/ui/icons";
import { Notice } from "@/components/ui/notice";

const ANALYSIS_FAILED_MESSAGE = "The analysis could not be completed. Please try again.";

function analysisErrorMessage(error: unknown): string {
  // Client-side messages (validation, network, timeout) are safe to show.
  // Server 5xx details are replaced with a generic message.
  if (error instanceof ApiError && error.status < 500) return error.message;
  return ANALYSIS_FAILED_MESSAGE;
}

export function ReportDetail() {
  const params = useParams<{ documentId: string }>();
  const documentId = params.documentId;

  const [document, setDocument] = useState<DocumentStatusResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [loadError, setLoadError] = useState<{ status: number; message: string } | null>(null);
  const [attempt, setAttempt] = useState(0);

  const [analysis, setAnalysis] = useState<AnalysisResponse | null>(null);
  const [analyzing, setAnalyzing] = useState(false);
  const [analysisError, setAnalysisError] = useState<string | null>(null);
  const analysisInFlight = useRef(false);

  useEffect(() => {
    if (!documentId) return;

    const controller = new AbortController();

    (async () => {
      try {
        const data = await getDocument(documentId, controller.signal);
        if (controller.signal.aborted) return;
        setDocument(data);
        setLoadError(null);
      } catch (error) {
        if (controller.signal.aborted) return;
        if (error instanceof ApiError) {
          setLoadError({ status: error.status, message: error.message });
        } else {
          setLoadError({ status: 0, message: "We couldn't load this report. Please try again." });
        }
      } finally {
        if (!controller.signal.aborted) setLoading(false);
      }
    })();

    return () => controller.abort();
  }, [documentId, attempt]);

  function retryLoad() {
    setLoading(true);
    setLoadError(null);
    setAttempt((value) => value + 1);
  }

  async function runAnalysis() {
    if (!document || analysisInFlight.current) return;

    analysisInFlight.current = true;
    setAnalyzing(true);
    setAnalysisError(null);

    try {
      const result = await analyzeReport(document.document_id);
      setAnalysis(result);
      // The backend marks the document as processed only after a successful run.
      setDocument((current) => (current ? { ...current, status: "processed" } : current));
    } catch (error) {
      setAnalysisError(analysisErrorMessage(error));
    } finally {
      analysisInFlight.current = false;
      setAnalyzing(false);
    }
  }

  if (loading) {
    return <LoadingState />;
  }

  if (loadError || !document) {
    const notFound = loadError?.status === 404;
    return (
      <div className="space-y-8">
        <BackLink />
        <Card>
          <EmptyState
            icon={<IconDocument className="size-6" />}
            title={notFound ? "We couldn't find this report" : "This report isn't available"}
            action={
              notFound ? (
                <Link href="/upload" className={buttonClasses("primary")}>
                  Upload a report
                </Link>
              ) : (
                <Button variant="secondary" onClick={retryLoad}>
                  <IconRefresh className="size-4" />
                  Try again
                </Button>
              )
            }
          >
            {loadError?.message ?? "Please check the link and try again."}
          </EmptyState>
        </Card>
      </div>
    );
  }

  const status = describeDocumentStatus(document.status);
  const hasResults = analysis !== null;
  const actionLabel = hasResults
    ? "Run analysis again"
    : document.status === "failed"
      ? "Try analysis again"
      : document.status === "processing"
        ? "Restart analysis"
        : "Analyze report";

  return (
    <div className="space-y-8">
      <BackLink />

      <PageHeader
        eyebrow="Report"
        title={document.filename}
        description="Each value is shown with its unit and the reference range printed on the report."
      />

      <Card className="flex flex-col gap-5 p-6 sm:flex-row sm:items-center sm:justify-between">
        <dl className="grid grid-cols-2 gap-x-8 gap-y-3 text-sm sm:flex sm:flex-wrap">
          <div>
            <dt className="text-ink-500">Status</dt>
            <dd className="mt-1">
              <Badge tone={status.tone}>{status.label}</Badge>
            </dd>
          </div>
          <div>
            <dt className="text-ink-500">Uploaded</dt>
            <dd className="mt-1 font-medium text-ink-900">{formatDate(document.created_at)}</dd>
          </div>
          <div>
            <dt className="text-ink-500">File</dt>
            <dd className="num mt-1 font-medium text-ink-900">
              {document.file_type.toUpperCase()} · {formatBytes(document.size_bytes)}
            </dd>
          </div>
        </dl>

        <Button onClick={runAnalysis} disabled={analyzing} className="shrink-0 sm:min-w-44">
          {analyzing ? (
            <>
              <Spinner />
              Analyzing
            </>
          ) : (
            actionLabel
          )}
        </Button>
      </Card>

      {!analyzing && !hasResults && document.status === "uploaded" && (
        <Notice tone="info">
          Analysis reads the values, units and reference ranges printed in your report. It usually takes a few seconds.
        </Notice>
      )}

      {!analyzing && !hasResults && document.status === "failed" && (
        <Notice tone="caution" title="The last analysis didn't finish">
          You can try again. If it keeps failing, the file may be a scan or a format the analysis can&apos;t read yet.
        </Notice>
      )}

      {!analyzing && !hasResults && document.status === "processing" && (
        <Notice tone="info" title="An earlier analysis didn't finish">
          You can start it again.
        </Notice>
      )}

      {!analyzing && !hasResults && document.status === "processed" && (
        <Notice tone="info">
          Results from earlier analyses aren&apos;t stored yet, so run the analysis again to view them.
        </Notice>
      )}

      {analysisError && (
        <Notice tone="danger" title="Analysis unsuccessful">
          {analysisError}
        </Notice>
      )}

      {analyzing && <AnalyzingState />}

      {!analyzing && analysis && <AnalysisResults analysis={analysis} />}
    </div>
  );
}

function BackLink() {
  return (
    <Link
      href="/upload"
      className="inline-flex items-center gap-2 text-sm font-medium text-ink-700 transition-colors hover:text-ink-900"
    >
      <IconArrowLeft className="size-4" />
      Back to upload
    </Link>
  );
}

export function ReportDetailFallback() {
  return <LoadingState />;
}

function LoadingState() {
  return (
    <div className="space-y-8" aria-busy="true" aria-live="polite">
      <span className="sr-only">Loading report</span>
      <Skeleton className="h-4 w-24" />
      <Skeleton className="h-10 w-2/3" />
      <Skeleton className="h-28 w-full rounded-2xl" />
      <Skeleton className="h-64 w-full rounded-2xl" />
    </div>
  );
}

function AnalyzingState() {
  return (
    <Card className="p-8">
      <div className="flex items-start gap-4" role="status">
        <span className="grid size-11 shrink-0 place-items-center rounded-xl bg-brand-50 text-brand-700">
          <Spinner className="size-5" />
        </span>
        <div>
          <p className="font-semibold text-ink-900">Analyzing your report</p>
          <p className="mt-1 text-sm leading-relaxed text-ink-500">
            This can take a moment. Keep this page open until the results appear.
          </p>
        </div>
      </div>
      <div className="mt-8 grid gap-3 sm:grid-cols-5">
        {Array.from({ length: 5 }, (_, index) => (
          <Skeleton key={index} className="h-20" />
        ))}
      </div>
    </Card>
  );
}
