
import Link from "next/link";
import {
  IconArrowRight,
  IconChart,
  IconCheck,
  IconDocument,
  IconShield,
  IconUpload,
} from "@/components/ui/icons";

const steps = [
  {
    number: "01",
    title: "Upload your medical report",
    text: "Choose a supported PDF or image file. The current upload workflow accepts files up to 10 MB.",
  },
  {
    number: "02",
    title: "Extract available information",
    text: "The backend processes the document and extracts supported report information, such as test names, measurements and reference ranges.",
  },
  {
    number: "03",
    title: "Compare available ranges",
    text: "Where values and reference intervals are successfully extracted, the application can classify results using its supported rules.",
  },
  {
    number: "04",
    title: "Review your findings",
    text: "Inspect the returned results, verify the details against the original report and prepare questions for your healthcare professional.",
  },
];

const features = [
  {
    number: "01",
    title: "Understand the structure",
    text: "Organize supported laboratory measurements, units and reference ranges into information that is easier to review.",
    icon: IconDocument,
    tag: "Report extraction",
  },
  {
    number: "02",
    title: "See range comparisons",
    text: "Identify values classified below or above an available reference interval without treating every result as a diagnosis.",
    icon: IconChart,
    tag: "Rule-based analysis",
  },
  {
    number: "03",
    title: "Review with confidence",
    text: "Check the displayed information against your original report and use it to support a more informed clinical conversation.",
    icon: IconShield,
    tag: "Responsible review",
  },
];

const faqs = [
  {
    q: "What is MedInsight AI?",
    a: "MedInsight AI is a medical laboratory-report understanding project that organizes supported report information and compares extracted measurements with available reference ranges.",
  },
  {
    q: "Does the website diagnose diseases?",
    a: "No. It is an informational report-review aid, not a diagnostic system. Only a qualified healthcare professional can interpret your results in the context of your medical history, symptoms and other findings.",
  },
  {
    q: "Which file formats are supported?",
    a: "The current upload workflow accepts PDF, PNG, JPG and JPEG files up to 10 MB. Successful upload does not guarantee that the contents of every file can be analyzed.",
  },
  {
    q: "Can I upload a scanned report?",
    a: "You may be able to upload it, but scanned documents may not contain selectable text. Do not assume OCR is available. Extraction depends on the current backend capabilities and document quality.",
  },
  {
    q: "What do high and low values mean?",
    a: "They indicate that an extracted measurement falls above or below the reference interval used by the application. They do not independently establish a disease or determine treatment.",
  },
  {
    q: "Is my medical information safe?",
    a: "Only upload documents you are authorized to share. Review the project's actual data-handling and retention practices before uploading sensitive information. Do not assume that uploaded reports are automatically deleted or anonymized.",
  },
];

function SectionTitle({
  eyebrow,
  title,
  description,
}: {
  eyebrow: string;
  title: string;
  description: string;
}) {
  return (
    <div className="mx-auto max-w-3xl text-center">
      <p className="text-xs font-semibold uppercase tracking-[0.2em] text-blue-700">
        {eyebrow}
      </p>
      <h2 className="editorial-heading mt-4 text-3xl leading-tight tracking-tight text-stone-950 sm:text-4xl lg:text-5xl">
        {title}
      </h2>
      <p className="mx-auto mt-5 max-w-2xl text-base leading-8 text-stone-600 sm:text-lg">
        {description}
      </p>
    </div>
  );
}

