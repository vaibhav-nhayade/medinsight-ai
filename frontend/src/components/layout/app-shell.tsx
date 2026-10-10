import Link from "next/link";
import { Suspense, type ReactNode } from "react";
import { Logo } from "./logo";
import { SiteNav } from "./site-nav";

export function AppShell({ children }: { children: ReactNode }) {
  return (
    <div className="min-h-dvh lg:grid lg:grid-cols-[17rem_minmax(0,1fr)]">
      <a
        href="#main"
        className="sr-only focus:not-sr-only focus:fixed focus:left-4 focus:top-4 focus:z-50 focus:rounded-lg focus:bg-surface focus:px-4 focus:py-2 focus:text-sm focus:font-medium focus:shadow-card"
      >
        Skip to content
      </a>

      <aside className="hidden border-r border-line bg-surface lg:sticky lg:top-0 lg:flex lg:h-dvh lg:flex-col lg:px-5 lg:py-8">
        <Link href="/" aria-label="MedInsight AI home" className="px-2">
          <Logo />
        </Link>
        <div className="mt-10">
          <Suspense fallback={<NavFallback />}>
            <SiteNav orientation="vertical" />
          </Suspense>
        </div>
        <div className="mt-auto rounded-xl bg-canvas p-4 text-xs leading-relaxed text-ink-500">
          <p className="font-semibold text-ink-700">Informational only</p>
          <p className="mt-1">
            MedInsight AI is not a diagnosis. Discuss results with a qualified healthcare professional.
          </p>
        </div>
      </aside>

      <div className="flex min-w-0 flex-col">
        <header className="sticky top-0 z-30 border-b border-line bg-surface/95 backdrop-blur lg:hidden">
          <div className="px-5 pb-2 pt-4">
            <Link href="/" aria-label="MedInsight AI home">
              <Logo />
            </Link>
          </div>
          <div className="px-3 pb-3">
            <Suspense fallback={<NavFallback />}>
              <SiteNav orientation="horizontal" />
            </Suspense>
          </div>
        </header>

        <main id="main" className="mx-auto w-full max-w-5xl flex-1 px-5 py-8 sm:px-8 lg:py-12">
          {children}
        </main>
      </div>
    </div>
  );
}

function NavFallback() {
  return (
    <div aria-hidden="true" className="flex flex-col gap-2">
      <div className="h-10 rounded-xl bg-line/60" />
      <div className="h-10 rounded-xl bg-line/60" />
    </div>
  );
}
