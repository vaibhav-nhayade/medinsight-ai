import type { ReactNode } from "react";

export function PageHeader({
  eyebrow,
  title,
  description,
  actions,
}: {
  eyebrow?: string;
  title: string;
  description?: string;
  actions?: ReactNode;
}) {
  return (
    <header className="flex flex-col gap-5 sm:flex-row sm:items-end sm:justify-between">
      <div className="max-w-2xl">
        {eyebrow && <p className="text-sm font-semibold text-brand-700">{eyebrow}</p>}
        <h1 className="mt-1.5 text-3xl font-semibold tracking-tight text-ink-900 sm:text-4xl">
          {title}
        </h1>
        {description && (
          <p className="mt-3 text-base leading-relaxed text-ink-500">{description}</p>
        )}
      </div>
      {actions && <div className="flex shrink-0 flex-wrap gap-3">{actions}</div>}
    </header>
  );
}
