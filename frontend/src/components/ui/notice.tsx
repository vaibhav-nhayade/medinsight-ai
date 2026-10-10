import type { ReactNode } from "react";
import { cx } from "@/lib/cx";
import { IconAlert, IconCheck, IconInfo } from "./icons";

type NoticeTone = "info" | "caution" | "danger" | "success";

const styles: Record<NoticeTone, { box: string; icon: string }> = {
  info: { box: "border-brand-100 bg-brand-50", icon: "text-brand-700" },
  caution: { box: "border-caution-700/20 bg-caution-50", icon: "text-caution-700" },
  danger: { box: "border-danger-700/20 bg-danger-50", icon: "text-danger-700" },
  success: { box: "border-success-700/20 bg-success-50", icon: "text-success-700" },
};

export function Notice({
  tone = "info",
  title,
  children,
  className,
}: {
  tone?: NoticeTone;
  title?: string;
  children?: ReactNode;
  className?: string;
}) {
  const Icon = tone === "success" ? IconCheck : tone === "info" ? IconInfo : IconAlert;

  return (
    <div
      role={tone === "danger" ? "alert" : "status"}
      className={cx(
        "flex gap-3 rounded-xl border p-4 text-sm leading-relaxed text-ink-900",
        styles[tone].box,
        className,
      )}
    >
      <Icon className={cx("mt-0.5 size-5", styles[tone].icon)} />
      <div className="min-w-0">
        {title && <p className="font-semibold">{title}</p>}
        {children && <div className={cx(title && "mt-1 text-ink-700")}>{children}</div>}
      </div>
    </div>
  );
}
