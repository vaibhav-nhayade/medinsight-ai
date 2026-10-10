"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { cx } from "@/lib/cx";
import { IconGrid, IconUpload } from "@/components/ui/icons";

const items = [
  { href: "/", label: "Overview", icon: IconGrid, also: [] as string[] },
  { href: "/upload", label: "Upload report", icon: IconUpload, also: ["/reports"] },
];

export function SiteNav({ orientation }: { orientation: "vertical" | "horizontal" }) {
  const pathname = usePathname();

  return (
    <nav aria-label="Primary">
      <ul
        className={cx(
          orientation === "vertical" ? "flex flex-col gap-1" : "flex gap-1 overflow-x-auto",
        )}
      >
        {items.map((item) => {
          const active =
            pathname === item.href ||
            (item.href !== "/" && pathname.startsWith(item.href)) ||
            item.also.some((path) => pathname.startsWith(path));
          const Icon = item.icon;

          return (
            <li key={item.href}>
              <Link
                href={item.href}
                aria-current={active ? "page" : undefined}
                className={cx(
                  "flex items-center gap-3 whitespace-nowrap rounded-xl px-3.5 py-2.5 text-sm font-medium transition-colors duration-150",
                  active
                    ? "bg-ink-900 text-white"
                    : "text-ink-700 hover:bg-ink-900/5 hover:text-ink-900",
                )}
              >
                <Icon className="size-[18px]" />
                {item.label}
              </Link>
            </li>
          );
        })}
      </ul>
    </nav>
  );
}
