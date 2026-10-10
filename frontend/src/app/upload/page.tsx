import type { Metadata } from "next";
import { PageHeader } from "@/components/layout/page-header";
import { UploadReport } from "@/components/upload/upload-report";

export const metadata: Metadata = {
  title: "Upload report",
};

export default function UploadPage() {
  return (
    <div className="space-y-8">
      <PageHeader
        eyebrow="New report"
        title="Upload a lab report"
        description="Choose a PDF lab report. The file is sent to the MedInsight service only when you press Upload."
      />
      <UploadReport />
    </div>
  );
}
