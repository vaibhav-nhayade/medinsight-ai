
import Link from "next/link";
import { Suspense, type ReactNode } from "react";
import { Logo } from "./logo";
import { SiteNav } from "./site-nav";

export function AppShell({ children }: { children: ReactNode }) {
  return (
    <div className="min-h-dvh">
      <a
        href="#main"
        className="sr-only focus:not-sr-only focus:fixed focus:left-4 focus:top-4 focus:z-50 focus:rounded-lg focus:bg-white focus:px-4 focus:py-2 focus:text-sm focus:font-medium focus:shadow-lg"
      >
        Skip to content
      </a>

      <header className="sticky top-0 z-30 border-b border-stone-200 bg-[#f8f7f3]/95 backdrop-blur">
        <div className="mx-auto flex min-h-[76px] max-w-[1600px] items-center justify-between gap-6 px-5 sm:px-8 lg:px-12">
          <Link href="/" aria-label="MedInsight AI home" className="shrink-0">
            <Logo />
          </Link>

          <div className="min-w-0">
            <Suspense
              fallback={
                <div className="h-10 w-40 animate-pulse rounded-xl bg-stone-200" />
              }
            >
              <SiteNav orientation="horizontal" />
            </Suspense>
          </div>
        </div>
      </header>

      <main id="main" className="min-w-0">
        {children}
      </main>

      <div className="border-t border-stone-200 bg-[#eeece5] px-5 py-5 text-center text-xs leading-6 text-stone-600 sm:px-8">
        MedInsight AI is informational only and does not provide a medical
        diagnosis. Discuss your results with a qualified healthcare
        professional.
      </div>
    </div>
  );
}
