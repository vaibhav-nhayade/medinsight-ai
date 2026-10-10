import type { ReactNode } from "react";
import { cx } from "@/lib/cx";

export function Spinner({ className }: { className?: string }) {
  return (
    <span
      aria-hidden="true"
      className={cx(
        "inline-block size-4 animate-spin rounded-full border-2 border-current border-r-transparent",
        className,
      )}
    />
  );
}

export function Skeleton({ className }: { className?: string }) {
  return <div aria-hidden="true" className={cx("animate-pulse rounded-lg bg-line", className)} />;
}

export function EmptyState({
  icon,
  title,
  children,
  action,
}: {
  icon: ReactNode;
  title: string;
  children?: ReactNode;
  action?: ReactNode;
}) {
  return (
    <div className="flex flex-col items-center px-6 py-12 text-center">
      <div className="grid size-12 place-items-center rounded-2xl bg-brand-50 text-brand-700">
        {icon}
      </div>
      <h3 className="mt-4 text-base font-semibold text-ink-900">{title}</h3>
      {children && (
        <div className="mt-2 max-w-md text-sm leading-relaxed text-ink-500">{children}</div>
      )}
      {action && <div className="mt-6">{action}</div>}
    </div>
  );
}
