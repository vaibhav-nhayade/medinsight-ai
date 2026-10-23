
"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { cx } from "@/lib/cx";
import { IconGrid, IconUpload } from "@/components/ui/icons";

const items = [
  { href: "/", label: "Overview", icon: IconGrid, also: [] as string[] },
  {
    href: "/upload",
    label: "Upload report",
    icon: IconUpload,
    also: ["/reports"],
  },
];

export function SiteNav({
  orientation,
}: {
  orientation: "vertical" | "horizontal";
}) {
  const pathname = usePathname();

  return (
    <nav aria-label="Primary">
      <ul
        className={cx(
          "flex items-center gap-1 sm:gap-2",
          orientation === "vertical" ? "flex-col" : "flex-row",
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
                  "flex items-center gap-2 whitespace-nowrap rounded-full px-3 py-2 text-sm font-medium transition-colors sm:px-4",
                  active
                    ? "bg-stone-950 text-white"
                    : "text-stone-700 hover:bg-stone-200/70 hover:text-stone-950",
                )}
              >
                <Icon className="size-[18px]" />
                <span>{item.label}</span>
              </Link>
            </li>
          );
        })}
      </ul>
    </nav>
  );
}
