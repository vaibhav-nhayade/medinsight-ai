import type { Metadata } from "next";
import { Suspense } from "react";
import { ReportDetail, ReportDetailFallback } from "@/components/report/report-detail";

export const metadata: Metadata = {
  title: "Report analysis",
};

export default function ReportPage() {
  return (
    <Suspense fallback={<ReportDetailFallback />}>
      <ReportDetail />
    </Suspense>
  );
}
