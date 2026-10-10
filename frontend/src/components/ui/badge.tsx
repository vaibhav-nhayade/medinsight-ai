import type { ReactNode } from "react";
import { cx } from "@/lib/cx";
import type { Tone } from "@/lib/result-status";

const tones: Record<Tone, string> = {
  success: "bg-success-50 text-success-700 ring-success-700/20",
  caution: "bg-caution-50 text-caution-700 ring-caution-700/20",
  neutral: "bg-ink-900/5 text-ink-700 ring-ink-900/10",
  brand: "bg-brand-50 text-brand-700 ring-brand-600/20",
  danger: "bg-danger-50 text-danger-700 ring-danger-700/20",
};

/** Status is conveyed by text and a dot shape, never by color alone. */
export function Badge({
  tone = "neutral",
  className,
  children,
}: {
  tone?: Tone;
  className?: string;
  children: ReactNode;
}) {
  return (
    <span
      className={cx(
        "inline-flex items-center gap-1.5 whitespace-nowrap rounded-full px-2.5 py-1 text-xs font-medium ring-1 ring-inset",
        tones[tone],
        className,
      )}
    >
      <span aria-hidden="true" className="size-1.5 rounded-full bg-current" />
      {children}
    </span>
  );
}
