import type { ButtonHTMLAttributes } from "react";
import { cx } from "@/lib/cx";

export type ButtonVariant = "primary" | "secondary" | "ghost" | "inverse";

const variants: Record<ButtonVariant, string> = {
  primary: "bg-brand-600 text-white shadow-sm hover:bg-brand-700 active:bg-brand-700",
  secondary:
    "border border-line-strong bg-surface text-ink-900 shadow-sm hover:border-ink-400 hover:bg-surface-muted",
  ghost: "text-brand-700 hover:bg-brand-50",
  inverse: "bg-white text-ink-900 shadow-sm hover:bg-brand-50",
};

/** Class names for buttons; use on <Link> when navigation is needed. */
export function buttonClasses(variant: ButtonVariant = "primary", extra?: string): string {
  return cx(
    "inline-flex items-center justify-center gap-2 rounded-xl px-4 py-2.5 text-sm font-semibold",
    "transition-colors duration-150 disabled:cursor-not-allowed disabled:opacity-50",
    variants[variant],
    extra,
  );
}

type ButtonProps = ButtonHTMLAttributes<HTMLButtonElement> & {
  variant?: ButtonVariant;
};

export function Button({ variant = "primary", className, type = "button", ...props }: ButtonProps) {
  return <button type={type} className={buttonClasses(variant, className)} {...props} />;
}
