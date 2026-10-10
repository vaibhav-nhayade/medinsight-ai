"use client";

import Link from "next/link";
import { useId, useRef, useState, type ChangeEvent, type DragEvent } from "react";
import { ApiError, uploadReport } from "@/lib/api/client";
import type { UploadResponse } from "@/lib/api/types";
import { cx } from "@/lib/cx";
import { formatBytes } from "@/lib/format";
import { ACCEPT_ATTRIBUTE, validateReportFile } from "@/lib/report-rules";
import { Badge } from "@/components/ui/badge";
import { Button, buttonClasses } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Spinner } from "@/components/ui/feedback";
import { IconDocument, IconRefresh, IconUpload, IconCheck, IconClose } from "@/components/ui/icons";
import { Notice } from "@/components/ui/notice";

type Phase = "idle" | "uploading" | "uploaded" | "error";

const GENERIC_UPLOAD_ERROR = "The upload could not be completed. Please try again.";

export function UploadReport() {
  const inputId = useId();
  const inputRef = useRef<HTMLInputElement>(null);
  const controllerRef = useRef<AbortController | null>(null);

  const [file, setFile] = useState<File | null>(null);
  const [selectionError, setSelectionError] = useState<string | null>(null);
  const [isDragging, setIsDragging] = useState(false);
  const [phase, setPhase] = useState<Phase>("idle");
  const [progress, setProgress] = useState(0);
  const [uploaded, setUploaded] = useState<UploadResponse | null>(null);
  const [submitError, setSubmitError] = useState<string | null>(null);

  const isUploading = phase === "uploading";

  function chooseFile(candidate: File | undefined) {
    if (!candidate || isUploading) return;

    const problem = validateReportFile(candidate);
    setSelectionError(problem);
    setFile(problem ? null : candidate);
    setPhase("idle");
    setUploaded(null);
    setSubmitError(null);
    setProgress(0);
  }

  function handleInputChange(event: ChangeEvent<HTMLInputElement>) {
    chooseFile(event.target.files?.[0]);
    // Allow choosing the same file again after removing it.
    event.target.value = "";
  }

  function handleDrop(event: DragEvent<HTMLDivElement>) {
    event.preventDefault();
    setIsDragging(false);
    chooseFile(event.dataTransfer.files[0]);
  }

  function reset() {
    setFile(null);
    setSelectionError(null);
    setPhase("idle");
    setUploaded(null);
    setSubmitError(null);
    setProgress(0);
  }

  async function handleUpload() {
    // Ref-based guard blocks duplicate submissions even before re-render.
    if (!file || controllerRef.current) return;

    const controller = new AbortController();
    controllerRef.current = controller;
    setPhase("uploading");
    setProgress(0);
    setSubmitError(null);

    try {
      const result = await uploadReport(file, {
        onProgress: setProgress,
        signal: controller.signal,
      });
      setUploaded(result);
      setPhase("uploaded");
    } catch (error) {
      if (controller.signal.aborted) {
        setPhase("idle");
      } else {
        // ApiError messages are already safe for display (5xx details are generalized).
        setSubmitError(error instanceof ApiError ? error.message : GENERIC_UPLOAD_ERROR);
        setPhase("error");
      }
    } finally {
      controllerRef.current = null;
    }
  }

  function cancelUpload() {
    controllerRef.current?.abort();
  }

  const percent = Math.round(progress * 100);

  return (
    <div className="grid gap-6 lg:grid-cols-5">
      <Card className="p-6 sm:p-8 lg:col-span-3">
        {phase === "uploaded" && uploaded ? (
          <UploadSuccess report={uploaded} onUploadAnother={reset} />
        ) : (
          <>
            <div
              onDragOver={(event) => {
                event.preventDefault();
                if (!isUploading) setIsDragging(true);
              }}
              onDragLeave={() => setIsDragging(false)}
              onDrop={handleDrop}
              className={cx(
                "rounded-2xl border-2 border-dashed p-8 text-center transition-colors duration-150 sm:p-10",
                isDragging ? "border-brand-600 bg-brand-50" : "border-line-strong bg-surface-muted",
              )}
            >
              <input
                ref={inputRef}
                id={inputId}
                type="file"
                accept={ACCEPT_ATTRIBUTE}
                onChange={handleInputChange}
                className="sr-only"
                tabIndex={-1}
                aria-hidden="true"
                disabled={isUploading}
              />

              {!file ? (
                <div className="flex flex-col items-center">
                  <span className="grid size-14 place-items-center rounded-2xl bg-brand-50 text-brand-700">
                    <IconUpload className="size-6" />
                  </span>
                  <p className="mt-5 text-base font-semibold text-ink-900">Drop your PDF report here</p>
                  <p className="mt-1 text-sm text-ink-500">
                    or choose a file from your device · up to 10 MB
                  </p>
                  <Button
                    variant="secondary"
                    className="mt-6"
                    onClick={() => inputRef.current?.click()}
                    disabled={isUploading}
                  >
                    Choose a PDF
                  </Button>
                </div>
              ) : (
                <div className="flex flex-col items-center gap-5 sm:flex-row sm:text-left">
                  <span className="grid size-14 shrink-0 place-items-center rounded-2xl bg-brand-50 text-brand-700">
                    <IconDocument className="size-6" />
                  </span>
                  <div className="min-w-0 flex-1">
                    <p className="break-all text-base font-semibold text-ink-900">{file.name}</p>
                    <p className="num mt-1 text-sm text-ink-500">
                      {formatBytes(file.size)} · PDF
                    </p>
                  </div>
                  <div className="flex gap-2">
                    <Button
                      variant="secondary"
                      onClick={() => inputRef.current?.click()}
                      disabled={isUploading}
                    >
                      <IconRefresh className="size-4" />
                      Replace
                    </Button>
                    <Button variant="ghost" onClick={reset} disabled={isUploading}>
                      <IconClose className="size-4" />
                      Remove
                    </Button>
                  </div>
                </div>
              )}
            </div>

            {selectionError && (
              <div className="mt-4">
                <Notice tone="danger">{selectionError}</Notice>
              </div>
            )}

            {isUploading && (
              <div className="mt-6 space-y-3" aria-live="polite">
                <div className="flex items-center justify-between text-sm text-ink-700">
                  <span className="flex items-center gap-2">
                    <Spinner className="text-brand-600" />
                    {progress < 1 ? "Uploading report…" : "Saving report…"}
                  </span>
                  <span className="num font-medium">{percent}%</span>
                </div>
                <div
                  role="progressbar"
                  aria-label="Upload progress"
                  aria-valuemin={0}
                  aria-valuemax={100}
                  aria-valuenow={percent}
                  className="h-2 overflow-hidden rounded-full bg-line"
                >
                  <div
                    className="h-full rounded-full bg-brand-600 transition-[width] duration-200"
                    style={{ width: `${percent}%` }}
                  />
                </div>
              </div>
            )}

            {submitError && (
              <div className="mt-6">
                <Notice tone="danger" title="Upload unsuccessful">
                  {submitError}
                </Notice>
              </div>
            )}

            <div className="mt-6 flex flex-col-reverse gap-3 sm:flex-row sm:justify-end">
              {isUploading ? (
                <Button variant="secondary" onClick={cancelUpload}>
                  Cancel upload
                </Button>
              ) : null}
              <Button
                onClick={handleUpload}
                disabled={!file || isUploading}
                className="sm:min-w-40"
              >
                {isUploading ? (
                  <>
                    <Spinner />
                    Uploading
                  </>
                ) : phase === "error" ? (
                  "Try again"
                ) : (
                  "Upload report"
                )}
              </Button>
            </div>
          </>
        )}
      </Card>

      <aside className="space-y-4 lg:col-span-2">
        <Card className="p-6">
          <h2 className="text-base font-semibold text-ink-900">What happens next</h2>
          <ol className="mt-4 space-y-4 text-sm leading-relaxed text-ink-700">
            <li className="flex gap-3">
              <span className="num grid size-6 shrink-0 place-items-center rounded-full bg-brand-50 text-xs font-semibold text-brand-700">1</span>
              The report is stored by the MedInsight service so it can be analyzed.
            </li>
            <li className="flex gap-3">
              <span className="num grid size-6 shrink-0 place-items-center rounded-full bg-brand-50 text-xs font-semibold text-brand-700">2</span>
              You start the analysis from the report page.
            </li>
            <li className="flex gap-3">
              <span className="num grid size-6 shrink-0 place-items-center rounded-full bg-brand-50 text-xs font-semibold text-brand-700">3</span>
              Results show every value with its unit, reference range and source page.
            </li>
          </ol>
        </Card>
        <Notice tone="caution" title="Limitations">
          PNG and JPG reports can&apos;t be analyzed yet, and scanned pages may not produce values.
        </Notice>
      </aside>
    </div>
  );
}

