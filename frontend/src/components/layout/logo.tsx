import { IconPulse } from "@/components/ui/icons";

export function Logo() {
  return (
    <span className="inline-flex items-center gap-2.5">
      <span className="grid size-9 place-items-center rounded-xl bg-ink-900 text-brand-100">
        <IconPulse className="size-5" />
      </span>
      <span className="text-[15px] font-semibold tracking-tight text-ink-900">
        MedInsight <span className="text-brand-600">AI</span>
      </span>
    </span>
  );
}
