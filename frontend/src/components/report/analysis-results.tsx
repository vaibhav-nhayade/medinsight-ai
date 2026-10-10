import type { AnalysisResponse, Finding, ReportResult } from "@/lib/api/types";
import {
  formatReferenceRange,
  formatResultValue,
  formatTestName,
} from "@/lib/format";
import { describeFindingSeverity, describeResultStatus } from "@/lib/result-status";
import { Badge } from "@/components/ui/badge";
import { Card } from "@/components/ui/card";
import { EmptyState } from "@/components/ui/feedback";
import { IconDocument, IconInfo } from "@/components/ui/icons";
import { Notice } from "@/components/ui/notice";

export function AnalysisResults({ analysis }: { analysis: AnalysisResponse }) {
  const { summary, results, findings } = analysis;
  const outsideRange = summary.low_results + summary.high_results;

  return (
    <div className="space-y-8">
      <Notice tone="caution" title="Read this first">
        A value outside the reference range printed on your report is not a diagnosis. Ranges differ
        between laboratories, and a clinician needs to interpret results in the context of your health.
      </Notice>

      <section aria-labelledby="summary-heading" className="space-y-4">
        <h2 id="summary-heading" className="text-lg font-semibold text-ink-900">
          Summary
        </h2>
        <dl className="grid grid-cols-2 gap-3 lg:grid-cols-5">
          <StatTile label="Values found" value={summary.total_results} />
          <StatTile label="Within range" value={summary.normal_results} tone="success" />
          <StatTile label="Outside range" value={outsideRange} tone="caution" />
          <StatTile label="Not classified" value={summary.unknown_results} />
          <StatTile label="Need verification" value={summary.verification_required} />
        </dl>
        <p className="text-sm text-ink-500">
          &ldquo;Not classified&rdquo; means the report did not provide a range to compare against. It is not the same as normal.
        </p>
      </section>

      {results.length === 0 ? (
        <Card>
          <EmptyState icon={<IconDocument className="size-6" />} title="No lab values were recognized">
            The document may be a scan or image, or its tables may use a layout the parser can&apos;t read yet.
            This does not mean the results are normal.
          </EmptyState>
        </Card>
      ) : (
        <ResultsTable results={results} />
      )}

      <section aria-labelledby="findings-heading" className="space-y-4">
        <h2 id="findings-heading" className="text-lg font-semibold text-ink-900">
          Findings
        </h2>
        {findings.length === 0 ? (
          <Notice tone="info">
            {results.length === 0
              ? "No findings could be generated because no values were recognized."
              : "No findings were generated from the recognized values. Check the table above for values that were not classified."}
          </Notice>
        ) : (
          <ul className="grid gap-4 md:grid-cols-2">
            {findings.map((finding, index) => (
              <FindingCard key={`${finding.test_name}-${index}`} finding={finding} />
            ))}
          </ul>
        )}
      </section>

      <p className="flex gap-2 text-xs leading-relaxed text-ink-500">
        <IconInfo className="mt-0.5 size-4 shrink-0" />
        Values, units and reference ranges are shown as they appear in the report. Nothing has been converted.
      </p>
    </div>
  );
}

function StatTile({
  label,
  value,
  tone,
}: {
  label: string;
  value: number;
  tone?: "success" | "caution";
}) {
  const accent =
    tone === "success" ? "bg-success-700" : tone === "caution" ? "bg-caution-700" : "bg-ink-400";

  return (
    <Card className="relative overflow-hidden p-5">
      <span aria-hidden="true" className={`absolute inset-x-0 top-0 h-1 ${accent}`} />
      <dt className="text-sm text-ink-500">{label}</dt>
      <dd className="num mt-2 text-3xl font-semibold tracking-tight text-ink-900">{value}</dd>
    </Card>
  );
}

function ResultsTable({ results }: { results: ReportResult[] }) {
  return (
    <Card className="overflow-hidden p-0">
      <div className="flex flex-wrap items-center justify-between gap-2 border-b border-line px-5 py-4">
        <h2 className="text-lg font-semibold text-ink-900">Extracted values</h2>
        <span className="num text-sm text-ink-500">{results.length} total</span>
      </div>
      <div className="overflow-x-auto">
        <table className="w-full min-w-[42rem] text-left text-sm">
          <caption className="sr-only">
            Values extracted from the report with their reference ranges and status
          </caption>
          <thead className="bg-surface-muted text-ink-500">
            <tr>
              <th scope="col" className="px-5 py-3 font-medium">Test</th>
              <th scope="col" className="px-5 py-3 font-medium">Result</th>
              <th scope="col" className="px-5 py-3 font-medium">Reference range</th>
              <th scope="col" className="px-5 py-3 font-medium">Status</th>
              <th scope="col" className="px-5 py-3 font-medium">Source</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-line">
            {results.map((result, index) => {
              const status = describeResultStatus(result.status);
              return (
                <tr key={`${result.test_name}-${index}`} className="align-top transition-colors hover:bg-surface-muted">
                  <th scope="row" className="px-5 py-4 font-medium text-ink-900">
                    <span className="block">{formatTestName(result.test_name)}</span>
                    {result.needs_verification && (
                      <span className="mt-2 inline-block">
                        <Badge tone="neutral">Verify value</Badge>
                      </span>
                    )}
                  </th>
                  <td className="num px-5 py-4 whitespace-nowrap font-medium text-ink-900">
                    {formatResultValue(result.value, result.unit)}
                  </td>
                  <td className="num px-5 py-4 whitespace-nowrap text-ink-700">
                    {formatReferenceRange(result.reference_minimum, result.reference_maximum, result.unit)}
                  </td>
                  <td className="px-5 py-4">
                    <Badge tone={status.tone}>{status.label}</Badge>
                  </td>
                  <td className="px-5 py-4 whitespace-nowrap text-ink-500">
                    {result.source_page !== null ? `Page ${result.source_page}` : "Not stated"}
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </Card>
  );
}

function FindingCard({ finding }: { finding: Finding }) {
  const severity = describeFindingSeverity(finding.severity);

  return (
    <li>
      <Card className="h-full p-5">
        <div className="flex flex-wrap items-center justify-between gap-2">
          <Badge tone={severity.tone}>{severity.label}</Badge>
          {finding.source_page !== null && (
            <span className="num text-xs text-ink-500">Page {finding.source_page}</span>
          )}
        </div>
        <h3 className="mt-4 text-base font-semibold text-ink-900">{finding.title}</h3>
        <p className="mt-2 text-sm leading-relaxed text-ink-700">{finding.description}</p>
        <p className="mt-3 text-xs text-ink-500">{formatTestName(finding.test_name)}</p>
        {finding.needs_verification && (
          <p className="mt-3 text-xs font-medium text-ink-700">
            This value should be checked against the original report.
          </p>
        )}
      </Card>
    </li>
  );
}