function UploadSuccess({
  report,
  onUploadAnother,
}: {
  report: UploadResponse;
  onUploadAnother: () => void;
}) {
  return (
    <div className="flex flex-col gap-6" role="status">
      <div className="flex items-start gap-4">
        <span className="grid size-12 shrink-0 place-items-center rounded-2xl bg-success-50 text-success-700">
          <IconCheck className="size-6" />
        </span>
        <div className="min-w-0">
          <h2 className="text-xl font-semibold text-ink-900">Report uploaded</h2>
          <p className="mt-1 break-all text-sm text-ink-500">{report.filename}</p>
        </div>
      </div>

      <dl className="grid gap-4 rounded-xl border border-line bg-surface-muted p-5 text-sm sm:grid-cols-3">
        <div>
          <dt className="text-ink-500">Status</dt>
          <dd className="mt-1">
            <Badge tone="neutral">Ready to analyze</Badge>
          </dd>
        </div>
        <div>
          <dt className="text-ink-500">File size</dt>
          <dd className="num mt-1 font-medium text-ink-900">{formatBytes(report.size_bytes)}</dd>
        </div>
        <div>
          <dt className="text-ink-500">Format</dt>
          <dd className="mt-1 font-medium uppercase text-ink-900">{report.file_type}</dd>
        </div>
      </dl>

      <div className="flex flex-col gap-3 sm:flex-row">
        <Link
          href={`/reports/${encodeURIComponent(report.document_id)}`}
          className={buttonClasses("primary")}
        >
          Go to analysis
        </Link>
        <Button variant="secondary" onClick={onUploadAnother}>
          Upload another report
        </Button>
      </div>
    </div>
  );
}
