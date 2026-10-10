import type { ComponentProps } from "react";
import { cx } from "@/lib/cx";

export function Card({ className, ...props }: ComponentProps<"div">) {
  return (
    <div
      className={cx("rounded-2xl border border-line bg-surface shadow-card", className)}
      {...props}
    />
  );
}
