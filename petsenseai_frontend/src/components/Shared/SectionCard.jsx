import clsx from "clsx";

export function SectionCard({ title, subtitle, children, tone = "default" }) {
  return (
    <section className={clsx("section-card", `tone-${tone}`)}>
      {(title || subtitle) && (
        <div className="section-head">
          {title && <h2>{title}</h2>}
          {subtitle && <p>{subtitle}</p>}
        </div>
      )}
      {children}
    </section>
  );
}
