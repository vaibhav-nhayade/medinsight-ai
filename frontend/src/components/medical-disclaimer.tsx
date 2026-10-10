import { IconShield } from "@/components/ui/icons";

export function MedicalDisclaimer({ compact = false }: { compact?: boolean }) {
  return (
    <aside
      aria-label="Medical information notice"
      className="flex gap-3 rounded-2xl border border-line bg-surface p-5 text-sm leading-relaxed text-ink-700"
    >
      <IconShield className="mt-0.5 size-5 text-brand-700" />
      <p>
        {compact
          ? "Informational only. This is not a diagnosis. Discuss results with a qualified healthcare professional."
          : "MedInsight AI is an informational tool. It does not diagnose conditions, recommend treatment, or replace a qualified healthcare professional. Reference ranges differ between laboratories, so check the range printed on your own report and bring questions to your clinician."}
      </p>
    </aside>
  );
}