function ReportIllustration() {
  return (
    <div
      role="img"
      aria-label="Decorative illustration of a laboratory report and structured results"
      className="report-art relative mx-auto w-full max-w-lg"
    >
      <div className="art-orbit art-orbit-one" aria-hidden="true" />
      <div className="art-orbit art-orbit-two" aria-hidden="true" />

      <div className="report-paper relative z-10 rounded-3xl border border-stone-200 bg-white p-5 shadow-xl sm:p-7">
        <div className="flex items-center justify-between gap-3 border-b border-stone-100 pb-5">
          <div className="flex items-center gap-3">
            <div className="grid size-11 place-items-center rounded-xl bg-blue-50 text-blue-700">
              <IconDocument />
            </div>
            <div>
              <p className="text-sm font-semibold text-stone-900">
                Laboratory report
              </p>
              <p className="mt-1 text-xs text-stone-500">
                Illustrative interface
              </p>
            </div>
          </div>
          <span className="rounded-full bg-blue-50 px-3 py-1.5 text-xs font-medium text-blue-700">
            Preview
          </span>
        </div>

        <div className="mt-6 rounded-2xl bg-stone-50 p-4">
          <div className="flex items-center justify-between gap-3">
            <div>
              <p className="text-xs text-stone-500">Report overview</p>
              <p className="mt-1 text-lg font-semibold text-stone-900">
                Structured information
              </p>
            </div>
            <div className="grid size-10 place-items-center rounded-xl bg-white text-blue-700 shadow-sm">
              <IconChart />
            </div>
          </div>

          <div className="mt-5 space-y-4">
            {[
              { name: "Test information", width: "84%" },
              { name: "Measured value", width: "65%" },
              { name: "Reference interval", width: "76%" },
            ].map((item) => (
              <div key={item.name}>
                <div className="mb-2 flex items-center justify-between gap-2 text-xs text-stone-500">
                  <span>{item.name}</span>
                  <span>Example</span>
                </div>
                <div className="h-2 overflow-hidden rounded-full bg-stone-200">
                  <div
                    className="report-bar h-full rounded-full bg-blue-600"
                    style={{ width: item.width }}
                  />
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="mt-4 rounded-2xl border border-stone-100 p-4">
          <div className="flex items-start gap-3">
            <div className="grid size-9 shrink-0 place-items-center rounded-xl bg-emerald-50 text-emerald-700">
              <IconCheck />
            </div>
            <div>
              <p className="text-sm font-semibold text-stone-900">
                Review the original report
              </p>
              <p className="mt-1 text-xs leading-6 text-stone-500">
                Confirm extracted information before drawing conclusions.
              </p>
            </div>
          </div>
        </div>
      </div>

      <div className="report-float absolute -right-2 top-8 z-20 hidden rounded-2xl border border-stone-100 bg-white p-4 shadow-lg sm:block">
        <p className="text-xs text-stone-500">Processing workflow</p>
        <p className="mt-1 text-sm font-semibold text-stone-900">
          Extract → Compare
        </p>
      </div>

      <div className="report-float report-float-delayed absolute -bottom-4 -left-2 z-20 hidden rounded-2xl border border-stone-100 bg-white p-4 shadow-lg sm:block">
        <div className="flex items-center gap-2">
          <span className="size-2 rounded-full bg-blue-600" />
          <span className="text-sm font-medium text-stone-800">
            Source-aware review
          </span>
        </div>
      </div>
    </div>
  );
}

export default function HomePage() {
  return (
    <main className="medinsight-home overflow-hidden bg-[#f8f7f3] text-stone-950">
      {/* Hero */}
      <section className="mx-auto grid max-w-7xl items-center gap-12 px-5 pb-20 pt-12 sm:px-8 sm:pb-28 sm:pt-16 lg:grid-cols-2 lg:gap-16 lg:px-12">
        <div className="relative z-10">
          <div className="inline-flex items-center gap-2 rounded-full border border-stone-200 bg-white px-4 py-2 text-xs font-medium text-stone-700">
            <span className="size-2 rounded-full bg-blue-600" />
            MEDICAL REPORT UNDERSTANDING
          </div>

          <p className="mt-8 text-sm font-medium text-blue-700">
            Understand. Review. Ask better questions.
          </p>

          <h1 className="editorial-heading mt-5 max-w-2xl text-5xl leading-[1.07] tracking-tight sm:text-6xl lg:text-7xl">
            Explain and understand your medical reports.
          </h1>

          <p className="mt-6 max-w-xl text-base leading-8 text-stone-600 sm:text-lg">
            Turn supported laboratory reports into structured information.
            Review extracted measurements, understand available reference
            ranges and prepare questions for your healthcare professional.
          </p>

          <div className="mt-8 flex flex-wrap gap-3">
            <Link
              href="/upload"
              className="inline-flex min-h-12 items-center justify-center gap-2 rounded-xl bg-stone-950 px-5 py-3 text-sm font-semibold text-white transition hover:-translate-y-0.5 hover:bg-stone-800"
            >
              <IconUpload />
              Upload medical report
              <IconArrowRight />
            </Link>

            <a
              href="#how-it-works"
              className="inline-flex min-h-12 items-center justify-center rounded-xl border border-stone-300 bg-transparent px-5 py-3 text-sm font-semibold text-stone-800 transition hover:bg-white"
            >
              How it works
            </a>
          </div>

          <div className="mt-9 flex flex-wrap gap-x-6 gap-y-3 border-t border-stone-200 pt-6 text-xs text-stone-600">
            <span className="inline-flex items-center gap-2">
              <IconCheck />
              Structured results
            </span>
            <span className="inline-flex items-center gap-2">
              <IconCheck />
              Reference-range review
            </span>
            <span className="inline-flex items-center gap-2">
              <IconShield />
              Informational only
            </span>
          </div>
        </div>

        <div className="px-2 py-6 sm:px-6 lg:px-0">
          <ReportIllustration />
          <p className="mt-7 text-center text-xs leading-6 text-stone-500">
            Conceptual illustration only. The cards above are not real patient
            results or a live processing status.
          </p>
        </div>
      </section>

      {/* Product explanation */}
      <section className="border-y border-stone-200 bg-white px-5 py-20 sm:px-8 sm:py-24">
        <SectionTitle
          eyebrow="Why MedInsight AI"
          title="Make a dense medical report easier to review."
          description="Laboratory reports can contain technical terms, numerical measurements, units and reference intervals. MedInsight AI helps organize supported information into a clearer review experience."
        />

        <div className="mx-auto mt-12 grid max-w-7xl gap-5 md:grid-cols-3">
          {features.map((feature) => {
            const Icon = feature.icon;
            return (
              <article
                key={feature.number}
                className="feature-card rounded-3xl border border-stone-200 bg-[#fdfcf9] p-7 sm:p-8"
              >
                <div className="flex items-center justify-between">
                  <div className="grid size-12 place-items-center rounded-2xl border border-stone-200 bg-white text-stone-900">
                    <Icon />
                  </div>
                  <span className="text-xs font-medium tracking-widest text-stone-400">
                    {feature.number}
                  </span>
                </div>
                <p className="mt-7 text-xs font-semibold uppercase tracking-wider text-blue-700">
                  {feature.tag}
                </p>
                <h3 className="mt-3 text-xl font-semibold tracking-tight">
                  {feature.title}
                </h3>
                <p className="mt-4 text-sm leading-7 text-stone-600">
                  {feature.text}
                </p>
              </article>
            );
          })}
        </div>
      </section>

      {/* Example report review */}
      <section className="mx-auto max-w-7xl px-5 py-20 sm:px-8 sm:py-28 lg:px-12">
        <div className="grid items-center gap-12 lg:grid-cols-2 lg:gap-20">
          <div>
            <p className="text-xs font-semibold uppercase tracking-[0.2em] text-blue-700">
              From report to review
            </p>
            <h2 className="editorial-heading mt-4 text-4xl leading-tight sm:text-5xl">
              See information organized for closer inspection.
            </h2>
            <p className="mt-5 text-base leading-8 text-stone-600">
              The purpose is not to replace the original document. It is to
              make the available information easier to find, compare and
              discuss.
            </p>

            <div className="mt-8 space-y-5">
              {[
                {
                  title: "Test names and measurements",
                  text: "Review the extracted test name, measured value and unit.",
                },
                {
                  title: "Available reference intervals",
                  text: "Check whether the source report provides a range for comparison.",
                },
                {
                  title: "Classification and source",
                  text: "Review the returned classification and verify important details against the original report.",
                },
              ].map((item, index) => (
                <div key={item.title} className="flex gap-4">
                  <span className="grid size-9 shrink-0 place-items-center rounded-xl bg-blue-50 text-sm font-semibold text-blue-700">
                    {index + 1}
                  </span>
                  <div>
                    <h3 className="font-semibold">{item.title}</h3>
                    <p className="mt-2 text-sm leading-7 text-stone-600">
                      {item.text}
                    </p>
                  </div>
                </div>
              ))}
            </div>
          </div>

          <div className="rounded-3xl border border-stone-200 bg-white p-5 shadow-sm sm:p-8">
            <div className="flex items-center justify-between gap-3 border-b border-stone-100 pb-5">
              <div>
                <p className="text-xs uppercase tracking-wider text-stone-500">
                  Example layout
                </p>
                <h3 className="mt-1 text-lg font-semibold">
                  Extracted report information
                </h3>
              </div>
              <IconDocument />
            </div>

            <div className="mt-5 space-y-3">
              {[
                ["Test name", "Example test"],
                ["Measured value", "Value from report"],
                ["Unit", "As reported"],
                ["Reference range", "If available"],
              ].map(([label, value]) => (
                <div
                  key={label}
                  className="flex flex-wrap items-center justify-between gap-3 rounded-xl bg-[#f8f7f3] px-4 py-4"
                >
                  <span className="text-sm text-stone-600">{label}</span>
                  <span className="text-sm font-medium text-stone-900">
                    {value}
                  </span>
                </div>
              ))}
            </div>

            <div className="mt-5 rounded-xl border border-blue-100 bg-blue-50/60 p-4">
              <p className="text-sm font-semibold text-blue-950">
                Always verify the original
              </p>
              <p className="mt-2 text-sm leading-6 text-blue-900/80">
                This is a design example, not actual patient data or an
                indication of a real result.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* How it works */}
      <section
        id="how-it-works"
        className="scroll-mt-20 border-y border-stone-200 bg-[#eeece5] px-5 py-20 sm:px-8 sm:py-24"
      >
        <SectionTitle
          eyebrow="How the project works"
          title="Four steps from upload to informed discussion."
          description="The frontend communicates with a backend that processes the document, extracts supported information and returns analysis results."
        />

        <ol className="mx-auto mt-12 grid max-w-7xl gap-5 sm:grid-cols-2 lg:grid-cols-4">
          {steps.map((step) => (
            <li
              key={step.number}
              className="rounded-3xl border border-stone-200 bg-white p-6 sm:p-7"
            >
              <p className="text-sm font-semibold tracking-widest text-blue-700">
                {step.number}
              </p>
              <div className="mt-6 h-px w-full bg-stone-200" />
              <h3 className="mt-6 text-xl font-semibold tracking-tight">
                {step.title}
              </h3>
              <p className="mt-4 text-sm leading-7 text-stone-600">
                {step.text}
              </p>
            </li>
          ))}
        </ol>
      </section>

      {/* Limitations and safe use */}
      <section className="mx-auto max-w-7xl px-5 py-20 sm:px-8 sm:py-24 lg:px-12">
        <SectionTitle
          eyebrow="Responsible use"
          title="Helpful information needs the right context."
          description="Reference-range comparisons are only one part of understanding a medical report. A result must be considered alongside the original document and your individual circumstances."
        />

        <div className="mx-auto mt-12 grid max-w-5xl gap-4 sm:grid-cols-2">
          {[
            {
              title: "A comparison is not a diagnosis",
              text: "An out-of-range result does not independently establish a disease or its severity.",
            },
            {
              title: "Extraction may be incomplete",
              text: "Poor-quality scans, unsupported formats and unrecognized text can affect the information returned.",
            },
            {
              title: "Ranges can differ",
              text: "Reference intervals may vary by laboratory, test method and patient circumstances.",
            },
            {
              title: "Professional advice matters",
              text: "Do not change medication or treatment based on this website. Discuss concerns with a qualified healthcare professional.",
            },
          ].map((item) => (
            <article
              key={item.title}
              className="rounded-2xl border border-stone-200 bg-white p-6 sm:p-7"
            >
              <div className="flex items-start gap-3">
                <span className="mt-0.5 text-blue-700">
                  <IconShield />
                </span>
                <div>
                  <h3 className="font-semibold">{item.title}</h3>
                  <p className="mt-3 text-sm leading-7 text-stone-600">
                    {item.text}
                  </p>
                </div>
              </div>
            </article>
          ))}
        </div>

        <div className="mx-auto mt-8 max-w-5xl rounded-2xl border border-amber-200 bg-amber-50 p-6 sm:p-7">
          <p className="font-semibold text-amber-950">
            Important medical disclaimer
          </p>
          <p className="mt-3 text-sm leading-7 text-amber-950/80">
            MedInsight AI is an informational software project. It does not
            provide a medical diagnosis, prescribe treatment or replace a
            clinician. If you have concerning symptoms, seek appropriate
            medical care. For a medical emergency, contact local emergency
            services.
          </p>
        </div>
      </section>

      {/* FAQ */}
      <section
        id="faq"
        className="scroll-mt-20 border-t border-stone-200 bg-white px-5 py-20 sm:px-8 sm:py-24"
      >
        <SectionTitle
          eyebrow="Frequently asked questions"
          title="What to know before you upload."
          description="Straightforward answers about the current workflow and its limitations."
        />

        <div className="mx-auto mt-10 max-w-3xl divide-y divide-stone-200 border-y border-stone-200">
          {faqs.map((faq, index) => (
            <details key={faq.q} className="faq-row py-5" open={index === 0}>
              <summary className="flex cursor-pointer list-none items-center justify-between gap-5 text-left text-base font-medium text-stone-900 sm:text-lg">
                {faq.q}
                <span className="faq-symbol grid size-8 shrink-0 place-items-center rounded-full border border-stone-200 text-xl font-normal">
                  +
                </span>
              </summary>
              <p className="max-w-2xl pt-4 pr-8 text-sm leading-7 text-stone-600">
                {faq.a}
              </p>
            </details>
          ))}
        </div>
      </section>

      {/* Final CTA */}
      <section className="px-5 py-16 sm:px-8 sm:py-20">
        <div className="cta-panel mx-auto max-w-7xl rounded-3xl bg-stone-950 px-6 py-10 text-white sm:px-10 sm:py-14 lg:px-14">
          <div className="relative z-10 flex flex-col items-start justify-between gap-8 md:flex-row md:items-center">
            <div className="max-w-2xl">
              <p className="text-xs font-semibold uppercase tracking-[0.2em] text-blue-200">
                Start your review
              </p>
              <h2 className="editorial-heading mt-4 text-3xl leading-tight sm:text-4xl lg:text-5xl">
                A clearer way to begin understanding your report.
              </h2>
              <p className="mt-4 max-w-xl text-sm leading-7 text-stone-300 sm:text-base">
                Organize supported report information and use it to prepare
                questions for a healthcare professional.
              </p>
            </div>

            <Link
              href="/upload"
              className="inline-flex min-h-12 shrink-0 items-center justify-center gap-2 rounded-xl bg-white px-5 py-3 text-sm font-semibold text-stone-950 transition hover:-translate-y-0.5 hover:bg-stone-100"
            >
              Upload a report
              <IconArrowRight />
            </Link>
          </div>
        </div>
      </section>

      {/* Footer content */}
      <footer className="border-t border-stone-200 bg-[#eeece5] px-5 py-10 sm:px-8">
        <div className="mx-auto flex max-w-7xl flex-col gap-8 sm:flex-row sm:items-start sm:justify-between">
          <div className="max-w-sm">
            <Link href="/" className="text-lg font-semibold tracking-tight">
              MedInsight <span className="text-blue-700">AI</span>
            </Link>
            <p className="mt-3 text-sm leading-7 text-stone-600">
              Making supported medical laboratory-report information easier
              to organize and review.
            </p>
          </div>

          <div className="flex flex-wrap gap-x-7 gap-y-3 text-sm text-stone-600">
            <Link href="/upload" className="transition hover:text-stone-950">
              Upload report
            </Link>
            <a
              href="#how-it-works"
              className="transition hover:text-stone-950"
            >
              How it works
            </a>
            <a href="#faq" className="transition hover:text-stone-950">
              FAQs
            </a>
          </div>
        </div>

        <div className="mx-auto mt-8 max-w-7xl border-t border-stone-300 pt-5 text-xs leading-6 text-stone-500">
          MedInsight AI is an informational project, not a substitute for
          professional medical advice, diagnosis or treatment.
        </div>
      </footer>
    </main>
  );
}
