export default function PageHeader({ tag, title, subtitle, children }) {
  return (
    <div className="topbar">
      <div>
        {tag && <div className="section-tag">{tag}</div>}
        <h2>{title}</h2>
        {subtitle && <p>{subtitle}</p>}
      </div>
      <div className="row">{children}</div>
    </div>
  );
}
